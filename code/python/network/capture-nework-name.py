# coding=UTF-8
import optparse
from scapy.all import *

def sniffReqProbe(pkt):
    #print('[+] pkt got once ... ')
    #sniffAllandParse(pkt)
    if pkt.haslayer(Dot11ProbeReq):
        print('[+] Dot11ProbeReq Detected ')
        netName = pkt.getlayer(Dot11ProbeReq).info
        if netName not in probeReqs:
            probeReqs.append(netName)
            print('[+] Detected new Probe Request : '+ netName )
    pass
def sniffAllandParse(pkt):
    if pkt.haslayer(Dot11ProbeReq):
        print('[+] Dot11ProbeReq Detected ')
    if pkt.haslayer(Dot11Beacon):
        print('[+] Dot11Beacon Detected')
    if pkt.haslayer(TCP):
        print('[+]TCP Detected')
    if pkt.haslayer(DNS):
        print('[+] DNS Detected')
        pass
    pass
def snifDot11(pkt):
    if pkt.haslayer(Dot11Beacon):
        if pkt.getlayer(Dot11Beacon).info == '':
            addr2 = pkt.getlayer(Dot11).addr2
            if addr2 not in hidAddrs:
                hidAddrs.append(addr2)
                print('[-] hide network Detected addr : '+addr2)
            pass
    pass
interface = 'wlan1mon'
probeReqs = []
sniff(iface=interface,prn=sniffReqProbe)
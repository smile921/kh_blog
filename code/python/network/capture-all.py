from scapy.all import *

def packetPrint(pkt):
	if pkt.haslayer(Dot11Beacon):
		print('[+]Detected 802.11 Beacon Frame')
	if pkt.haslayer(Dot11ProbeReq):
		print('[+]Detected 802.11 Probe Request Frame')
	if pkt.haslayer(TCP):
		print('[+] Detected a TCP Packet')
	if pkt.haslayer(DNS):
		print('[+]Detected a DNS Packet')
def pktPrint(pkt):
    if pkt.haslayer(Dot11Beacon):
        print('[+] Detected 802.11 Beacon Frame')
    elif pkt.haslayer(Dot11ProbeReq):
        print('[+] Detected 802.11 Probe Request Frame')
    elif pkt.haslayer(TCP):
        print('[+] Detected a TCP Packet')
    elif pkt.haslayer(DNS):
        print('[+] Detected a DNS Packet')
conf.iface = 'wlan0mon'
sniff(prn=packetPrint)
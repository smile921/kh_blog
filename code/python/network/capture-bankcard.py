# coding=UTF-8
import optparse
from scapy.all import *
import re

def sniffReqProbe(pkt):
    if pkt.haslayer(Dot11ProbeReq):
        netName = pkt.getlayer(Dot11ProbeReq).info
        if netName not in probeReqs:
            probeReqs.append(netName)
            print ('[+] Detected new Probe Request : '+ netName)

    pass
def findCreditCard(raw):
    americaRE= re.findall("3[47][0-9]{13}", raw)
    masterCardRE = re.findall("5[15][0-9]{16}",raw)
    visaRE = re.findall("4[0-9]{12}(?:[0-9]{3})?",raw)
    if americaRE :
        print("[+] Found American Express Card: "+americaRE[0])
    if masterCardRE :
         print("[+] Fund master card :"+masterCardRE[0])
    if visaRE:
        print("[+] Fund visa card :"+ visaRE[0])
    pass
def main_9_demo():
    tests = []
    tests.append('I would like to buy 1337 copies of that dvd')
    tests.append('Bill my card: 378282246310005 for \$2600')
    for test in tests:
        findCreditCard(test)
    pass
def main():
    parser = optparse.OptionParser(' usage  %  prog -i<interface>  ')
    parser.add_option('-i',dest='interface',type='string',help='specify a interface to listen ')
    (options,args) = parser.parse_args()
    if(options.interface == None):
        print parser.usage
        exit(0)
    else:
        conf.iface = options.interface
    try:
        print('[+]sniff starting ... ')
        #sniff(fillter='tcp',prn=findCreditCard,store=0)
        sniff(conf.iface,prn=sniffReqProbe)
    except KeyboardInterrupt :
        exit(0)
    pass
if __name__ == "__main__":
    main()

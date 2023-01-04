from scapy.all import *
from .utils import Port

openp = []
filterdp = []

def probe_port(ip, port, result = 1):
    src_port = RandShort()
    try:
        p = IP(dst=ip)/TCP(sport=src_port, dport=port, flags='F')
        resp = sr1(p, timeout=2) # Sending packet
        if resp is None:
            result = Port.OPEN
        elif resp.haslayer(TCP):
            if resp.getlayer(TCP).flags == 0x14:
                result = Port.CLOSED
            elif (int(resp.getlayer(ICMP).type)==3 and int(resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
                result = Port.MIX

    except Exception as e:
        pass

    return result


def fin(ip, common_ports):
    conf.verb = 0 
    
    for port in common_ports:
        port = int(port)
        response = probe_port(ip, port)
        if response == Port.OPEN:
            openp.append(port)
        elif response == Port.MIX:
            filterdp.append(port)

    if len(openp) != 0:
        print ("Possible Open or Filtered Ports:")
        print (openp)
    if len(filterdp) != 0:
        print ("Possible Filtered Ports:")
        print (filterdp)
    if (len(openp) == 0) and (len(filterdp) == 0):
        print ("Sorry, No open ports found.!!")

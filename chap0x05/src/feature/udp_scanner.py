from scapy.all import *
from .utils import Port

openp = []
unknownp = []
filterdp = []
mixp = []

def probe_port(ip, port, result = 1):
    src_port = RandShort()
    try:
        p = IP(dst=ip)/UDP(sport=src_port, dport=port)
        resp = sr1(p, timeout=2, verbose=0) # Sending packet
        if resp.haslayer(UDP):
            result = Port.OPEN
        elif resp is None:
            result = Port.MIX
        elif resp.haslayer(ICMP):
            if int(resp.getlayer(ICMP).type) == 3 and int(resp.getlayer(ICMP).code) == 3:
                result = Port.CLOSED
            elif int(resp.getlayer(ICMP).type) == 3 and int(resp.getlayer(ICMP).code) in [1, 2, 9, 10, 13]:
                result = Port.FILTERED
            elif resp.haslayer(IP) and resp.getlayer(IP).proto == IP_PROTOS.udp:
                result = Port.OPEN
            else:
                result = Port.UNKNOWN
    except Exception as e:
        pass

    return result


def udp(ip, common_ports):
    conf.verb = 0 
    for port in common_ports:
        port = int(port)
        response = probe_port(ip, port)
        if response == Port.OPEN:
            openp.append(port)
        elif response == Port.FILTERED:
            filterdp.append(port)
        elif response == Port.MIX:
            mixp.append(port)
        elif response == Port.UNKNOWN:
            unknownp.append(port)

    if len(openp) != 0:
        print ("Open Ports:")
        print (openp)
    if len(unknownp) != 0:
        print ("Unknown Ports:")
        print (unknownp)
    if len(filterdp) != 0:
        print ("Filtered Ports:")
        print (filterdp)
    if len(mixp) != 0:
        print("Possible Open or Filtered Ports:")
        print (mixp)

    if (len(openp) == 0) and (len(filterdp) == 0) and (len(mixp) == 0):
        print ("Sorry, No open ports found.!!")


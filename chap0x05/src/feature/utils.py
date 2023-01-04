from scapy.all import *
from enum import Enum

class Port(Enum):
    CLOSED = 0
    OPEN = 1
    FILTERED = 2
    MIX = 3
    UNKNOWN = 4

def is_up(ip):
    icmp = IP(dst=ip)/ICMP()
    resp = sr1(icmp, timeout=10, verbose=0)
    if resp is None:
        return False
    else:
        return True
import argparse
from scapy.all import *
import feature

modes = {
    "syn":feature.syn,
    "connect":feature.connect,
    "xmas":feature.xmas,
    "fin":feature.fin,
    "null":feature.null,
    "udp":feature.udp
}

if __name__ == '__main__':

    ip = ''

    common_ports = set(line.strip() for line in open('ports.txt'))

    parser = argparse.ArgumentParser()
    
    group = parser.add_mutually_exclusive_group(required=True)
    
    group.add_argument('--ip',
                       action="store_true",
                       help="Setting the ip address of the destination")
    
    group.add_argument('--host',
                       action="store_true",
                       help="Setting the hostname of the destination")
    
    parser.add_argument('destination',
                        type=str)

    parser.add_argument('mode',
                        type=str,
                        choices=['fin', 'connect', 'xmas', 'null','syn','udp'],
                        help="Choose the scanning mode",
                        nargs='?',
                        default='syn')
    
    args = parser.parse_args()

    if args.host:
        ip = socket.gethostbyname(args.destination)
    else:
        ip = args.destination

    try:
        if not feature.is_up(ip):
            raise Exception("Host is down")
    except Exception as e:
        print(e)
    else:
        try:
            modes[args.mode](ip, common_ports)
        except Exception as e:
            print(e)

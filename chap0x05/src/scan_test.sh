#!/usr/bin/bash

MODE="connect syn xmas fin null"
FW="OPEN FILTERED CLOSED"
IP="192.168.56.113"

GREEN='\033[0;32m' 
RED='\033[0;31m'
NC='\033[0m' # No Color
 
ssh -i /home/lsj/.ssh/gateway root@${IP} "ufw allow ssh && exit"

for i in $MODE
do  
    echo -e "------Current Mode: [${RED}$i${NC}]------"
    
    for j in $FW 
    do

    case "$j" in
        "OPEN") ssh -i /home/lsj/.ssh/gateway root@${IP} "ufw disable && (nohup python3 -m http.server 80  > /dev/null 2>&1 &) && exit"
        ;;
        "FILTERED") ssh -i /home/lsj/.ssh/gateway root@${IP} "yes | sudo ufw enable && ufw deny 80/tcp && exit"
        ;;
        "CLOSED") ssh -i /home/lsj/.ssh/gateway root@${IP} "ufw disable && pkill python3 && exit"
        ;;
    esac
    
    echo -e "---Current Status: [${GREEN}$j${NC}]---"
       
    sudo nohup tcpdump -w "./pkts/${i}_${j}.pcap" > /dev/null 2>&1 & 
    
    python ./main.py --ip $IP $i
    
    killall tcpdump
  
    done
done

echo -e "------Current Mode: [${RED}udp${NC}]------"
echo -e "---Current Status: [${GREEN}OPEN${NC}]---"
sudo nohup tcpdump -w "./pkts/udp_OPEN.pcap" > /dev/null 2>&1 & 
python ./main.py --ip $IP udp
killall tcpdump
echo -e "---Current Status: [${GREEN}FILTERED${NC}]---"
ssh -i /home/lsj/.ssh/gateway root@${IP} "yes | sudo ufw enable && ufw deny 53/udp && exit"
sudo nohup tcpdump -w "./pkts/udp_FILTERED.pcap" > /dev/null 2>&1 & 
python ./main.py --ip $IP udp
killall tcpdump


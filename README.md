# ARP Spoofer 

- Scan all the current IP on your network with their MAC address

# Tech part

This script uses a number of open source projects to work properly:

- scapy
- argparse
- python3

### Installation

```
pip install scapy 
pip install argparse
```

### Usage

```
usage: main.py [-h] [-i TARGET_IP] [-g GATEWAY]

optional arguments:
  -h, --help            show this help message and exit
  -i TARGET_IP, --ip TARGET_IP
                        Target IP (ex: 192.168.1.44)
  -g GATEWAY, --gateway GATEWAY
                        Gateway of the network (ex: 192.168.1.1)
```

```
python3 main.py -i 192.168.1.44 -g 192.168.1.1
```

### Pictures

[![N|Solid](https://i.imgur.com/1uGJ4d4.png)](https://i.imgur.com/1uGJ4d4.png)

@LasCC

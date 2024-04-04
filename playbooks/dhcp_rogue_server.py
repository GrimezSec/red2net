import subprocess

def restart_dnsmasq():
    subprocess.run(["systemctl", "restart", "dnsmasq"])

def update_dnsmasq_conf(interface, dhcp_range_start, dhcp_range_end, lease_time, gateway, dns):
    with open("/etc/dnsmasq.conf", "w") as f:
        f.write(f"interface={interface}\n")
        f.write(f"dhcp-range={dhcp_range_start},{dhcp_range_end},{lease_time}\n")
        f.write(f"dhcp-option=3,{gateway}\n")
        f.write(f"dhcp-option=6,{dns}\n")

    restart_dnsmasq()

def main():
    interface = input("Network Interface: ")
    start = input("DHCP Range Start: ")
    end = input("DHCP Range End: ")
    lease = input("Lease Time (seconds): ")
    gateway = input("Default Gateway: ")
    dns = input("DNS Server: ")

    update_dnsmasq_conf(interface, start, end, lease, gateway, dns)
    print("dnsmasq configuration updated and restarted.")

if __name__ == "__main__":
    main()

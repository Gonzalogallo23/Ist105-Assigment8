import sys
import json
import re
import ipaddress

# Define subnets
IPV4_SUBNET = "192.168.1.0/24"
IPV6_SUBNET = "2001:db8::"  # Quitamos /64 para asegurar la correcta concatenación

# Lease database to track assigned IPs
lease_db = {}

# Validate MAC address format
def is_valid_mac(mac):
    return re.match(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$", mac) is not None

# Generate IPv6 address using EUI-64
def generate_ipv6(mac):
    mac = mac.lower().replace(":", "")

    # Insert "fffe" in the middle to form EUI-64
    mac = mac[:6] + "fffe" + mac[6:]

    # Convert MAC string to a list of bytes
    mac_bytes = bytearray.fromhex(mac)

    # Flip the 7th bit of the first byte (modified EUI-64 rule)
    mac_bytes[0] ^= 0x02

    # Convert to IPv6 format
    ipv6_suffix = ":".join(f"{mac_bytes[i]:02x}{mac_bytes[i+1]:02x}" for i in range(0, len(mac_bytes), 2))

    # Ensure proper IPv6 format
    return f"{IPV6_SUBNET}{ipv6_suffix}"

# Assign an IPv4 address from the subnet
def assign_ipv4():
    subnet = ipaddress.IPv4Network(IPV4_SUBNET)
    for ip in subnet.hosts():
        if str(ip) not in lease_db.values():
            return str(ip)
    return None  # No available IP

# Process DHCP request
def process_request(mac, dhcp_type):
    if not is_valid_mac(mac):
        return {"error": "Invalid MAC address format"}

    # Check if MAC already has an assigned IP
    if mac in lease_db:
        assigned_ip = lease_db[mac]
    else:
        if dhcp_type == "DHCPv4":
            assigned_ip = assign_ipv4()
        elif dhcp_type == "DHCPv6":
            assigned_ip = generate_ipv6(mac)
        else:
            return {"error": "Invalid DHCP type"}

        if assigned_ip:
            lease_db[mac] = assigned_ip
        else:
            return {"error": "No available IP addresses"}

    response = {
        "mac_address": mac,
        "assigned_ip": assigned_ip,
        "lease_time": "3600 seconds",
    }
    return response

# Main execution
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Missing parameters"}))
        sys.exit(1)

    mac_address = sys.argv[1]
    dhcp_version = sys.argv[2]
    
    result = process_request(mac_address, dhcp_version)
    print(json.dumps(result))

import subprocess
import requests
import uuid
import hashlib
import socket

from Objects.HashTable import HashTable

#hash_table = HashTable.__init__(50)


def get_network_ip():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Connect to a dummy server (Google DNS) to get the default gateway IP address
        s.connect(('8.8.8.8', 80))

        # Get the default gateway IP address
        network_ip = s.getsockname()[0]
    except socket.error:
        network_ip = "127.0.0.1"  # If unable to connect, default to localhost

    finally:
        s.close()  # Close the socket

    return network_ip


def get_own_ip_address():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Connect to a dummy server (Google DNS) to get the local IP address
        s.connect(('8.8.8.8', 80))

        # Get the local IP address
        ip_address = s.getsockname()[0]
    except socket.error:
        ip_address = "127.0.0.1"  # If unable to connect, default to localhost

    finally:
        s.close()  # Close the socket

    return ip_address


def get_hash_mac_address():
    mac_address = get_mac_address()
    # Convert the MAC address string to bytes
    mac_bytes = mac_address.encode('utf-8')

    # Create a hash SHA-256 object
    sha256_hash = hashlib.sha256()

    # Update the hash object with the MAC address bytes
    sha256_hash.update(mac_bytes)

    # Get the hexadecimal representation of the hashed MAC address
    hashed_mac = sha256_hash.hexdigest()

    return hashed_mac


def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    formatted_mac = ":".join([mac[i:i + 2] for i in range(0, 12, 2)])
    return formatted_mac


def scan_network(ip_range, subnet_octet):
    """
    Scan a given IP range for reachable devices using ICMP ping.

    Args:
    - ip_range (str): The IP range to scan (e.g., '192.168.1' for a typical subnet).
    - subnet_octet (int): The last octet of the subnet mask (e.g., 24 for '192.168.1.x').

    Returns:
    - reachable_devices (list): List of reachable device IP addresses.
    """
    reachable_devices = []

    # Calculate the maximum value for the last octet based on the subnet mask
    max_value = 2 ** (32 - subnet_octet) - 1

    # Loop through IP addresses in the specified range
    for i in range(1, max_value):
        ip = ip_range + '.' + str(i)
        response = subprocess.run(['ping', '-c', '1', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print('-')
        if 'Destination host unreachable' not in str(response):
            print(ip)
            # If the ping was successful, the device is reachable
            reachable_devices.append(ip)

    return reachable_devices


def discover(ip_range, subnet_octet):
    for ip in scan_network(ip_range, subnet_octet):
        response = requests.get(url='https://' + ip + '5000/host', headers={"content-type": "application/json"}).json()
        network = response["network"]
        server_ip = response['serverIp']
        mac_address = response['macaddress']
        if response.status_code == 200 & (network == get_network_ip() & server_ip == get_own_ip_address()):
            hash_table.add(key=mac_address, value=ip)
    return hash_table

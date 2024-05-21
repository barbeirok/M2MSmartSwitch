import ipaddress
import platform
import subprocess
import requests
import uuid
import hashlib
import socket

from Objects.HashTable import HashTable

hash_table = HashTable(50)


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

    print(network_ip)
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


def ping(host):
    """
    Returns True if host responds to a ping request
    """
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', str(host)]
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
        return "unreachable" not in output and "100% packet loss" not in output
    except subprocess.CalledProcessError:
        return False


def get_all_hosts(network):
    """
    Returns all the IP addresses in the network
    """
    net = ipaddress.ip_network(network)
    return [str(ip) for ip in net.hosts()]


def scan_network(network):
    """
    Main function to get all pingable devices in the network
    """
    all_hosts = get_all_hosts(network)
    pingable_hosts = []

    for host in all_hosts:
        if ping(host):
            pingable_hosts.append(host)
            print(f"{host} is pingable")

    return pingable_hosts


def discover(ip_range):
    print("entrou")
    for ip in scan_network(ip_range):
        print(f"scanning... ip:{ip}")
        response = requests.get(url='https://' + ip + '5000/host', headers={"content-type": "application/json"}).json()
        network = response["network"]
        server_ip = response['serverIp']
        mac_address = response['macaddress']
        if response.status_code == 200 & (network == get_network_ip() & server_ip == get_own_ip_address()):
            hash_table.add(key=mac_address, value=ip)
    return hash_table

import subprocess
import requests
import uuid


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
    for i in range(1, 7):
        ip = ip_range + '.' + str(i)
        response = subprocess.run(['ping', '-c', '1', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print('-')
        if 'Destination host unreachable' not in str(response):
            print(ip)
            # If the ping was successful, the device is reachable
            reachable_devices.append(ip)

    return reachable_devices


def discover():
    connectable_devices = []
    for ip in scan_network():
        response = requests.get(url='https://' + ip + '5000/host', headers={"content-type": "application/json"})
        if response.status_code == 200:
            connectable_devices.append(ip)
    return connectable_devices

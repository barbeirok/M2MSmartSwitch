import platform
import requests
import uuid
import hashlib
import subprocess
import re
import socket
import ipaddress

import http.client
import threading

from Objects.HashTable import HashTable

hash_table = HashTable(50)
selected = None

def get_all_devices():
    return hash_table

def select_next_device():
    global selected
    selected = hash_table.get_next_key_value(selected)
    return selected

def get_host_ip():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Connect to a dummy server (Google DNS) to get the host IP address
        s.connect(('8.8.8.8', 80))
        # Get the host IP address
        host_ip = s.getsockname()[0]
    except socket.error:
        host_ip = "127.0.0.1"  # If unable to connect, default to localhost
    finally:
        s.close()  # Close the socket

    return host_ip


def get_subnet_mask():
    # Retrieve subnet mask using ipconfig command
    try:
        result = subprocess.run(['ipconfig'], capture_output=True, text=True)
        output = result.stdout

        # Find the subnet mask in the ipconfig output
        ip_pattern = re.compile(r'Subnet Mask[ .]*: (\d+\.\d+\.\d+\.\d+)')
        match = ip_pattern.search(output)
        if match:
            return match.group(1)
    except Exception as e:
        print(f"An error occurred while retrieving subnet mask: {e}")

    return None


def get_network_ip():
    host_ip = get_host_ip()
    subnet_mask = get_subnet_mask()

    if host_ip and subnet_mask:
        # Calculate the network address
        network = ipaddress.IPv4Network(f"{host_ip}/{subnet_mask}", strict=False)
        print(str(network.network_address))
        return str(network.network_address)

    return None


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


#def get_all_hosts(network):
    """
    Returns all the IP addresses in the network
    """
    #net = ipaddress.ip_network(network)
    #return [str(ip) for ip in net.hosts()]


def scan_network():
    # Run the 'arp -a' command
    result = subprocess.run(['arp', '-a'], capture_output=True, text=True)

    # Initialize an empty list to store the IP addresses
    ip_addresses = []
    # Check if the command was successful
    if result.returncode == 0:
        output = result.stdout

        # Regular expression to match IP addresses
        ip_pattern = re.compile(r'\d+\.\d+\.\d+\.\d+')

        # Find all IP addresses in the output
        ip_addresses = ip_pattern.findall(output)

        # Print the list of IP addresses
    else:
        print(f"Command failed with return code {result.returncode}")
        print(result.stderr)

    network_ips = [ip for ip in ip_addresses if ip.startswith('192.168.226.')]
    print(network_ips)
    return network_ips


def discover():
    print("entrou")
    for ip in scan_network():
        print(f"scanning... ip:{ip}")
        try:
            response = requests.get(
                url='http://' + ip + ':5000/host',  # Change to http if https is not needed
                headers={"Content-Type": "application/json"},
                timeout=5  # Add a timeout to avoid hanging
            )
            register(response, ip)
        except requests.exceptions.RequestException as e:
            print(f"Failed to connect to IP: {ip} - {e}")
    global selected
    selected = hash_table.get_first_pair()
    return hash_table
def register(response, ip):
    if response.status_code == 200:
        response_json = response.json()
        network = response_json["network"]
        server_ip = response_json['serverIP']
        mac_address = response_json['macaddress']
        # print(f"{network} == {get_network_ip()} & {server_ip} == {get_own_ip_address()}")
        # if network == get_network_ip():
        hash_table.add(key=mac_address, value=ip)
        hash_table.print_table()
        print("entered if")
        #TESTAR ISTO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#----------- ------------- ------------ ------------ ----------- ---------
def send_request(ip):
    try:
        conn = http.client.HTTPConnection(ip, 5000, timeout=5)  # Especifica a porta 5000
        conn.request("GET", "/discovernotifier")
        response = conn.getresponse()
        print(f'Request sent to {ip}, status: {response.status}')
    except http.client.HTTPException as e:
        print(f'HTTP error for {ip}: {e}')
    except OSError as e:
        print(f'OS error for {ip}: {e}')
    except Exception as e:
        print(f'Failed to send request to {ip}: {e}')
    finally:
        if 'conn' in locals():
            conn.close()

def send_requests_to_ips(ips):
    threads = []
    for ip in ips:
        thread = threading.Thread(target=send_request, args=(ip,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def get_subnet_ips(network_mask, my_ip):
    # Cria a rede a partir da máscara e do IP
    network = ipaddress.IPv4Network(f"{my_ip}/{network_mask}", strict=False)

    # Gera a lista de todos os IPs na sub-rede
    all_ips = [str(ip) for ip in network.hosts()]

    return all_ips
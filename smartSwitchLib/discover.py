import socket
import requests
import ipaddress
from app import discovered_devices, get_own_ip_address
import threading


discovered_devices = {}

def get_broadcast_address(ip_address, netmask):
    network = ipaddress.IPv4Network(ip_address + '/' + netmask, strict=False)
    return str(network.broadcast_address)

def send_broadcast_message():
    message = "DISCOVER_REQUEST"
    network_ip = get_own_ip_address()  # Obtém o endereço IP da rede local
    netmask = '255.255.254.0'  # Máscara de sub-rede
    broadcast_ip = get_broadcast_address(network_ip, netmask)  # Obtém o endereço de broadcast da rede local
    port = 5000  # Porta usada pela rota /host

    # Itera sobre todos os IPs na rede local e envia a mensagem de broadcast para cada um deles
    for ip in ipaddress.IPv4Network(network_ip + '/' + netmask, strict=False):
        ip_str = str(ip)
        if ip_str != network_ip:  # Ignora o próprio IP da máquina
            print(f"Sending broadcast message to {ip_str}:5000", flush=True)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(message.encode(), (ip_str, port))
            sock.close()

def listen_for_responses():
    global discovered_devices
    port = 5000
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', port))

    while True:
        data, addr = sock.recvfrom(1024)
        ip = addr[0]
        try:
            response = requests.get(f'http://{ip}:5000/', headers={"content-type": "application/json"})
            if response.status_code == 200:
                try:
                    response_json = response.json()
                except ValueError as e:
                    print(f"Error parsing JSON from {ip}: {e}")
                    print(f"Response content: {response.text}")
                    continue

                mac_address = response_json.get("macaddress")
                if mac_address:
                    discovered_devices[mac_address] = {
                        "network": response_json.get("network"),
                        "serverIP": response_json.get("serverIP")
                    }
                    print(f"Discovered device: {discovered_devices[mac_address]}", flush=True)
                    print(f"Received broadcast from: {ip}", flush=True)  # Adicionado print da origem do broadcast
                else:
                    print(f"No 'macaddress' found in response from {ip}")
            else:
                print(f"Received unexpected status code {response.status_code} from {ip}")

        except requests.RequestException as e:
            print(f"Error contacting {ip}: {e}", flush=True)
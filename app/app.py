import logging
import sys
from flask import Flask, request, jsonify
import threading
import requests
import socket
import ipaddress
import hashlib
import uuid
from flask import Flask, request, jsonify

# Configurar o logger do Flask para imprimir no console
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

app = Flask(__name__)
discovered_devices = {}


def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    formatted_mac = ":".join([mac[i:i + 2] for i in range(0, 12, 2)])
    return formatted_mac


def get_hash_mac_address():
    mac_address = get_mac_address()
    mac_bytes = mac_address.encode('utf-8')
    sha256_hash = hashlib.sha256()
    sha256_hash.update(mac_bytes)
    hashed_mac = sha256_hash.hexdigest()
    return hashed_mac


def get_own_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


@app.route('/host', methods=['GET'])
def discover_devices():
    client_ip = request.remote_addr
    object_to_send = {
        "macaddress": get_hash_mac_address(),
        "network": get_own_ip_address(),
        "serverIP": client_ip
    }
    return jsonify(object_to_send), 200

@app.route('/', methods=['GET'])
def d():
    print("Discovering devices", flush=True)
    return jsonify({
        "macaddress": "hfndn",
        "network": "get_own_ip_address()",
        "serverIP": "client_ip"
    }), 200

@app.route('/discover', methods=['GET'])
def discover():
    from smartSwitchLib.discover import send_broadcast_message, listen_for_responses

    # Iniciar a thread para escutar as respostas
    #threading.Thread(target=listen_for_responses, daemon=True).start()

    # Enviar o pedido broadcast
    send_broadcast_message()
    return jsonify("OK"),200

if __name__ == '__main__':
    from smartSwitchLib.discover import send_broadcast_message, listen_for_responses

    # Iniciar a thread para escutar as respostas
    threading.Thread(target=listen_for_responses, daemon=True).start()

    # Enviar o pedido broadcast
    #send_broadcast_message()

    # Iniciar o servidor Flask na porta 5000
    app.run(port=5000)

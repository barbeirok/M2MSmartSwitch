import requests
from flask import Flask, request, jsonify
import smartSwitchLib.discover as smartSwitchLib
import smartSwitchLib.receiver as smartSwitchLibr
import smartSwitchLib.ACME as ACME

import http.client
import threading

from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/host', methods=['GET'])
def discover_devices():
    client_ip = request.remote_addr
    object_to_send = {
        "macaddress": smartSwitchLib.get_hash_mac_address(),
        "network": smartSwitchLib.get_network_ip(),
        "serverIP": client_ip
    }
    return jsonify(object_to_send), 200


smartSwitchLib.discover()

@app.route('/toggle', methods=['PATCH'])
def toggle_device():
    smartSwitchLibr.toggle()
    return "success",200


@app.route('/selected', methods=['PATCH'])
def select_next():
    """
     tentativa de alterar os modulos dentro de cada app
     teria de ter uma tabela em cada app que teria uma quantiade de modulos que iriam ser alterados sem esta app saber
     qual ao certo estaria selecionado ou seja teria uma especie de hash table em cada app
     response = requests.get()
        url='http://' + smartSwitchLib.hash_table.get(smartSwitchLib.selected) + ':5000/',  #
        headers={"Content-Type": "application/json"},
        timeout=5  # Add a timeout to avoid hanging
    )
    if response.status_code != 200:
        this code
    return "Same mac different module", 200
    """
    next_selected = smartSwitchLib.select_next_device()
    if next_selected is None:
        return "No object is selected", 200
    return jsonify(next_selected), 200

@app.route('/aes', methods=['POST'])
def createAE():
    ae_name = request.json.get('ae_name', 'SmartSwitch')
    originator = request.json.get('originator', 'SmartSwitch')
    res = ACME.create_ae(ae_name,originator)
    print(res)
    print("Finish")
    return res, 200
@app.route('/ae_cont', methods=['POST'])
def createCont():
    ae_name = request.json.get('ae_name', 'SmartSwitch')
    originator = request.json.get('originator', 'SmartSwitch')
    container_name = request.json.get('container_name', 'SmartSwitch')
    res = ACME.create_container(ae_name,originator,container_name)
    print(res)
    print("Finish")
    return res, 200

@app.route('/ae_ci', methods=['POST'])
def createCI():
    ae_name = request.json.get('ae_name', 'SmartSwitch')
    originator = request.json.get('originator', 'SmartSwitch')
    container_name = request.json.get('container_name', 'SmartSwitch')
    res = ACME.create_ci(ae_name,originator, container_name,"cont")
    print(res)
    print("Finish")
    return res, 200

@app.route('/dataci', methods=['GET'])
def getDataCI():
    ae_name = request.json.get('ae_name', 'SmartSwitch')
    originator = request.json.get('originator', 'SmartSwitch')
    container_name = request.json.get('container_name', 'SmartSwitch')
    res = ACME.get_data_from_container(ae_name,originator, container_name)
    print(res)
    print("Finish")
    return res, 200

@app.route('/discovernotifier', methods=['POST'])
def discovernotifier():
    print("i was discovered")
    server_ip = request.json.get('server_ip', '')
    print("SERVER IP ->"+server_ip)
    mac_address = smartSwitchLib.get_hash_mac_address()
    network_ip = smartSwitchLib.get_own_ip_address()
    curl = f'curl -X POST http://{server_ip}:5000/registerdiscovered -H "Content-Type: application/json" -d \'{{ "macaddress": "{mac_address}", "network": "{network_ip}" }}\''
    print(curl)
    res = ACME.execute_curl(curl)
    #
    """url = f'http://{server_ip}:5000/'
    payload = {
        "macaddress": smartSwitchLib.get_hash_mac_address(),
        "network": smartSwitchLib.get_network_ip()
    }
    response = requests.post(url, json=payload)
    #Faz o pedido para a rota /registerdiscovered"""
    return "res", 200

@app.route('/registerdiscovered', methods=['POST'])
def registerdiscovered():
    #Recebe dados do cliente e regista-os
    return "i was discovered", 201

@app.route('/start', methods=['PATCH'])
def st():
    ips = smartSwitchLib.get_subnet_ips("255.255.255.0",smartSwitchLib.get_own_ip_address())
    smartSwitchLib.send_requests_to_ips(ips)
    return "Discover",200


if __name__ == '__main__':
    app.run()


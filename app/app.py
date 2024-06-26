import requests
from flask import Flask, request, jsonify
import smartSwitchLib.discover as smartSwitchLib
import smartSwitchLib.receiver as smartSwitchLibr
import smartSwitchLib.ACME as ACME
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


@app.route('/arpdiscover', methods=['PATCH'])
def arpdiscover():
    smartSwitchLib.discover()
    return "Discover", 200


@app.route('/discover', methods=['PATCH'])
def st():
    ips = smartSwitchLib.get_subnet_ips("255.255.255.0", smartSwitchLib.get_own_ip_address())
    smartSwitchLib.send_requests_to_ips(ips)
    return "Discover", 200


@app.route('/toggle', methods=['PATCH'])
def toggle_device():
    data = str(smartSwitchLibr.toggle())
    ACME.create_ci('SmartSwitch', 'SmartSwitch', smartSwitchLib.get_hash_mac_address(), data)
    return data, 200


@app.route('/togglelistener', methods=['PATCH'])
def call_toggle():
    server_ip = smartSwitchLib.hash_table.get(smartSwitchLib.selected)
    try:
        response = requests.patch(
            url=f'http://{server_ip}:5000/toggle',
            headers={"Content-Type": "application/json"},
            timeout=5  # Add a timeout to avoid hanging
        )
    except requests.exceptions.RequestException as e:
        print(f'Failed to send request to server: {e}')

    return "Sending request to selected device", 201


@app.route('/selected', methods=['PATCH'])
def select_next():
    next_selected = smartSwitchLib.select_next_device()
    if next_selected is None:
        return "No object is selected", 200
    return jsonify(next_selected), 200


@app.route('/aes', methods=['POST'])
def createAE():
    ae_name = request.json.get('ae_name', 'SmartSwitch')
    originator = request.json.get('originator', 'SmartSwitch')
    res = ACME.create_ae(ae_name, originator)
    print(res)
    print("Finish")
    return res, 200


@app.route('/ae_cont', methods=['POST'])
def createCont():
    ae_name = request.json.get('ae_name', 'SmartSwitch')
    originator = request.json.get('originator', 'SmartSwitch')
    container_name = request.json.get('container_name', 'SmartSwitch')
    res = ACME.create_container(ae_name, originator, container_name)
    print(res)
    print("Finish")
    return res, 200


@app.route('/ae_ci', methods=['POST'])
def createCI():
    ae_name = request.json.get('ae_name', 'SmartSwitch')
    originator = request.json.get('originator', 'SmartSwitch')
    container_name = request.json.get('container_name', 'SmartSwitch')
    res = ACME.create_ci(ae_name, originator, container_name, "cont")
    print(res)
    print("Finish")
    return res, 200


@app.route('/dataci', methods=['GET'])
def getDataCI():
    res = ACME.get_data_from_container('SmartSwitch', 'SmartSwitch', smartSwitchLib.get_hash_mac_address())
    print(res)
    print("Finish")
    return jsonify(res), 200


@app.route('/discovernotifier', methods=['POST'])
def discover_notifier():
    print("i was discovered")
    server_ip = request.json.get('server_ip', '')
    print("SERVER IP ->" + server_ip)
    mac_adress = smartSwitchLib.get_hash_mac_address()
    data = {
        "macaddress": mac_adress,
        "network": smartSwitchLib.get_own_ip_address()
    }
    print(mac_adress)
    try:
        response = requests.post(
            url=f'http://{server_ip}:5000/registerdiscovered',
            headers={"Content-Type": "application/json"},
            json=data,
            timeout=5  # Add a timeout to avoid hanging
        )
    except requests.exceptions.RequestException as e:
        print(f'Failed to send request to server: {e}')

    ACME.create_container("SmartSwitch", "SmartSwitch", mac_adress)
    ACME.create_ci("SmartSwitch", "SmartSwitch", smartSwitchLib.get_hash_mac_address(), "OFF")
    return "res", 200


@app.route('/registerdiscovered', methods=['POST'])
def register_discovered():
    macaddress = request.json.get('macaddress')
    network = request.json.get('network')
    smartSwitchLib.register(macaddress, network)
    return "Registered", 201



with app.app_context():
    ACME.create_ae("SmartSwitch", "SmartSwitch")

if __name__ == '__main__':
    app.run()

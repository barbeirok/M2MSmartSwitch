import requests
from flask import Flask, request, jsonify
import smartSwitchLib.discover as smartSwitchLib
import smartSwitchLib.receiver as smartSwitchLibr

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run()


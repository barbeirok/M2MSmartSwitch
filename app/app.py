from flask import Flask, request, jsonify
import smartSwitchLib.discover as smartSwitchLib

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




if __name__ == '__main__':
    app.run()


smartSwitchLib.discover('10.20.228.0/23')

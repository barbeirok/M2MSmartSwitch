import subprocess
import ipaddress
import json

from flask import Flask, request, jsonify

from smartSwitchLib.discover import discover

app = Flask(__name__)


@app.route('/host', methods=['GET'])
def discover_devices():
    client_ip = request.remote_addr
    object_to_send = {
        "macaddress": discover.get_hash_mac_address(),
        "network": discover.get_network_ip(),
        "serverIP": client_ip
    }
    return jsonify(object_to_send), 200


if __name__ == '__main__':
    app.run()

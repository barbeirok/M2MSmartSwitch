import subprocess
import ipaddress

from flask import Flask

from smartSwitchLib.discover import discover

app = Flask(__name__)


@app.route('/discover', methods=['GET'])
def discover_devices():
    return discover.scan_network('192.168.38', 24), 200


@app.route('/host', methods=['GET'])
def discover_devices():
    return discover.get_mac_address(), 200


if __name__ == '__main__':
    app.run()

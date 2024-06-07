from flask import Flask, jsonify, request, make_response
import requests
import json
import subprocess
#import MQTT

acme_url = 'http://127.0.0.1:8080'

def create_ae(ae_name='SmartSwitch', originator='SmartSwitch'):
    print(originator)
    originator = str(originator)
    print(ae_name)
    ae_name = str(ae_name)
    curl_command = f'curl -X POST {acme_url}/cse-in -H "X-M2M-RI: 12345" -H "X-M2M-Origin: CAdmin-{originator}" -H "X-M2M-RVI: 3" -H "Content-Type: application/json;ty=2" -d \"{{ \\"m2m:ae\\": {{ \\"rn\\": \\"{ae_name}\\", \\"api\\": \\"N-{originator}\\", \\"rr\\": true, \\"srv\\": [\\"3\\"] }} }}'
    print(curl_command)
    res = execute_curl(curl_command)
    print("Executed")
    return jsonify({'response': json.loads(res['stdout'])})

def create_container(ae_name:str, originator='SmartSwitch', container_name='SmartSwitch'):
    print(ae_name)
    ae_name = str(ae_name)
    curl_command = f'curl -X POST {acme_url}/cse-in/{ae_name} -H "X-M2M-RI: 54321" -H "X-M2M-Origin: CAdmin-{originator}" -H "X-M2M-RVI: 3" -H "Content-Type: application/json;ty=3" -d \"{{ \\"m2m:cnt\\": {{ \\"rn\\": \\"{container_name}\\"}} }}'
    print(curl_command)
    res = execute_curl(curl_command)
    print("Executed")
    return jsonify({'response': json.loads(res['stdout'])})

def get_data_from_container(ae_name:str, originator='SmartSwitch', container_name='SmartSwitch', ci_name='SmartSwitch'):
    print(f"aename {ae_name} \noriginator {originator} \ncontainer_name {container_name}")
    curl_command = (f'curl -X GET {acme_url}/cse-in/{ae_name}/{container_name}/{ci_name} '
                        f'-H "X-M2M-RI: 54321" '
                        f'-H "X-M2M-Origin: CAdmin-{originator}" '
                        f'-H "X-M2M-RVI: 3" '
                        f'-H "Accept: application/json"')
    """
    Explicação dos Parâmetros
    fu=2: Define a operação de descoberta de recursos.
    rcn=4: Indica que queremos os conteúdos dos recursos (representação completa).
    la=1: Indica que queremos o último (mais recente) ContentInstance.
    """
    curl_command = (f'curl -X GET {acme_url}/cse-in/{ae_name}/{container_name}?rcn=4 '
                        f'-H "X-M2M-RI: 54321" '
                        f'-H "X-M2M-Origin: CAdmin-{originator}" '
                        f'-H "X-M2M-RVI: 3" '
                        f'-H "Accept: application/json"')

    print(curl_command)
    res = execute_curl(curl_command)
    data = json.loads(res["stdout"])

    content_instances = data["m2m:cnt"]["m2m:cin"]

    # Sort instances by creation time (ct) in descending order and get the latest one
    latest_instance = sorted(content_instances, key=lambda x: x["ct"], reverse=True)[0]
    print(res)
    return jsonify({'response': latest_instance})

def create_ci(ae_name: str, originator:str, container_name: str, cont:str):
    print(ae_name)
    ae_name = str(ae_name)
    curl_command = (f'curl -X POST {acme_url}/cse-in/{ae_name}/{container_name} -H "X-M2M-RI: 98765" -H "X-M2M-Origin: CAdmin-{originator}" -H "X-M2M-RVI: 3" -H "Content-Type: application/json;ty=4" -d \"{{ \\"m2m:cin\\": {{ \\"con\\": \\"{{\\\\\\\"message\\\\\\":\\\\\\\"{cont}\\\\\\"}}\\" }} }}"')
    print(curl_command)
    res = execute_curl(curl_command)
    print("Executed")
    return jsonify({'response': json.loads(res['stdout'])})

"""
def create_MQTT_chanel():
    #logo se vê

def create_MQTT_sub():
    #logo se vê

def stop_MQTT():
    #stop chanel and subs
"""
def execute_curl(curl_command):
    try:
        # Executa o comando CURL
        result = subprocess.run(curl_command, shell=True, check=True, text=True, capture_output=True)
        return {
            'stdout': result.stdout.strip(),
            'stderr': result.stderr.strip()
        }
    except subprocess.CalledProcessError as e:
        return {
            'stdout': e.stdout.strip(),
            'stderr': e.stderr.strip()
        }

"""def publish_MQTT_message(topic='SmartSwitch', message:String):
    mqtt_client = MQTT.connect_mqtt('10.20.140.120','1884','admin','c2es4')
    MQTT.publish_mqtt(mqtt_client,'topic')"""

# CRUL PARA CRIAR UAM AE
#curl -X POST http://127.0.0.1:8080/cse-in -H "X-M2M-RI: 12345" -H "X-M2M-Origin: CAdminAE2" -H "X-M2M-RVI: 3" -H "Content-Type: application/json;ty=2" -d "{ \"m2m:ae\": { \"rn\": \"SmartSwitch\", \"api\": \"Ncase-in\", \"rr\": true, \"srv\": [\"3\"] } }"
#CURL PARA CRIAR CONTAINER
#curl -X POST http://127.0.0.1:8080/cse-in/YourAEName -H "X-M2M-RI: 54321" -H "X-M2M-Origin: CAdmin3" -H "X-M2M-RVI: 3" -H "Content-Type: application/json;ty=3" -d "{ \"m2m:cnt\": { \"rn\": \"YourContainerName\" } }"
#CURL PARA CONTENT INSTANCE
#curl -X POST http://127.0.0.1:8080/cse-in/SmartSwitch/LAMP1 -H "X-M2M-RI: 98765" -H "X-M2M-Origin: CAdmin3" -H "X-M2M-RVI: 3" -H "Content-Type: application/json;ty=4" -d "{ \"m2m:cin\": { \"con\": \"LAMP1\" } }"
#CURL PARA ESCREVER JSON ESPECÍFICO DENTRO DO CI
#curl -X POST http://127.0.0.1:8080/cse-in/YourAEName/YourContainerName -H "X-M2M-RI: 98765" -H "X-M2M-Origin: CAdmin3" -H "X-M2M-RVI: 3" -H "Content-Type: application/json;ty=4" -d "{ \"m2m:cin\": { \"con\": \"{\\\"message\\\":\\\"LAMP1 is ON\\\"}\" } }"
    #no fundo foi a adição de uma noca CI

###ACME SALA###
# curl -X POST http://10.20.140.120:8000/cse-mn -H "X-M2M-RI: 12345" -H "X-M2M-Origin: CAdminAE2" -H "X-M2M-RVI: 3" -H "Content-Type: application/json;ty=2" -d "{ \"m2m:ae\": { \"rn\": \"SmartSwitch\", \"api\": \"N-smartswitch\", \"rr\": true, \"srv\": [\"3\"] } }"
# curl -X POST http://10.20.140.120:8000/cse-mn/SmartSwitch -H "X-M2M-RI: 54321" -H "X-M2M-Origin: CAdminAE2" -H "X-M2M-RVI: 3" -H "Content-Type: application/json;ty=3" -d "{ \"m2m:cnt\": { \"rn\": \"LAMP1\" } }

from flask import Flask, jsonify, request, make_response
import requests
import json
import subprocess


def create_ae(ae_name='SmartSwitch', originator='SmartSwitch'):
    print(originator)
    originator = str(originator)
    print(ae_name)
    ae_name = str(ae_name)
    curl_command = f'curl -X POST http://127.0.0.1:8080/cse-in -H "X-M2M-RI: 12345" -H "X-M2M-Origin: CAdmin-{originator}" -H "X-M2M-RVI: 3" -H "Content-Type: application/json;ty=2" -d \"{{ \\"m2m:ae\\": {{ \\"rn\\": \\"{ae_name}\\", \\"api\\": \\"N-{originator}\\", \\"rr\\": true, \\"srv\\": [\\"3\\"] }} }}'
    print(curl_command)
    res = execute_curl(curl_command)
    print("Executed")
    """if res['stderr']:
        # Filtra a mensagem de erro para uma resposta legível
        error_message = res['stderr'].splitlines()
        return make_response(jsonify({'error': error_message[-1]}), 500)"""
    return jsonify({'response': json.loads(res['stdout'])})

def create_container(ae_name:str, originator='SmartSwitch', container_name='SmartSwitch'):
    print(ae_name)
    ae_name = str(ae_name)
    curl_command = f'curl -X POST http://127.0.0.1:8080/cse-in/{ae_name} -H "X-M2M-RI: 54321" -H "X-M2M-Origin: {originator}" -H "X-M2M-RVI: 3" -H "Content-Type: application/json;ty=3" -d \"{{ \\"m2m:cnt\\": {{ \\"rn\\": \\"{container_name}\\"}} }}'
    print(curl_command)
    res = execute_curl(curl_command)
    print("Executed")
    return jsonify({'response': json.loads(res['stdout'])})
    #if AE not exists on ACME server
        # return 'AE does not exists'
    # if CONT already exists on ACME server
        # return 'CONT already exists'
    #create container associated to AE

def create_ci(ae_name: str, originator:str, container_name: str, cont:str):
    print(ae_name)
    ae_name = str(ae_name)
    curl_command = f'curl -X POST http://127.0.0.1:8080/cse-in/{ae_name}/{container_name} -H "X-M2M-RI: 98765" -H "X-M2M-Origin: {originator}" -H "X-M2M-RVI: 3" -H "Content-Type: application/json;ty=4" -d \"{{ \\"m2m:cin\\": {{ \\"con\\": \\"{{\\\\\\\"message\\\\\\":\\\\\\\"LAMP1 is ON\\\\\\"}}\\" }} }}"'
    print(curl_command)
    res = execute_curl(curl_command)
    print("Executed")
    return jsonify({'response': json.loads(res['stdout'])})
    # if AE does not exists on ACME server
        # return 'AE does not exists'
    # if CONT does not exists on ACME server
        # return 'CONT dos not exists'
    # if CI does not exists on ACME server
        # create a new CI (ci_name,cont)
    # if CI already exists on ACME server
        #update (ci_name,cont)

"""
def create_MQTT_chanel():
    #logo se vê

def create_MQTT_sub():
    #logo se vê

def stop_MQTT():
    #stop chanel and subs
"""
def execute_curl(curl_command):
    """
    Executa um comando CURL e retorna a resposta.

    :param curl_command: str - O comando CURL completo a ser executado.
    :return: dict - Um dicionário contendo 'stdout' (a resposta do comando) e 'stderr' (qualquer erro ocorrido).
    """
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


"""
import requests

ACME_SERVER_IP = '127.30.30.30'
ACME_SERVER_PORT = '3001'
BASE_URL = f'http://{ACME_SERVER_IP}:{ACME_SERVER_PORT}/'

def ae_exists(ae_name):
    response = requests.get(f'{BASE_URL}ae/{ae_name}')
    return response.status_code == 200

def container_exists(ae_name, container_name):
    response = requests.get(f'{BASE_URL}ae/{ae_name}/containers/{container_name}')
    return response.status_code == 200

def ci_exists(ae_name, container_name, ci_name):
    response = requests.get(f'{BASE_URL}ae/{ae_name}/containers/{container_name}/cis/{ci_name}')
    return response.status_code == 200

def create_ae(ae_name: str):
    if ae_exists(ae_name):
        return 'AE is already created'
    response = requests.post(f'{BASE_URL}ae', json={'ae_name': ae_name})
    return response.json()

def create_container(ae_name: str, container_name: str):
    if not ae_exists(ae_name):
        return 'AE does not exist'
    if container_exists(ae_name, container_name):
        return 'Container already exists'
    response = requests.post(f'{BASE_URL}ae/{ae_name}/containers', json={'container_name': container_name})
    return response.json()

def create_ci(ae_name: str, container_name: str, ci_name: str, content: str):
    if not ae_exists(ae_name):
        return 'AE does not exist'
    if not container_exists(ae_name, container_name):
        return 'Container does not exist'
    if ci_exists(ae_name, container_name, ci_name):
        response = requests.put(f'{BASE_URL}ae/{ae_name}/containers/{container_name}/cis/{ci_name}', json={'content': content})
        return response.json()
    else:
        response = requests.post(f'{BASE_URL}ae/{ae_name}/containers/{container_name}/cis', json={'ci_name': ci_name, 'content': content})
        return response.json()

def create_MQTT_channel():
    # Implementar conforme necessário
    pass

def create_MQTT_sub():
    # Implementar conforme necessário
    pass

def stop_MQTT():
    # Implementar conforme necessário
    pass

# Exemplos de uso:
print(create_ae('AE1'))
print(create_container('AE1', 'Container1'))
print(create_ci('AE1', 'Container1', 'CI1', 'Sample Content'))

"""

import paho.mqtt.client as paho

def connect_mqtt(broker, port, user, password) -> paho.mqtt.client.Client:
    client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    client.username_pw_set("username", "password")
    client.connect("14b5793c334743769b3e9fb1e4008401.s2.eu.hivemq.cloud", 8883)
    client.connect("ssl://localhost", 8883)
    return client

def publish_mqtt( client:paho.mqtt.client.Client, topic):
    client.publish("encyclopedia/temperature", payload="hot", qos=1)

def subscribe_mqtt(client:paho.mqtt):
    client.subscribe("encyclopedia/#", qos=1)
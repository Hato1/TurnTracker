from paho.mqtt import client as mqtt

class Mqtt():
    def __enter__(self, *args, **kwargs):
        self.client.loop_start()

    def __exit__(self, *args, **kwargs):
        self.client.loop_stop()

    def __init__(self, broker: str, client_id: str, port: int) -> mqtt.Client:
        def on_connect(client, userdata, flags, rc, _properties):
            if rc == 0:
                print("Connected to MQTT Broker.")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id)
        # client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.connect(broker, port)
        self.client = client


    def subscribe(self, topics: str, handler):
        """Subscribe to multiple topics.
        
        Running this method more than once with different handlers will cause
        all callbacks to use the most recently specified handler.
        """
        def on_message(client, userdata, msg):
            nonlocal handler
            print(f"Received '{msg.payload.decode()}' from '{msg.topic}'")
            handler(msg.topic, msg.payload.decode())

        for topic in topics:
            self.client.subscribe(topic)
            self.client.on_message = on_message


    def publish(self, topic: str, msg: str):
        result = self.client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send '{msg}' to '{topic}'")
        else:
            print(f"Failed to send message {msg} to topic {topic}")
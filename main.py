from dataclasses import dataclass
import random

from mqtt import Mqtt
from gui import GUI
from shared import Buttons


@dataclass
class Config():
    # TODO: Read from file.
    # MQTT:
    broker = 'broker.emqx.io'
    port = 1883
    topic = "button-controller"
    client_id = f'jkfnj{random.randint(0, 100)}'
    # username = 'emqx'
    # password = 'public'


class Main():
    def __init__(self, config):
        self.config = config
        self.client = Mqtt(config.broker, config.client_id, config.port)
        for b in Buttons:
            self.client.subscribe([config.topic, b], self.event_handler)

        self.gui = GUI(self.client)

        self.main_loop()

    def event_handler(self, topic, msg):
        if topic in Buttons:
            self.gui.event_handler(topic, msg)
            return
        print(f"UNHANDLED: {topic, msg}")


    def main_loop(self):
        # Start async loop on its own thread for subscribed topic callbacks.
        with self.client:
            while self.gui.running:
                self.gui.update()
            self.gui.quit()
                # gui.GUI_Player.update_all()
                # gui.GUI_Logic.update_all()
                # print(self.loop_active)
                    # window.quit()
                    # LOOP_ACTIVE = False
                # else:
                #     LABEL = Label(ROOT, text=USER_INPUT)
                #     LABEL.pack()



if __name__ == '__main__':
    Main(Config())

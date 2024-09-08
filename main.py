from dataclasses import dataclass
from enum import Enum
import random

from mqtt import Mqtt
import gui

class Buttons(str, Enum):
    RED = "RED"
    GREEN = "GREEN"
    BLUE = "BLUE"
    YELLOW = "YELLOW"
    WHITE = "WHITE"


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
        self.running = False

        self.buttons = {
            b: [0, 0.0, None]
            for b in Buttons
        }

        self.client.subscribe([config.topic, "GUI"], self.event_handler)

        self.main_loop()

    def event_handler(self, topic, msg):
        if topic == "GUI":
            if msg == "Quit":
                self.running = False
                return
            if msg in Buttons:
                self.buttons[msg][0] = 1 - self.buttons[msg][0]
                print(self.buttons[msg][0])
                return
        print(f"UNHANDLED: {topic, msg}")


    def main_loop(self):
        # Start async loop on its own thread for subscribed topic callbacks.
        with self.client:
            window = gui.get_window(self.client)
            self.running = True
            while self.running:
                window.update()
                # print(self.loop_active)
                    # window.quit()
                    # LOOP_ACTIVE = False
                # else:
                #     LABEL = Label(ROOT, text=USER_INPUT)
                #     LABEL.pack()
            window.quit()



if __name__ == '__main__':
    Main(Config())

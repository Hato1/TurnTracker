from pathlib import Path
import time
from tkinter import Tk
import customtkinter
from PIL import Image

import logic
from mqtt import Mqtt
from shared import Buttons


ASSETS = {
    b: customtkinter.CTkImage(Image.open(Path(f"assets/{b.value.lower()}.png")), size=(80,80)) for b in Buttons
}


class Tk_object():
    FONT = ("Arial", 14)
    TEXT_COLOR = "#000000"
    BORDER_COLOR = "#000000"
    HEIGHT = 30
    BG_COLOR = "#9c9c9c"

    def __init__(self):
        self.update_queue = []
        self.obj: customtkinter.CTkBaseClass

    def update(self):
        while self.update_queue:
            self.obj.configure(**self.update_queue.pop(0))


class Button_obj(Tk_object):
    HOVER_COLOR = "#949494"
    FG_COLOR = "#F0F0F0"

    def __init__(self, window: Tk, pos: tuple[float, float], text: str, callback=None, image=None, size=None):
        self.obj = customtkinter.CTkButton(
            master=window,
            text=text,
            font=self.FONT,
            text_color=self.TEXT_COLOR,
            hover=True,
            hover_color=self.HOVER_COLOR,
            height=self.HEIGHT,
            width=120,
            border_width=2,
            corner_radius=6,
            border_color=self.BORDER_COLOR,
            bg_color=self.BG_COLOR,
            fg_color=self.FG_COLOR,
            image=image,
            command=callback
        )
        self.obj.place(relx=pos[0], rely=pos[1], anchor="c")
        super().__init__()


class Label(Tk_object):
    FG_COLOR = "#9c9c9c"

    def __init__(self, window: Tk, pos: tuple[float, float], text: str):
        self.obj = customtkinter.CTkLabel(
            master=window,
            text=text,
            font=self.FONT,
            text_color=self.TEXT_COLOR,
            height=self.HEIGHT,
            width=95,
            corner_radius=0,
            bg_color=self.BG_COLOR,
            fg_color=self.FG_COLOR,
        )
        self.obj.place(relx=pos[0], rely=pos[1], anchor="c")
        super().__init__()


class Image_obj(Tk_object):
    def __init__(self, window: Tk, pos: tuple[float, float], image):
        self.obj = customtkinter.CTkLabel(
            master=window,
            text='',
            image=image,
        )
        self.obj.place(relx=pos[0], rely=pos[1], anchor="c")
        super().__init__()


class GUI_Player(logic.Player):
    def __init__(self, window: Tk, client, xpos: float, button: Buttons):
        self.button = button
        self.image = Image_obj(window, (xpos, 0.4), ASSETS[Buttons.BLACK])
        callback = lambda b=button: client.publish(b, "push")
        self.debug_button = Button_obj(window, (xpos, 0.6), f"Press", callback=callback)
        callback = lambda b=button: client.publish(b, "long-push")
        self.pass_button = Button_obj(window, (xpos, 0.7), f"Long press (Pass)", callback=callback)
        self.label = Label(window, (xpos, 0.8), "0:00:00")
        super().__init__(button)
         
    def led_setter(self, state: bool):
        image = ASSETS[self.button if state else Buttons.BLACK]
        self.image.update_queue.append({"image": image})

    def queue_label_update(self, label: str):
        self.label.update_queue.append({"text": label})

    def update(self, time: float = 0.0):
        """Time can be used to temporarily adjust the timer label."""
        self.label.update_queue.append({"text": f"{self.elapsed_time+time:.2f}"})
        self.image.update()
        self.debug_button.update()
        self.label.update()


class GUI(logic.Game):
    def __init__(self, mqtt: Mqtt):
        self.window = self.create_window()
        self.mqtt = mqtt
        player_names = [b for b in Buttons if b != Buttons.BLACK]
        players = [GUI_Player(self.window, self.mqtt, (i+0.5) / len(player_names), b) for i, b in enumerate(player_names)]
        self.running = True

        self.players: list[GUI_Player]
        super().__init__(players)
        self.reset_leds()

    def quit(self):
        self.window.quit()

    def create_window(self):
            def on_closing():
                self.running = False
            window = Tk()
            window.title("Button controller")
            window.geometry("800x350")
            window.configure(bg="#9c9c9c")
            window.protocol("WM_DELETE_WINDOW", on_closing)

            Button_obj(window, (0.1, 0.1), "Pause")
            Button_obj(window, (0.5, 0.1), "Set turn order")
            Button_obj(window, (0.9, 0.1), "Reset")
            return window
    
    def event_handler(self, player: Buttons, action: str):
        if player == self.players[0].name:
            self.players[0].led_setter(False)
            self.take_turn()
            self.players[0].led_setter(True)

    def reset_leds(self):
        self.players[0].led_setter(True)
        for p in self.players[1:]:
            p.led_setter(False)
    
    def update(self):
            self.players[0].update(time.time() - self.time_since_last_action)
            for p in self.players[1:]:
                p.update()

            self.window.update()

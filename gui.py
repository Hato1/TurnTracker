from enum import Enum
from tkinter import *
import customtkinter

from mqtt import Mqtt


class Buttons(str, Enum):
    RED = "RED"
    GREEN = "GREEN"
    BLUE = "BLUE"
    YELLOW = "YELLOW"
    WHITE = "WHITE"


def get_window(client):
    def on_closing():
        client.publish("GUI", "Quit")
    window = Tk()
    window.title("Button controller")
    window.geometry("800x350")
    window.configure(bg="#9c9c9c")
    window.protocol("WM_DELETE_WINDOW", on_closing)
    draw_stuff(window, client)
    return window




class Tk_object():
    FONT = ("Arial", 14)
    TEXT_COLOR = "#000000"
    BORDER_COLOR = "#000000"
    HEIGHT = 30
    BG_COLOR = "#9c9c9c"


class Button(Tk_object):
    HOVER_COLOR = "#949494"
    FG_COLOR = "#F0F0F0"

    def __init__(self, window: Tk, pos: tuple[int, int], text: str, callback=None):
        b = customtkinter.CTkButton(
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
        command=callback
        )
        b.place(relx=pos[0], rely=pos[1], anchor="c")


class Label(Tk_object):
    FG_COLOR = "#9c9c9c"

    def __init__(self, window: Tk, pos: tuple[int, int], text: str):
        l = customtkinter.CTkLabel(
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
        l.place(relx=pos[0], rely=pos[1], anchor="c")


def draw_stuff(window, client):
    for i, button in enumerate(Buttons):
        xpos = (i+0.5) / len(Buttons)
        callback = lambda b=button: client.publish("GUI", b)
        Button(window, (xpos, 0.6), f"Press {button.value}", callback=callback)
        Label(window, (xpos, 0.7), "0:00:00")
    Button(window, (0.1, 0.1), "Pause")
    Button(window, (0.5, 0.1), "Set turn order")
    Button(window, (0.9, 0.1), "Reset")
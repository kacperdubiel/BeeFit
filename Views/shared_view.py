import tkinter.font as tk_font
from tkinter import messagebox
from tkinter.ttk import Style


class SharedView:
    def __init__(self):
        self.VERY_SMALL_PAD = 2
        self.SMALL_PAD = 5
        self.NORMAL_PAD = 10
        self.BIG_PAD = 20

        self.ICON_SIZE = 16
        self.LIST_IMG_SIZE = 48

        self.font_style_10 = tk_font.Font(size=10)
        self.font_style_10_bold = tk_font.Font(size=10, weight='bold')
        self.font_style_12 = tk_font.Font(size=12)
        self.font_style_12_bold = tk_font.Font(size=12, weight='bold')
        self.font_style_35_bold = tk_font.Font(size=35, weight='bold')
        self.btn_size = 15

        self.style_notebook_tab = Style().configure('TNotebook.Tab', font=self.font_style_10_bold, padding=(15, 5))
        self.style_notebook_tab = Style().configure('TToplevel', background="black")

        self.style_frame_black_bg = Style().configure("BlackBG.TFrame", background="black")
        self.style_frame_red_bg = Style().configure("RedBG.TFrame", background="red")
        self.style_frame_green_bg = Style().configure("GreenBG.TFrame", background="green")
        self.style_frame_blue_bg = Style().configure("BlueBG.TFrame", background="blue")
        self.style_frame_yellow_bg = Style().configure("YellowBG.TFrame", background="yellow")
        self.style_frame_pink_bg = Style().configure("PinkBG.TFrame", background="pink")


def center_window(win):
    win.update()
    width = win.winfo_width()
    height = win.winfo_height()

    x_offset = (win.winfo_screenwidth() - width) // 2
    y_offset = (win.winfo_screenheight() - height) // 2

    win.geometry(
        f'{width}x{height}+{x_offset}+{y_offset}'
    )


def show_errorbox(title, message):
    messagebox.showerror(title, message)


def show_infobox(title, message):
    messagebox.showinfo(title, message)

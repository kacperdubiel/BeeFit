import tkinter as tk
from tkinter import ttk
from tkinter import *

from PIL import ImageTk

from Views.shared_view import center_window


class UserView(tk.Toplevel):
    def __init__(self, master, shared_view, user):
        tk.Toplevel.__init__(self, master)
        self.shared_view = shared_view
        self.user = user

        self.protocol('WM_DELETE_WINDOW', self.master.destroy)
        self.title('BeeFit')
        self.resizable(False, False)

        self._create_user_view_frames()
        self._create_user_view_widgets()

        center_window(self)

    def _create_user_view_frames(self):
        self.frame_user_view = ttk.Frame(self)
        self.frame_user_view.pack(padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

        self.frame_left_block = ttk.Frame(self.frame_user_view)
        self.frame_left_block.pack(side="left", fill=tk.BOTH, padx=(0, self.shared_view.NORMAL_PAD))

        self.frame_right_block = ttk.Frame(self.frame_user_view, borderwidth=2, relief="groove")
        self.frame_right_block.pack(side="right", fill=tk.BOTH)

        self.frame_right_block_first_row = ttk.Frame(self.frame_right_block)
        self.frame_right_block_first_row.pack(expand=True, fill=tk.BOTH, padx=self.shared_view.SMALL_PAD,
                                              pady=self.shared_view.SMALL_PAD)

        self.frame_right_block_second_row = ttk.Frame(self.frame_right_block)
        self.frame_right_block_second_row.pack(expand=True, fill=tk.BOTH, padx=self.shared_view.SMALL_PAD,
                                               pady=self.shared_view.SMALL_PAD)

        self.frame_right_block_third_row = ttk.Frame(self.frame_right_block)
        self.frame_right_block_third_row.pack(expand=True, fill=tk.BOTH, padx=self.shared_view.SMALL_PAD,
                                              pady=self.shared_view.SMALL_PAD)

        self.frame_right_block_fourth_row = ttk.Frame(self.frame_right_block)
        self.frame_right_block_fourth_row.pack(expand=True, fill=tk.BOTH, padx=self.shared_view.SMALL_PAD,
                                               pady=self.shared_view.SMALL_PAD)

    def _create_user_view_widgets(self):
        # Avatar
        self.frame_avatar = ttk.Frame(self.frame_left_block, borderwidth=2, relief="groove")
        self.frame_avatar.grid(column=0, row=0)
        self.frame_left_block.rowconfigure(0, weight=1)

        self.img_render = ImageTk.PhotoImage(self.user['avatar'])
        self.img_avatar = Label(self.frame_avatar, image=self.img_render)
        self.img_avatar.pack()

        # First row - Greetings and logout btn
        self.label_greetings = Label(self.frame_right_block_first_row, text=f"Witaj {self.user['login']}!",
                                     font=self.shared_view.font_style_10_bold)
        self.label_greetings.pack(side="left")
        self.btn_logout = tk.Button(self.frame_right_block_first_row,
                                    text="Wyloguj",
                                    font=self.shared_view.font_style_10)
        self.btn_logout.pack(side='right')

        # Second row - Date settings
        self.btn_next_date = tk.Button(self.frame_right_block_second_row,
                                       text=">",
                                       font=self.shared_view.font_style_10)
        self.btn_next_date.pack(side='right', padx=(self.shared_view.SMALL_PAD, 0))

        self.label_current_date = Label(self.frame_right_block_second_row, text=f"{self.user['current_date']}",
                                        font=self.shared_view.font_style_10)
        self.label_current_date.pack(side="right", padx=(self.shared_view.SMALL_PAD, 0))

        self.btn_prev_date = tk.Button(self.frame_right_block_second_row,
                                       text="<",
                                       font=self.shared_view.font_style_10)
        self.btn_prev_date.pack(side='right', padx=(self.shared_view.SMALL_PAD, 0))

        self.btn_set_to_today = tk.Button(self.frame_right_block_second_row,
                                          text="Dzisiaj",
                                          font=self.shared_view.font_style_10)
        self.btn_set_to_today.pack(side='right')

        # Third row - Calories status
        self.label_calories_consumed = Label(self.frame_right_block_third_row,
                                             text=f"Spożyto: {self.user['calories_consumed']} kcal",
                                             font=self.shared_view.font_style_10)
        self.label_calories_consumed.pack(side="left")

        self.label_calories_left = Label(self.frame_right_block_third_row,
                                         text=f"Pozostało: {self.user['calories_left']} kcal",
                                         font=self.shared_view.font_style_10)
        self.label_calories_left.pack(side="right")

        # Fourth row - Progress bar
        self.progressbar_calories = ttk.Progressbar(self.frame_right_block_fourth_row, orient=HORIZONTAL, length=420,
                                                    mode="determinate")
        self.progressbar_calories.pack()
        self.progressbar_calories['value'] = self.user['progressbar_percent']

    def update_user_status_view(self):
        self.label_current_date.configure(text=f"{self.user['current_date']}")
        self.label_calories_consumed.configure(text=f"Spożyto: {self.user['calories_consumed']} kcal")
        self.label_calories_left.configure(text=f"Pozostało: {self.user['calories_left']} kcal")

        self.progressbar_calories['value'] = self.user['progressbar_percent']


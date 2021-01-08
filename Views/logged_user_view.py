import tkinter as tk
from tkinter import *
from tkinter import ttk

from PIL import ImageTk

from Views.meal_plan_view import MealPlanView
from Views.profile_view import ProfileView
from Views.shared_view import center_window
from Views.user_dishes_view import UserDishesView
from Views.user_products_view import UserProductsView


class LoggedUserView(tk.Toplevel):
    def __init__(self, master, shared_view, user):
        tk.Toplevel.__init__(self, master)
        self.shared_view = shared_view
        self.user = user
        self.withdraw()

        self.protocol('WM_DELETE_WINDOW', self.master.destroy)
        self.title('BeeFit')
        self.resizable(False, False)

        self._create_user_view_frames()

        self._create_user_view_widgets()

        self._create_tabs()

        center_window(self)
        self.deiconify()

    def _create_user_view_frames(self):
        self.frame_user_view = ttk.Frame(self)
        self.frame_user_view.pack(padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

        # TOP BLOCK
        self.frame_top_block = ttk.Frame(self.frame_user_view)
        self.frame_top_block.pack()

        self.frame_top_left_block = ttk.Frame(self.frame_top_block, borderwidth=2, relief="groove")
        self.frame_top_left_block.pack(side="left", fill=tk.BOTH, padx=(0, self.shared_view.NORMAL_PAD))

        self.frame_top_right_block = ttk.Frame(self.frame_top_block, borderwidth=2, relief="groove")
        self.frame_top_right_block.pack(side="right", fill=tk.BOTH)

        self.frame_top_right_block_first_row = ttk.Frame(self.frame_top_right_block)
        self.frame_top_right_block_first_row.pack(expand=True, fill=tk.BOTH, padx=self.shared_view.SMALL_PAD,
                                                  pady=self.shared_view.SMALL_PAD)

        self.frame_top_right_block_second_row = ttk.Frame(self.frame_top_right_block)
        self.frame_top_right_block_second_row.pack(expand=True, fill=tk.BOTH, padx=self.shared_view.SMALL_PAD,
                                                   pady=self.shared_view.SMALL_PAD)

        self.frame_top_right_block_third_row = ttk.Frame(self.frame_top_right_block)
        self.frame_top_right_block_third_row.pack(expand=True, fill=tk.BOTH, padx=self.shared_view.SMALL_PAD,
                                                  pady=self.shared_view.SMALL_PAD)

        self.frame_top_right_block_fourth_row = ttk.Frame(self.frame_top_right_block)
        self.frame_top_right_block_fourth_row.pack(expand=True, fill=tk.BOTH, padx=self.shared_view.SMALL_PAD,
                                                   pady=self.shared_view.SMALL_PAD)

        # BOTTOM BLOCK
        self.frame_bottom_block = ttk.Frame(self.frame_user_view)
        self.frame_bottom_block.pack(pady=(self.shared_view.NORMAL_PAD, 0))

    def _create_user_view_widgets(self):
        # Avatar
        self.canvas_avatar = tk.Canvas(self.frame_top_left_block, width=140, height=140)

        self.avatar_render = ImageTk.PhotoImage(self.user['avatar'])
        self.canvas_image_avatar = self.canvas_avatar.create_image(70, 70, image=self.avatar_render)
        self.btn_change_avatar = tk.Button(self.frame_top_left_block, text="Zmień", anchor='w', width=5)
        self.window_btn_change_avatar = self.canvas_avatar.create_window(140, 140, anchor='se',
                                                                         window=self.btn_change_avatar)
        self.canvas_avatar.pack()

        # First row - Greetings and logout btn
        self.label_greetings = Label(self.frame_top_right_block_first_row, text=f"Witaj {self.user['login']}!",
                                     font=self.shared_view.font_style_12_bold)
        self.label_greetings.pack(side="left")
        self.btn_logout = tk.Button(self.frame_top_right_block_first_row,
                                    text="Wyloguj",
                                    font=self.shared_view.font_style_10)
        self.btn_logout.pack(side='right')

        # Second row - Date settings
        self.btn_next_date = tk.Button(self.frame_top_right_block_second_row,
                                       text=">",
                                       font=self.shared_view.font_style_10)
        self.btn_next_date.pack(side='right', padx=(self.shared_view.SMALL_PAD, 0))

        self.label_current_date = Label(self.frame_top_right_block_second_row, text=f"{self.user['current_date']}",
                                        font=self.shared_view.font_style_10)
        self.label_current_date.pack(side="right", padx=(self.shared_view.SMALL_PAD, 0))

        self.btn_prev_date = tk.Button(self.frame_top_right_block_second_row,
                                       text="<",
                                       font=self.shared_view.font_style_10)
        self.btn_prev_date.pack(side='right', padx=(self.shared_view.SMALL_PAD, 0))

        self.btn_set_to_today = tk.Button(self.frame_top_right_block_second_row,
                                          text="Dzisiaj",
                                          font=self.shared_view.font_style_10)
        self.btn_set_to_today.pack(side='right')

        # Third row - Calories status
        self.label_calories_consumed = Label(self.frame_top_right_block_third_row,
                                             text=f"Spożyto: {self.user['calories_consumed']} kcal",
                                             font=self.shared_view.font_style_10)
        self.label_calories_consumed.pack(side="left")

        self.label_calories_left = Label(self.frame_top_right_block_third_row,
                                         text=f"Pozostało: {self.user['calories_left']} kcal",
                                         font=self.shared_view.font_style_10)
        self.label_calories_left.pack(side="right")

        # Fourth row - Progress bar
        self.progressbar_calories = ttk.Progressbar(self.frame_top_right_block_fourth_row, orient=HORIZONTAL,
                                                    length=420, mode="determinate")
        self.progressbar_calories.pack()
        self.progressbar_calories['value'] = self.user['progressbar_percent']

    def update_user_status_view(self):
        self.label_current_date.configure(text=f"{self.user['current_date']}")
        self.label_calories_consumed.configure(text=f"Spożyto: {self.user['calories_consumed']} kcal")
        self.label_calories_left.configure(text=f"Pozostało: {self.user['calories_left']} kcal")

        self.progressbar_calories['value'] = self.user['progressbar_percent']

    def update_user_avatar(self):
        self.avatar_render = ImageTk.PhotoImage(self.user['avatar'])
        self.canvas_avatar.itemconfig(self.canvas_image_avatar, image=self.avatar_render)

    def _create_tabs(self):
        self.tab_control = ttk.Notebook(self.frame_bottom_block)
        self.tab_control.bind("<<NotebookTabChanged>>", _on_tab_changed)

        self.tab_profile = ttk.Frame(self.tab_control)
        self.tab_meal_plan = ttk.Frame(self.tab_control)
        self.tab_products = ttk.Frame(self.tab_control)
        self.tab_dishes = ttk.Frame(self.tab_control)
        self.tab_trainings = ttk.Frame(self.tab_control)
        self.tab_raports = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_profile, text='Profil')
        self.tab_control.add(self.tab_meal_plan, text='Dziennik posiłków')
        self.tab_control.add(self.tab_products, text='Produkty')
        self.tab_control.add(self.tab_dishes, text='Dania')
        self.tab_control.add(self.tab_trainings, text='Treningi')
        self.tab_control.add(self.tab_raports, text='Raporty')

        self.tab_control.pack()

        self.profile_view = ProfileView(self.tab_profile, self.shared_view, self.user)
        self.profile_view.pack()

        self.meal_plan_view = MealPlanView(self.tab_meal_plan, self.shared_view, self.user)
        self.meal_plan_view.pack()

        self.user_products_view = UserProductsView(self.tab_products, self.shared_view, self.user)
        self.user_products_view.pack()

        self.user_dishes_view = UserDishesView(self.tab_dishes, self.shared_view, self.user)
        self.user_dishes_view.pack()


def _on_tab_changed(event):
    event.widget.update_idletasks()

    tab = event.widget.nametowidget(event.widget.select())
    event.widget.configure(height=tab.winfo_reqheight())

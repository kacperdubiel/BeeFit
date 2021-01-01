import tkinter as tk
from tkinter import ttk
from tkinter import *
from Views.shared_view import center_window


class RegisterView(tk.Toplevel):
    def __init__(self, master, shared_view):
        tk.Toplevel.__init__(self, master)
        self.shared_view = shared_view

        self.title('BeeFit - Rejestracja')
        self.resizable(False, False)

        self._create_register_frame()

        self._create_account_data_entries()
        self._create_user_data_entries()
        self._create_buttons()

        center_window(self)

    def _create_register_frame(self):
        self.frame_register = Frame(self)
        self.frame_register.pack(padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

    def _create_account_data_entries(self):
        # Account data frame
        self.frame_account_data = LabelFrame(self.frame_register, text="Dane konta",
                                             font=self.shared_view.font_style_10_bold)
        self.frame_account_data.pack(fill=tk.BOTH, pady=(0, self.shared_view.SMALL_PAD))

        # Login
        label_login = tk.Label(self.frame_account_data, text="Podaj login:", font=self.shared_view.font_style_12)
        label_login.pack()
        self.entry_login = tk.Entry(self.frame_account_data, font=self.shared_view.font_style_12)
        self.entry_login.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=(0, self.shared_view.SMALL_PAD))

        # Password
        label_password = tk.Label(self.frame_account_data, text="Podaj hasło:", font=self.shared_view.font_style_12)
        label_password.pack()
        self.entry_password = tk.Entry(self.frame_account_data, show="*", font=self.shared_view.font_style_12)
        self.entry_password.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=(0, self.shared_view.SMALL_PAD))

        # Password check
        label_password_check = tk.Label(self.frame_account_data, text="Podaj hasło ponownie:",
                                        font=self.shared_view.font_style_12)
        label_password_check.pack()
        self.entry_password_check = tk.Entry(self.frame_account_data, show="*", font=self.shared_view.font_style_12)
        self.entry_password_check.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD,
                                       pady=(0, self.shared_view.SMALL_PAD))

        # Email
        label_email = tk.Label(self.frame_account_data, text="Podaj adres email:", font=self.shared_view.font_style_12)
        label_email.pack()
        self.entry_email = tk.Entry(self.frame_account_data, font=self.shared_view.font_style_12)
        self.entry_email.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=(0, self.shared_view.NORMAL_PAD))

    def _create_user_data_entries(self):
        # User data frame
        self.frame_user_data = LabelFrame(self.frame_register, text="Dane osobowe",
                                          font=self.shared_view.font_style_10_bold)
        self.frame_user_data.pack(fill=tk.BOTH)

        # Gender
        gender_frame = ttk.Frame(self.frame_user_data)
        gender_frame.pack(pady=self.shared_view.SMALL_PAD)

        self.gender_value = tk.StringVar(value="M")
        gender_radio_btn1 = Radiobutton(gender_frame, text="Mężczyzna", variable=self.gender_value, value="M",
                                        font=self.shared_view.font_style_12)
        gender_radio_btn1.pack(side='left')

        gender_radio_btn2 = Radiobutton(gender_frame, text="Kobieta", variable=self.gender_value, value="K",
                                        font=self.shared_view.font_style_12)
        gender_radio_btn2.pack(side='left')

        # Weight
        label_weight = tk.Label(self.frame_user_data, text="Podaj aktualną wagę [kg]:",
                                font=self.shared_view.font_style_12)
        label_weight.pack()
        self.entry_weight = tk.Entry(self.frame_user_data, font=self.shared_view.font_style_12)
        self.entry_weight.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=(0, self.shared_view.SMALL_PAD))

        # Height
        label_height = tk.Label(self.frame_user_data, text="Podaj aktualny wzrost [cm]:",
                                font=self.shared_view.font_style_12)
        label_height.pack()
        self.entry_height = tk.Entry(self.frame_user_data, font=self.shared_view.font_style_12)
        self.entry_height.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=(0, self.shared_view.SMALL_PAD))

        # Age
        label_age = tk.Label(self.frame_user_data, text="Podaj aktualny wiek:",
                             font=self.shared_view.font_style_12)
        label_age.pack()
        self.entry_age = tk.Entry(self.frame_user_data, font=self.shared_view.font_style_12)
        self.entry_age.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=(0, self.shared_view.SMALL_PAD))

        # Physical Activity
        label_activity = tk.Label(self.frame_user_data, text="Aktywność fizyczna w ciągu dnia:",
                                  font=self.shared_view.font_style_12)
        label_activity.pack()

        activity_options_list = ["1 - Bardzo niska", "2 - Niska", "3 - Średnia", "4 - Wysoka", "5 - Bardzo wysoka"]
        self.activity_value = tk.StringVar(value=activity_options_list[2])
        activity_option_menu = tk.OptionMenu(self.frame_user_data, self.activity_value, *activity_options_list)
        activity_option_menu.config(font=self.shared_view.font_style_12)
        activity_option_menu.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD,
                                  pady=(self.shared_view.SMALL_PAD, self.shared_view.SMALL_PAD))

        # Goal
        label_goal = tk.Label(self.frame_user_data, text="Cel:",
                              font=self.shared_view.font_style_12)
        label_goal.pack()

        goal_options_list = ["1 - Zmniejszyć wagę", "2 - Utrzymać aktualną wagę", "3 - Zwiększyć wagę"]
        self.goal_value = tk.StringVar(value=goal_options_list[1])
        activity_option_menu = tk.OptionMenu(self.frame_user_data, self.goal_value, *goal_options_list)
        activity_option_menu.config(font=self.shared_view.font_style_12)
        activity_option_menu.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD,
                                  pady=(self.shared_view.SMALL_PAD, self.shared_view.NORMAL_PAD))

    def _create_buttons(self):
        self.btn_back = tk.Button(self.frame_register,
                                  text="Powrót",
                                  width=self.shared_view.btn_size,
                                  font=self.shared_view.font_style_12)
        self.btn_back.pack(side='left', padx=(0, self.shared_view.NORMAL_PAD), pady=(self.shared_view.NORMAL_PAD, 0))

        self.btn_register_new_user = tk.Button(self.frame_register,
                                               text="Zarejestruj",
                                               width=self.shared_view.btn_size,
                                               font=self.shared_view.font_style_12)
        self.btn_register_new_user.pack(side='left', pady=(self.shared_view.NORMAL_PAD, 0))

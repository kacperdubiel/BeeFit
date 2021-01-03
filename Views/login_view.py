import tkinter as tk
from tkinter import ttk
from tkinter import *
from Views.shared_view import center_window


class LoginView(tk.Toplevel):
    def __init__(self, master, shared_view):
        tk.Toplevel.__init__(self, master)
        self.shared_view = shared_view
        self.withdraw()

        self.protocol('WM_DELETE_WINDOW', self.master.destroy)
        self.title('BeeFit - Logowanie')
        self.resizable(False, False)

        self._create_login_frame()

        # Header label
        self.label_login = tk.Label(self.frame_login, text="BeeFit", font=self.shared_view.font_style_35_bold)
        self.label_login.pack(pady=(0, self.shared_view.SMALL_PAD))

        self._create_entries()
        self._create_buttons()

        center_window(self)
        self.deiconify()

    def _create_login_frame(self):
        self.frame_login = ttk.Frame(self)
        self.frame_login.pack(padx=self.shared_view.NORMAL_PAD, pady=self.shared_view.NORMAL_PAD)

    def _create_entries(self):
        # Login data frame
        self.frame_login_data = LabelFrame(self.frame_login, text="Dane logowania",
                                           font=self.shared_view.font_style_10_bold)
        self.frame_login_data.pack(fill=tk.BOTH)

        self.label_login = tk.Label(self.frame_login_data, text="Login:", font=self.shared_view.font_style_12)
        self.label_login.pack()
        self.entry_login = tk.Entry(self.frame_login_data, font=self.shared_view.font_style_12)
        self.entry_login.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=(0, self.shared_view.SMALL_PAD))

        self.label_password = tk.Label(self.frame_login_data, text="Hasło:", font=self.shared_view.font_style_12)
        self.label_password.pack()
        self.entry_password = tk.Entry(self.frame_login_data, show="*", font=self.shared_view.font_style_12)
        self.entry_password.pack(fill=tk.BOTH, padx=self.shared_view.NORMAL_PAD, pady=(0, self.shared_view.NORMAL_PAD))

    def _create_buttons(self):
        self.btn_register = tk.Button(self.frame_login,
                                      text="Zarejestruj",
                                      width=self.shared_view.btn_size,
                                      font=self.shared_view.font_style_12)
        self.btn_register.pack(side='left', padx=(0, self.shared_view.NORMAL_PAD), pady=(self.shared_view.NORMAL_PAD, 0))

        self.btn_login = tk.Button(self.frame_login,
                                   text="Zaloguj",
                                   width=self.shared_view.btn_size,
                                   font=self.shared_view.font_style_12)
        self.btn_login.pack(side='left', pady=(self.shared_view.NORMAL_PAD, 0))

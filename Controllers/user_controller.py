from datetime import datetime, timedelta
from tkinter import filedialog
import os
from Misc.config import DATE_FORMAT
from Views.user_view import UserView
from Models.user_model import UserModel
from Models.main_model import get_current_date, format_date, convert_to_binary_data


class UserController:
    def __init__(self, master, database_model, shared_view, user):
        self.master = master
        self.database_model = database_model
        self.shared_view = shared_view

        self.user_model = UserModel(user, self.database_model)
        self.user_view = UserView(master, self.shared_view, self.user_model.user)

        self.user_view.btn_change_avatar.config(command=self.change_user_avatar)

        self.user_view.btn_set_to_today.config(command=self.set_to_todays_date)
        self.user_view.btn_prev_date.config(command=self.set_to_prev_day_date)
        self.user_view.btn_next_date.config(command=self.set_to_next_day_date)

    def change_user_avatar(self):
        new_avatar_filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Wybierz obrazek",
                                                         filetypes=(("Pliki jpg", "*.jpg"), ("Pliki png", "*.png")))
        if new_avatar_filename:
            new_avatar = convert_to_binary_data(new_avatar_filename)
            self.user_model.set_user_avatar(new_avatar)
            self.user_view.update_user_avatar()

    def set_to_todays_date(self):
        new_date = get_current_date()
        self.set_current_date(new_date)

    def set_to_prev_day_date(self):
        curr_date = datetime.strptime(self.user_model.user['current_date'], DATE_FORMAT)
        new_date = curr_date - timedelta(days=1)
        self.set_current_date(format_date(new_date))

    def set_to_next_day_date(self):
        curr_date = datetime.strptime(self.user_model.user['current_date'], DATE_FORMAT)
        new_date = curr_date + timedelta(days=1)
        self.set_current_date(format_date(new_date))

    def set_current_date(self, new_date):
        self.user_model.set_current_date(new_date)
        self.user_view.update_user_status_view()

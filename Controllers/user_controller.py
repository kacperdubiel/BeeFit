from datetime import datetime, timedelta
from Misc.config import DATE_FORMAT
from Views.user_view import UserView
from Models.user_model import UserModel
from Models.main_model import get_current_date, format_date


class UserController:
    def __init__(self, master, database_model, shared_view, user):
        self.master = master
        self.database_model = database_model
        self.shared_view = shared_view

        self.user_model = UserModel(user, self.database_model)
        self.user_view = UserView(master, self.shared_view, self.user_model.user)

        self.user_view.btn_set_to_today.config(command=self.set_to_todays_date)
        self.user_view.btn_prev_date.config(command=self.set_to_prev_day_date)
        self.user_view.btn_next_date.config(command=self.set_to_next_day_date)

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

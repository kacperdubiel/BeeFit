from datetime import datetime, timedelta
from tkinter import filedialog
import os
from Misc.config import DATE_FORMAT, WEIGHT_MIN, WEIGHT_MAX, HEIGHT_MIN, HEIGHT_MAX, \
    AGE_MIN, AGE_MAX, ACTIVITY_VALUE_MIN, ACTIVITY_VALUE_MAX, GOAL_VALUE_MIN, GOAL_VALUE_MAX, GRAMMAGE_MIN, GRAMMAGE_MAX
from Views.meal_plan_view import DeleteConsumedProductWindow, AddConsumedProductWindow
from Views.profile_view import SetGenderWindow, SetHeightWindow, SetAgeWindow, SetWeightWindow, SetActivityWindow, \
    SetGoalWindow, EvaluateGDAWindow
from Views.shared_view import show_errorbox
from Views.logged_user_view import LoggedUserView
from Models.user_model import UserModel
from Models.main_model import get_current_date, format_date, convert_to_binary_data
import Controllers.main_controller as main_controller


class UserController:
    def __init__(self, master, database_model, shared_view, user):
        self.master = master
        self.database_model = database_model
        self.shared_view = shared_view

        self.user_model = UserModel(user, self.database_model)
        self.logged_user_view = LoggedUserView(master, self.shared_view, self.user_model.user)

        self.logged_user_view.btn_change_avatar.config(command=self.change_user_avatar)

        self.logged_user_view.btn_set_to_today.config(command=self.set_to_todays_date)
        self.logged_user_view.btn_prev_date.config(command=self.set_to_prev_day_date)
        self.logged_user_view.btn_next_date.config(command=self.set_to_next_day_date)

        self.profile_view = self.logged_user_view.profile_view
        self.meal_plan_view = self.logged_user_view.meal_plan_view

        self.popup_window = None
        self.configure_profile_view_buttons()
        self.configure_meal_plan_view_buttons()

    def change_user_avatar(self):
        new_avatar_filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Wybierz obrazek",
                                                         filetypes=(("Pliki jpg", "*.jpg"), ("Pliki png", "*.png")))
        if new_avatar_filename:
            new_avatar = convert_to_binary_data(new_avatar_filename)
            self.user_model.set_user_avatar(new_avatar)
            self.logged_user_view.update_user_avatar()

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
        self.logged_user_view.update_user_status_view()
        self.meal_plan_view.update_consumed_products()
        self.close_popup_window()

    def close_popup_window(self):
        if self.popup_window is not None:
            self.popup_window.destroy()
            self.popup_window = None

    # --- PROFILE VIEW ---

    def open_profile_view_popup_window(self, window_type):
        if self.popup_window is None:
            if window_type == "gender":
                self.popup_window = SetGenderWindow(self.master, self.shared_view, self.user_model.user['gender'])
                self.popup_window.btn_set_gender.config(command=self.set_user_gender)
            elif window_type == 'weight':
                self.popup_window = SetWeightWindow(self.master, self.shared_view,
                                                    self.user_model.user['weight']['weight_value'])
                self.popup_window.btn_set_weight.config(command=self.set_user_weight)
            elif window_type == 'height':
                self.popup_window = SetHeightWindow(self.master, self.shared_view, self.user_model.user['height'])
                self.popup_window.btn_set_height.config(command=self.set_user_height)
            elif window_type == 'age':
                self.popup_window = SetAgeWindow(self.master, self.shared_view, self.user_model.user['age'])
                self.popup_window.btn_set_age.config(command=self.set_user_age)
            elif window_type == 'physical_activity':
                self.popup_window = SetActivityWindow(self.master, self.shared_view,
                                                      self.user_model.user['physical_activity'])
                self.popup_window.btn_set_activity.config(command=self.set_user_physical_activity)
            elif window_type == 'goal':
                self.popup_window = SetGoalWindow(self.master, self.shared_view, self.user_model.user['goal'])
                self.popup_window.btn_set_goal.config(command=self.set_user_goal)
            elif window_type == 'eval_gda':
                self.popup_window = EvaluateGDAWindow(self.master, self.shared_view)
                self.popup_window.btn_eval_gda.config(command=self.eval_user_gda)

            if self.popup_window is not None:
                self.popup_window.protocol('WM_DELETE_WINDOW', self.close_popup_window)
                self.popup_window.btn_back.config(command=self.close_popup_window)

                self.popup_window.focus_force()
        else:
            self.close_popup_window()

    def configure_profile_view_buttons(self):
        self.profile_view.btn_set_gender.config(command=lambda: self.open_profile_view_popup_window('gender'))
        self.profile_view.btn_set_weight.config(command=lambda: self.open_profile_view_popup_window('weight'))
        self.profile_view.btn_set_height.config(command=lambda: self.open_profile_view_popup_window('height'))
        self.profile_view.btn_set_age.config(command=lambda: self.open_profile_view_popup_window('age'))
        self.profile_view.btn_set_activity.config(
            command=lambda: self.open_profile_view_popup_window('physical_activity')
        )
        self.profile_view.btn_set_goal.config(command=lambda: self.open_profile_view_popup_window('goal'))
        self.profile_view.btn_eval_gda.config(command=lambda: self.open_profile_view_popup_window('eval_gda'))

    def set_user_gender(self):
        new_gender = self.popup_window.gender_value.get()
        if new_gender != self.user_model.user['gender'] and (new_gender == GENDER_MALE or new_gender == GENDER_FEMALE):
            self.database_model.update_user_gender(self.user_model.user['id_user'], new_gender)
            self.user_model.user['gender'] = new_gender
            self.profile_view.update_gender()

        self.close_popup_window()

    def set_user_weight(self):
        new_weight = self.popup_window.entry_weight.get()

        if not main_controller.is_float(new_weight):
            show_errorbox("Błędna waga", f"Waga musi być liczbą rzeczywistą!")
            return

        new_weight = round(float(new_weight), 1)
        if new_weight < WEIGHT_MIN or new_weight > WEIGHT_MAX:
            show_errorbox("Błędna waga", f"Waga musi być z przedziału [{WEIGHT_MIN},{WEIGHT_MAX}]!")
            return

        current_date = get_current_date()
        current_day_weight = self.database_model.select_user_weight_by_date(self.user_model.user['id_user'],
                                                                            current_date)
        update_weight = False
        if current_day_weight:
            if current_day_weight['weight_value'] != new_weight:
                self.database_model.update_user_weight_on_date(self.user_model.user['id_user'],
                                                               current_date, new_weight)
                update_weight = True
        else:
            self.database_model.insert_weight(self.user_model.user['id_user'], new_weight, current_date)
            update_weight = True

        if update_weight:
            self.user_model.update_weight()
            self.profile_view.update_weight()

        self.close_popup_window()

    def set_user_height(self):
        new_height = self.popup_window.entry_height.get()

        if not main_controller.is_float(new_height):
            show_errorbox("Błędny wzrost", f"Wzrost musi być liczbą rzeczywistą!")
            return

        new_height = round(float(new_height), 1)
        if new_height < HEIGHT_MIN or new_height > HEIGHT_MAX:
            show_errorbox("Błędny wzrost", f"Wzrost musi być z przedziału [{HEIGHT_MIN},{HEIGHT_MAX}]!")
            return

        if new_height != self.user_model.user['height']:
            self.database_model.update_user_height(self.user_model.user['id_user'], new_height)
            self.user_model.user['height'] = new_height
            self.profile_view.update_height()

        self.close_popup_window()

    def set_user_age(self):
        new_age = self.popup_window.entry_age.get()

        if not main_controller.is_int(new_age):
            show_errorbox("Błędny wiek", f"Wiek musi być liczbą całkowitą!")
            return

        new_age = int(new_age)
        if new_age < AGE_MIN or new_age > AGE_MAX:
            show_errorbox("Błędny wiek", f"Wiek musi być z przedziału [{AGE_MIN},{AGE_MAX}]!")
            return

        if new_age != self.user_model.user['age']:
            self.database_model.update_user_age(self.user_model.user['id_user'], new_age)
            self.user_model.user['age'] = new_age
            self.profile_view.update_age()

        self.close_popup_window()

    def set_user_physical_activity(self):
        new_physical_activity = self.popup_window.activity_value.get()[0]

        if not main_controller.is_int(new_physical_activity):
            show_errorbox("Błędna aktywność ruchowa", f"Wybierz swoją aktywność ruchową!")
            return

        new_physical_activity = int(new_physical_activity)
        if new_physical_activity < ACTIVITY_VALUE_MIN or new_physical_activity > ACTIVITY_VALUE_MAX:
            show_errorbox("Błędna aktywność ruchowa", f"Wybierz swoją aktywność ruchową!")
            return

        if new_physical_activity != self.user_model.user['physical_activity']:
            self.database_model.update_user_physical_activity(self.user_model.user['id_user'], new_physical_activity)
            self.user_model.user['physical_activity'] = new_physical_activity
            self.profile_view.update_physical_activity()

        self.close_popup_window()

    def set_user_goal(self):
        new_goal = self.popup_window.goal_value.get()[0]

        if not main_controller.is_int(new_goal):
            show_errorbox("Błędny cel", f"Wybierz swoj cel!")
            return

        new_goal = int(new_goal)
        if new_goal < GOAL_VALUE_MIN or new_goal > GOAL_VALUE_MAX:
            show_errorbox("Błędny cel", f"Wybierz swoj cel!")
            return

        if new_goal != self.user_model.user['goal']:
            self.database_model.update_user_goal(self.user_model.user['id_user'], new_goal)
            self.user_model.user['goal'] = new_goal
            self.profile_view.update_goal()

        self.close_popup_window()

    def eval_user_gda(self):
        new_gda = self.user_model.eval_gda_from_current_data()
        old_gda = self.user_model.user['gda']

        current_date = get_current_date()

        update_data = False
        if current_date == old_gda['gda_date']:
            if old_gda['gda_value'] != new_gda:
                self.database_model.update_user_gda_on_date(self.user_model.user['id_user'], current_date, new_gda)
                update_data = True
        elif old_gda['gda_date'] < current_date:
            self.database_model.insert_gda(self.user_model.user['id_user'], new_gda, current_date)
            update_data = True

        if update_data:
            self.user_model.update_gda()
            self.profile_view.update_gda()
            self.user_model.set_current_date(self.user_model.user['current_date'])
            self.logged_user_view.update_user_status_view()

        self.close_popup_window()

    # --- MEAL PLAN VIEW ---

    def configure_meal_plan_view_buttons(self):
        self.meal_plan_view.btn_delete_prod.config(command=lambda: self.open_meal_plan_popup_window('delete_prod'))
        self.meal_plan_view.btn_edit_prod.config(command=lambda: self.open_meal_plan_popup_window('edit_prod'))
        self.meal_plan_view.btn_add_prod.config(command=lambda: self.open_meal_plan_popup_window('add_prod'))

    def open_meal_plan_popup_window(self, window_type):
        if self.popup_window is None:
            if window_type == "delete_prod":
                if len(self.user_model.user['consumed_products']) > 0:
                    cprod_id = self.meal_plan_view.product_selected.get()
                    self.popup_window = DeleteConsumedProductWindow(self.master, self.shared_view,
                                                                    self.user_model.user['consumed_products'][cprod_id])
                    self.popup_window.btn_delete_prod.config(command=lambda: self.delete_consumed_product(cprod_id))
            if window_type == "edit_prod":
                if len(self.user_model.user['consumed_products']) > 0:
                    c_prod_index = self.meal_plan_view.product_selected.get()
                    product_to_edit = self.user_model.user['consumed_products'][c_prod_index]
                    radio_index = self.user_model.user['products_ids'].index(product_to_edit['id_product'])
                    grammage = self.user_model.user['consumed_products'][c_prod_index]['product_grammage']
                    self.popup_window = AddConsumedProductWindow(self.master, self.shared_view,
                                                                 self.user_model.user['products'],
                                                                 self.user_model.user['products_ids'], radio_index,
                                                                 grammage)
                    self.popup_window.btn_search.config(command=self.search_product)
                    self.popup_window.btn_add_prod.config(command=lambda: self.edit_consumed_product(c_prod_index))
            if window_type == "add_prod":
                self.popup_window = AddConsumedProductWindow(self.master, self.shared_view,
                                                             self.user_model.user['products'],
                                                             self.user_model.user['products_ids'])
                self.popup_window.btn_search.config(command=self.search_product)
                self.popup_window.btn_add_prod.config(command=self.add_consumed_product)

            if self.popup_window is not None:
                self.popup_window.protocol('WM_DELETE_WINDOW', self.close_popup_window)
                self.popup_window.btn_back.config(command=self.close_popup_window)

                self.popup_window.focus_force()
        else:
            self.close_popup_window()

    def delete_consumed_product(self, c_prod_index):
        consumed_product_id = self.user_model.user['consumed_products'][c_prod_index]['id_consumed_product']
        self.database_model.delete_consumed_product_by_id(self.user_model.user['id_user'], consumed_product_id)

        self.update_consumed_products()

        self.close_popup_window()

    def search_product(self):
        str_to_look_for = self.popup_window.entry_search.get()
        self.user_model.update_selected_products_ids(str_to_look_for)
        self.popup_window.update_products_list(self.user_model.user['selected_products_ids'])

    def edit_consumed_product(self, c_prod_index):
        consumed_product_id = self.user_model.user['consumed_products'][c_prod_index]['id_consumed_product']
        index = self.popup_window.product_selected.get()
        new_product_id = self.user_model.user['selected_products_ids'][index]
        new_grammage = self.popup_window.entry_grammage.get()

        if not self.correct_grammage_value(new_grammage):
            return

        self.database_model.update_consumed_product(consumed_product_id, new_product_id, new_grammage)

        self.update_consumed_products()

        self.close_popup_window()

    def add_consumed_product(self):
        if len(self.user_model.user['selected_products_ids']):
            index = self.popup_window.product_selected.get()

            product_id = self.user_model.user['selected_products_ids'][index]
            grammage = self.popup_window.entry_grammage.get()

            if not self.correct_grammage_value(grammage):
                return

            self.database_model.insert_consumed_product(product_id, self.user_model.user['id_user'],
                                                        self.user_model.user['current_date'], grammage)

            self.update_consumed_products()

        self.close_popup_window()

    def update_consumed_products(self):
        self.user_model.set_current_date(self.user_model.user['current_date'])
        self.meal_plan_view.update_consumed_products()
        self.logged_user_view.update_user_status_view()

    @staticmethod
    def correct_grammage_value(grammage):
        if not main_controller.is_int(grammage):
            show_errorbox("Błędna waga produktu", f"Waga produktu musi być liczbą całkowitą!")
            return False

        grammage = int(grammage)
        if grammage < GRAMMAGE_MIN or grammage > GRAMMAGE_MAX:
            show_errorbox("Błędna waga produktu", f"Waga produktu musi być z przedziału "
                                                  f"[{GRAMMAGE_MIN},{GRAMMAGE_MAX}]!")
            return False

        return True

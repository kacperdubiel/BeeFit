import os
from datetime import datetime, timedelta
from tkinter import filedialog

import Controllers.main_controller as main_controller
from Misc.config import DATE_FORMAT, WEIGHT_MIN, WEIGHT_MAX, HEIGHT_MIN, HEIGHT_MAX, \
    AGE_MIN, AGE_MAX, ACTIVITY_VALUE_MIN, ACTIVITY_VALUE_MAX, GOAL_VALUE_MIN, GOAL_VALUE_MAX, GRAMMAGE_MIN, \
    GRAMMAGE_MAX, FOOD_NAME_LENGTH_MIN, FOOD_NAME_LENGTH_MAX, CALORIES_MIN, CALORIES_MAX, GI_RATING_OPTIONS_LIST, \
    TRAINING_DURATION_MIN, TRAINING_DURATION_MAX
from Models.main_model import get_current_date, format_date, convert_to_binary_data
from Models.user_model import UserModel
from Views.logged_user_view import LoggedUserView, SetDateWindow
from Views.meal_plan_view import DeleteConsumedProductWindow, AddConsumedProductWindow, DeleteConsumedDishWindow, \
    AddConsumedDishWindow
from Views.profile_view import SetGenderWindow, SetHeightWindow, SetAgeWindow, SetWeightWindow, SetActivityWindow, \
    SetGoalWindow, EvaluateGDAWindow
from Views.shared_view import show_errorbox
from Views.user_dishes_view import DeleteDishWindow, AddDishWindow, DeleteDishProductWindow, AddDishProductWindow
from Views.user_products_view import DeleteProductWindow, AddProductWindow
from Views.user_trainings_view import DeleteTrainingWindow, AddTrainingWindow


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
        self.logged_user_view.btn_set_date.config(command=self.open_set_date_window)

        self.profile_view = self.logged_user_view.profile_view
        self.meal_plan_view = self.logged_user_view.meal_plan_view
        self.user_products_view = self.logged_user_view.user_products_view
        self.user_dishes_view = self.logged_user_view.user_dishes_view
        self.user_trainings_view = self.logged_user_view.user_trainings_view
        self.raports_view = self.logged_user_view.raports_view

        self.popup_window = None
        self.second_popup_window = None
        self.configure_profile_view_buttons()
        self.configure_meal_plan_view_buttons()
        self.configure_user_products_view_buttons()
        self.configure_user_dishes_view_buttons()
        self.configure_user_trainings_view_buttons()

    def change_user_avatar(self):
        new_avatar_filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Wybierz obrazek",
                                                         filetypes=(("Pliki jpg", "*.jpg"), ("Pliki png", "*.png")))
        if new_avatar_filename:
            new_avatar = convert_to_binary_data(new_avatar_filename)
            self.user_model.set_user_avatar(new_avatar)
            self.logged_user_view.update_user_avatar()

    # --- DATE ---

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

    def set_date(self):
        calendar_date = self.popup_window.calendar.get_date()
        self.set_current_date(calendar_date)

    def set_current_date(self, new_date):
        # Update data
        self.user_model.set_current_date(new_date)

        # Update views
        self.meal_plan_view.update_consumed_products()
        self.meal_plan_view.update_consumed_dishes()
        self.logged_user_view.update_user_status_view()
        self.profile_view.update_weight()
        self.profile_view.update_gda()
        self.user_trainings_view.update_trainings()
        self.raports_view.update_raports()

        self.close_popup_window()

    def open_set_date_window(self):
        if self.popup_window is None:
            current_date_string = self.user_model.user['current_date']
            date = datetime.strptime(current_date_string, DATE_FORMAT)
            current_date = {
                'day': date.day,
                'month': date.month,
                'year': date.year
            }

            self.popup_window = SetDateWindow(self.master, self.shared_view, current_date)
            self.popup_window.btn_set_date.config(command=self.set_date)

            if self.popup_window is not None:
                self.popup_window.protocol('WM_DELETE_WINDOW', self.close_popup_window)
                self.popup_window.btn_back.config(command=self.close_popup_window)

                self.popup_window.focus_force()
        else:
            self.close_popup_window()

    def close_popup_window(self):
        self.close_second_popup_window()
        if self.popup_window is not None:
            self.popup_window.destroy()
            self.popup_window = None

        str_to_find = self.user_products_view.entry_search.get()
        self.user_model.update_selected_products_ids(str_to_find)
        self.update_products()

        str_to_find = self.user_dishes_view.entry_search.get()
        self.user_model.update_selected_dishes_ids(str_to_find)
        self.update_dishes()

        self.update_user_trainings()
        self.raports_view.update_raports()

    @staticmethod
    def correct_grammage_value(grammage):
        if not main_controller.is_int(grammage):
            show_errorbox("Błędna waga", f"Waga musi być liczbą całkowitą!")
            return False

        grammage = int(grammage)
        if grammage < GRAMMAGE_MIN or grammage > GRAMMAGE_MAX:
            show_errorbox("Błędna waga", f"Waga musi być z przedziału [{GRAMMAGE_MIN},{GRAMMAGE_MAX}] g!")
            return False

        return True

    @staticmethod
    def correct_name(name):
        if len(name) < FOOD_NAME_LENGTH_MIN or len(name) > FOOD_NAME_LENGTH_MAX:
            show_errorbox("Błędna nazwa",
                          f"Nazwa musi mieć od {FOOD_NAME_LENGTH_MIN} do {FOOD_NAME_LENGTH_MAX} znaków!")
            return False

        return True

    @staticmethod
    def correct_calories_value(calories):
        if not main_controller.is_int(calories):
            show_errorbox("Błędna liczba kalorii", f"Liczba kalorii musi być liczbą całkowitą!")
            return False

        calories = int(calories)
        if calories < CALORIES_MIN or calories > CALORIES_MAX:
            show_errorbox("Błędna liczba kalorii",
                          f"Liczba kalorii musi być z przedziału [{CALORIES_MIN},{CALORIES_MAX}] kcal!")
            return False

        return True

    @staticmethod
    def correct_duration_value(duration):
        if not main_controller.is_int(duration):
            show_errorbox("Błędny czas treningu", f"Czas trwania treningu musi być liczbą całkowitą!")
            return False

        duration = int(duration)
        if duration < TRAINING_DURATION_MIN or duration > TRAINING_DURATION_MAX:
            show_errorbox("Błędny czas treningu",
                          f"Czas trwania treningu musi być z przedziału "
                          f"[{TRAINING_DURATION_MIN},{TRAINING_DURATION_MAX}] min!")
            return False

        return True

    @staticmethod
    def convert_gi_rating_name_to_number(value):
        if value == GI_RATING_OPTIONS_LIST[1]:
            return 1
        elif value == GI_RATING_OPTIONS_LIST[2]:
            return 2
        elif value == GI_RATING_OPTIONS_LIST[3]:
            return 3
        else:
            return 0

    # --- PROFILE VIEW ---

    def open_profile_view_popup_window(self, window_type):
        if self.popup_window is None:
            if window_type == "gender":
                self.popup_window = SetGenderWindow(self.master, self.shared_view, self.user_model.user['gender'])
                self.popup_window.btn_set_gender.config(command=self.set_user_gender)
            elif window_type == 'weight':
                self.popup_window = SetWeightWindow(self.master, self.shared_view,
                                                    self.user_model.user['current_date_weight']['weight_value'])
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

        current_date = self.user_model.user['current_date']
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
            self.user_model.set_current_date(self.user_model.user['current_date'])
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
        old_gda = self.user_model.user['current_date_gda']

        current_date = self.user_model.user['current_date']

        update_data = False
        if current_date == old_gda['gda_date']:
            if old_gda['gda_value'] != new_gda:
                self.database_model.update_user_gda_on_date(self.user_model.user['id_user'], current_date, new_gda)
                update_data = True
        else:
            self.database_model.insert_gda(self.user_model.user['id_user'], new_gda, current_date)
            update_data = True

        if update_data:
            self.user_model.set_current_date(self.user_model.user['current_date'])
            self.profile_view.update_gda()
            self.logged_user_view.update_user_status_view()

        self.close_popup_window()

    # --- MEAL PLAN VIEW ---

    def configure_meal_plan_view_buttons(self):
        self.meal_plan_view.btn_delete_prod.config(command=lambda: self.open_meal_plan_popup_window('delete_prod'))
        self.meal_plan_view.btn_edit_prod.config(command=lambda: self.open_meal_plan_popup_window('edit_prod'))
        self.meal_plan_view.btn_add_prod.config(command=lambda: self.open_meal_plan_popup_window('add_prod'))

        self.meal_plan_view.btn_delete_dish.config(command=lambda: self.open_meal_plan_popup_window('delete_dish'))
        self.meal_plan_view.btn_edit_dish.config(command=lambda: self.open_meal_plan_popup_window('edit_dish'))
        self.meal_plan_view.btn_add_dish.config(command=lambda: self.open_meal_plan_popup_window('add_dish'))

    def open_meal_plan_popup_window(self, window_type):
        if self.popup_window is None:
            if window_type == "delete_prod":
                if len(self.user_model.user['consumed_products']) > 0:
                    cprod_id = self.meal_plan_view.product_selected.get()
                    self.popup_window = DeleteConsumedProductWindow(self.master, self.shared_view,
                                                                    self.user_model.user['consumed_products'][cprod_id])
                    self.popup_window.btn_delete_prod.config(command=lambda: self.delete_consumed_product(cprod_id))
            elif window_type == "edit_prod":
                if len(self.user_model.user['consumed_products']) > 0:
                    c_prod_index = self.meal_plan_view.product_selected.get()
                    product_to_edit = self.user_model.user['consumed_products'][c_prod_index]
                    radio_index = self.user_model.user['products_ids'].index(product_to_edit['id_product'])
                    grammage = self.user_model.user['consumed_products'][c_prod_index]['product_grammage']
                    self.popup_window = AddConsumedProductWindow(self.master, self.shared_view,
                                                                 self.user_model.user['products'],
                                                                 self.user_model.user['products_ids'], radio_index,
                                                                 grammage)
                    self.popup_window.btn_search.config(command=self.search_product_popup)
                    self.popup_window.btn_add_prod.config(command=lambda: self.edit_consumed_product(c_prod_index))
            elif window_type == "add_prod":
                self.popup_window = AddConsumedProductWindow(self.master, self.shared_view,
                                                             self.user_model.user['products'],
                                                             self.user_model.user['products_ids'])
                self.popup_window.btn_search.config(command=self.search_product_popup)
                self.popup_window.btn_add_prod.config(command=self.add_consumed_product)
            elif window_type == "delete_dish":
                if len(self.user_model.user['consumed_dishes']) > 0:
                    cdish_id = self.meal_plan_view.dish_selected.get()
                    self.popup_window = DeleteConsumedDishWindow(self.master, self.shared_view,
                                                                 self.user_model.user['consumed_dishes'][cdish_id])
                    self.popup_window.btn_delete_dish.config(command=lambda: self.delete_consumed_dish(cdish_id))
            elif window_type == "edit_dish":
                if len(self.user_model.user['consumed_dishes']) > 0:
                    c_dish_index = self.meal_plan_view.dish_selected.get()
                    dish_to_edit = self.user_model.user['consumed_dishes'][c_dish_index]
                    radio_index = self.user_model.user['dishes_ids'].index(dish_to_edit['id_dish'])
                    grammage = self.user_model.user['consumed_dishes'][c_dish_index]['dish_grammage']
                    self.popup_window = AddConsumedDishWindow(self.master, self.shared_view,
                                                              self.user_model.user['dishes'],
                                                              self.user_model.user['dishes_ids'], radio_index,
                                                              grammage)
                    self.popup_window.btn_search.config(command=self.search_dish_popup)
                    self.popup_window.btn_add_dish.config(command=lambda: self.edit_consumed_dish(c_dish_index))
            elif window_type == "add_dish":
                self.popup_window = AddConsumedDishWindow(self.master, self.shared_view,
                                                          self.user_model.user['dishes'],
                                                          self.user_model.user['dishes_ids'])
                self.popup_window.btn_search.config(command=self.search_dish_popup)
                self.popup_window.btn_add_dish.config(command=self.add_consumed_dish)

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

    def search_product_popup(self):
        str_to_look_for = self.popup_window.entry_search.get()
        self.user_model.update_selected_products_ids(str_to_look_for)
        self.popup_window.default_radio = 0
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
        if len(self.user_model.user['selected_products_ids']) > 0:
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

    def delete_consumed_dish(self, c_dish_index):
        consumed_dish_id = self.user_model.user['consumed_dishes'][c_dish_index]['id_consumed_dish']
        self.database_model.delete_consumed_dish_by_id(self.user_model.user['id_user'], consumed_dish_id)

        self.update_consumed_dishes()

        self.close_popup_window()

    def search_dish_popup(self):
        str_to_look_for = self.popup_window.entry_search.get()
        self.user_model.update_selected_dishes_ids(str_to_look_for)
        self.popup_window.default_radio = 0
        self.popup_window.update_dishes_list(self.user_model.user['selected_dishes_ids'])

    def edit_consumed_dish(self, c_dish_index):
        consumed_dish_id = self.user_model.user['consumed_dishes'][c_dish_index]['id_consumed_dish']
        index = self.popup_window.dish_selected.get()
        new_dish_id = self.user_model.user['selected_dishes_ids'][index]
        new_grammage = self.popup_window.entry_grammage.get()

        if not self.correct_grammage_value(new_grammage):
            return

        self.database_model.update_consumed_dish(consumed_dish_id, new_dish_id, new_grammage)

        self.update_consumed_dishes()
        self.close_popup_window()

    def add_consumed_dish(self):
        if len(self.user_model.user['selected_dishes_ids']) > 0:
            index = self.popup_window.dish_selected.get()

            dish_id = self.user_model.user['selected_dishes_ids'][index]
            grammage = self.popup_window.entry_grammage.get()

            if not self.correct_grammage_value(grammage):
                return

            self.database_model.insert_consumed_dish(dish_id, self.user_model.user['id_user'],
                                                     self.user_model.user['current_date'], grammage)

        self.update_consumed_dishes()
        self.close_popup_window()

    def update_consumed_dishes(self):
        self.user_model.set_current_date(self.user_model.user['current_date'])
        self.meal_plan_view.update_consumed_dishes()
        self.logged_user_view.update_user_status_view()

    # --- USER PRODUCTS VIEW ---

    def configure_user_products_view_buttons(self):
        self.user_products_view.btn_delete_prod.config(
            command=lambda: self.open_user_products_popup_window('delete_prod'))
        self.user_products_view.btn_edit_prod.config(command=lambda: self.open_user_products_popup_window('edit_prod'))
        self.user_products_view.btn_add_prod.config(command=lambda: self.open_user_products_popup_window('add_prod'))
        self.user_products_view.btn_search.config(command=self.search_product)

    def open_user_products_popup_window(self, window_type):
        if self.popup_window is None:
            if window_type == "delete_prod":
                if len(self.user_model.user['selected_products_ids']) > 0:
                    prod_index = self.user_products_view.product_selected.get()
                    prod_id = self.user_model.user['selected_products_ids'][prod_index]
                    product = self.user_model.user['products'][f'{prod_id}']
                    self.popup_window = DeleteProductWindow(self.master, self.shared_view, product)
                    self.popup_window.btn_delete_prod.config(command=lambda: self.delete_product(prod_id))
            elif window_type == "edit_prod":
                if len(self.user_model.user['selected_products_ids']) > 0:
                    prod_index = self.user_products_view.product_selected.get()
                    prod_id = self.user_model.user['selected_products_ids'][prod_index]
                    product_to_edit = self.user_model.user['products'][f'{prod_id}']

                    product_name = product_to_edit['product_name']
                    product_calories = product_to_edit['calories']
                    product_image = product_to_edit['image']
                    product_gi_rating = product_to_edit['glycemic_index_rating']

                    self.popup_window = AddProductWindow(self.master, self.shared_view, product_name, product_calories,
                                                         product_image, product_gi_rating)
                    self.popup_window.btn_add_img.config(command=self.change_product_image)
                    self.popup_window.btn_add_prod.config(command=lambda: self.edit_product(prod_id))
            elif window_type == "add_prod":
                self.popup_window = AddProductWindow(self.master, self.shared_view)
                self.popup_window.btn_add_img.config(command=self.change_product_image)
                self.popup_window.btn_add_prod.config(command=self.add_product)

            if self.popup_window is not None:
                self.popup_window.protocol('WM_DELETE_WINDOW', self.close_popup_window)
                self.popup_window.btn_back.config(command=self.close_popup_window)

                self.popup_window.focus_force()
        else:
            self.close_popup_window()

    def delete_product(self, prod_id):
        self.database_model.delete_consumed_products_by_product_id(prod_id)
        self.database_model.delete_dishes_products_by_product_id(prod_id)
        self.database_model.delete_product_by_id(self.user_model.user['id_user'], prod_id)

        self.update_products()
        self.meal_plan_view.update_consumed_products()
        self.meal_plan_view.update_consumed_dishes()
        self.close_popup_window()

    def search_product(self):
        self.update_products()

    def edit_product(self, product_id):
        new_name = self.popup_window.entry_name.get()
        new_calories = self.popup_window.entry_calories.get()
        new_image = self.popup_window.default_image
        new_gi_rating = self.popup_window.gi_rating_value.get()
        new_gi_rating = self.convert_gi_rating_name_to_number(new_gi_rating)

        if not self.correct_name(new_name):
            return

        if not self.correct_calories_value(new_calories):
            return

        if self.popup_window.new_image:
            self.database_model.update_product(product_id, new_name, new_calories, new_image, new_gi_rating)
        else:
            self.database_model.update_product_without_img(product_id, new_name, new_calories, new_gi_rating)

        self.update_products()

        self.close_popup_window()

    def add_product(self):
        prod_name = self.popup_window.entry_name.get()
        prod_calories = self.popup_window.entry_calories.get()
        prod_image = self.popup_window.default_image
        prod_gi_rating = self.popup_window.gi_rating_value.get()
        prod_gi_rating = self.convert_gi_rating_name_to_number(prod_gi_rating)

        if not self.correct_name(prod_name):
            return

        if not self.correct_calories_value(prod_calories):
            return

        self.database_model.insert_product(self.user_model.user['id_user'], prod_name, prod_calories, prod_image,
                                           prod_gi_rating)

        self.update_products()

        self.close_popup_window()

    def change_product_image(self):
        new_image_filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Wybierz obrazek",
                                                        filetypes=(("Pliki jpg", "*.jpg"), ("Pliki png", "*.png")))
        if new_image_filename:
            new_image = convert_to_binary_data(new_image_filename)
            self.popup_window.set_product_image(new_image)

    def update_products(self):
        self.user_model.set_current_date(self.user_model.user['current_date'])
        str_to_find = self.user_products_view.entry_search.get()
        self.user_model.update_selected_products_ids(str_to_find)
        self.user_products_view.update_products()
        self.logged_user_view.update_user_status_view()

    # --- USER DISHES VIEW ---

    def configure_user_dishes_view_buttons(self):
        self.user_dishes_view.btn_delete_dish.config(
            command=lambda: self.open_user_dishes_popup_window('delete_dish'))
        self.user_dishes_view.btn_edit_dish.config(command=lambda: self.open_user_dishes_popup_window('edit_dish'))
        self.user_dishes_view.btn_add_dish.config(command=lambda: self.open_user_dishes_popup_window('add_dish'))
        self.user_dishes_view.btn_search.config(command=self.search_dish)

    def open_user_dishes_popup_window(self, window_type):
        if self.popup_window is None:
            if window_type == "delete_dish":
                if len(self.user_model.user['selected_dishes_ids']) > 0:
                    dish_index = self.user_dishes_view.dish_selected.get()
                    dish_id = self.user_model.user['selected_dishes_ids'][dish_index]
                    dish = self.user_model.user['dishes'][f'{dish_id}']
                    self.popup_window = DeleteDishWindow(self.master, self.shared_view, dish)
                    self.popup_window.btn_delete_dish.config(command=lambda: self.delete_dish(dish_id))
            elif window_type == "edit_dish":
                if len(self.user_model.user['selected_dishes_ids']) > 0:
                    dish_index = self.user_dishes_view.dish_selected.get()
                    dish_id = self.user_model.user['selected_dishes_ids'][dish_index]
                    dish_to_edit = self.user_model.user['dishes'][f'{dish_id}']

                    dish_name = dish_to_edit['dish_name']
                    dish_products = dish_to_edit['products']
                    dish_gi_rating = dish_to_edit['glycemic_index_rating']
                    dish_image = dish_to_edit['image']

                    self.products_ids_list = list()
                    self.products_grammage_list = list()

                    for dish_prod in dish_products:
                        self.products_ids_list.append(dish_prod['id_product'])
                        self.products_grammage_list.append(dish_prod['product_grammage'])

                    self.popup_window = AddDishWindow(self.master, self.shared_view, self.user_model.user['products'],
                                                      self.products_ids_list, self.products_grammage_list,
                                                      dish_name, dish_gi_rating, dish_image)
                    self.popup_window.btn_delete_prod.config(
                        command=lambda: self.open_dishes_products_popup_window('delete_prod', self.products_ids_list,
                                                                               self.products_grammage_list))
                    self.popup_window.btn_edit_prod.config(
                        command=lambda: self.open_dishes_products_popup_window('edit_prod', self.products_ids_list,
                                                                               self.products_grammage_list))
                    self.popup_window.btn_add_prod.config(
                        command=lambda: self.open_dishes_products_popup_window('add_prod', self.products_ids_list,
                                                                               self.products_grammage_list))

                    self.popup_window.btn_add_img.config(command=self.change_dish_image)
                    self.popup_window.btn_add_dish.config(command=lambda: self.edit_dish(dish_id,
                                                                                         self.products_ids_list,
                                                                                         self.products_grammage_list))
            elif window_type == "add_dish":
                self.products_ids_list = list()
                self.products_grammage_list = list()

                self.popup_window = AddDishWindow(self.master, self.shared_view, self.user_model.user['products'])

                self.popup_window.btn_delete_prod.config(
                    command=lambda: self.open_dishes_products_popup_window('delete_prod', self.products_ids_list,
                                                                           self.products_grammage_list))
                self.popup_window.btn_edit_prod.config(
                    command=lambda: self.open_dishes_products_popup_window('edit_prod', self.products_ids_list,
                                                                           self.products_grammage_list))
                self.popup_window.btn_add_prod.config(
                    command=lambda: self.open_dishes_products_popup_window('add_prod', self.products_ids_list,
                                                                           self.products_grammage_list))

                self.popup_window.btn_add_img.config(command=self.change_dish_image)
                self.popup_window.btn_add_dish.config(command=lambda: self.add_dish(self.products_ids_list,
                                                                                    self.products_grammage_list))

            if self.popup_window is not None:
                self.popup_window.protocol('WM_DELETE_WINDOW', self.close_popup_window)
                self.popup_window.btn_back.config(command=self.close_popup_window)

                self.popup_window.focus_force()
        else:
            self.close_popup_window()

    def delete_dish(self, dish_id):
        self.database_model.delete_consumed_dishes_by_dish_id(dish_id)
        self.database_model.delete_dishes_products_by_dish_id(dish_id)
        self.database_model.delete_dish_by_id(self.user_model.user['id_user'], dish_id)

        self.update_dishes()
        self.meal_plan_view.update_consumed_dishes()
        self.close_popup_window()

    def search_dish(self):
        self.update_dishes()

    def edit_dish(self, dish_id, products_ids_list, products_grammage_list):
        new_name = self.popup_window.entry_name.get()
        new_image = self.popup_window.default_image
        new_gi_rating = self.popup_window.gi_rating_value.get()
        new_gi_rating = self.convert_gi_rating_name_to_number(new_gi_rating)

        if not self.correct_name(new_name):
            return

        if self.popup_window.new_image:
            self.database_model.update_dish(dish_id, new_name, new_image, new_gi_rating)
        else:
            self.database_model.update_dish_without_img(dish_id, new_name, new_gi_rating)

        self.database_model.delete_dishes_products_by_dish_id(dish_id)
        self.database_model.insert_many_dishes_products(dish_id, products_ids_list, products_grammage_list)

        self.update_dishes()
        self.meal_plan_view.update_consumed_dishes()
        self.close_popup_window()

    def add_dish(self, products_ids_list, products_grammage_list):
        dish_name = self.popup_window.entry_name.get()
        dish_image = self.popup_window.default_image
        dish_gi_rating = self.popup_window.gi_rating_value.get()
        dish_gi_rating = self.convert_gi_rating_name_to_number(dish_gi_rating)

        if not self.correct_name(dish_name):
            return

        self.database_model.insert_dish(self.user_model.user['id_user'], dish_name, dish_image, dish_gi_rating)

        dish_id = self.database_model.select_user_last_dish_id(self.user_model.user['id_user'])
        self.database_model.insert_many_dishes_products(dish_id, products_ids_list, products_grammage_list)

        self.update_dishes()
        self.meal_plan_view.update_consumed_dishes()
        self.close_popup_window()

    def change_dish_image(self):
        new_image_filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Wybierz obrazek",
                                                        filetypes=(("Pliki jpg", "*.jpg"), ("Pliki png", "*.png")))
        if new_image_filename:
            new_image = convert_to_binary_data(new_image_filename)
            self.popup_window.set_dish_image(new_image)

    def update_dishes(self):
        self.user_model.set_current_date(self.user_model.user['current_date'])
        str_to_find = self.user_dishes_view.entry_search.get()
        self.user_model.update_selected_dishes_ids(str_to_find)
        self.user_dishes_view.update_dishes()
        self.logged_user_view.update_user_status_view()

    def open_dishes_products_popup_window(self, window_type, products_ids_list, products_grammage_list):
        if self.second_popup_window is None:
            if window_type == "delete_prod":
                if len(products_ids_list) > 0:
                    index = self.popup_window.product_selected.get()
                    product_id = products_ids_list[index]
                    product = self.user_model.user['products'][f'{product_id}']
                    self.second_popup_window = DeleteDishProductWindow(self.master, self.shared_view, product)
                    self.second_popup_window.btn_delete_prod.config(
                        command=lambda: self.delete_dish_product(products_ids_list, products_grammage_list, index))
            elif window_type == "edit_prod":
                if len(products_ids_list) > 0:
                    self.user_model.update_selected_products_ids("")
                    index = self.popup_window.product_selected.get()
                    product_id = products_ids_list[index]
                    product = self.user_model.user['products'][f'{product_id}']
                    radio_index = self.user_model.user['products_ids'].index(product['id_product'])
                    grammage = products_grammage_list[index]
                    self.second_popup_window = AddDishProductWindow(self.master, self.shared_view,
                                                                    self.user_model.user['products'],
                                                                    self.user_model.user['products_ids'], radio_index,
                                                                    grammage)
                    self.second_popup_window.btn_search.config(command=self.search_product_second_popup)
                    self.second_popup_window.btn_add_prod.config(
                        command=lambda: self.edit_dish_product(products_ids_list, products_grammage_list, index))
            elif window_type == "add_prod":
                self.user_model.update_selected_products_ids("")
                self.second_popup_window = AddDishProductWindow(self.master, self.shared_view,
                                                                self.user_model.user['products'],
                                                                self.user_model.user['products_ids'])
                self.second_popup_window.btn_search.config(command=self.search_product_second_popup)
                self.second_popup_window.btn_add_prod.config(
                    command=lambda: self.add_dish_product(products_ids_list, products_grammage_list))

            if self.second_popup_window is not None:
                self.second_popup_window.protocol('WM_DELETE_WINDOW', self.close_second_popup_window)
                self.second_popup_window.btn_back.config(command=self.close_second_popup_window)

                self.second_popup_window.focus_force()
        else:
            self.close_second_popup_window()

    def close_second_popup_window(self):
        if self.second_popup_window is not None:
            self.second_popup_window.destroy()
            self.second_popup_window = None

    def delete_dish_product(self, products_ids_list, products_grammage_list, index):
        products_ids_list.pop(index)
        products_grammage_list.pop(index)
        self.popup_window.update_products_list(products_ids_list, products_grammage_list)
        self.close_second_popup_window()

    def edit_dish_product(self, products_ids_list, products_grammage_list, index):
        position = self.second_popup_window.product_selected.get()
        product_new_id = self.user_model.user['selected_products_ids'][position]
        product_new_grammage = self.second_popup_window.entry_grammage.get()

        if not self.correct_grammage_value(product_new_grammage):
            return

        products_ids_list[index] = product_new_id
        products_grammage_list[index] = product_new_grammage
        self.popup_window.update_products_list(products_ids_list, products_grammage_list)

        self.close_second_popup_window()

    def add_dish_product(self, products_ids_list, products_grammage_list):
        position = self.second_popup_window.product_selected.get()
        new_product_id = self.user_model.user['selected_products_ids'][position]
        new_product_grammage = self.second_popup_window.entry_grammage.get()

        if not self.correct_grammage_value(new_product_grammage):
            return

        products_ids_list.append(new_product_id)
        products_grammage_list.append(new_product_grammage)
        self.popup_window.update_products_list(products_ids_list, products_grammage_list)

        self.close_second_popup_window()

    def search_product_second_popup(self):
        str_to_look_for = self.second_popup_window.entry_search.get()
        self.user_model.update_selected_products_ids(str_to_look_for)
        self.second_popup_window.update_products_list(self.user_model.user['selected_products_ids'])

    # --- USER TRAININGS VIEW

    def configure_user_trainings_view_buttons(self):
        self.user_trainings_view.btn_delete_training.config(
            command=lambda: self.open_user_trainings_popup_window('delete_training'))
        self.user_trainings_view.btn_edit_training.config(
            command=lambda: self.open_user_trainings_popup_window('edit_training'))
        self.user_trainings_view.btn_add_training.config(
            command=lambda: self.open_user_trainings_popup_window('add_training'))

    def open_user_trainings_popup_window(self, window_type):
        if self.popup_window is None:
            if window_type == "delete_training":
                if len(self.user_model.user['current_date_trainings']) > 0:
                    index = self.user_trainings_view.training_selected.get()
                    training = self.user_model.user['current_date_trainings'][index]

                    self.popup_window = DeleteTrainingWindow(self.master, self.shared_view, training)
                    self.popup_window.btn_delete_training.config(
                        command=lambda: self.delete_user_training(training['id_training']))
            elif window_type == "edit_training":
                if len(self.user_model.user['current_date_trainings']) > 0:
                    index = self.user_trainings_view.training_selected.get()
                    training = self.user_model.user['current_date_trainings'][index]

                    training_types = list()
                    for training_type in self.user_model.user['training_types']:
                        training_types.append(training_type['id_training_type'])

                    radio_index = training_types.index(training['id_training_type'])

                    duration = training['duration_in_min']

                    self.popup_window = AddTrainingWindow(self.master, self.shared_view,
                                                          self.user_model.user['training_types'], radio_index, duration)
                    self.search_training_type()
                    self.popup_window.btn_search.config(command=self.search_training_type)
                    self.popup_window.btn_add_training.config(
                        command=lambda: self.edit_user_training(training['id_training']))
            elif window_type == "add_training":
                self.popup_window = AddTrainingWindow(self.master, self.shared_view,
                                                      self.user_model.user['training_types'])
                self.search_training_type()
                self.popup_window.btn_search.config(command=self.search_training_type)
                self.popup_window.btn_add_training.config(command=self.add_user_training)

            if self.popup_window is not None:
                self.popup_window.protocol('WM_DELETE_WINDOW', self.close_popup_window)
                self.popup_window.btn_back.config(command=self.close_popup_window)

                self.popup_window.focus_force()
        else:
            self.close_popup_window()

    def delete_user_training(self, training_id):
        self.database_model.delete_training_by_id(training_id)

        self.update_user_trainings()

        self.close_popup_window()

    def search_training_type(self):
        str_to_look_for = self.popup_window.entry_search.get()
        self.user_model.update_selected_training_types(str_to_look_for)
        self.popup_window.default_radio = 0
        self.popup_window.update_training_types_list(self.user_model.user['selected_training_types'])

    def edit_user_training(self, training_id):
        index = self.popup_window.training_type_selected.get()
        new_training_type_id = self.user_model.user['selected_training_types'][index]['id_training_type']
        new_duration = self.popup_window.entry_duration.get()

        if not self.correct_duration_value(new_duration):
            return

        self.database_model.update_training(training_id, new_training_type_id, new_duration)

        self.update_user_trainings()

        self.close_popup_window()

    def add_user_training(self):
        if len(self.user_model.user['selected_training_types']) > 0:
            index = self.popup_window.training_type_selected.get()
            training_type_id = self.user_model.user['selected_training_types'][index]['id_training_type']

            duration = self.popup_window.entry_duration.get()

            if not self.correct_duration_value(duration):
                return

            self.database_model.insert_training(training_type_id, self.user_model.user['id_user'], duration,
                                                self.user_model.user['current_date'])

            self.update_user_trainings()

        self.close_popup_window()

    def update_user_trainings(self):
        self.user_model.set_current_date(self.user_model.user['current_date'])
        self.user_trainings_view.update_trainings()
        self.logged_user_view.update_user_status_view()


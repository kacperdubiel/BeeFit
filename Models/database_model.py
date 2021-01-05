import json
import os.path

from Database import sqlite_db
from Misc.config import TRAINING_TYPES_JSON_PATH, DB_NAME, DB_DIR
from Models.main_model import get_image_from_bytes


class DatabaseModel:
    def __init__(self):
        db_file_found = self.database_file_found()

        self.conn = sqlite_db.connect_to_db()

        if not db_file_found:
            self.create_database_tables()
            self.insert_default_training_types()

    @staticmethod
    def database_file_found():
        return os.path.isfile(f"{DB_DIR}{DB_NAME}.db")

    def create_database_tables(self):
        sqlite_db.create_all_tables(self.conn)

    def insert_default_training_types(self):
        json_file = open(TRAINING_TYPES_JSON_PATH, "r", encoding="utf-8")
        training_types_dict = json.load(json_file)
        json_file.close()

        training_types_list = list()
        for t in training_types_dict:
            training_types_list.append((t['training_name'], t['burned_calories_per_hour']))

        sqlite_db.insert_many_training_types(self.conn, training_types_list)

    # --- INSERT ---

    def insert_user(self, login, password, email, gender, height, age, physical_activity, goal, avatar):
        sqlite_db.insert_user(self.conn, login, password, email, gender, height, age, physical_activity, goal, avatar)

    def insert_weight(self, user_id, weight_value, weight_date):
        sqlite_db.insert_weight(self.conn, user_id, weight_value, weight_date)

    def insert_gda(self, user_id, gda_value, gda_date):
        sqlite_db.insert_gda(self.conn, user_id, gda_value, gda_date)

    def insert_product(self, id_user, new_prod_name, new_prod_calories, new_prod_img):
        sqlite_db.insert_product(self.conn, id_user, new_prod_name, new_prod_calories, new_prod_img)

    def insert_consumed_product(self, product_id, user_id, date, grammage):
        sqlite_db.insert_consumed_product(self.conn, product_id, user_id, date, grammage)

    def insert_consumed_dish(self, dish_id, user_id, date, grammage):
        sqlite_db.insert_consumed_dish(self.conn, dish_id, user_id, date, grammage)

    # --- SELECT ---

    def select_user_by_login(self, login):
        row = sqlite_db.select_user_by_login(self.conn, login)
        user = self.user_row_to_user_dict(row)
        user['avatar'] = get_image_from_bytes(user['avatar'])
        return user

    def select_user_by_login_and_password(self, login, password):
        row = sqlite_db.select_user_by_login_and_password(self.conn, login, password)
        user = self.user_row_to_user_dict(row)
        user['avatar'] = get_image_from_bytes(user['avatar'])
        return user

    def select_user_by_email(self, email):
        return sqlite_db.select_user_by_email(self.conn, email)

    def select_user_weight(self, id_user):
        row = sqlite_db.select_user_weight(self.conn, id_user)
        return self.weight_row_to_weight_dict(row)

    def select_user_weight_by_date(self, id_user, date):
        row = sqlite_db.select_user_weight_by_date(self.conn, id_user, date)
        return self.weight_row_to_weight_dict(row)

    def select_first_weight_before_date(self, id_user, current_date):
        row = sqlite_db.select_first_weight_before_date(self.conn, id_user, current_date)
        return self.weight_row_to_weight_dict(row)

    def select_first_weight_after_date(self, id_user, current_date):
        row = sqlite_db.select_first_weight_after_date(self.conn, id_user, current_date)
        return self.weight_row_to_weight_dict(row)

    def select_user_gda(self, id_user):
        row = sqlite_db.select_user_gda(self.conn, id_user)
        return self.gda_row_to_gda_dict(row)

    def select_first_gda_before_date(self, id_user, current_date):
        row = sqlite_db.select_first_gda_before_date(self.conn, id_user, current_date)
        return self.gda_row_to_gda_dict(row)

    def select_first_gda_after_date(self, id_user, current_date):
        row = sqlite_db.select_first_gda_after_date(self.conn, id_user, current_date)
        return self.gda_row_to_gda_dict(row)

    def select_user_products(self, id_user):
        rows = sqlite_db.select_user_products(self.conn, id_user)

        products = list()
        for row in rows:
            prod = self.product_row_to_product_dict(row)
            prod['image'] = get_image_from_bytes(prod['image'])
            products.append(prod)
        return products

    def select_user_dishes(self, id_user):
        rows = sqlite_db.select_user_dishes(self.conn, id_user)

        dishes = list()
        for row in rows:
            dish = self.dish_row_to_dish_dict(row)
            dish['image'] = get_image_from_bytes(dish['image'])

            dish['products'] = []
            dishes_products = sqlite_db.select_dishes_products(self.conn, dish['id_dish'])
            dish_calories = 0
            for d_product in dishes_products:
                d_prod_dict = self.dishes_products_row_to_dishes_products_dict(d_product)
                d_prod_dict['image'] = get_image_from_bytes(d_prod_dict['image'])

                dish_calories += int((d_prod_dict['calories'] * d_prod_dict['product_grammage']) / 100)
                dish['products'].append(d_prod_dict)

            dish['calories'] = dish_calories
            dishes.append(dish)
        return dishes

    def select_user_trainings_at_date(self, id_user, current_date):
        rows = sqlite_db.select_user_trainings_at_date(self.conn, id_user, current_date)

        trainings = list()
        for row in rows:
            trainings.append(self.training_row_to_training_dict(row))
        return trainings

    def select_user_consumed_products_at_date(self, id_user, current_date):
        rows = sqlite_db.select_user_consumed_products_at_date(self.conn, id_user, current_date)

        consumed_products = list()
        for row in rows:
            c_prod = self.consumed_prod_row_to_consumed_prod_dict(row)
            c_prod['image'] = get_image_from_bytes(c_prod['image'])
            c_prod['calories'] = int(float(c_prod['calories']) / 100 * c_prod['product_grammage'])
            consumed_products.append(c_prod)
        return consumed_products

    def select_user_consumed_dishes_at_date(self, id_user, current_date):
        rows = sqlite_db.select_user_consumed_dishes_at_date(self.conn, id_user, current_date)

        consumed_dishes = list()
        for row in rows:
            c_dish = self.consumed_dish_row_to_consumed_dish_dict(row)
            c_dish['image'] = get_image_from_bytes(c_dish['image'])
            consumed_dishes.append(c_dish)
        return consumed_dishes

    # --- UPDATE ---

    def update_user_avatar(self, id_user, new_avatar):
        sqlite_db.update_user_avatar(self.conn, id_user, new_avatar)

    def update_user_gender(self, id_user, new_gender):
        sqlite_db.update_user_gender(self.conn, id_user, new_gender)

    def update_user_weight_on_date(self, id_user, date, new_weight):
        sqlite_db.update_user_weight_on_date(self.conn, id_user, date, new_weight)

    def update_user_height(self, id_user, new_height):
        sqlite_db.update_user_height(self.conn, id_user, new_height)

    def update_user_age(self, id_user, new_age):
        sqlite_db.update_user_age(self.conn, id_user, new_age)

    def update_user_physical_activity(self, id_user, new_physical_activity):
        sqlite_db.update_user_physical_activity(self.conn, id_user, new_physical_activity)

    def update_user_goal(self, id_user, new_goal):
        sqlite_db.update_user_goal(self.conn, id_user, new_goal)

    def update_user_gda_on_date(self, id_user, date, new_gda):
        sqlite_db.update_user_gda_on_date(self.conn, id_user, date, new_gda)

    def update_product(self, id_product, new_prod_name, new_prod_calories, new_prod_img):
        sqlite_db.update_product(self.conn, id_product, new_prod_name, new_prod_calories, new_prod_img)

    def update_product_without_img(self, id_product, new_prod_name, new_prod_calories):
        sqlite_db.update_product_without_img(self.conn, id_product, new_prod_name, new_prod_calories)

    def update_consumed_product(self, id_consumed_product, new_product_id, new_grammage):
        sqlite_db.update_consumed_product(self.conn, id_consumed_product, new_product_id, new_grammage)

    def update_consumed_dish(self, id_consumed_dish, new_dish_id, new_grammage):
        sqlite_db.update_consumed_dish(self.conn, id_consumed_dish, new_dish_id, new_grammage)

    # --- DELETE ---

    def delete_product_by_id(self, id_user, id_product):
        sqlite_db.delete_product_by_id(self.conn, id_user, id_product)

    def delete_dish_by_id(self, id_user, id_dish):
        sqlite_db.delete_dish_by_id(self.conn, id_user, id_dish)

    def delete_consumed_product_by_id(self, id_user, id_consumed_product):
        sqlite_db.delete_consumed_product_by_id(self.conn, id_user, id_consumed_product)

    def delete_consumed_products_by_product_id(self, id_product):
        sqlite_db.delete_consumed_products_by_product_id(self.conn, id_product)

    def delete_consumed_dish_by_id(self, id_user, id_consumed_dish):
        sqlite_db.delete_consumed_dish_by_id(self.conn, id_user, id_consumed_dish)

    def delete_dishes_products_by_product_id(self, id_product):
        sqlite_db.delete_dishes_products_by_product_id(self.conn, id_product)

    # --- MISC ---

    @staticmethod
    def user_row_to_user_dict(row):
        if row is not None:
            user = {
                'id_user': row[0],
                'login': row[1],
                'password': row[2],
                'email': row[3],
                'gender': row[4],
                'height': row[5],
                'age': row[6],
                'physical_activity': row[7],
                'goal': row[8],
                'avatar': row[9]
            }
            return user
        else:
            return None

    @staticmethod
    def weight_row_to_weight_dict(row):
        if row is not None:
            weight = {
                'id_weight': row[0],
                'id_user': row[1],
                'weight_value': row[2],
                'weight_date': row[3]
            }
            return weight
        else:
            return None

    @staticmethod
    def product_row_to_product_dict(row):
        if row is not None:
            product = {
                'id_product': row[0],
                'id_user': row[1],
                'product_name': row[2],
                'calories': row[3],
                'image': row[4]
            }
            return product
        else:
            return None

    @staticmethod
    def dish_row_to_dish_dict(row):
        if row is not None:
            dish = {
                'id_dish': row[0],
                'id_user': row[1],
                'dish_name': row[2],
                'image': row[3]
            }
            return dish
        else:
            return None

    @staticmethod
    def dishes_products_row_to_dishes_products_dict(row):
        if row is not None:
            dish_product = {
                'id_dishes_products': row[0],
                'id_dish': row[1],
                'id_product': row[2],
                'product_grammage': row[3],
                'product_name': row[4],
                'calories': row[5],
                'image': row[6]
            }
            return dish_product
        else:
            return None

    @staticmethod
    def consumed_prod_row_to_consumed_prod_dict(row):
        if row is not None:
            consumed_product = {
                'id_consumed_product': row[0],
                'id_product': row[1],
                'id_user': row[2],
                'consumption_date': row[3],
                'product_grammage': row[4],
                'product_name': row[5],
                'calories': row[6],
                'image': row[7]
            }
            return consumed_product
        else:
            return None

    @staticmethod
    def consumed_dish_row_to_consumed_dish_dict(row):
        if row is not None:
            consumed_dish = {
                'id_consumed_dish': row[0],
                'id_dish': row[1],
                'id_user': row[2],
                'consumption_date': row[3],
                'dish_grammage': row[4],
                'dish_name': row[5],
                'image': row[6]
            }
            return consumed_dish
        else:
            return None

    @staticmethod
    def gda_row_to_gda_dict(row):
        if row is not None:
            gda = {
                'id_gda': row[0],
                'id_user': row[1],
                'gda_value': row[2],
                'gda_date': row[3]
            }
            return gda
        else:
            return None

    @staticmethod
    def training_row_to_training_dict(row):
        if row is not None:
            training = {
                'id_training': row[0],
                'id_training_type': row[1],
                'id_user': row[2],
                'duration_in_min': row[3],
                'training_date': row[4],
                'training_name': row[6],
                'burned_calories_per_min_per_kg': row[7]
            }
            return training
        else:
            return None

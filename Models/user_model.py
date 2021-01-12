import io
from calendar import monthrange
from datetime import datetime, timedelta

from PIL import Image

from Misc.config import DATE_FORMAT
from Models.main_model import get_current_date, evaluate_gda


class UserModel:
    def __init__(self, user, database_model):
        self.user = user
        self.database_model = database_model

        self.user['current_date'] = get_current_date()
        self.user['weight'] = self.get_user_weight()
        self.user['current_date_weight'] = self.get_user_current_date_weight()
        self.user['current_month_weights'] = self.get_user_current_month_weights()

        self.user['gda'] = self.get_user_gda()
        self.user['current_date_gda'] = self.get_user_current_date_gda()

        # Avatar settings
        self.AVATAR_MAX_SIZE = 140.0
        self.avatar_settings()

        self.user['products_ids'] = []
        self.user['products'] = self.get_user_products()
        self.user['selected_products_ids'] = self.get_user_selected_products_ids()

        self.user['dishes_ids'] = []
        self.user['dishes'] = self.get_user_dishes()
        self.user['selected_dishes_ids'] = self.get_user_selected_dishes_ids()

        self.user['consumed_products'] = self.get_user_consumed_products()
        self.user['consumed_dishes'] = self.get_user_consumed_dishes()

        self.user['training_types'] = self.get_training_types()
        self.user['current_date_trainings'] = self.get_user_current_date_trainings()
        self.user['selected_training_types'] = self.get_selected_training_types()

        self.user['calories_to_consume'] = self.get_calories_burned_current_date()
        self.user['calories_consumed'] = self.get_calories_consumed()
        self.user['calories_left'] = self.get_calories_left()
        self.user['current_week_calories_data'] = self.get_current_week_calories_data()

        self.user['progressbar_percent'] = self.get_progressbar_percent()

    def get_user_weight(self):
        return self.database_model.select_user_weight(self.user['id_user'])

    def get_user_current_date_weight(self):
        return self.get_user_closest_weight_to_date(self.user['current_date'])

    def get_user_closest_weight_to_date(self, date):
        found_weight = self.database_model.select_first_weight_before_date(self.user['id_user'], date)
        if found_weight is None:
            found_weight = self.database_model.select_first_weight_after_date(self.user['id_user'], date)
        return found_weight

    def get_user_current_month_weights(self):
        date = datetime.strptime(self.user['current_date'], DATE_FORMAT)
        _, end_day = monthrange(date.year, date.month)

        year = f"{date.year}"
        month = f"0{date.month}" if date.month < 10 else f"{date.month}"

        month_weights = list()
        for i in range(1, end_day + 1):
            day = f"0{i}" if i < 10 else f"{i}"
            current_date = f"{year}/{month}/{day}"

            weight = self.get_user_closest_weight_to_date(current_date)
            if weight:
                weight['weight_date'] = current_date
            else:
                weight = {
                    'weight_date': current_date,
                    'weight_value': 0
                }
            weight['year'] = f"{year}"
            weight['month'] = f"{month}"
            weight['day'] = f"{day}"
            month_weights.append(weight)

        return month_weights

    def get_user_gda(self):
        return self.database_model.select_user_gda(self.user['id_user'])

    def get_user_current_date_gda(self):
        return self.get_user_closest_gda_to_date(self.user['current_date'])

    def get_user_closest_gda_to_date(self, date):
        found_gda = self.database_model.select_first_gda_before_date(self.user['id_user'], date)
        if found_gda is None:
            found_gda = self.database_model.select_first_gda_after_date(self.user['id_user'], date)
        return found_gda

    def avatar_settings(self):
        self.user['avatar_width'], self.user['avatar_height'] = scale_image(self.user['avatar'], self.AVATAR_MAX_SIZE)
        self.user['avatar'] = self.user['avatar'].resize((self.user['avatar_width'], self.user['avatar_height']))

    def get_user_products(self):
        user_products = self.database_model.select_user_products(self.user['id_user'])
        products = {}
        self.user['products_ids'] = []
        for product in user_products:
            products[f'{product["id_product"]}'] = product
            self.user['products_ids'].append(product["id_product"])

        return products

    def get_user_selected_products_ids(self, str_to_look_for=""):
        found_ids = list()
        for prod_id in self.user['products_ids']:
            product_name = self.user['products'][f'{prod_id}']['product_name']
            str_to_look_for = str_to_look_for.lower()
            product_name = product_name.lower()
            if str_to_look_for in product_name:
                found_ids.append(prod_id)
        return found_ids

    def get_user_dishes(self):
        user_dishes = self.database_model.select_user_dishes(self.user['id_user'])
        dishes = {}
        self.user['dishes_ids'] = []
        for dish in user_dishes:
            dishes[f'{dish["id_dish"]}'] = dish
            self.user['dishes_ids'].append(dish["id_dish"])

        return dishes

    def get_user_selected_dishes_ids(self, str_to_look_for=""):
        found_ids = list()
        for dish_id in self.user['dishes_ids']:
            dish_name = self.user['dishes'][f'{dish_id}']['dish_name']
            str_to_look_for = str_to_look_for.lower()
            dish_name = dish_name.lower()
            if str_to_look_for in dish_name:
                found_ids.append(dish_id)
        return found_ids

    def get_user_consumed_products_at_date(self, date):
        return self.database_model.select_user_consumed_products_at_date(self.user['id_user'], date)

    def get_user_consumed_products(self):
        return self.get_user_consumed_products_at_date(self.user['current_date'])

    def get_user_consumed_dishes_at_date(self, date):
        consumed_dishes = self.database_model.select_user_consumed_dishes_at_date(self.user['id_user'], date)
        for c_dish in consumed_dishes:
            id_dish = c_dish['id_dish']
            dish_calories_per_100g = self.user['dishes'][f'{id_dish}']['calories_per_100g']
            grammage_consumed = c_dish['dish_grammage']
            c_dish['calories'] = int((dish_calories_per_100g * grammage_consumed) / 100)

        return consumed_dishes

    def get_user_consumed_dishes(self):
        return self.get_user_consumed_dishes_at_date(self.user['current_date'])

    def get_user_trainings_at_date(self, date):
        current_trainings = self.database_model.select_user_trainings_at_date(self.user['id_user'], date)
        current_weight = self.get_user_closest_weight_to_date(date)
        for training in current_trainings:
            training['burned_calories_per_min'] = round(training['burned_calories_per_min_per_kg']
                                                        * current_weight['weight_value'], 2)
            training['burned_calories'] = int(training['burned_calories_per_min'] * training['duration_in_min'])
            training['duration_hours'] = training['duration_in_min'] // 60
            training['duration_minutes'] = training['duration_in_min'] % 60

        return current_trainings

    def get_user_current_date_trainings(self):
        return self.get_user_trainings_at_date(self.user['current_date'])

    def get_training_types(self):
        training_types = self.database_model.select_training_types()
        for training_type in training_types:
            training_type['burned_calories_per_min'] = round(training_type['burned_calories_per_min_per_kg']
                                                             * self.user['current_date_weight']['weight_value'], 2)
        return training_types

    def update_training_types_burned_calories(self):
        for training_type in self.user['training_types']:
            training_type['burned_calories_per_min'] = round(training_type['burned_calories_per_min_per_kg']
                                                             * self.user['current_date_weight']['weight_value'], 2)

    def get_selected_training_types(self, str_to_look_for=""):
        found_training_types = list()
        for training in self.user['training_types']:
            training_name = training['training_name']
            str_to_look_for = str_to_look_for.lower()
            training_name = training_name.lower()
            if str_to_look_for in training_name:
                found_training_types.append(training)
        return found_training_types

    def get_calories_burned_at_date(self, date):
        calories_burned = 0
        gda = self.get_user_closest_gda_to_date(date)
        calories_burned += gda['gda_value']

        trainings = self.get_user_trainings_at_date(date)
        for t in trainings:
            calories_burned += t['burned_calories']

        return calories_burned

    def get_calories_burned_current_date(self):
        calories_to_consume = self.user['current_date_gda']['gda_value']

        for training in self.user['current_date_trainings']:
            calories_to_consume += training['burned_calories']

        return calories_to_consume

    def get_calories_consumed_at_date(self, date):
        calories_consumed = 0

        # Products calories
        consumed_products = self.get_user_consumed_products_at_date(date)
        for c_product in consumed_products:
            calories_consumed += c_product['calories']

        # Dishes calories
        consumed_dishes = self.get_user_consumed_dishes_at_date(date)
        for c_dish in consumed_dishes:
            calories_consumed += c_dish['calories']

        return calories_consumed

    def get_calories_consumed(self):
        calories_consumed = 0

        # Products calories
        for c_product in self.user['consumed_products']:
            calories_consumed += c_product['calories']

        # Dishes calories
        for c_dish in self.user['consumed_dishes']:
            calories_consumed += c_dish['calories']

        return calories_consumed

    def get_calories_left(self):
        calories_left = self.user['calories_to_consume'] - self.user['calories_consumed']
        if calories_left < 0:
            calories_left = 0
        return calories_left

    def get_progressbar_percent(self):
        progressbar_percent = 100
        if self.user['calories_to_consume'] > 0:
            progressbar_percent = int((self.user['calories_consumed'] * 100) / self.user['calories_to_consume'])
        return progressbar_percent

    def get_current_week_calories_data(self):
        date = datetime.strptime(self.user['current_date'], DATE_FORMAT)
        monday_date = date - timedelta(days=date.weekday())

        calories_data = []
        for i in range(0, 7):
            date = monday_date + timedelta(days=i)

            year = f"{date.year}"
            month = f"0{date.month}" if date.month < 10 else f"{date.month}"
            day = f"0{date.day}" if date.day < 10 else f"{date.day}"

            current_date = f"{year}/{month}/{day}"

            calories_consumed = self.get_calories_consumed_at_date(current_date)
            calories_burned = self.get_calories_burned_at_date(current_date)

            obj = {
                'date': current_date,
                'year': year,
                'month': month,
                'day': day,
                'calories_consumed': calories_consumed,
                'calories_burned': calories_burned
            }
            calories_data.append(obj)

        return calories_data

    def set_current_date(self, new_date):
        self.user['current_date'] = new_date

        self.user['products'] = self.get_user_products()
        self.user['dishes'] = self.get_user_dishes()

        self.user['current_date_weight'] = self.get_user_current_date_weight()
        self.update_current_month_weights()
        self.user['current_date_gda'] = self.get_user_current_date_gda()

        self.user['consumed_products'] = self.get_user_consumed_products()
        self.user['consumed_dishes'] = self.get_user_consumed_dishes()

        self.user['current_date_trainings'] = self.get_user_current_date_trainings()
        self.update_training_types_burned_calories()

        self.user['calories_to_consume'] = self.get_calories_burned_current_date()
        self.user['calories_consumed'] = self.get_calories_consumed()
        self.user['calories_left'] = self.get_calories_left()
        self.user['current_week_calories_data'] = self.get_current_week_calories_data()

        self.user['progressbar_percent'] = self.get_progressbar_percent()

    def set_user_avatar(self, new_avatar):
        self.database_model.update_user_avatar(self.user['id_user'], new_avatar)
        self.user['avatar'] = Image.open(io.BytesIO(new_avatar))
        self.avatar_settings()

    def update_weight(self):
        self.user['weight'] = self.get_user_weight()

    def update_current_month_weights(self):
        self.user['current_month_weights'] = self.get_user_current_month_weights()

    def eval_gda_from_current_data(self):
        return evaluate_gda(self.user['gender'], float(self.user['current_date_weight']['weight_value']),
                            float(self.user['height']), int(self.user['age']), int(self.user['physical_activity']),
                            int(self.user['goal']))

    def update_gda(self):
        self.user['gda'] = self.get_user_gda()

    def update_consumed_products(self):
        self.user['consumed_products'] = self.get_user_consumed_products()

    def update_selected_products_ids(self, str_to_look_for):
        self.user['selected_products_ids'] = self.get_user_selected_products_ids(str_to_look_for)

    def update_selected_dishes_ids(self, str_to_look_for):
        self.user['selected_dishes_ids'] = self.get_user_selected_dishes_ids(str_to_look_for)

    def update_selected_training_types(self, str_to_look_for):
        self.user['selected_training_types'] = self.get_selected_training_types(str_to_look_for)


# --- STATIC METHODS ---

def scale_image(img, max_size):
    img_width, img_height = img.size
    scale_from_width = img_height / max_size
    scale_from_height = img_width / max_size
    scale = max(scale_from_width, scale_from_height)
    new_img_width = int(img_width / scale)
    new_img_height = int(img_height / scale)
    return new_img_width, new_img_height

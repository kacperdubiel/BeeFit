import io
from Models.main_model import get_current_date, evaluate_gda
from PIL import Image


class UserModel:
    def __init__(self, user, database_model):
        self.user = user
        self.database_model = database_model

        self.user['current_date'] = get_current_date()
        self.user['weight'] = self.get_user_weight()
        self.user['current_date_weight'] = self.get_user_current_date_weight()

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

        self.user['consumed_products'] = self.get_user_consumed_products()
        self.user['consumed_dishes'] = self.get_user_consumed_dishes()

        self.user['current_date_trainings'] = self.get_user_current_date_trainings()

        self.user['calories_to_consume'] = self.get_calories_to_consume()
        self.user['calories_consumed'] = self.get_calories_consumed()
        self.user['calories_left'] = self.get_calories_left()

        self.user['progressbar_percent'] = self.get_progressbar_percent()

    def get_user_weight(self):
        return self.database_model.select_user_weight(self.user['id_user'])

    def get_user_current_date_weight(self):
        found_weight = self.database_model.select_first_weight_before_date(self.user['id_user'],
                                                                           self.user['current_date'])
        if found_weight is None:
            found_weight = self.database_model.select_first_weight_after_date(self.user['id_user'],
                                                                              self.user['current_date'])
        return found_weight

    def get_user_gda(self):
        return self.database_model.select_user_gda(self.user['id_user'])

    def get_user_current_date_gda(self):
        found_gda = self.database_model.select_first_gda_before_date(self.user['id_user'], self.user['current_date'])
        if found_gda is None:
            found_gda = self.database_model.select_first_gda_after_date(self.user['id_user'], self.user['current_date'])
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

    def get_user_consumed_products(self):
        return self.database_model.select_user_consumed_products_at_date(self.user['id_user'],
                                                                         self.user['current_date'])

    def get_user_consumed_dishes(self):
        consumed_dishes = self.database_model.select_user_consumed_dishes_at_date(self.user['id_user'],
                                                                                  self.user['current_date'])
        for c_dish in consumed_dishes:
            id_dish = c_dish['id_dish']
            dish_calories_per_100g = self.user['dishes'][f'{id_dish}']['calories']
            c_dish['calories'] = int(c_dish['dish_grammage'] * float(dish_calories_per_100g) / 100)

        return consumed_dishes

    def get_user_current_date_trainings(self):
        current_trainings = self.database_model.select_user_trainings_at_date(self.user['id_user'],
                                                                              self.user['current_date'])
        for training in current_trainings:
            training['burned_calories'] = int(training['burned_calories_per_min_per_kg'] * training['duration_in_min']
                                              * self.user['current_date_weight']['weight_value'])

        return current_trainings

    def get_calories_to_consume(self):
        calories_to_consume = self.user['current_date_gda']['gda_value']

        for training in self.user['current_date_trainings']:
            calories_to_consume += training['burned_calories']

        return calories_to_consume

    def get_calories_consumed(self):
        calories_consumed = 0

        # Products calories
        for c_product in self.user['consumed_products']:
            calories_consumed += c_product['calories']

        # Dishes calories
        for c_dish in self.user['consumed_dishes']:
            calories_consumed += self.user['dishes'][f'{c_dish["id_dish"]}']['calories']

        return calories_consumed

    def get_calories_left(self):
        calories_left = self.user['calories_to_consume'] - self.user['calories_consumed']
        if calories_left < 0:
            calories_left = 0
        return calories_left

    def get_progressbar_percent(self):
        progressbar_percent = 100
        if self.user['calories_to_consume'] > 0:
            progressbar_percent = int((self.user['calories_consumed']*100) / self.user['calories_to_consume'])
        return progressbar_percent

    def set_current_date(self, new_date):
        self.user['current_date'] = new_date

        self.user['current_date_weight'] = self.get_user_current_date_weight()
        self.user['current_date_gda'] = self.get_user_current_date_gda()

        self.user['consumed_products'] = self.get_user_consumed_products()
        self.user['consumed_dishes'] = self.get_user_consumed_dishes()

        self.user['current_date_trainings'] = self.get_user_current_date_trainings()

        self.user['calories_to_consume'] = self.get_calories_to_consume()
        self.user['calories_consumed'] = self.get_calories_consumed()
        self.user['calories_left'] = self.get_calories_left()

        self.user['progressbar_percent'] = self.get_progressbar_percent()

    def set_user_avatar(self, new_avatar):
        self.database_model.update_user_avatar(self.user['id_user'], new_avatar)
        self.user['avatar'] = Image.open(io.BytesIO(new_avatar))
        self.avatar_settings()

    def update_weight(self):
        self.user['weight'] = self.get_user_weight()

    def eval_gda_from_current_data(self):
        return evaluate_gda(self.user['gender'], float(self.user['weight']['weight_value']), float(self.user['height']),
                            int(self.user['age']), int(self.user['physical_activity']), int(self.user['goal']))

    def update_gda(self):
        self.user['gda'] = self.get_user_gda()

    def update_consumed_products(self):
        self.user['consumed_products'] = self.get_user_consumed_products()

    def update_selected_products_ids(self, str_to_look_for):
        self.user['selected_products_ids'] = self.get_user_selected_products_ids(str_to_look_for)


# --- STATIC METHODS ---

def scale_image(img, max_size):
    img_width, img_height = img.size
    scale_from_width = img_height / max_size
    scale_from_height = img_width / max_size
    scale = max(scale_from_width, scale_from_height)
    new_img_width = int(img_width / scale)
    new_img_height = int(img_height / scale)
    return new_img_width, new_img_height

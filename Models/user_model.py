import io
from Models.main_model import get_current_date
from PIL import Image


class UserModel:
    def __init__(self, user, database_model):
        self.user = user
        self.database_model = database_model

        self.user['weight'] = self.get_user_current_weight()

        # Avatar settings
        self.AVATAR_MAX_SIZE = 140.0
        self.avatar_settings()

        self.user['current_date'] = get_current_date()

        self.user['products'] = self.get_user_products()
        self.user['products_ids'] = []
        self.user['dishes'] = self.get_user_dishes()
        self.user['dishes_ids'] = []

        self.user['calories_to_consume'] = self.get_calories_to_consume()
        self.user['calories_consumed'] = self.get_calories_consumed()
        self.user['calories_left'] = self.get_calories_left()

        self.user['progressbar_percent'] = self.get_progressbar_percent()

    def get_user_current_weight(self):
        return self.database_model.select_user_current_weight(self.user['id_user'])

    def avatar_settings(self):
        self.user['avatar'] = self.get_image_from_bytes(self.user['avatar'])
        self.user['avatar_width'], self.user['avatar_height'] = self.scale_avatar()
        self.user['avatar'] = self.user['avatar'].resize((self.user['avatar_width'], self.user['avatar_height']))

    @staticmethod
    def get_image_from_bytes(bytes_img):
        return Image.open(io.BytesIO(bytes_img))

    def scale_avatar(self):
        avatar_width, avatar_height = self.user['avatar'].size
        scale_from_width = avatar_height / self.AVATAR_MAX_SIZE
        scale_from_height = avatar_width / self.AVATAR_MAX_SIZE
        scale = max(scale_from_width, scale_from_height)
        new_avatar_width = int(avatar_width / scale)
        new_avatar_height = int(avatar_height / scale)
        return new_avatar_width, new_avatar_height

    def get_user_products(self):
        user_products = self.database_model.select_user_products(self.user['id_user'])
        products = {}
        products_ids = []
        for product in user_products:
            products[f'{product["id_product"]}'] = product
            products_ids.append(product["id_product"])

        self.user['products_ids'] = products_ids
        return products

    def get_user_dishes(self):
        user_dishes = self.database_model.select_user_dishes(self.user['id_user'])
        dishes = {}
        dishes_ids = []
        for dish in user_dishes:
            dishes[f'{dish["id_dish"]}'] = dish
            dishes_ids.append(dish["id_dish"])

        self.user['dishes_ids'] = dishes_ids
        return dishes

    def get_user_current_gda(self):
        gda = 0

        found_gda = self.database_model.select_first_gda_before_date(self.user['id_user'], self.user['current_date'])
        if found_gda:
            gda = found_gda['gda_value']
        else:
            found_gda = self.database_model.select_first_gda_after_date(self.user['id_user'], self.user['current_date'])
            if found_gda:
                gda = found_gda['gda_value']

        return gda

    def get_calories_to_consume(self):
        calories_to_consume = self.get_user_current_gda()
        current_trainings = self.database_model.select_user_trainings_by_date(self.user['id_user'],
                                                                              self.user['current_date'])
        for training in current_trainings:
            calories_to_consume += int(training['duration'] * (training['burned_calories_per_hour']/60))

        return calories_to_consume

    def get_calories_consumed(self):
        calories_consumed = 0

        # Products calories
        consumed_products = self.database_model.select_user_consumed_products_at_date(self.user['id_user'],
                                                                                      self.user['current_date'])
        for c_product in consumed_products:
            calories_consumed += int((c_product['calories'] * c_product['product_grammage']) / 100)

        # Dishes calories
        consumed_dishes = self.database_model.select_user_consumed_dishes_at_date(self.user['id_user'],
                                                                                  self.user['current_date'])
        for c_dish in consumed_dishes:
            dish_calories = self.user['dishes'][f'{c_dish["id_dish"]}']['calories']
            calories_consumed += int((dish_calories * c_dish['dish_grammage']) / 100)

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

        self.user['products'] = self.get_user_products()
        self.user['dishes'] = self.get_user_dishes()

        self.user['calories_to_consume'] = self.get_calories_to_consume()
        self.user['calories_consumed'] = self.get_calories_consumed()
        self.user['calories_left'] = self.get_calories_left()

        self.user['progressbar_percent'] = self.get_progressbar_percent()

    def set_user_avatar(self, new_avatar):
        self.user['avatar'] = new_avatar
        self.avatar_settings()
        self.database_model.update_user_avatar(self.user['id_user'], new_avatar)

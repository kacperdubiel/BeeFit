import sqlite3
from sqlite3 import OperationalError, ProgrammingError

import Database.tables_schema as tables_schema
from Misc.config import DB_NAME, DB_DIR


# --- MAIN FUNCTIONS ---

def connect_to_db():
    mydb = f'{DB_DIR}{DB_NAME}.db'
    print('New connection to SQLite DB...')
    connection = sqlite3.connect(mydb)
    return connection


def disconnect_from_db(conn=None):
    if conn is not None:
        conn.close()


def connect(func):
    """
    Decorator to (re)open a sqlite database connection when needed.
    """

    def inner_func(conn, *args, **kwargs):
        try:
            # Simple query
            conn.execute(
                'SELECT name FROM sqlite_temp_master WHERE type="table";')
        except (AttributeError, ProgrammingError):
            conn = connect_to_db()
        return func(conn, *args, **kwargs)

    return inner_func


@connect
def create_table(conn, sql):
    try:
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        c.close()
    except OperationalError as e:
        print(e)


def create_all_tables(conn=None):
    create_table(conn, tables_schema.SQL_USERS_TABLE)
    create_table(conn, tables_schema.SQL_WEIGHTS_TABLE)
    create_table(conn, tables_schema.SQL_GDAS_TABLE)
    create_table(conn, tables_schema.SQL_TRAINING_TYPES_TABLE)
    create_table(conn, tables_schema.SQL_TRAININGS_TABLE)
    create_table(conn, tables_schema.SQL_PRODUCTS_TABLE)
    create_table(conn, tables_schema.SQL_DISHES_TABLE)
    create_table(conn, tables_schema.SQL_DISHES_PRODUCTS_TABLE)
    create_table(conn, tables_schema.SQL_CONSUMED_PRODUCTS_TABLE)
    create_table(conn, tables_schema.SQL_CONSUMED_DISHES_TABLE)


# --- CRUDs ---

@connect
def query(conn, sql, data_tuple):
    cursor = conn.cursor()
    cursor.execute(sql, data_tuple)
    conn.commit()
    cursor.close()


# --- INSERT ---

@connect
def insert_many_training_types(conn, training_types_list):
    sql = """
          INSERT INTO TrainingTypes (TrainingName, BurnedCaloriesPerMinPerKg)
          VALUES (?,?) 
          """

    cursor = conn.cursor()
    cursor.executemany(sql, training_types_list)
    conn.commit()
    cursor.close()


@connect
def insert_user(conn, login, password, email, gender, height, age, physical_activity, goal, avatar):
    sql = """
          INSERT INTO Users (Login,Password,Email,Gender,Height,Age,PhysicalActivity,Goal,Avatar)
          VALUES (?,?,?,?,?,?,?,?,?) 
          """
    data_tuple = (login, password, email, gender, height, age, physical_activity, goal, avatar)
    query(conn, sql, data_tuple)


@connect
def insert_weight(conn, user_id, weight_value, weight_date):
    sql = """
          INSERT INTO Weights (IdUser,WeightValue,WeightDate)
          VALUES (?,?,?) 
          """
    data_tuple = (user_id, weight_value, weight_date)

    query(conn, sql, data_tuple)


@connect
def insert_gda(conn, user_id, gda_value, gda_date):
    sql = """
          INSERT INTO GDAs (IdUser,GDAValue,GDADate)
          VALUES (?,?,?) 
          """
    data_tuple = (user_id, gda_value, gda_date)

    query(conn, sql, data_tuple)


@connect
def insert_product(conn, id_user, product_name, calories, image, glycemic_index_rating):
    sql = """
          INSERT INTO Products (IdUser,ProductName,Calories,Image,GlycemicIndexRating)
          VALUES (?,?,?,?,?) 
          """
    data_tuple = (id_user, product_name, calories, image, glycemic_index_rating)

    query(conn, sql, data_tuple)


@connect
def insert_dish(conn, id_user, dish_name, dish_image, dish_gi_rating):
    sql = """
          INSERT INTO Dishes (IdUser,DishName,Image,GlycemicIndexRating)
          VALUES (?,?,?,?) 
          """
    data_tuple = (id_user, dish_name, dish_image, dish_gi_rating)

    query(conn, sql, data_tuple)


@connect
def insert_many_dishes_products(conn, values):
    sql = """
          INSERT INTO DishesProducts (IdDish,IdProduct,ProductGrammage)
          VALUES (?,?,?) 
          """
    cursor = conn.cursor()
    cursor.executemany(sql, values)
    conn.commit()
    cursor.close()


@connect
def insert_consumed_product(conn, product_id, user_id, date, grammage):
    sql = """
          INSERT INTO ConsumedProducts (IdProduct,IdUser,ConsumptionDate,ProductGrammage)
          VALUES (?,?,?,?) 
          """
    data_tuple = (product_id, user_id, date, grammage)

    query(conn, sql, data_tuple)


@connect
def insert_consumed_dish(conn, dish_id, user_id, date, grammage):
    sql = """
          INSERT INTO ConsumedDishes (IdDish,IdUser,ConsumptionDate,DishGrammage)
          VALUES (?,?,?,?) 
          """
    data_tuple = (dish_id, user_id, date, grammage)

    query(conn, sql, data_tuple)


# --- SELECT ---

@connect
def select_user_by_login(conn, user_login):
    sql = """
          SELECT * FROM Users WHERE Login=?
          """
    cursor = conn.cursor()
    cursor.execute(sql, (user_login,))

    row = cursor.fetchone()
    return row


@connect
def select_user_by_login_and_password(conn, user_login, user_password):
    sql = """
          SELECT * FROM Users WHERE Login=? AND Password=?
          """
    cursor = conn.cursor()
    cursor.execute(sql, (user_login, user_password))

    row = cursor.fetchone()
    return row


@connect
def select_user_by_email(conn, user_email):
    sql = """
          SELECT * FROM Users WHERE Email=?
          """
    cursor = conn.cursor()
    cursor.execute(sql, (user_email,))

    row = cursor.fetchone()
    return row


@connect
def select_user_weight(conn, user_login):
    sql = """
          SELECT * FROM Weights WHERE IdUser=? ORDER BY WeightDate DESC LIMIT 1
          """
    cursor = conn.cursor()
    cursor.execute(sql, (user_login,))

    row = cursor.fetchone()
    return row


@connect
def select_user_weight_by_date(conn, user_login, date):
    sql = """
          SELECT * FROM Weights WHERE IdUser=? AND WeightDate=?
          """
    cursor = conn.cursor()
    cursor.execute(sql, (user_login, date))

    row = cursor.fetchone()
    return row


@connect
def select_first_weight_before_date(conn, id_user, current_date):
    sql = """
          SELECT * FROM Weights WHERE IdUser=? AND WeightDate<=? ORDER BY WeightDate DESC LIMIT 1
          """
    cursor = conn.cursor()
    cursor.execute(sql, (id_user, current_date))

    row = cursor.fetchone()
    return row


@connect
def select_first_weight_after_date(conn, id_user, current_date):
    sql = """
          SELECT * FROM Weights WHERE IdUser=? AND WeightDate>=? ORDER BY WeightDate ASC LIMIT 1
          """
    cursor = conn.cursor()
    cursor.execute(sql, (id_user, current_date))

    row = cursor.fetchone()
    return row


@connect
def select_user_gda(conn, user_login):
    sql = """
          SELECT * FROM GDAs WHERE IdUser=? ORDER BY GDADate DESC LIMIT 1
          """
    cursor = conn.cursor()
    cursor.execute(sql, (user_login,))

    row = cursor.fetchone()
    return row


@connect
def select_first_gda_before_date(conn, id_user, current_date):
    sql = """
          SELECT * FROM GDAs WHERE IdUser=? AND GDADate<=? ORDER BY GDADate DESC LIMIT 1
          """
    cursor = conn.cursor()
    cursor.execute(sql, (id_user, current_date))

    row = cursor.fetchone()
    return row


@connect
def select_first_gda_after_date(conn, id_user, current_date):
    sql = """
          SELECT * FROM GDAs WHERE IdUser=? AND GDADate>=? ORDER BY GDADate ASC LIMIT 1
          """
    cursor = conn.cursor()
    cursor.execute(sql, (id_user, current_date))

    row = cursor.fetchone()
    return row


@connect
def select_user_products(conn, user_id):
    sql = """
          SELECT * FROM Products WHERE IdUser=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (user_id,))

    rows = cursor.fetchall()
    return rows


@connect
def select_user_dishes(conn, user_id):
    sql = """
          SELECT * FROM Dishes WHERE IdUser=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (user_id,))

    rows = cursor.fetchall()
    return rows


@connect
def select_dishes_products(conn, dish_id):
    sql = """
          SELECT dp.IdDishesProducts, dp.IdDish, dp.IdProduct, dp.ProductGrammage, p.ProductName, p.Calories, p.Image,
          p.GlycemicIndexRating
          FROM DishesProducts AS dp
          INNER JOIN Products AS p ON dp.IdProduct=p.IdProduct
          WHERE IdDish=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (dish_id,))

    rows = cursor.fetchall()
    return rows


@connect
def select_user_last_dish_id(conn, id_user):
    sql = """
          SELECT IdDish FROM Dishes WHERE IdUser=? ORDER BY IdDish DESC LIMIT 1
          """
    cursor = conn.cursor()
    cursor.execute(sql, (id_user,))

    row = cursor.fetchone()
    return row


@connect
def select_user_trainings_at_date(conn, user_id, current_date):
    sql = """
          SELECT t.*, tt.*
          FROM Trainings AS t
          INNER JOIN TrainingTypes AS tt ON t.IdTrainingType=tt.IdTrainingType
          WHERE t.IdUser=? AND t.TrainingDate=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (user_id, current_date))

    rows = cursor.fetchall()
    return rows


@connect
def select_user_consumed_products_at_date(conn, user_id, current_date):
    sql = """
          SELECT cp.IdConsumedProduct, cp.IdProduct, cp.IdUser, cp.ConsumptionDate, cp.ProductGrammage, 
                 p.ProductName, p.Calories, p.Image, p.GlycemicIndexRating
          FROM ConsumedProducts AS cp
          INNER JOIN Products AS p ON cp.IdProduct=p.IdProduct
          WHERE cp.IdUser=? AND cp.ConsumptionDate=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (user_id, current_date))

    rows = cursor.fetchall()
    return rows


@connect
def select_user_consumed_dishes_at_date(conn, user_id, current_date):
    sql = """
          SELECT cd.IdConsumedDish, cd.IdDish, cd.IdUser, cd.ConsumptionDate, cd.DishGrammage, d.DishName, d.Image, 
          d.GlycemicIndexRating
          FROM ConsumedDishes AS cd
          INNER JOIN Dishes AS d ON cd.IdDish=d.IdDish
          WHERE cd.IdUser=? AND cd.ConsumptionDate=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (user_id, current_date))

    rows = cursor.fetchall()
    return rows


# --- UPDATE ---

@connect
def update_user_avatar(conn, user_id, new_avatar):
    sql = """
          UPDATE Users SET Avatar=? WHERE IdUser=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (new_avatar, user_id))
    conn.commit()


@connect
def update_user_gender(conn, user_id, new_gender):
    sql = """
          UPDATE Users SET Gender=? WHERE IdUser=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (new_gender, user_id))
    conn.commit()


@connect
def update_user_weight_on_date(conn, user_id, date, new_weight):
    sql = """
          UPDATE Weights SET WeightValue=? WHERE IdUser=? AND WeightDate=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (new_weight, user_id, date))
    conn.commit()


@connect
def update_user_height(conn, user_id, new_height):
    sql = """
          UPDATE Users SET Height=? WHERE IdUser=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (new_height, user_id))
    conn.commit()


@connect
def update_user_age(conn, user_id, new_age):
    sql = """
          UPDATE Users SET Age=? WHERE IdUser=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (new_age, user_id))
    conn.commit()


@connect
def update_user_physical_activity(conn, user_id, new_physical_activity):
    sql = """
          UPDATE Users SET PhysicalActivity=? WHERE IdUser=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (new_physical_activity, user_id))
    conn.commit()


@connect
def update_user_goal(conn, user_id, new_goal):
    sql = """
          UPDATE Users SET Goal=? WHERE IdUser=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (new_goal, user_id))
    conn.commit()


@connect
def update_user_gda_on_date(conn, user_id, date, new_gda):
    sql = """
          UPDATE GDAs SET GDAValue=? WHERE IdUser=? AND GDADate=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (new_gda, user_id, date))
    conn.commit()


@connect
def update_product(conn, id_product, new_prod_name, new_prod_calories, new_prod_img, glycemic_index_rating):
    sql = """
          UPDATE Products SET ProductName=?,Calories=?,Image=?,GlycemicIndexRating=? WHERE IdProduct=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (new_prod_name, new_prod_calories, new_prod_img, glycemic_index_rating, id_product))
    conn.commit()


@connect
def update_product_without_img(conn, id_product, new_prod_name, new_prod_calories, glycemic_index_rating):
    sql = """
          UPDATE Products SET ProductName=?,Calories=?,GlycemicIndexRating=? WHERE IdProduct=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (new_prod_name, new_prod_calories, glycemic_index_rating, id_product))
    conn.commit()


@connect
def update_dish(conn, dish_id, new_name, new_image, new_gi_rating):
    sql = """
          UPDATE Dishes SET DishName=?,Image=?,GlycemicIndexRating=? WHERE IdDish=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (new_name, new_image, new_gi_rating, dish_id))
    conn.commit()


@connect
def update_dish_without_img(conn, dish_id, new_name, new_gi_rating):
    sql = """
          UPDATE Dishes SET DishName=?,GlycemicIndexRating=? WHERE IdDish=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (new_name, new_gi_rating, dish_id))
    conn.commit()


@connect
def update_consumed_product(conn, id_consumed_product, new_product_id, new_grammage):
    sql = """
          UPDATE ConsumedProducts SET IdProduct=?,ProductGrammage=? WHERE IdConsumedProduct=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (new_product_id, new_grammage, id_consumed_product))
    conn.commit()


@connect
def update_consumed_dish(conn, id_consumed_dish, new_dish_id, new_grammage):
    sql = """
          UPDATE ConsumedDishes SET IdDish=?,DishGrammage=? WHERE IdConsumedDish=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (new_dish_id, new_grammage, id_consumed_dish))
    conn.commit()


# --- DELETE ---

def delete_product_by_id(conn, id_user, id_product):
    sql = """
          DELETE FROM Products WHERE IdProduct=? AND IdUser=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (id_product, id_user))
    conn.commit()


def delete_dish_by_id(conn, id_user, id_dish):
    sql = """
          DELETE FROM Dishes WHERE IdDish=? AND IdUser=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (id_dish, id_user))
    conn.commit()


def delete_consumed_product_by_id(conn, id_user, id_consumed_product):
    sql = """
          DELETE FROM ConsumedProducts WHERE IdConsumedProduct=? AND IdUser=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (id_consumed_product, id_user))
    conn.commit()


def delete_consumed_products_by_product_id(conn, id_product):
    sql = """
          DELETE FROM ConsumedProducts WHERE IdProduct=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (id_product,))
    conn.commit()


def delete_consumed_dish_by_id(conn, id_user, id_consumed_dish):
    sql = """
          DELETE FROM ConsumedDishes WHERE IdConsumedDish=? AND IdUser=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (id_consumed_dish, id_user))
    conn.commit()


def delete_consumed_dishes_by_dish_id(conn, id_dish):
    sql = """
          DELETE FROM ConsumedDishes WHERE IdDish=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (id_dish,))
    conn.commit()


def delete_dishes_products_by_product_id(conn, id_product):
    sql = """
          DELETE FROM DishesProducts WHERE IdProduct=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (id_product,))
    conn.commit()


def delete_dishes_products_by_dish_id(conn, id_dish):
    sql = """
          DELETE FROM DishesProducts WHERE IdDish=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (id_dish,))
    conn.commit()

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
          INSERT INTO TrainingTypes (TrainingName, BurnedCaloriesPerHour)
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
def select_user_current_weight(conn, user_login):
    sql = """
          SELECT WeightValue FROM Weights WHERE IdUser=? ORDER BY WeightDate DESC LIMIT 1
          """
    cursor = conn.cursor()
    cursor.execute(sql, (user_login,))

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
          SELECT dp.IdDishesProducts, dp.IdDish, dp.IdProduct, dp.ProductGrammage, p.ProductName, p.Calories, p.Image
          FROM DishesProducts AS dp
          INNER JOIN Products AS p ON dp.IdProduct=p.IdProduct
          WHERE IdDish=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (dish_id,))

    rows = cursor.fetchall()
    return rows

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
def select_user_trainings_by_date(conn, user_id, current_date):
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
                 p.ProductName, p.Calories, p.Image
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
          SELECT cd.IdConsumedDish, cd.IdDish, cd.IdUser, cd.ConsumptionDate, cd.DishGrammage, d.DishName, d.Image
          FROM ConsumedDishes AS cd
          INNER JOIN Dishes AS d ON cd.IdDish=d.IdDish
          WHERE cd.IdUser=? AND cd.ConsumptionDate=?;
          """
    cursor = conn.cursor()
    cursor.execute(sql, (user_id, current_date))

    rows = cursor.fetchall()
    return rows

import Controllers.main_controller as main_controller
from Controllers.user_controller import UserController
from Misc.config import NO_AVATAR_IMG_PATH
from Models.main_model import convert_to_binary_data, get_current_date, evaluate_gda
from Views.login_view import LoginView
from Views.register_view import RegisterView
from Views.shared_view import show_errorbox, show_infobox


class AccountController:
    def __init__(self, master, database_model, shared_view):
        self.master = master
        self.database_model = database_model
        self.shared_view = shared_view

        # Login view
        self.login_view = LoginView(master, self.shared_view)
        self.login_view.btn_register.config(command=self.open_register_window)
        self.login_view.btn_login.config(command=self.login)

        # Register
        self.register_view = None

        # User Controller
        self.user_controller = None

    # --- REGISTER ---

    def open_register_window(self):
        if self.register_view is None:
            self.register_view = RegisterView(self.master, self.shared_view)
            self.register_view.protocol('WM_DELETE_WINDOW', self.close_register_window)

            self.register_view.btn_back.config(command=self.close_register_window)
            self.register_view.btn_register_new_user.config(command=self.register_new_user)
        else:
            self.close_register_window()

    def close_register_window(self):
        if self.register_view is not None:
            self.register_view.destroy()
            self.register_view = None

    def register_new_user(self):
        entry_values = self.get_register_entry_values()

        error_title, error_msg = self.check_errors(entry_values)

        if error_title or error_msg:
            show_errorbox(error_title, error_msg)
        else:
            avatar = convert_to_binary_data(NO_AVATAR_IMG_PATH)
            self.database_model.insert_user(entry_values['login'], entry_values['password'], entry_values['email'],
                                            entry_values['gender'], entry_values['height'], entry_values['age'],
                                            entry_values['activity'], entry_values['goal'], avatar)
            user_id = self.database_model.select_user_by_login(entry_values['login'])['id_user']

            current_date = get_current_date()

            self.database_model.insert_weight(user_id, entry_values['weight'], current_date)

            gda_value = evaluate_gda(entry_values['gender'], float(entry_values['weight']),
                                     float(entry_values['height']), int(entry_values['age']),
                                     int(entry_values['activity']), int(entry_values['goal']))
            self.database_model.insert_gda(user_id, gda_value, current_date)
            self.close_register_window()
            show_infobox("Rejestracja udana", f"Utworzono nowego użytkownika o loginie: {entry_values['login']}")

    def get_register_entry_values(self):
        entry_values = {
            'login': self.register_view.entry_login.get(),
            'password': self.register_view.entry_password.get(),
            'password_check': self.register_view.entry_password_check.get(),
            'email': self.register_view.entry_email.get(),
            'gender': self.register_view.gender_value.get(),
            'weight': self.register_view.entry_weight.get(),
            'height': self.register_view.entry_height.get(),
            'age': self.register_view.entry_age.get(),
            'activity': self.register_view.activity_value.get()[0],
            'goal': self.register_view.goal_value.get()[0]
        }
        return entry_values

    def check_errors(self, vals):
        if vals['login'] is None or len(vals['login']) < 3 or len(vals['login']) > 30:
            return "Błędny login", "Login musi mieć od 3 do 30 znaków!"
        elif vals['login'] != main_controller.scrub(vals['login']):
            return "Błędny login", "Login posiada niedozwolone znaki!"
        elif vals['login'] and self.database_model.select_user_by_login(vals['login']) is not None:
            return "Błędny login", "Ten login jest już używany!"
        elif vals['password'] is None or len(vals['password']) < 3 or len(vals['password']) > 50:
            return "Błędne hasło", "Hasło musi mieć od 3 do 50 znaków!"
        elif vals['password'] != main_controller.scrub(vals['password']):
            return "Błędne hasło", "Hasło posiada niedozwolone znaki!"
        elif vals['password'] != vals['password_check']:
            return "Błąd w powtórzeniu hasła", "Hasła się różnią!"
        elif vals['email'] is None or len(vals['email']) < 5 or len(vals['email']) > 50:
            return "Błędny email", "Email musi mieć od 5 do 50 znaków!"
        elif vals['email'] and self.database_model.select_user_by_email(vals['email']) is not None:
            return "Błędny email", "Ten adres email jest już używany!"
        elif vals['gender'] != "M" and vals['gender'] != "K":
            return "Błędna płeć", "Wybierz płeć!"
        elif not main_controller.is_float(vals['weight']):
            return "Błędna waga", "Waga musi być liczbą rzeczywistą!"
        elif float(vals['weight']) < 10 or float(vals['weight']) > 300:
            return "Błędna waga", "Waga musi być liczbą rzeczywistą z przedziału [10,300]!"
        elif not main_controller.is_float(vals['height']):
            return "Błędny wzrost", "Wzrost musi być liczbą rzeczywistą!"
        elif float(vals['height']) < 60 or float(vals['height']) > 250:
            return "Błędny wzrost", "Wzrost musi być liczbą rzeczywistą z przedziału [60,250]!"
        elif not main_controller.is_int(vals['age']):
            return "Błędny wiek", "Wiek musi być liczbą całkowitą!"
        elif int(vals['age']) < 18 or int(vals['age']) > 150:
            return "Błędny wiek", "Wiek musi być liczbą całkowitą z przedziału [18,150]!"
        elif not main_controller.is_int(vals['activity']) or int(vals['activity']) < 1 or int(vals['activity']) > 5:
            return "Błędna aktywność ruchowa", "Wybierz swoją aktywność ruchową!"
        elif not main_controller.is_int(vals['goal']) or int(vals['goal']) < 1 or int(vals['goal']) > 3:
            return "Błędny cel", "Wybierz swoj cel!"
        else:
            return "", ""

    # --- LOGIN ---

    def login(self):
        login, password = self.get_login_entry_values()
        user = self.database_model.select_user_by_login_and_password(login, password)

        if user is not None:
            self.open_user_window(user)
        else:
            show_errorbox("Błąd logowania", "Podano błędny login lub hasło!")

    def get_login_entry_values(self):
        # Get login and password from login entries
        login = self.login_view.entry_login.get()
        password = self.login_view.entry_password.get()

        return login, password

    def open_user_window(self, user):
        # Close register window
        if self.register_view is not None:
            self.close_register_window()

        # Hide login window
        self.login_view.withdraw()

        # Create UserController with UserView
        if self.user_controller is None:
            self.user_controller = UserController(self.master, self.database_model, self.shared_view, user)
            self.user_controller.user_view.btn_logout.config(command=self.logout)
        else:
            self.logout()

    def logout(self):
        # Clear UserView and UserController then show login window.
        if self.user_controller.user_view:
            self.user_controller.user_view.destroy()

        if self.user_controller is not None:
            self.user_controller = None

        self.login_view.deiconify()


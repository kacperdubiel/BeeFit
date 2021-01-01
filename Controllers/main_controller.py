from Controllers.account_controller import AccountController
from Models.database_model import DatabaseModel
from Views.shared_view import SharedView


class MainController:
    def __init__(self, root):
        self.database_model = DatabaseModel()
        self.shared_view = SharedView()

        self.account_controller = AccountController(root, self.database_model, self.shared_view)


# --- MISC ---

def scrub(input_string):
    """
    Clean an input string (to prevent SQL injection).
    """
    return ''.join(k for k in input_string if k.isalnum())


def is_float(string_number):
    try:
        float(string_number)
        return True
    except ValueError:
        return False


def is_int(string_number):
    try:
        int(string_number)
        return True
    except ValueError:
        return False

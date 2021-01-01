from datetime import datetime

from Misc.config import DATE_FORMAT


class MainModel:
    def __init__(self):
        pass


def evaluate_gda(gender, weight, height, age, activity_val, goal_val):
    bmr_value = 0
    if gender == "M":
        bmr_value = 66.47 + (13.7 * weight) + (5 * height) - (6.76 * age)
    elif gender == "K":
        bmr_value = 665.09 + (9.56 * weight) + (1.85 * height) - (4.67 * age)

    gda_value = bmr_value
    if activity_val == 1:
        gda_value *= 1.2
    elif activity_val == 2:
        gda_value *= 1.4
    elif activity_val == 3:
        gda_value *= 1.65
    elif activity_val == 4:
        gda_value *= 1.9
    elif activity_val == 5:
        gda_value *= 2.1

    if goal_val == 1:
        return int(gda_value * 0.85)
    elif goal_val == 2:
        return int(gda_value)
    elif goal_val == 3:
        return int(gda_value * 1.17)


def get_current_date():
    current_date = datetime.now()
    return format_date(current_date)


def format_date(date):
    return date.strftime(DATE_FORMAT)


def convert_to_binary_data(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

from flask import request, make_response
import mysql.connector
import re  # Regular expressions
from functools import wraps


##############################
def db():
    try:
        db = mysql.connector.connect(
            host="mariadb",
            user="root",
            password="password",
            database="2026_1_wash_world_backend"
        )
        cursor = db.cursor(dictionary=True)
        return db, cursor
    except Exception as e:
        print(e, flush=True)
        raise Exception("Database under maintenance", 500)


##############################

"""REGEX_USER_EMAIL = "^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"""
REGEX_USER_EMAIL = "^(?:@a|@b|[^@\s]+@(?:[a-zA-Z0-9-]+.)+[a-zA-Z]{2,})$"


def validate_user_email():
    user_email = request.form.get("user_email", "").strip()
    if not re.match(REGEX_USER_EMAIL, user_email):
        raise Exception("company_exception user_email")
    return user_email


##############################
USER_FIRST_NAME_MIN = 2
USER_FIRST_NAME_MAX = 20
USER_FIRST_NAME_REGEX = f"^.{{{USER_FIRST_NAME_MIN},{USER_FIRST_NAME_MAX}}}$"


def validate_user_first_name():
    user_first_name = request.form.get("user_first_name", "").strip()
    if not re.match(USER_FIRST_NAME_REGEX, user_first_name):
        raise Exception(f"--error-- user_first_name")

    return user_first_name


##############################
USER_LAST_NAME_MIN = 2
USER_LAST_NAME_MAX = 20


def validate_user_last_name():
    user_last_name = request.form.get("user_last_name", "").strip()
    if len(user_last_name) < USER_LAST_NAME_MIN:
        raise Exception(
            f"User last name minimum {USER_LAST_NAME_MIN} characters", 400)
    if len(user_last_name) > USER_LAST_NAME_MAX:
        raise Exception(
            f"User last name maximum {USER_LAST_NAME_MAX} characters", 400)
    return user_last_name


##############################
USER_USERNAME_MIN = 2
USER_USERNAME_MAX = 20
USER_USERNAME_REGEX = f"^.{{{USER_USERNAME_MIN},{USER_USERNAME_MAX}}}$"


def validate_user_username():
    user_username = request.form.get("user_username", "").strip()
    if not re.match(USER_USERNAME_REGEX, user_username):
        raise Exception("--error-- user_username")
    return user_username


##############################
def no_cache(view):
    @wraps(view)
    def no_cache_view(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    return no_cache_view


###############################
USER_PASSWORD_MIN = 8
USER_PASSWORD_MAX = 50
REGEX_USER_PASSWORD = f"^.{{{USER_PASSWORD_MIN},{USER_PASSWORD_MAX}}}$"


def validate_user_password():
    user_password = request.form.get("user_password", "").strip()
    if not re.match(REGEX_USER_PASSWORD, user_password):
        raise Exception("company_exception user_password")
    return user_password


###############################
ALLOWED_USER_ROLES = {"user", "admin"}


def validate_user_role(user_role):
    user_role = str(user_role).strip().lower()
    if user_role not in ALLOWED_USER_ROLES:
        raise Exception("company_exception in user_role")
    return user_role

###############################
CAR_NUMBER_PLATE_REGEX = r"^[A-Z]{2}[0-9]{6}$"

def validate_car_number_plate():
    car_number_plate = request.form.get("car_number_plate", "").strip().upper()
    if not re.match(CAR_NUMBER_PLATE_REGEX, car_number_plate):
        raise Exception("company_exception car_number_plate")
    return car_number_plate

##############################
CAR_MODEL_MIN = 2
CAR_MODEL_MAX = 20
CAR_MODEL_REGEX = f"^.{{{CAR_MODEL_MIN},{CAR_MODEL_MAX}}}$"

def validate_car_model():
    car_model = request.form.get("car_model", "").strip()
    if not re.match(CAR_MODEL_REGEX, car_model):
        raise Exception("company_exception car_model")
    return car_model

##############################
CAR_BRAND_MIN = 2
CAR_BRAND_MAX = 20
CAR_BRAND_REGEX = f"^.{{{CAR_BRAND_MIN},{CAR_BRAND_MAX}}}$"

def validate_car_brand():
    car_brand = request.form.get("car_brand", "").strip()
    if not re.match(CAR_BRAND_REGEX, car_brand):
        raise Exception("company_exception car_brand")
    return car_brand
###############################
CAR_YEAR_MIN = 1900
CAR_YEAR_MAX = 2026
def validate_car_year():
    try:
        car_year = int(request.form.get("car_year", "").strip())
    except ValueError:
        raise Exception("company_exception car_year")
    if car_year < CAR_YEAR_MIN or car_year > CAR_YEAR_MAX:
        raise Exception("company_exception car_year")
    return car_year

##############################
CAR_COLOR_MAX = 20
REGEX_CAR_COLOR = rf"^[A-Za-zÆØÅæøå -]{{1,{CAR_COLOR_MAX}}}$"

def validate_car_color():
    car_color = request.form.get("car_color", "").strip()
    if not re.match(REGEX_CAR_COLOR, car_color):
        raise Exception("company_exception car_color")
    return car_color


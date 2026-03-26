from flask import Flask, render_template, request, jsonify, session, redirect
import x
import uuid
import time
from flask_session import Session


from icecream import ic
ic.configureOutput(prefix=f'______ | ', includeContext=True)

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


# TODO: "The next challenge. Same approach, create a fully working "signup" based on the requirements from Wash World. Design the database, think about validation, and the whole process"


###############################
@app.get("/")
def show_index():
    return render_template("index.html", x=x)

###############################


@app.get("/signup")
def show_signup():
    try:
        return render_template("signup.html", x=x)

    except Exception as ex:
        return ic(ex)

################################


@app.get("/login")
def show_login():
    try:
        
            return render_template("login.html", x=x)
    except Exception as ex:
        return ic(ex)


###############################
@app.get("/profile")
def show_profile():
    try:
        user = session.get("user", "") or session.get("admin", "")
        if not user:
            return redirect("/login")

        db, cursor = x.db()

        q = """
            SELECT 
            cars.car_plate_number,
            cars.car_model,
            cars.car_brand,
            cars.car_year,
            cars.car_color
            FROM user_cars
            INNER JOIN cars
                ON user_cars.cars_pk = cars.cars_pk
            WHERE user_cars.user_pk = %s
        """
        cursor.execute(q, (user["user_pk"],))
        cars = cursor.fetchall()

        return render_template("profile.html", x=x, user=user, cars=cars)
    except Exception as ex:
        ic(ex)

        return jsonify({"status": "error", "message": "nope"}), 500
    finally:
        if "cursor" in locals():
            cursor.close()
        if "db" in locals():
            db.close()

################################
@x.no_cache
@app.get("/logout")
def logout():
    try:
        session.clear()
        return redirect("/login")
    except Exception as ex:
        ic(ex)
        return "ups"




###############################
########### APIS ##############
###############################

@app.post("/signup")
def signup():
    try:
        user_first_name = x.validate_user_first_name()
        user_last_name = x.validate_user_last_name()
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()

        user_role = request.form.get("user_role", "").strip()

        user_role = x.validate_user_role(user_role)

        user_pk = uuid.uuid4().hex
        user_created_at = int(time.time())
        user_updated_at = int(time.time())
        user_deleted_at = int(time.time())

        db, cursor = x.db()

        q = "INSERT INTO users VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(q, (user_pk, user_email, user_password, user_first_name,
                       user_last_name, user_role, user_created_at, user_updated_at, user_deleted_at))

        db.commit()

        form_signup = render_template("___form_signup.html", x=x)

        return f"""
        <browser mix-replace="form">{form_signup}</browser>
        <browser mix-redirect="/login"></browser>
        
        """

    except Exception as ex:
        ic(ex)
        if "company_exception user_email" in str(ex):
            ic(ex)
            return jsonify({"status": "error", "message": "nope"}), 400
        return "ups"
    finally:
        if "cursor" in locals():
            cursor.close()
        if "db" in locals():
            db.close()


###############################


@app.post("/api-login")
def api_login():
    try:
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()

        

        db, cursor = x.db()

        


        q = "SELECT * FROM users WHERE user_email = %s"
        cursor.execute(q, (user_email,))

        user = cursor.fetchone()

        if not user:
            return jsonify({"status": "error", "message": "Invalid credentials"}), 400

        if user["user_password"] != user_password:
            return jsonify({"status": "error", "message": "Invalid credentials"}), 400
        
        user_role = x.validate_user_role(user["user_role"])

        safe_user = dict(user)
        safe_user.pop("user_password", None)
        session["user"] = safe_user

        return redirect("/profile")

    except Exception as ex:
        ic(ex)

        if "company_exception user_email" in str(ex):
            return jsonify({"status": "error", "message": "invalid email format"}), 400

        if "company_exception user_password" in str(ex):
            error_message = f"user password {x.USER_PASSWORD_MIN} to {x.USER_PASSWORD_MAX} characters"
            return jsonify({"status": "error", "message": error_message}), 400

        return jsonify({"status": "error", "message": "an unexpected error occurred"}), 500

    finally:
        if "cursor" in locals():
            cursor.close()
        if "db" in locals():
            db.close()


#############################
"""

@app.post("/login")
def login():
    try:
        user_email = x.validate_user_email()

        db, cursor = x.db()

        q = "SELECT user_role FROM users WHERE user_email = %s"
        cursor.execute(q, (user_email,))
        user = cursor.fetchone()
        
        if not user:
            data = {"status": "error"}
            return jsonify(data), 404

        data = {"status": "ok", "role": user["user_role"]}
        return jsonify(data)

    except Exception as ex:
        ic(ex)
        if "company_exception user_email" in str(ex):
            ic(ex)
            return jsonify({"status": "error", "message": "invalid email format"}), 400
        return "ups"
    finally:
        if "cursor" in locals():
            cursor.close()
        if "db" in locals():
            db.close()

"""


################################
@app.get("/api-user-cars/<user_pk>")
def get_user_cars(user_pk):
    try:
        db, cursor = x.db()

        q = """
            SELECT cars.*
            FROM user_cars
            INNER JOIN cars
            ON user_cars.cars_pk = cars.cars_pk
            WHERE user_cars.user_pk = %s
            """
        cursor.execute(q, (user_pk,))
        car = cursor.fetchall()

        if not car:
            return jsonify({"status": "error", "message": "Car not found"}), 404

        return jsonify({"status": "ok", "car": car})
    except Exception as ex:
        ic(ex)
        return jsonify({"status": "error", "message": "an unexpected error occurred"}), 500
    finally:
        if "cursor" in locals():
            cursor.close()
        if "db" in locals():
            db.close()

##############################
@app.post("/create-car")
def create_car():
    try:

        user = session.get("user")

        if not user:
            return redirect("/login")
        
        car_plate_number = x.validate_car_number_plate()
        car_model = x.validate_car_model()
        car_brand = x.validate_car_brand()
        car_year = x.validate_car_year()
        car_color = x.validate_car_color()



        car_pk = uuid.uuid4().hex
        

        db, cursor = x.db()

        q = """
            INSERT INTO cars (cars_pk, car_plate_number, car_model, car_brand, car_year, car_color)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(q, (car_pk, car_plate_number, car_model, car_brand, car_year, car_color))

        q = """
        INSERT INTO user_cars (user_pk, cars_pk)
        VALUES (%s, %s)
        """
        cursor.execute(q, (user["user_pk"], car_pk))
        db.commit()

        return redirect("/profile")

    except Exception as ex:
        ic(ex)
        return jsonify({"status": "error", "message": "an unexpected error occurred"}), 500

    finally:
        if "cursor" in locals():
            cursor.close()
        if "db" in locals():
            db.close()

###############################
@app.post("/api-get-name")
def api_get_name():
    try:
        name = "Mo"  # This comes from the database
        data = {"name": name}  # Dictionary

        return jsonify(data)
    except Exception as ex:
        ic(ex)
        return "ups"

    finally:
        pass


###############################
@app.post("/api-get-locations")
def api_get_locations():
    locations = [
        {"lat": 1, "lon": 11},
        {"lat": 2, "lon": 22},
        {"lat": 3, "lon": 33},
    ]
    return jsonify(locations)

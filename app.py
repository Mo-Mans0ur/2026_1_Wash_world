from flask import Flask, render_template, request, jsonify, session, redirect
import x
import uuid
import time
from flask_session import Session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

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
        user_role = x.validate_user_role(user_role)


       

        user_pk = uuid.uuid4().hex
        user_created_at = int(time.time())
        user_updated_at = int(time.time())

        db, cursor = x.db()

        q = "INSERT INTO users VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(q, (user_pk, user_first_name, user_last_name, user_email, user_password,user_role, user_created_at, user_updated_at))

        db.commit()

        form_signup = render_template("___form_signup.html")

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

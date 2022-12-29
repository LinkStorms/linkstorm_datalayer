from flask import Flask, request
from sqlalchemy import exc
import bcrypt

from models import db, User
from validation import (
    password_validation,
    username_validation,
    email_validation
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/create_user", methods=["POST"])
def create_user_endpoint():
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")

    validation_errors = []
    try:
        username_validation(username)
    except ValueError as e:
        validation_errors.append(str(e))
    try:
        email_validation(email)
    except ValueError as e:
        validation_errors.append(str(e))
    try:
        password_validation(password)
    except ValueError as e:
        validation_errors.append(str(e))
    
    if validation_errors:
        return {
            "code": 400,
            "data": {},
            "errors": validation_errors
        }

    # hash password with salt
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user = User(username=username, email=email, password=hashed_password)
    try:
        db.session.add(user)
        db.session.commit()
    except exc.IntegrityError:
        return {
            "code": 409,
            "data": {},
            "errors": ["User already exists."]
        }
    except exc.SQLAlchemyError:
        return {
            "code": 500,
            "data": {},
            "errors": ["Something went wrong."]
        }

    return {
        "code": 200,
        "data": {"user_id": user.id},
        "errors": []
    }

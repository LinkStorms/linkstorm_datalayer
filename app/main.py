from flask import Flask, request
from sqlalchemy import exc
from flasgger import Swagger, swag_from
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

Swagger(app)

with app.app_context():
    db.create_all()


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        # "name": e.name,
        "data": {},
        "errors": [e.description],
    })
    response.content_type = "application/json"
    return response


@app.route("/create_user", methods=["POST"])
@swag_from("flasgger_docs/create_user_endpoint.yml")
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

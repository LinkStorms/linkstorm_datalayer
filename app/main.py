from flask import Flask, request, json
from werkzeug.exceptions import HTTPException
from sqlalchemy import exc
from flasgger import Swagger, swag_from
import bcrypt

from models import (
    db,
    User,
    ShortUrl
)
from validation import (
    password_validation,
    username_validation,
    email_validation,
    user_id_validation,
    url_validation
)


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

Swagger(app)

with app.app_context():
    db.drop_all()
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
    username = request.json.get("username", "")
    email = request.json.get("email", "")
    password = request.json.get("password", "")

    # TODO: should we check if json only contains these three keys?

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


@app.route("/create_short_url", methods=["POST"])
@swag_from("flasgger_docs/create_short_url_endpoint.yml")
def create_short_url_endpoint():
    short_url = request.json.get("short_url", "")
    long_url = request.json.get("long_url", "")
    note = request.json.get("note", "")
    user_id = request.json.get("user_id", None)

    short_url_obj = ShortUrl(short_url=short_url, long_url=long_url, note=note, user_id=user_id)

    errors = []
    try:
        user_id_validation(user_id)
    except ValueError as e:
        errors.append(str(e))
    try:
        url_validation(long_url, url_name="long_url")
    except ValueError as e:
        errors.append(str(e))
    try:
        url_validation(short_url, url_name="short_url")
    except ValueError as e:
        errors.append(str(e))
    
    if errors:
        return {
            "code": 400,
            "data": {},
            "errors": errors
        }, 400

    try:
        db.session.add(short_url_obj)
        db.session.commit()
    except exc.IntegrityError:
        return {
            "code": 409,
            "data": {},
            "errors": ["Short Url already exists."]
        }, 409
    except exc.SQLAlchemyError:
        return {
            "code": 500,
            "data": {},
            "errors": ["Something went wrong."]
        }, 500

    return {
        "code": 200,
        "data": {"short_url_id": short_url_obj.id},
        "errors": []
    }, 200


@app.route("/short_url_list", methods=["GET"])
@swag_from("flasgger_docs/get_short_urls_for_user_endpoint.yml")
def get_short_urls_for_user_endpoint():
    user_id = request.args.get("user_id", None)

    try:
        user_id_validation(user_id)
    except ValueError as e:
        return {
            "code": 400,
            "data": {},
            "errors": [str(e)]
        }, 400

    short_url_list = ShortUrl.query.filter_by(user_id=user_id).all()
    data = {
        "code": 200,
        "data": {
            "short_url_list":
                [
                    {
                        "short_url": url.short_url,
                        "long_url": url.long_url,
                        "note": url.note
                    } for url in short_url_list
                ]
        },
        "errors": []
    }, 200
    return data

from flask import Flask, request
from sqlalchemy import exc

from models import db, User

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

    user = User(username=username, email=email, password=password)
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

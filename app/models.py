from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    short_urls = db.relationship("ShortUrl", backref="user")

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"


class ShortUrl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    short_url = db.Column(db.String, unique=True, nullable=False)
    long_url = db.Column(db.String, nullable=False)
    service = db.Column(db.String, nullable=False)
    note = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"<ShortUrl {self.id} for {self.user_id}: {self.short_url} -> {self.long_url}>"


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    token = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return f"<Token {self.id} for {self.user_id}: {self.name}>"

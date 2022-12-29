from models import  User

from email_validator import validate_email, EmailNotValidError


def password_validation(password):
    """ Returns true if password is at least 8 characters long, contains at
    least one number and one letter.
    """
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    if not any(char.isdigit() for char in password):
        raise ValueError ("Password must contain at least one digit.")
    if not any(char.isalpha() for char in password):
        return ValueError ("Password must contain at least one letter.")


def username_validation(username):
    """ Returns true if username is at least 3 characters long and contains
    only letters and numbers.
    """
    if len(username) < 3:
        raise ValueError("Username must be at least 3 characters long.")
    if not all(char.isalnum() for char in username):
        raise ValueError("Username must can only be letters and numbers.")
    if not any(char.isalpha() for char in username):
        raise ValueError("Username must contain at least one letter.")


def email_validation(email):
    """ Returns true if email is valid.
    """
    try:
        # check_deliverability is set to false to be able to create users with
        # fake emails.
        validate_email(email, check_deliverability=False)
    except EmailNotValidError as e:
        raise ValueError(str(e))


def user_id_validation(user_id, check_if_exists=True):
    """ Returns true if user_id is a valid user id.
    """

    if not user_id:
        raise ValueError("User id is required.")

    try:
        user_id = int(user_id)
    except ValueError:
        raise ValueError("User id must be an integer.")

    if check_if_exists:
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User does not exist.")

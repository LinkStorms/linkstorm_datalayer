from models import  User

from email_validator import validate_email, EmailNotValidError


def password_validation(password):
    """ Raises an exception if password is not valid.
    """
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    if not any(char.isdigit() for char in password):
        raise ValueError ("Password must contain at least one digit.")
    if not any(char.isalpha() for char in password):
        return ValueError ("Password must contain at least one letter.")


def username_validation(username):
    """ Raises an exception if username is not valid.
    """
    if len(username) < 3:
        raise ValueError("Username must be at least 3 characters long.")
    if not all(char.isalnum() for char in username):
        raise ValueError("Username must can only be letters and numbers.")
    if not any(char.isalpha() for char in username):
        raise ValueError("Username must contain at least one letter.")


def email_validation(email):
    """ Raises an exception if email is not valid.
    """
    try:
        # check_deliverability is set to false to be able to create users with
        # fake emails.
        validate_email(email, check_deliverability=False)
    except EmailNotValidError as e:
        raise ValueError(str(e))


def user_id_validation(user_id, check_if_exists=True):
    """  Raises an exception if user_id is not valid.
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

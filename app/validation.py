from email_validator import validate_email, EmailNotValidError
import validators

from settings import (
    PASSWORD_LENGTH_RANGE,
    USERNAME_LENGTH_RANGE,
    TOKEN_LENGTH_RANGE,
    TOKEN_NAME_LENGTH_RANGE,
    SERVICE_LENGTH_RANGE,
)
from models import  User


def password_validation(password, password_length_range=PASSWORD_LENGTH_RANGE):
    """ Raises an exception if password is not valid.
    """
    min_length, max_length = password_length_range
    if len(password) < min_length:
        raise ValueError(f"Password must be at least {min_length} characters long.")
    if len(password) > max_length:
        raise ValueError(f"Password must be less than {max_length} characters long.")
    if not any(char.isdigit() for char in password):
        raise ValueError ("Password must contain at least one digit.")
    if not any(char.isalpha() for char in password):
        return ValueError ("Password must contain at least one letter.")


def username_validation(username, username_length_range=USERNAME_LENGTH_RANGE):
    """ Raises an exception if username is not valid.
    """
    min_length, max_length = username_length_range
    if len(username) < min_length:
        raise ValueError(f"Username must be at least {min_length} characters long.")
    if len(username) > max_length:
        raise ValueError(f"Username must be less than {max_length} characters long.")
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


def url_validation(url, url_name="Url", ignore_protocol=False):
    """ Raises an exception if url is not valid.
    """
    if not url:
        raise ValueError("Url is required.")

    if ignore_protocol:
        url_with_protocol = "http://" + url
        if not validators.url(url_with_protocol) and not validators.url(url):
            raise ValueError(f"{url_name} is not valid.")
    else:
        if not validators.url(url):
            raise ValueError(f"{url_name} is not valid.")


def token_validation(token, token_length_range=TOKEN_LENGTH_RANGE):
    """ Raises an exception if token is not valid.
    """
    min_length, max_length = token_length_range

    if not token:
        raise ValueError("Token is required.")

    if len(token) < min_length:
        raise ValueError(f"Token must be at least {min_length} characters long.")
    if len(token) > max_length:
        raise ValueError(f"Token must be less than {max_length} characters long.")


def token_name_validation(token_name, token_name_length_range=TOKEN_NAME_LENGTH_RANGE):
    """ Raises an exception if token_name is not valid.
    """
    min_length, max_length = token_name_length_range

    if not token_name:
        raise ValueError("Token name is required.")

    if len(token_name) < min_length:
        raise ValueError(f"Token name must be at least {min_length} characters long.")
    if len(token_name) > max_length:
        raise ValueError(f"Token name must be less than {max_length} characters long.")


def token_id_validation(token_id):
    """ Raises an exception if token_id is not valid.
    """
    if not token_id:
        raise ValueError("Token id is required.")

    try:
        token_id = int(token_id)
    except ValueError:
        raise ValueError("Token id must be an integer.")


def short_url_id_validation(short_url_id):
    """ Raises an exception if short_url_id is not valid.
    """
    if not short_url_id:
        raise ValueError("Short url id is required.")

    try:
        short_url_id = int(short_url_id)
    except ValueError:
        raise ValueError("Short url id must be an integer.")


def service_validation(service, service_length_range=SERVICE_LENGTH_RANGE):
    """ Raises an exception if service is not valid.
    """
    if not service:
        raise ValueError("Service is required.")
    
    min_length, max_length = service_length_range
    if len(service) < min_length:
        raise ValueError(f"Service must be at least {min_length} characters long.")
    if len(service) > max_length:
        raise ValueError(f"Service must be less than {max_length} characters long.")

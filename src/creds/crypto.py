from . import __key
from . import Fernet

from errors.error import PropertyNotExistException


def encrypt_email(self):
    """Method encrypt_email() encrypts the user email so
    to store this field as a cache later. We use 'Fernet'
    class to encrypt user password.

        Fernet:
        Fernet guarantees that a message encrypted using it cannot
        be manipulated or read without the key. Fernet is an
        implementation of symmetric (also known as “secret key”)
        authenticated cryptography.
    """
    if not hasattr(self, "encrypted_email"):
        raise PropertyNotExistException(
            "Object 'self' must have a property 'encrypted_email' with credentials value in it!")

    if not hasattr(self, "data"):
        raise PropertyNotExistException(
            "Object 'self' must have a property 'data' with user's decoded credentials field in it!")

    fernet = Fernet(__key)

    self.encrypted_email = fernet.encrypt(
        self.data["user_email"].encode()).decode()

    del fernet


def encrypt_password(self):
    """Method encrypt_password() encrypts the user password so
    to store this field as a cache later. We use 'Fernet' class
    to encrypt user password.

    Fernet:
        Fernet guarantees that a message encrypted using it cannot
        be manipulated or read without the key. Fernet is an
        implementation of symmetric (also known as “secret key”)
        authenticated cryptography.
    """
    if not hasattr(self, "encrypted_password"):
        raise PropertyNotExistException(
            "Object 'self' must have a property 'encrypted_password' with credentials value in it!")

    if not hasattr(self, "data"):
        raise PropertyNotExistException(
            "Object 'self' must have a property 'data' with user's decoded credentials field in it!")

    fernet = Fernet(__key)

    self.encrypted_password = fernet.encrypt(
        self.data["user_password"].encode()).decode()

    del fernet


def decrypt_credentials(self, config):
    """Method decrypt_credentials() decrypts the encrypted user
    credentials that are stored in the Credentials file. We use
    class 'Fernet' to achive this functionality.

    Fernet:
        Fernet guarantees that a message encrypted using it cannot
        be manipulated or read without the key. Fernet is an
        implementation of symmetric (also known as “secret key”)
        authenticated cryptography.

    Args:
        config: it is a dictionary object that holds user encrypted
        fields.
    """
    if not hasattr(self, "data"):
        raise PropertyNotExistException(
            "Object 'self' must have a property 'data' with user's encoded credentials field in it!")

    fernet = Fernet(__key)

    self.data["user_email"] = fernet.decrypt(
        config["Username"].encode('utf-8')).decode('utf-8')
    self.data["user_password"] = fernet.decrypt(
        config["Password"].encode('utf-8')).decode('utf-8')

    del fernet

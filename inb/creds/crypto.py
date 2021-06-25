from . import Creds
from . import Fernet

from errors.error import PropertyNotExistException


def encrypt_email(self: object) -> None:
    """Function encrypt_email() encrypts the user email so to store this field 
    as cache later.

    :Fernet:
        Fernet guarantees that a message encrypted using it cannot be manipulated
        or read without the key. Fernet is an implementation of symmetric (also known 
        as “secret key”) authenticated cryptography.

    :Args:
        - self: {object} object from which 'encrypted_email' and 'data' properties are to be
            accessed.

    :Raises:
        - {PropertyNotExistException} if required properties can't be found in 'self' object.

    :Returns:
        - {None} 
    """
    if not hasattr(self, "encrypted_email"):
        raise PropertyNotExistException(
            "Object 'self' must have a property 'encrypted_email' with credentials value in it!")

    if not hasattr(self, "user"):
        raise PropertyNotExistException(
            "Object 'self' must have a property 'data' with user's decoded credentials field in it!")

    fernet = Fernet(Creds.get_key())

    setattr(self, "encrypted_email", fernet.encrypt(
        self.user_email.encode()).decode())

    del fernet


def encrypt_password(self: object) -> None:
    """Function encrypt_password() encrypts the user password so to store this field 
    as cache later.

    :Fernet:
        Fernet guarantees that a message encrypted using it cannot be manipulated
        or read without the key. Fernet is an implementation of symmetric (also known 
        as “secret key”) authenticated cryptography.

    :Args:
        - self: {object} object from which 'encrypted_password' and 'data' properties are to be
            accessed.

    :Raises:
        - {PropertyNotExistException} if required properties can't be found in 'self' object.

    :Returns:
        - {None}
    """
    if not hasattr(self, "encrypted_password"):
        raise PropertyNotExistException(
            "Object 'self' must have a property 'encrypted_password' with credentials value in it!")

    if not hasattr(self, "user"):
        raise PropertyNotExistException(
            "Object 'self' must have a property 'data' with user's decoded credentials field in it!")

    fernet = Fernet(Creds.get_key())

    setattr(self, "encrypted_password", fernet.encrypt(
        self.user_password.encode()).decode())

    del fernet


def decrypt_credentials(self: object, config: dict) -> None:
    """Function decrypt_credentials() decrypts the encrypted user credentials that 
    are stored in the Credentials file.

    :Fernet:
        Fernet guarantees that a message encrypted using it cannot be manipulated
        or read without the key. Fernet is an implementation of symmetric (also known 
        as “secret key”) authenticated cryptography.

    :Args:
        - self: {object} object from which 'data' property is to be accessed.
        - config: {dict} dictionary that holds user's encrypted fields.

    :Raises:
        - {PropertyNotExistException} if required properties can't be found in 'self' object.

    :Returns:
        - {None}
    """
    if not hasattr(self, "user"):
        raise PropertyNotExistException(
            "Object 'self' must have a property 'data' with user's encoded credentials field in it!")

    fernet = Fernet(Creds.get_key())

    self.user_email = fernet.decrypt(
        config["Username"].encode("utf-8")).decode("utf-8")
    self.user_password = fernet.decrypt(
        config["Password"].encode("utf-8")).decode("utf-8")

    del fernet

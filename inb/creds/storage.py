import os

from . import Creds

from creds.crypto import decrypt_credentials

from errors.error import PropertyNotExistException
from errors.error import UserCacheNotFoundException


def store_credentials(self: object) -> None:
    """Function store_credentials() stores the user secret fields as cache in a file 
    'CredentialsFile.ini' inside of the 'creds' folder that is inside of the project's
    root directory so to use these fields later.

    :Args:
        - self: {object} object from which 'encrypted_email' and 'encrypted_password' are
            to be accessed.

    :Raises:
        - {PropertyNotExistsException} if required properties can't be found in 'self' object.

    :Returns:
        - {None}
    """
    if not hasattr(self, "encrypted_email") or not hasattr(self, "encrypted_password"):
        raise PropertyNotExistException(
            "Object 'self' must have properties 'encrypted_email'|'encrypted_password' with credentials value in it!")

    with open(Creds.get_credentials_file(), 'w') as creds_file:
        creds_file.write("Username={}\nPassword={}\n".format(
            getattr(self, "encrypted_email"), getattr(self, "encrypted_password")))


def get_credentials(self: object) -> None:
    """Function get_credentials() reads the credentials stored as cache in file 
    'CredentialsFile.ini' inside of the 'creds' folder that is inside of the project's
    root directory if exists.

    :Args:
        - self: {object} object from which 'data' property is to be accessed.

    :Raises:
        - {UserCacheNotFoundException} if user's credentials are not found.

    :Returns:
        - {None}
    """
    if not os.path.exists(Creds.get_credentials_file()):
        return

    try:
        with open(Creds.get_credentials_file(), 'r') as creds_file:
            lines = creds_file.readlines()

            config = {
                "Username": "",
                "Password": ""
            }

            for line in lines:
                creds = line.rstrip('\n').split('=', 1)
                if creds[0] in ("Username", "Password"):
                    config[creds[0]] = creds[1]

            decrypt_credentials(self, config)
    except FileNotFoundError:
        raise UserCacheNotFoundException(
            "You don't have any cache stored!")


def delete_cache() -> None:
    """Function delete_cache() deletes the stored cache (User credentials) if exists, 
    we use os.path.exists() to check if the file is present or not if present we remove it.

    :Args:
        - {None}

    :Raises:
        - {FileNotFoundError} if the credential file doesn't exist.

    :Returns:
        - {None}
    """
    if os.path.exists(Creds.get_credentials_file()):
        os.remove(Creds.get_credentials_file())
    else:
        raise FileNotFoundError("There's no credential file exists to delete.")


def delete_key() -> None:
    """Function delete_key() deletes the stored cipher key if exists, we use 
    os.path.exists() to check if the file is present or not if present we remove it.

    :Args:
        - {None}

    :Raises:
        - {FileNotFoundError} if the key file doesn't exist.

    :Returns:
        - {None}
    """
    if os.path.exists(Creds.get_key_file()):
        os.remove(Creds.get_key_file())
    else:
        raise FileNotFoundError("There's no key file exists to delete.")

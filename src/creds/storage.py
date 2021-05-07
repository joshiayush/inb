import os

from . import __key_file
from . import __credentials_file

from helpers.print import printRed
from creds.crypto import decrypt_credentials
from errors.error import PropertyNotExistException
from errors.error import UserCacheNotFoundException


def store_credentials(self):
    """Method store_credentials() stores the user secret fields
    as cache in a file 'CredentialsFile.ini' so to use these
    fields later.
    """
    if not hasattr(self, "encrypted_email") or not hasattr(self, "encrypted_password"):
        raise PropertyNotExistException(
            "Object 'self' must have properties 'encrypted_email'|'encrypted_password' with credentials value in it!")

    with open(__credentials_file, 'w') as creds_file:
        creds_file.write("Username={}\nPassword={}\n".format(
            self.encrypted_email, self.encrypted_password))


def get_credentials(self):
    """Method get_credentials() reads the credentials stored as
    cache in file 'CredentialsFile.ini' if exists.
    """
    if os.path.exists(__credentials_file):
        try:
            with open(__credentials_file, 'r') as creds_file:
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


def delete_cache():
    """Method delete_cache() deletes the stored cache (User credentials)
    if exists, we use os.path.exists() to check if the file is present or
    not if present we remove it.
    """
    if os.path.exists(__credentials_file):
        os.remove(__credentials_file)
    else:
        raise FileNotFoundError("There's no credential file exists to delete.")


def delete_key():
    """Method delete_key() deletes the stored cipher key if exists,
    we use os.path.exists() to check if the file is present or not if
    present we remove it.
    """
    if os.path.exists(__key_file):
        os.remove(__key_file)
    else:
        raise FileNotFoundError("There's no key file exists to delete.")

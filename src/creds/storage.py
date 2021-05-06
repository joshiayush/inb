from helpers.print import printRed
from errors.error import PropertyNotExistException
from errors.error import UserCacheNotFoundException


def store_credentials(self):
    """Method store_credentials() stores the user secret fields
    as cache in a file 'CredentialsFile.ini' so to use these
    fields later.
    """
    if not "__credentials_file" in self:
        raise PropertyNotExistException(
            "Object 'self' must have a property '__credentials_file' with credentials file location in it!")

    if not "encrypted_email" in self or not "encrypted_password" in self:
        raise PropertyNotExistException(
            "Object 'self' must have properties 'encrypted_email'|'encrypted_password' with credentials value in it!")

    with open(self.__credentials_file, 'w') as creds_file:
        creds_file.write("Username={}\nPassword={}\n".format(
            self.encrypted_email, self.encrypted_password))


def get_credentials(self):
    """Method get_credentials() reads the credentials stored as
    cache in file 'CredentialsFile.ini' if exists.
    """
    if not "__credentials_file" in self:
        raise PropertyNotExistException(
            "Object 'self' must have a property '__credentials_file' with credentials file location in it!")

    if os.path.exists(self.__credentials_file):
        try:
            with open(self.__credentials_file, 'r') as creds_file:
                lines = creds_file.readlines()

                config = {
                    "Username": "",
                    "Password": ""
                }

                for line in lines:
                    creds = line.rstrip('\n').split('=', 1)
                    if creds[0] in ("Username", "Password"):
                        config[creds[0]] = creds[1]

                self.decrypt_credentials(config)
                return True
        except FileNotFoundError:
            raise UserCacheNotFoundException(
                "You don't have any cache stored!")

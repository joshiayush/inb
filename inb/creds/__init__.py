__name__ = "creds"
__package__ = "creds"

import os
from cryptography.fernet import Fernet


class Creds:
    __key = ""
    __key_file = "/Python/inb/creds/.key.key"
    __credentials_file = "/Python/inb/creds/credentialsFile.ini"

    @staticmethod
    def get_key():
        if not os.path.exists(Creds.__key_file):
            Creds.__key = Fernet.generate_key()

            with open(Creds.__key_file, 'w') as key_file:
                key_file.write(Creds.__key.decode())
        else:
            with open(Creds.__key_file, 'r') as key_file:
                Creds.__key = key_file.readline().encode()

        return Creds.__key

    @staticmethod
    def get_credentials_file():
        return Creds.__credentials_file

    @staticmethod
    def get_key_file():
        return Creds.__key_file

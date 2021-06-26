from __future__ import annotations

from . import Creds
from . import Fernet


class Cipher(Creds):
    def encrypt(self: Cipher, value: str) -> str:
        """Method encrypt() encrypts the user password so to store this field 
        as cache later.

        :Fernet:
            Fernet guarantees that a message encrypted using it cannot be manipulated
            or read without the key. Fernet is an implementation of symmetric (also known 
            as “secret key”) authenticated cryptography.

        :Args:
            - password: {str} value to encrypt.

        :Returns:
            - {str}
        """
        return Fernet(self.get_key()).encrypt(value.encode()).decode()

    def decrypt(self: Cipher, value: str) -> str:
        """Method decrypt() decrypts the encrypted user credentials that 
        are stored in the Credentials file.

        :Fernet:
            Fernet guarantees that a message encrypted using it cannot be manipulated
            or read without the key. Fernet is an implementation of symmetric (also known 
            as “secret key”) authenticated cryptography.

        :Args:
            - password: {str} value to decrypt.

        :Returns:
            - {str}
        """
        return Fernet(self.get_key()).decrypt(value.encode("utf-8")).decode("utf-8")

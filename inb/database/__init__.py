import os

__all__ = ["SQL_DATABASE_PATH"]

SQL_DATABASE_PATH = os.path.dirname(
    os.path.abspath("setup.py")) + "/db/database.db"

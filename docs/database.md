# Database

Use [`SQLite3`][_sqlite3] database to store history records.

**Database path**

- **\*nix**

  `~/inb/database`

- **Windows**

  `%HOMEDRIVE%\\inb\\database`

## Database directories

- **`${{inbDir}}${{pathSep}}database`**

  We use this directory as a top-level directory to store the `registry.db` file that contains information about the actual databases that contains the invitation history of the user.

- **`${{inbDir}}${{pathSep}}database${{pathSep}}history`**

  We use this directory as a top-level directory to store the directories that gets created to store all the databases that gets created on a particular day but at different times.

  - **`r'[0-9]{2}-[0-9]{2}-[0-9]{4}'`**

    We use the above pattern to generate the name for the directory that will store all the databases that gets created on a particular day. Note, this pattern does not have time information in it that's because time information is used with actual database files that will store the invitation history. We generate the database directory name using the following Python statement:

    ```python
    datetime.now().strftime("%d-%m-%Y")
    ```

## Databases

- **`registry.db`**

  This database stores information about the database created on a specific day at a specific time and the absolute path to the database that contains the actual invitation history.

  Defining the database:

  ```SQL
  CREATE TABLE Registry (
    CreatedAt     TEXT
    AbsolutePath  TEXT NOT NULL PRIMARY KEY
  );
  ```

- **`r'[0-9]{2}-[0-9]{2}-[0-9]{4}_[0-9]{2}-[0-9]{2}-[0-9]{2}.[0-9]{4}.db'`**

  We use the above pattern to generate database name based on the time the database was getting created in order to store the invitation history of that time. We generate the database name using the following Python statement:

  ```python
  datetime.now().strftime("%d-%m-%Y_%H-%M-%S.%f")
  ```

  Multiple databases can be created on the same day if the user decides to use **inb** multiple times but these multiple databases will be inside a particular directory of that day.

  Defining the database:

  ```SQL
  CREATE TABLE History (
    Id                  TEXT NOT NULL PRIMARY KEY
    PersonName          TEXT
    Occupation          TEXT
    MutualConnections   TEXT
    ProfileUrl          TEXT
    Success             INTEGER
  );
  ```

<!-- Defintions -->

[_sqlite3]: https://docs.python.org/3/library/sqlite3.html

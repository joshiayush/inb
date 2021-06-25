# Command handlers

## `handle_send_commands()`

1. Connect to _database_.
2. Check if _user's information_ exists or not.
3. If _user's information_ exists invoke `send_invitation()` function with the data we are holding.
4. If _user's information_ does not exist even before that if the database does not exist `raise` _error_.

## `handle_show_command()`

1. Connect to _database_.
2. Check what _flag_ is given and according to it make a `GET` request to the _database_.
3. If no _flag_ is given then just _fetch_ everything that is there in the _database_ and put on the screen.

## `handle_config_command()`

1. Connect to _database_.
2. Check if the given _values_ are valid or not.
3. Encrypt _user's keys_.
4. Dump _user's keys_ with the _key_ that was used to encrypt them.

## `handle_delete_command()`

1. Check if the _identifier_ exists or not.
2. If the _identifier_ exists connect to _database_ and _delete_ the information.

## `handle_developer_command()`

1. Check what _flag_ is given.
2. Connect to _database_ and search for the value and put it on the screen.
3. If no _flag_ is given then just put everything on the screen.

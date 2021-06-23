# Commands

## `lbot`

### Positional arguments

- `send` - use to send invitations on _linkedin_.
- `show` - show the data stored in the _database_.
- `delete` - use to delete the _key_ (key for encrypting credentials) or data from the _database_.
- `config` - use to store _user's credentials_.
- `developer` - show the _author's_ details.

### Optional arguments

- `-h`, `--help` - print a help message.

## `send`

### Positional arguments

- `limit` - number of invitations to send in a go, (default `20`).

### Optional arguments

- `-c`, `--cookies` - use the cookies stored in the database.
- `-ngpu`, `--headless` - start chrome browser in headless mode.
- `-h`, `--help` - print the help message for this command.

## `show`

### Positional arguments

- `cookies` - show the cookies stored.

### Optional arguments

- `-e`, `--email` - show the email stored.
- `-p`, `--password` - show the password stored.
- `-h`, `--help` - print the help message for this command.

## `delete`

### Positional arguments

- `key` - delete the _key_ stored, then it also deletes the _cookies_ stored because there won't be any way of accessing that _encrypted_ information after this action.
- `cookies` - delete the _cookies_ stored.

### Optional

- `-h`, `--help` - print the help message for this command.

## `config`

### Positional arguments

- `value` - value to store in the database.

### Optional arguments

- `-e`, `--email` - store email address.
- `-p`, `--password` - store password.
- `-h`, `--help` - print the help message for this command.

## `developer`

### Positional arguments

- `{None}` - No positional arguments.

### Optional arguments

- `-n`, `--name` - print developer name.
- `-l`, `--linkedin` - print developer linkedin.
- `-g`, `--github` - print developer github.
- `-m`, `--mobile` - print developer mobile number.
- `-e`, `--email` - print developer email address.
- `-h`, `--help` - print a help message.

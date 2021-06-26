# Commands

## `inb`

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
- `-i`, `--incognito` - set browser in _incognito_ mode.
- `-m`, `--start-maximized` - set browser in _full screen_.
- `-ngpu`, `--headless` - set browser in _headless_ mode.
- `-h`, `--help` - print the help message for this command.

## `show`

### Positional arguments

- `cookies` - show the cookies stored.

### Optional arguments

- `-e`, `--email` - show the email stored.
- `-p`, `--password` - show the password stored.
- `-d`, `--decrypt` - show information in decrypted form.
- `-h`, `--help` - print the help message for this command.

## `delete`

### Positional arguments

- `identifier` - what to delete eg. `cookies`.

### Optional

- `-h`, `--help` - print the help message for this command.

## `config`

### Positional arguments

- `EMAIL` - user's email address.
- `PASSWORD` - user's password.

### Optional arguments

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

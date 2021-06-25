# inb

![](https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Logo.svg.original.svg)

This command line tool is very helpful to increase your connections on **LinkedIn**, you are going to achieve **500+** connections very easily. You just need to run it on your terminal, enter your LinkedIn username and password and execute command `linkedin send`.

## Dependencies

These dependencies will be installed automatically if not present in your system if you run `./run.sh` script but if in case it doesn't work then you can follow the methods.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install them.

```
$ pip3 install selenium

$ pip3 install webdriver-manager
```

**Google Chrome Version 91.0.4472.77 (Official Build) (64-bit)** to run chromedriver.

## Available Scripts

In the project directory, you can run:

### `./scripts/run.sh`

Runs the program.

### `sudo ./scripts/delete-garbage.sh`

Deletes all the cache files that gets created after the program run.

### `config.user.email "example@email.com"`

Add email to configurations.

### `config.user.password "example@password"`

Add password to configurations.

**OR**

### `config.user.password` (hit enter)

Add password to configurations by allowing you to enter the password in password prompt. I used `getpass.getpass()` method for this functionality.

Once you are done adding configurations you can run the command.

### `linkedin send`

It will start sending invitation.

## Commands

### `config.user.email "example@email.com" --cached`

This command stores the user email as cache so the user does not have to enter this field every time it has to automate LinkedIn.

### `config.user.password "example@password" --cached`

**OR**

### `config.user.password --cached`

This command stores the user password as cache so the user does not have to enter this field every time it has to automate LinkedIn.

_Note:_ Program only stores these fields as cache if it has both of the fields available.

### `linkedin send suggestions --auto --headless --use-cache`

Starts sending invitations to LinkedIn suggestions `--headless` starts the automation without opening the browser and `--use-cache` uses the cache stored for authentication.

### Happy Hacking

<!-- Definitions -->

[_stable]: https://github.com/JoshiAyush/linkedin-bot/tree/stable

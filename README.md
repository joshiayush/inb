# Getting started with LinkedIn Automater

## Available Scripts

In the project directory, you can run:

### `./run.sh`

Runs the program.

It will install dependencies if they are not present in your system,

it can install `python` interpreter `selenium`, `urllib`, `webdriver-manager`

packages on your system.

### `config.user.email=example@email.com`

Adds email to configurations.

### `config.user.password`

Adds password to configurations by allowing you to enter the password in password prompt

I used `getpass.getpass()` method for this functionality.

Once you are done adding configurations you can run the command.

### `linkedin send`

It will start sending invitation.

## Commands

### `config.user.email=example@email.com --cached`

This command stores the user email as cache so the user does not have

to enter this field every time it has to automate LinkedIn.

### `config.user.password --cached`

This command stores the user password as cache so the user does not have

to enter this field every time it has to automate LinkedIn.

_Note:_ Program only stores these field as cache if it has both of the

fields available.

### `linkedin send suggestions --auto --headless --use-cache`

Starts sending invitations to LinkedIn suggestions `--headless` starts

the automation without opening the browser and `--use-cache` uses the 

cache stored for authentication.

### `Happy Hacking`

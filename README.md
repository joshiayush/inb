# Getting started with LinkedIn Bot

![](https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Logo.svg.original.svg)

This command line tool is very helpful to increase your connections on **LinkedIn**, you are going to achieve **500+** connections very easily. You just need to run it on your terminal, enter your LinkedIn username and password and execute command `linkedin send`.

## Dependencies

These dependencies will be installed automatically if not present in your system if you run `./run.sh` script but if in case it doesn't work then you can follow the methods.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install them.

```
$ pip3 install selenium

$ pip3 install webdriver-manager
```

**Google Chrome Version 89.0.4389.114 (Official Build) (64-bit)** to run chromedriver.

## Available Scripts

In the project directory, you can run:

### `./run.sh`

Runs the program.

It will install dependencies if they are not present in your system,

it can install `python` interpreter `selenium`, `urllib`, `webdriver-manager`,

`cryptography` packages on your system.

### `./run.sh -d pycache`

Deletes all the cache files that gets created after the program run.

### `config.user.email "example@email.com"`

Add email to configurations.

### `config.user.password "example@password"`

Add password to configurations.

**OR**

### `config.user.password` (hit enter)

Add password to configurations by allowing you to enter the password in password prompt

I used `getpass.getpass()` method for this functionality.

Once you are done adding configurations you can run the command.

### `linkedin send`

It will start sending invitation.

# Usage

Note these imports should occur directly from `linkedin` module inside of the `src` directory, no
module in between.

## Module LinkedIn

```python3
from linkedin.LinkedIn import LinkedIn

from errors.error import DomainNameSystemNotResolveException

user_email = "example@gmail.com"
user_password = "xxxx-xxxx-xxxx"

driver_path = "chrome_driver_path"

# enable the headless mode when required or when you don't need it just don't call
# the method headless from LinkedIn class.
if_headless = True

# LinkedIn constructor takes user credentials and chromedriver path as its parameters.
_linkedin = LinkedIn(
            {"user_email": user_email, "user_password": user_password}, driver_path)

# set browser in incognito mode.
_linkedin.set_browser_incognito_mode()
# set ignore certificate errors true.
_linkedin.set_ignore_certificate_error()

if if_headless:
    # set browser in headless mode.
    _linkedin.set_headless()

# chromedriver options are set to ["--incognito", "--ignore-certificate-errors", "headless"]
# if all the above functions are executed, but if you skip the set_headless method then
# chromedriver options are set to ["--incognito", "--ignore-certificate-errors"], you decide
# what best fits for you.

# enables webdriver chrome and takes chromedriver options as its parameter.
# method get_chrome_driver_options() will return the webdriver options.
_linkedin.enable_webdriver_chrome(_linkedin.get_chrome_driver_options())

try:
    # method get_login_page() will send a get request for the given url, it raises error
    # DomainNameSystemNotResolveException if domain name system is not resolved by your
    # browser.
    _linkedin.get_login_page("https://www.linkedin.com/login")
except DomainNameSystemNotResolveException as error:
    print(f"""{error}""")

# login to LinkedIn, method login() throws the user credentials to there specific fields
# on the login form.
_linkedin.login()
```

## Module LinkedInConnectionsAuto

```python3
from linkedin.LinkedIn import LinkedIn

from errors.error import EmptyResponseException
from errors.error import DomainNameSystemNotResolveException

user_email = "example@gmail.com"
user_password = "xxxx-xxxx-xxxx"

driver_path = "chrome_driver_path"

# enable the headless mode when required or when you don't need it just don't call
# the method headless from LinkedIn class.
if_headless = True

# LinkedIn constructor takes user credentials and chromedriver path as its parameters.
_linkedin = LinkedIn(
            {"user_email": user_email, "user_password": user_password}, driver_path)

# set browser in incognito mode.
_linkedin.set_browser_incognito_mode()
# set ignore certificate errors true.
_linkedin.set_ignore_certificate_error()

if if_headless:
    # set browser in headless mode.
    _linkedin.set_headless()

# chromedriver options are set to ["--incognito", "--ignore-certificate-errors", "headless"]
# if all the above functions are executed, but if you skip the set_headless method then
# chromedriver options are set to ["--incognito", "--ignore-certificate-errors"], you decide
# what best fits for you.

# enables webdriver chrome and takes chromedriver options as its parameter.
# method get_chrome_driver_options() will return the webdriver options.
_linkedin.enable_webdriver_chrome(_linkedin.get_chrome_driver_options())

try:
    # method get_login_page() will send a GET request for the given url, it raises error
    # DomainNameSystemNotResolveException if domain name system is not resolved by your
    # browser.
    _linkedin.get_login_page("https://www.linkedin.com/login")
except DomainNameSystemNotResolveException as error:
    print(f"""{error}""")

# login to LinkedIn, method login() throws the user credentials to there specific fields
# on the login form.
_linkedin.login()

# LinkedInConnectionsAuto constructor takes LinkedIn object and daily connection limit as its
# parameters, it throws two errors one `PropertyNotExistException` if object _linkedin doesn't
# have property 'driver' in it because this class also needs the access of the driver and the
# another exception is `ConnectionLimitExceededException` if you gave a daily connection limit
# that is greater than 80, we recommend 40 so that your account won't be marked as a bot by
# linekdin, so make sure that you catch those errors too you can import them from the error file
# as we imported the DomainNameSystemNotResolveException Exception from it.
_linkedin_connection = LinkedInConnectionsAuto(_linkedin, limit=20)

try:
    # method get_my_network() sends a GET request for the url given, raise EmptyResponseException
    # if your internet connection is slow.
    _linkedin_connection.get_my_network("https://www.linkedin.com/mynetwork/")
except EmptyResponseException:
    print(f"""{error}""")

_linkedin_connection.run()
```

## Commands

### `config.user.email "example@email.com" --cached`

This command stores the user email as cache so the user does not have

to enter this field every time it has to automate LinkedIn.

### `config.user.password "example@password" --cached`

**OR**

### `config.user.password --cached`

This command stores the user password as cache so the user does not have

to enter this field every time it has to automate LinkedIn.

_Note:_ Program only stores these fields as cache if it has both of the

fields available.

### `linkedin send suggestions --auto --headless --use-cache`

Starts sending invitations to LinkedIn suggestions `--headless` starts

the automation without opening the browser and `--use-cache` uses the

cache stored for authentication.

## Contributing

**Your pull requests and stars are always welcome.**

- Clone the repository
- Install dependencies
- Add your features
- Fix bugs

```
git clone https://github.com/JoshiAyush/linkedin-bot.git linkedin-bot/

cd linkedin-bot/
```

### Happy Hacking

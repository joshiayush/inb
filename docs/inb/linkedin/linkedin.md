# LinkedIn Service

This service provides a service to login into your LinkedIn account (if already). You have to provide your LinkedIn _email_ and
_password_ while instantiating an object of `LinkedIn` class. This is the service that takes the chromedriver path and options for
[Chromedriver][_chromedriver_service] service.

This document has following sections:

- [LinkedIn Overview](#linkedin-overview)
- [System Call Interface](#system-call-interface)
- [System Internal Call Interface](#system-internal-call-interface)

## LinkedIn Overview

**LinkedIn Class:**

```python
class LinkedIn(Driver):
```

> Class `LinkedIn` has a base class `Driver` (i.e., [Chromedriver Service][_chromedriver_service]) to instantiate a chromedriver
> instance to communicate with the browser (i.e., Google Chrome).

**LinkedIn Constructor:**

> The constructor method takes in four arguments, obligatory arguments are `user_email`, `user_password` and `driver_path` and the
> optional one is `opt_chromedriver_options`.

```python
def __init__(
    self: LinkedIn,
    user_email: str = '',
    user_password: str = '',
    driver_path: str = '',
    opt_chromedriver_options: list = []
) -> None:
```

> Arguments `user_email` and `user_password` are obligatory otherwise you will end up having an exception 
> `CredentialsNotGivenException` that the constructor method will raise.
> <br><br>
> This constructor method instantiate a [chromedriver][_chromedriver_service] object by calling the `super` method to invoke the
> base class constructor. If the chromedriver path is not given then you will again get an exception
> `WebDriverPathNotGivenException` raised by the [Driver][_chromedriver_service] class constructor.
> <br><br>
> The argument `opt_chromedriver_options` is optional you may give the options for chromedriver to enable while using **inb**, you
> can find the options in [Chromedriver Service][_chromedriver_service] document.
> <br><br>
> If the arguments given to constructor method are valid then this constructor method creates two instance variables `__user_email`
> and `__user_password` holding the user email and user password respectively.

**LinkedIn Destructor:**

> The destructor method calls the `disable_webdriver_chrome()` on itself which it was given during the initialization from the base
> class `Driver`.

```python
def __del__(self: LinkedIn) -> None:
```

> The `disable_webdriver_chrome()` method sets the `Driver` class variable `__SESSION_ALREADY_EXISTS` to `False` which was set to
> `True` when you instantiate a `chromedriver` object and then the `quit` method is invoked on the `chromedriver` instance.

## System Call Interface

## System Internal Call Interface

<!-- Definitions -->

[_chromedriver_service]: https://github.com/joshiayush/inb/blob/master/docs/inb/linkedin/init.md

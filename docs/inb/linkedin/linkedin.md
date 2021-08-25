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

- **Method get_login_page()**

  > This method takes you to the LinkedIn login page.

  ```python
  def get_login_page(
      self: LinkedIn,
      _url: str = "https://www.linkedin.com/login"
  ) -> None:
  ```

  > This method will raise exception `DomainNameSystemNotResolveException` if weak network is found, means if `TimeoutException`
  > is raised by the `driver.get()` method.
  > <br><br>
  > This method takes in an argument `_url` which is set to `"https://www.linkedin.com/login"` by default but you can also
  > provide the value for this argument explicitly.

- **Method login()**

  > This method fills the login form that is in the LinkedIn login page.

  ```python
  def login(self: LinkedIn) -> None:
  ```

  > This method must be called after the successful execution of `get_login_page()` method otherwise you will get exceptions.
  > <br><br>
  > This method calls a private method called `__fill_credentials()` to fill the form.

## System Internal Call Interface

- **Method __get_email_box()**

    > This private method when called returns the email field element from the form that is in the LinkedIn login page.

    ```python
    def __get_email_box(self: LinkedIn) -> webdriver.Chrome:
    ```

    > This private method is internally used by the `__enter_email()` method to send user email to the form.

- **Method __enter_email()**

    > This private method interacts with the email field that is in the LinkedIn login page.

    ```python
    def __enter_email(
        self: LinkedIn, 
        _return: bool = False
    ) -> None:
    ```

    > This private method is internally used by the private method `__fill_credentials()`.
    > <br><br>
    > This private method internally uses the `__get_email_box()` private method to first get the element where it needs to send
    > the user email to.
    > <br><br>
    > You may notice an optional argument `_return` that is used internally to decide whether to send return (i.e., carriage return)
    > key after sending the user email. This carriage return if sent emits an submit event in the form.

- **Method __get_password_box()**

    > This private method when called returns the password field element from the form that is in the LinkedIn login page.

    ```python
    def __get_password_box(self: LinkedIn) -> webdriver.Chrome:
    ```

    > This private method is internally used by the `__enter_password()` method to send user password to the form.

- **Method __enter_password()**

    > This private method interacts with the password field that is in the LinkedIn login page.

    ```python
    def __enter_password(
        self: LinkedIn, 
        _return: bool = True
    ) -> None:
    ```

    > This private method is internally used by the private method `__fill_credentials()`.
    > <br><br>
    > This private method internally uses the `__get_password_box()` private method to first get the element where it needs to send
    > the user password to.
    > <br><br>
    > You may notice an optional argument `_return` that is used internally to decide whether to send return (i.e., carriage return)
    > key after sending the user email. This carriage return if sent emits an submit event in the form. This time this argument's
    > value is set to `True` that is because after sending the user password we want to submit the form.

- **Method __fill_credentials()**

    > This private method interacts with the form that is in the LinkedIn login page.

    ```python
    def __fill_credentials(self: LinkedIn) -> None:
    ```

    > As we have already discussed that this method is internally used by the `login()` method to log into LinkedIn.
    > <br>
    > This method internally uses private methods `__enter_email()` and `__enter_password()` to send the user email and password to
    > the login form.

<!-- Definitions -->

[_chromedriver_service]: https://github.com/joshiayush/inb/blob/master/docs/inb/linkedin/init.md

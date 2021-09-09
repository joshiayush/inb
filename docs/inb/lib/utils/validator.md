# Validator Service

This service provides a mechanism to validate `urls`, `emails` and `filesystems`. This service is basically divided into two
categories:

- [Validator](#validator)
- [InbValidator](#inbvalidator)

## Validator

This service provides a general validator that validates any kind or url `hyper text` or `file transfer`, any kind of emails and
filesystems.

We have the following sections on this topic:

- [Validator Overview](#validator-overview)
- [Validator System Call Interface](#validator-system-call-interface)

### Validator Overview

**Validator Class:**

> This class provides the general validator instance for use.
>
> ```python
> class Validator(object):
> ```
>
> This class inherits from the `object` class which is the default base class for every class in python, so there is nothing much
> in that.
>
> This `Validator` class provides a static data member called `ERROR_INVALID_NAME` which is a Windows-specific error code indicating
> and invalid pathname. Sadly, python fails to provide this magic number so we explicitly set it to value `123`.

**Validator Constructor:**

> The constructor method initializes the field attribute that we need to validate.
>
> ```python
> def __init__(self: Validator, field: str) -> None:
> ```
>
> The constructor method initializes the field attribute after checking if the argument `field` is an instance of `str` or not, if
> the `field` argument is not an instance of `str`, the constructor method raises `ValueError` exception.

### Validator System Call Interface

- **Method is_url():**

  > This method is publicly available for every instance of `Validator` class.
  >
  > ```python
  > def is_url(self: Validator) -> bool:
  > ```
  >
  > This method checks if the field is a valid url or not, it first compiles the following regex expression:
  >
  > ```python
  > re.compile(
  >     r"^(?:http|ftp)s?://"
  >     r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
  >     r"localhost|"
  >     r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
  >     r"(?::\d+)?"
  >     r"(?:/?|[/?]\S+)$", re.IGNORECASE)
  > ```
  >
  > Then we explicitly set the `IGNORECASE` constant to tell the regex compiler that you must ignore the upper and lower letter
  > cases.
  >
  > This method then internally calls the `match` method on `re` module with the compiled regex expression and the field to check if
  > it is a match, in case it finds a match it returns `True`, `False` otherwise.

- **Method is_email():**

  > This method is publicly available for every instance of `Validator` class.
  >
  > ```python
  > def is_email(self: Validator) -> bool:
  > ```
  >
  > This method checks if the field is a valid email address or not, it first compiles the following regex expressions:
  >
  > ```python
  > re.compile(
  >           r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", re.IGNORECASE)
  > ```
  >
  > Then we explicitly set the `IGNORECASE` constant to tell the regex compiler that you must ignore the upper and lower letter
  > cases.
  >
  > This method then internally calls the `match` method on `re` module with the compiled regex expression and the field to check if
  > it is a match, in case it finds a match it returns `True`, `False` otherwise.

- **Method is_path():**

  > This method is publicly available for every instance of `Validator` class.
  >
  > ```python
  > def is_path(self: Validator) -> bool:
  > ```
  >
  > This method checks if the given field is a valid file system path or not. This method is used for validating the paths for
  > chromedriver executable. This method is compatible for both `posix` and `windows` operating systems.

- **Method is_executable():**

  > This method is publicly available for every instance of `Validator` class.
  >
  > ```python
  > def is_executable(self: Validator) -> bool:
  > ```
  >
  > This method checks if the given field is a valid path and the path has its executable bit set to `True`. This method internally
  > takes help of the above method `is_path()` to validate the file system path and calls `os.access()` method to check if the path
  > has its executable bit set to `True.`
  >
  > This method will return `True` if all the above checks passed, `False` otherwise.

## InbValidator

This service provides a validator that validates the fields that are specifically made for `LinkedIn`. For example, if you give this
validator a url to validate it will return `True` if the url is an address to LinkedIn server but it will return `False` if the url
is not an address to LinkedIn server.

We have the following sections on this topic:

- [InbValidator Overview](#inbvalidator-overview)
- [InbValidator System Call Interface](#inbvalidator-system-call-interface)

### InbValidator Overview

**InbValidator Class:**

> This class provides the inb validator instance for use.
>
> ```python
> class InbValidator(object):
> ```
>
> This class inherits from the `object` class which is the default base class for every class in python, so there is nothing much
> in that.

**InbValidator Constructor:**

> The constructor method initializes the field attribute that we need to validate.
>
> ```python
> def __init__(self: InbValidator, field: str) -> None:
> ```
>
> The constructor method initializes the field attribute after checking if the argument `field` is an instance of `str` or not, if
> the `field` argument is not an instance of `str`, the constructor method raises `ValueError` exception.
>
> This constructor method also initializes an instance of `Validator` class to use for validating emails and urls. The attribute it
> initializes from the `Validator` class is a private attribute called `__validator`.

### InbValidator System Call Interface

- **Method is_url():**

  > This method is publicly available for every instance of `InbValidator` class.
  >
  > ```python
  > def is_url(self: InbValidator) -> bool:
  > ```
  >
  > This method checks if the given field is specifically a LinkedIn url or not. This method internally calls the method `is_url()`
  > of `Validator` class once it is confirmed that this url connects us with the LinkedIn server.

- **Method is_email():**

  > This method is publicly available for every instance of `InbValidator` class.
  >
  > ```python
  > def is_email(self: InbValidator) -> bool:
  > ```
  >
  > This method checks if the given field is a valid email address or not. This method internally calls the `Validator`'s
  > `is_email()` method to check if the field given is a valid email address or not.

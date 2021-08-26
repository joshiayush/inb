# LinkedInConnect Service

This service provides a way to send invitations to people that comes under the suggestion box of your _mynetwork_ page.

This document has the following sections:

- [Overview](#overview)
- [System Call Interface](#system-call-interface)
- [System Internal Call Interface](#system-internal-call-interface)

## Overview

**LinkedInConnect Class:**

```python
class LinkedInConnect(object):
```

> Class `LinkedInConnect` has a base class `object` which is the default base class of every class in python so there is nothing
> much in that.

**LinkedInConnect Constructor:**

```python
def __init__(
    self: LinkedInConnect,
    driver: webdriver.Chrome,
    limit: int = 40
) -> None:
```

> The constructor method intializes a `LinkedInConnect` instance this instance will have some methods on it to commence targetting
> people from the suggestion box in your _mynetwork_ page.
> <br><br>
> This method takes in two arguments, one is obligatory and the other one is optional.
> <br><br>
> The obligatory one is the `chromedriver` instance that you need to give while instantiating an object of `LinkedInConnect` class.
> If the driver given is not an instance of `webdriver.Chrome` then the constructor method will raise an `Exception` that 'the
> object given is not a `webdriver.Chrome` instance'.
> <br><br>
> The `limit` is optional, it is used to tell how many invitations it should send. **LinkedIn** does not allow more than 80 - 100
> invitations per week so you may not exceed the limit by 80 (we recommend 40).

**LinkedInConnect Destructor:**

```python
def __del__(self: LinkedInConnect) -> None:
```

> The destructor method sets the internal variable of `LinkedInConnect` class `(__INVITATION_SENT)` to `0` and it also calls the
> `quit` method on the `webdriver` instance it was given during initialization.

## System Call Interface

- **Method get_my_network()**

  ```python
  def get_my_network(
      self: LinkedInConnect,
      url: Union[str, None] = None
  ) -> None:
  ```

  > This method takes you to the _mynetwork_ page in your **LinkedIn** account.
  > <br><br>
  > This method takes in an argument `url` (i.e., the url to your _mynetwork_ page). Note that currently I haven't coded any kind of
  > validator to check if the url is valid or not, in case you provide an invalid url explicilty it will be taken in and you might
  > see some kind of unexpected behaviour. If the url is not given (means it is `None`) then the value of url is set to the value of
  > an internal variable called `MY_NETWORK_PAGE`, this is an static variable of `LinkedInConnect` class.
  > <br><br>
  > Note that this method will raise an exception `EmptyResponseException` in case weak network is found (means `TimeoutException`
  > is raised by the driver instance).

- **Method run()**

  ```python
  def run(self: LinkedInConnect) -> None:
  ```

## System Internal Call Interface

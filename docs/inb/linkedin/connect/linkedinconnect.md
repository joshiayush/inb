# LinkedInConnect Service

This service provides a way to send invitations to people that comes under the suggestion box of your _mynetwork_ page.

This document has the following sections:

- [Overview](#overview)
- [System Call Interface](#system-call-interface)
- [System Internal Call Interface](#system-internal-call-interface)

## Overview

**LinkedInConnect Class:**

> ```python
> class LinkedInConnect(object):
> ```
>
> Class `LinkedInConnect` has a base class `object` which is the default base class of every class in python so there is nothing
> much in that.

**LinkedInConnect Constructor:**

> ```python
> def __init__(
>     self: LinkedInConnect,
>     driver: webdriver.Chrome,
>     limit: int = 40
> ) -> None:
> ```
>
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

> ```python
> def __del__(self: LinkedInConnect) -> None:
> ```
>
> The destructor method sets the internal variable of `LinkedInConnect` class `(__INVITATION_SENT)` to `0` and it also calls the
> `quit` method on the `webdriver` instance it was given during initialization.

## System Call Interface

- **Method get_my_network()**

  > ```python
  > def get_my_network(
  >     self: LinkedInConnect,
  >     url: Union[str, None] = None
  > ) -> None:
  > ```
  >
  > This method takes you to the _mynetwork_ page in your **LinkedIn** account.
  > <br><br>
  > This method takes in an argument `url` (i.e., the url to your _mynetwork_ page). If the url is not given (means it is `None`)
  > then the value of url is set to the value of an internal variable called `MY_NETWORK_PAGE`, this is an static variable of
  > `LinkedInConnect` class.
  > <br><br>
  > Note that this method will raise an exception `EmptyResponseException` in case weak network is found (means `TimeoutException`
  > is raised by the driver instance).

- **Method run()**

  > ```python
  > def run(self: LinkedInConnect) -> None:
  > ```
  >
  > This method must be called after the successful execution of the above `get_my_network()` method, otherwise exceptions may
  > occur.
  > <br><br>
  > This method first performs cleanup on the page that has the person elements in it so that no other element overlap the person
  > element that way it will target every person element that is on the page. It calls an internal method called
  > `__execute_cleaners()` to perform cleanup on the page.
  > <br><br>
  > After performing cleanup it finally calls the internal method `__send_invitation()` that does the actual inviting job.

## System Internal Call Interface

- **Method \_\_execute_cleaners()**

  > ```python
  > def __execute_cleaners(self: LinkedInConnect) -> None:
  > ```
  >
  > This private method internally calls the `Cleaner` service to clean up certain elements from the page.
  > <br><br>
  > This time we remove the _message overlay_ that lies on the _mynetwork_ page. This _message overlay_ loads up dynamically so the
  > `Cleaner` service by default waits for `60` seconds for the arrival of this _message overlay_, if you have a weak network this
  > _message overlay_ might not arrive by that time and you will see some failures while sending invitations because of the
  > `ElementNotInteractableException`.

- **Method \_\_send_invitation()**

  > ```python
  > def __send_invitation(self: LinkedInConnect) -> None:
  > ```
  >
  > This private method internally calls the `get_suggestion_box_element()` method of the `Person` service to get a person element
  > from the page.
  > <br><br>
  > The element returned by the `get_suggestion_box_element()` method of the `Person` service is a `dict` (dictionary) object that
  > has keys `name`, `occupation` and `connect_button` attached to it. Later on this dictionary we access the `connect_button`
  > which is apparently a `webdriver.Chrome` object, therefore, we perform click operation on it by using `ActionChains` which
  > is a service that `selenium` provides.
  > <br><br>
  > We keep performing the above operations until we reach the limit. This method also logs the invitation status on the console
  > using the `Invitation` service.

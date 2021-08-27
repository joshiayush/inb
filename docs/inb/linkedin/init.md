# Chromedriver Service

This serivce provides a webdriver instance for our application to use. We can also provide _Chromedriver_ `options` while
instantiating a _chromedriver_ object.

This document has the following sections:

- [Driver Overview](#driver-overview)
- [Driver Options](#driver-options)
- [System Call Interface](#system-call-interface)

## Driver Overview

**Driver Class:**

```python
class Driver(object):
```

> Class `Driver` has a base class `object` which is the default base class of all the classes in python, so there is nothing much in
> that.

**Driver Constructor:**

> The constructor method takes in some arguments, one is compulsory and the other one is optional.

```python
def __init__(
    self: Driver,
    driver_path: str,
    options: list = []
) -> None:
```

> Argument `driver_path` is neccessary to locate the chromedriver executable in your system, you must give the absolute path to the
> `chromedriver` executable in your system, if the `driver_path` is not given, you will get an `WebDriverPathNotGivenException`.
> <br><br>
> Argument `options` is optional, it is a list of chromedriver options that you may want to enable while automating the browser. <br>

**Driver Destructor:**

> The destructor method turns the `Driver` class variable `__SESSION_ALREADY_EXISTS` to `False` which was set to `True` when you instantiate a `chromedriver` object.

```python
def __del__(self: Driver) -> None:
```

> It also calls the `quit` method (not `close` method) on the `chromedriver` object to delete the `chromedriver` instance.

## Driver Options

| Option                                                           | Use                                                             |
| ---------------------------------------------------------------- | --------------------------------------------------------------- |
| `HEADLESS: str = "--headless"`                                   | To set the chromedriver in _headless_ mode use                  |
| `INCOGNITO: str = "--incognito"`                                 | To set the chromedriver in _incognito_ mode use                 |
| `NO_SANDBOX: str = "--no-sandbox"`                               | To set the chromedriver in _no-snadbox_ mode use                |
| `DISABLE_GPU: str = "--disable-gpu"`                             | To set the chromedriver in _disable-gpu_ mode use               |
| `START_MAXIMIZED: str = "--start-maximized"`                     | To set the chromedriver in _start-maximized_ mode use           |
| `DISABLE_INFOBARS: str = "--disable-infobars"`                   | To set the chromedriver in _disable-infobars_ mode use          |
| `ENABLE_AUTOMATION: str = "--enable-automation"`                 | To set the chromedriver in _enable-automatio_ mode use          |
| `DISABLE_EXTENSIONS: str = "--disable-extensions"`               | To set the chromedriver in _disable-extensions_ mode use        |
| `DISABLE_NOTIFICATIONS: str = "--disable-notifications"`         | To set thr chromedriver in _disable-notifications_ mode use     |
| `DISABLE_SETUID_SANDBOX: str = "--disable-setuid-sandbox"`       | To set the chromedriver in _disable-setuid-sandbox_ mode use    |
| `IGNORE_CERTIFICATE_ERRORS: str = "--ignore-certificate-errors"` | To set the chromedriver in _ignore-certificate-errors_ mode use |

## System Call Interface

**Method enable_webdriver_chrome()**

> This method enables the `chromedriver` instance in the `Driver` instance.

```python
def enable_webdriver_chrome(self: Driver) -> None:
```

> This is the actual method that adds a `chromedriver` instance to the `Driver` instance, without calling this method the `Driver` instance will not have a `chromedriver` object.

**Method disable_webdriver_chrome()**

> This method disables the `chromedriver` instance in the `Driver` instance by calling the `quit` (not `close`) method on it.

```python
def disable_webdriver_chrome(self: Driver) -> None:
```

> This method also sets the class variable `__SESSION_ALREADY_EXISTS` to `False`, in simple words this method is identical to the _destructor_ method.

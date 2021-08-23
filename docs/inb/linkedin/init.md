# Chromedriver Service

This serivce provides a webdriver instance for our application to use. We can also provide _Chromedriver_ `options` while
instantiating a _chromedriver_ object.

This document has the following sections:

- [Driver Overview](#driver-overview)
- [Driver Options](#driver-options)
- [System Call Interface](#system-call-interface)

## Driver Overview

**Driver Class:**

> Class `Driver` has a base class `object` which is the default base class of all the classes in python, so there is nothing much in
> that. <br><br>
> `class Driver(object):`

**Driver Constructor:**

> The constructor method takes in some arguments, one is compulsory and the other one is optional. <br><br>
> `def __init__(self: Driver, driver_path: str, options: list = []) -> None:` <br><br>
> Argument `driver_path` is neccessary to locate the chromedriver executable in your system, you must give the absolute path to the `chromedriver` executable in your system. <br>
> Argument `options` is optional, it is a list of chromedriver options that you may want to enable while automating the browser. <br>

**Driver Destructor:**

> The destructor method turns the `Driver` class variable `__SESSION_ALREADY_EXISTS` to `False` which was set to `True` when you instantiate a `chromedriver` object. <br><br>
> `def __del__(self: Driver) -> None:` <br><br>
> It also calls the `quit` method (not `close` method) on the `chromedriver` object to delete the `chromedriver` instance. 

## Driver Options

> To set the chromedriver in _headless_ mode use: <br>
> `HEADLESS: str = "--headless"` <br><br>
> To set the chromedriver in _incognito_ mode use: <br>
> `INCOGNITO: str = "--incognito"` <br><br>
> To set the chromedriver in _no-snadbox_ mode use: <br>
> `NO_SANDBOX: str = "--no-sandbox"` <br><br>
> To set the chromedriver in _disable-gpu_ mode use: <br>
> `DISABLE_GPU: str = "--disable-gpu"` <br><br>
> To set the chromedriver in _start-maximized_ mode use: <br>
> `START_MAXIMIZED: str = "--start-maximized"` <br><br>
> To set the chromedriver in _disable-infobars_ mode use: <br>
> `DISABLE_INFOBARS: str = "--disable-infobars"` <br><br>
> To set the chromedriver in _enable-automatio_ mode use: <br>
> `ENABLE_AUTOMATION: str = "--enable-automation"` <br><br>
> To set the chromedriver in _disable-extensions_ mode use: <br>
> `DISABLE_EXTENSIONS: str = "--disable-extensions"` <br><br>
> To set thr chromedriver in _disable-notifications_ mode use: <br>
> `DISABLE_NOTIFICATIONS: str = "--disable-notifications"` <br><br>
> To set the chromedriver in _disable-setuid-sandbox_ mode use: <br>
> `DISABLE_SETUID_SANDBOX: str = "--disable-setuid-sandbox"` <br><br>
> To set the chromedriver in _ignore-certificate-errors_ mode use: <br>
> `IGNORE_CERTIFICATE_ERRORS: str = "--ignore-certificate-errors"` <br><br>

## System Call Interface

**Method enable_webdriver_chrome()**

> This method enables the `chromedriver` instance in the `Driver` instance. <br><br>
> `def enable_webdriver_chrome(self: Driver) -> None:` <br><br>
> This is the actual method that adds a `chromedriver` instance to the `Driver` instance, without calling this method the `Driver` instance will not have a `chromedriver` object. <br>

**Method disable_webdriver_chrome()**

> This method disables the `chromedriver` instance in the `Driver` instance by calling the `quit` (not `close`) method on it. <br><br>
> `def disable_webdriver_chrome(self: Driver) -> None:` <br><br>
> This method also sets the class variable `__SESSION_ALREADY_EXISTS` to `False`, in simple words this method is identical to the _destructor_ method.
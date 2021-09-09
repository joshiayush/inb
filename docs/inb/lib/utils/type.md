# Type Service

This service provides a way to find the class name of an instance.

This document contains the following section:

- [System Call Interface](#system-call-interface)

## System Call Interface

- **Method \_type():**

  > This method returns the class name of the instance it was given:
  >
  > ```python
  > def _type(t: Any) -> str:
  > ```
  >
  > This method returns the class name of an instance by using the `__name__` attribute of it, in case the `__name__` attribute is
  > not present, means `AttributeError` exception occured, it returns `None`.
  > 
  > This method is used in exceptions when the function receives the wrong type, using this function we can generate a error message
  > informing the programmer what was the function actually expecting and what was it that actually given.
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

- **Method is_int():**

  > This method identifies if the object given is an `int`.
  >
  > ```python
  > is_int: function = lambda field: isinstance(field, int)
  > ```
  >
  > It is a one-liner function that uses lambda for the operation.

- **Method is_str():**

  > This method identifies if the object given is an `str`.
  >
  > ```python
  > is_str: function = lambda field: isinstance(field, str)
  > ```
  >
  > It is a one-liner function that uses lambda for the operation.

- **Method is_list():**

  > This method identifies if the object given is a `list`.
  >
  > ```python
  > is_list: function = lambda field: isinstance(field, list)
  > ```
  >
  > It is a one-liner function that uses lambda for the operation.

- **Method is_none():**

  > This method identifies if the object given is `None`.
  >
  > ```python
  > is_none: function = lambda field: isinstance(field, None)
  > ```
  >
  > It is a one-liner function that uses lambda for the operation.

- **Method is_empty():**

  > Checks if the string given is empty.
  >
  > ```python
  > def is_empty(field: str) -> bool:
  > ```
  >
  > Checks if the string given is empty or not. If given a invalid type instead of `str` it returns `False`.

- **Method is_present():**

  > Checks if the object is present in the field.
  >
  > ```python
  > def is_present(obj: Any, field: Any) -> bool:
  > ```
  >
  > Checks if the object given is present in the field. Supports multiple types that support `in` operator.

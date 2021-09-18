# Exception Service

This service contains the exceptions objects that we use to inform user about certain errors.

This document contains the following sections:

- [WebDriverPathNotGivenException](#webdriverpathnotgivenexception)
- [WebDriverNotExecutableException](#webdrivernotexecutableexception)
- [CredentialsNotGivenException](#credentialsnotgivenexception)
- [ConnectionLimitExceededException](#connectionlimitexceededexception)
- [DatabaseDoesNotExistException](#databasedoesnotexistexception)
- [EmtpyDatabaseException](#emtpydatabaseexception)
- [ValidationError](#validationerror)
- [InternetNotConnectedException](#internetnotconnectedexception)

## WebDriverPathNotGivenException

> Thrown when chrome driver's path is not given or is not located in your system's executable path.
>
> ```python
> def __init__(self: WebDriverPathNotGivenException, *args: Tuple[Any]) -> None:
> ```
>
> The constructor method takes in a `tuple` with the first element as the exception message of type str.

## WebDriverNotExecutableException

> Thrown when the chrome driver is not executable.
>
> ```python
> def __init__(self: WebDriverNotExecutableException, *args: Tuple[Any]) -> None:
> ```
>
> The constructor method takes in a `tuple` with the first element as the exception message of type str.

## CredentialsNotGivenException

> Thrown when user's credentials are not given to the LinkedIn class.
>
> ```python
> def __init__(self: CredentialsNotGivenException, *args: Tuple[Any]) -> None:
> ```
>
> The constructor method takes in a `tuple` with the first element as the exception message of type str and the second element as
> the user's credentials dictionary (Optional).

## ConnectionLimitExceededException

> Thrown when the connections limit given by the user exceeds by the default LinkedIn connection limit.
>
> ```python
> def __init__(self: ConnectionLimitExceededException, *args: Tuple[Any]) -> None:
> ```
>
> The constructor method takes in a `tuple` with the first element as the exception message of type str.

## DatabaseDoesNotExistException

> Thrown when the database path does not exists.
>
> ```python
> def __init__(self: DatabaseDoesNotExistException, *args: Tuple[Any]) -> None:
> ```
>
> The constructor method takes in a `tuple` with the first element as the exception message of type str and the second element as
> the database path of type str.

## EmtpyDatabaseException

> Thrown when email and password are requested and database is empty.
>
> ```python
> def __init__(self: EmtpyDatabaseException, *args: Tuple[Any]) -> None:
> ```
>
> The constructor method takes in a `tuple` with the first element as the exception message of type str and the second element as
> the database path of type str.

## ValidationError

> Thrown when there is a validation error.
>
> ```python
> def __init__(self: ValidationError, *args: Tuple[Any]) -> None:
> ```
>
> The constructor method takes in a `tuple` with the first element as the exception message of type str.

## InternetNotConnectedException

> Thrown when internet is not connected.
>
> ```python
> def __init__(self: InternetNotConnectedException, *args: Tuple[Any]) -> None:
> ```
>
> The constructor method takes in a `tuple` with the first element as the exception message of type str.

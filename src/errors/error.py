"""from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!"""
from __future__ import annotations


class EmptyResponseException(Exception):
    """Thrown when recieved an empty response."""

    def __init__(self: EmptyResponseException, message: str = '') -> None:
        super(EmptyResponseException, self).__init__(message)


class FailedLoadingResourceException(Exception):
    """Thrown when failed loading the resources properly."""

    def __init__(self: FailedLoadingResourceException, message: str = '') -> None:
        super(FailedLoadingResourceException, self).__init__(message)


class LinkedInBlockException(Exception):
    """Thrown when LinkedIn blocks."""

    def __init__(self: LinkedInBlockException, message: str = '') -> None:
        super(LinkedInBlockException, self).__init__(message)


class DomainNameSystemNotResolveException(Exception):
    """Thrown when DNS could not be resolved."""

    def __init__(self: DomainNameSystemNotResolveException, message: str = '') -> None:
        super(DomainNameSystemNotResolveException, self).__init__(message)


class PropertyNotExistException(Exception):
    """Thrown when a binding does not have a property name."""

    def __init__(self: PropertyNotExistException, message: str = '') -> None:
        super(PropertyNotExistException, self).__init__(message)


class UserCacheNotFoundException(Exception):
    """Thrown when user doesn't have any cache stored."""

    def __init__(self: UserCacheNotFoundException, message: str = '') -> None:
        super(UserCacheNotFoundException, self).__init__(message)


class CredentialsNotFoundException(Exception):
    """Thrown when user's credentials are not found."""

    def __init__(self: CredentialsNotFoundException, message: str = '') -> None:
        super(CredentialsNotFoundException, self).__init__(message)


class CommandNotFoundError(Exception):
    """Thrown when user enters a command that is not recognized."""

    def __init__(self: CommandNotFoundError, message: str = '') -> None:
        super(CommandNotFoundError, self).__init__(message)


class CommandFlagNotFoundException(Exception):
    """Thrown when user enters a command flag that is not recognized."""

    def __init__(self: CommandFlagNotFoundException, message: str = '') -> None:
        super(CommandFlagNotFoundException, self).__init__(message)


class ZeroFlagException(Exception):
    """Thrown when a command is referenced without a flag."""

    def __init__(self: ZeroFlagException, message: str = '') -> None:
        super(ZeroFlagException, self).__init__(message)


class NoSuchConfigurationFoundException(Exception):
    """Thrown when user enters a configuration command that is not recognized."""

    def __init__(self: NoSuchConfigurationFoundException, message: str = '') -> None:
        super(NoSuchConfigurationFoundException, self).__init__(message)

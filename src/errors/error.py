class EmptyResponseException(Exception):
    """Thrown when recieved an empty response."""

    def __init__(self, message=""):
        super(EmptyResponseException, self).__init__(message)


class FailedLoadingResourceException(Exception):
    """Thrown when failed loading the resources properly."""

    def __init__(self, message=""):
        super(FailedLoadingResourceException, self).__init__(message)


class LinkedInBlockException(Exception):
    """Thrown when LinkedIn blocks."""

    def __init__(self, message=""):
        super(LinkedInBlockException, self).__init__(message)


class DomainNameSystemNotResolveException(Exception):
    """Thrown when DNS could not be resolved."""

    def __init__(self, message=""):
        super(DomainNameSystemNotResolveException, self).__init__(message)


class PropertyNotExistException(Exception):
    """Thrown when a binding does not have a property name."""

    def __init__(self, message=""):
        super(PropertyNotExistException, self).__init__(message)


class UserCacheNotFoundException(Exception):
    """Thrown when user doesn't have any cache stored."""

    def __init__(self, message=""):
        super(UserCacheNotFoundException, self).__init__(message)


class CredentialsNotFoundException(Exception):
    """Thrown when user's credentials are not found."""

    def __init__(self, message=""):
        super(CredentialsNotFoundException, self).__init__(message)


class CommandNotFoundError(Exception):
    """Thrown when user enters a command that is not recognized."""

    def __init__(self, message=""):
        super(CommandNotFoundError, self).__init__(message)


class CommandFlagNotFoundException(Exception):
    """Thrown when user enters a command flag that is not recognized."""

    def __init__(self, message=""):
        super(CommandFlagNotFoundException, self).__init__(message)


class ZeroFlagException(Exception):
    """Thrown when a command is referenced without a flag."""

    def __init__(self, message=""):
        super(ZeroFlagException, self).__init__(message)

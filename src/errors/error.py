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


class PropertyNotExistException(object):
    """Thrown when a binding does not have a property name."""

    def __init__(self, message=""):
        super(PropertyNotExistException, self).__init__(message)


class UserCacheNotFoundException(object):
    """Thrown when user doesn't have any cache stored."""

    def __init__(self, message=""):
        super(UserCacheNotFoundException, self).__init__(message)

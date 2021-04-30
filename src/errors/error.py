class EmptyResponseException(Exception):
    """Thrown when recieved an empty response."""

    def __init__(self, message):
        super(EmptyResponseException, self).__init__(message)


class FailedLoadingResourceException(Exception):
    """Thrown when failed loading the resources properly."""

    def __init__(self, message):
        super(FailedLoadingResourceException, self).__init__(message)


class LinkedInBlockException(Exception):
    """Thrown when LinkedIn blocks."""

    def __init__(self, message):
        super(LinkedInBlockException, self).__init__(message)

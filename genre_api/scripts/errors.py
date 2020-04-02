class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class APIError(Error):
    """Exception raised for errors in the API calls.

    Attributes:
        expression -- input expression in which the error occurred
        status_code -- status code raised by the API
        message -- explanation of the error
    """

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = f'{status_code} - {message}'

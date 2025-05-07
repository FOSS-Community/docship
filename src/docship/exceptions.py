class DockshipException(Exception):
    """
    Base exception class for Dockship.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class NginxNotInstalled(DockshipException):
    """
    Exception raised when Nginx is not installed.
    """


class NginxConfigError(DockshipException):
    """
    Exception raised when there is an error in the Nginx configuration.
    """

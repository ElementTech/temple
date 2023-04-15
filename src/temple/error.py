"""
A package for making HTTP requests from YAML files.

The package provides an interface for defining HTTP requests in YAML files
and making those requests with Python. The package raises several custom
exceptions, including:

- NoPlanError: raised when no requests plan file is provided.
- InvalidPlanError: raised when a requests plan file is invalid.
- InterruptedError: raised when the user interrupts the program.

The package defines several constants:

- NO_PLAN: exit code indicating that no requests plan file was provided.
- INVALID_PLAN: exit code indicating that a requests plan file was invalid.
- INTERRUPTED: exit code indicating that the user interrupted the program.
- UNKNOWN_ERROR: exit code indicating an unexpected error occurred.

If an unexpected error occurs, the package will catch the error and display
a message instructing the user to create a bug report on the package's GitHub
repository.
"""
# pylint: disable=redefined-builtin
NO_PLAN = 251
INVALID_PLAN = 252
INTERRUPTED = 253
UNKNOWN_ERROR = 254


UNKNOWN_ERROR_MSG = (
    "Caught unexpected error, see traceback and description below. "
    "If this seems like a bug to you, please consider creating a issue in "
    "https://github.com/jatalocks/temple/issues.\n"
)


class YamlRequestsError(Exception):
    """
    Base class for exceptions raised by the YamlRequests package.

    Args:
      message (str): A message describing the error.
      exit_code (int): An exit code indicating the type of error.
    """

    def __init__(self, message, exit_code):
        super().__init__(message)
        self.exit_code = exit_code


class NoPlanError(YamlRequestsError):
    """
    Exception raised when no requests plan file is provided.

    Args:
      path (str, optional): The path to the missing plan file.
    """

    def __init__(self, path=None):
        if not path:
            super().__init__("No requests plan file provided.", NO_PLAN)
        else:
            super().__init__(f"Did not find plan file in {path}.", NO_PLAN)


class InvalidPlanError(YamlRequestsError):
    """
    Exception raised when a requests plan file is invalid.

    Args:
      message (str): A message describing the error.
    """

    def __init__(self, message):
        super().__init__(message, INVALID_PLAN)


class InterruptedError(YamlRequestsError):
    """
    Exception raised when the user interrupts the program.

    Args:
      None
    """

    def __init__(self):
        super().__init__("", INTERRUPTED)

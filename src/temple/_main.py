"""
This module contains the main entry point for the Temple package.

The `main` function is responsible for parsing command line arguments,
loading a requests plan file, and running the requests specified in the
plan. If any errors occur during this process, they will be caught and
reported to the user.

The module also includes a `_print_versions` function that prints the
versions of the package's dependencies.

Functions:
  main: The main entry point for the package.
  _print_versions: Prints the versions of the package's dependencies.
"""
# pylint: disable=broad-exception-caught, redefined-builtin
from os import system
import platform
from traceback import print_exc

from jinja2 import __version__ as _jinja2_version
from yaml import __version__ as _pyyaml_version

from .utils.args import get_argparser, load_temple_file, parse_variables
from .logger import ConsoleLogger
from ._temple import Temple
from ._version import __version__
from .error import (
    NoPlanError,
    InterruptedError,
    InvalidPlanError,
    YamlRequestsError,
    INVALID_TEMPLE,
    UNKNOWN_ERROR,
    UNKNOWN_ERROR_MSG,
)


def _print_versions():
    print(f"{__version__} (" f"jinja2={_jinja2_version}", f"pyyaml={_pyyaml_version}" ")")


def main():
    """
    Parses command line arguments, loads a requests plan file, and runs
    the requests specified in the plan. If any errors occur during this
    process, they will be caught and reported to the user.

    Returns:
      int: The exit code for the program.
    """
    # On windows, run shell command to enable ANSI code support
    if platform.system() == "Windows":
        system("")

    args = get_argparser().parse_args()
    if args.version:
        _print_versions()
        return 0

    logger = ConsoleLogger(animations=args.animation, colors=args.colors)

    try:
        variables_override = parse_variables(args.variables)
    except ValueError as error:
        logger.error(str(error))
        return INVALID_TEMPLE

    try:
        num_errors = run(args.temple_file, logger, variables_override)
        return min(num_errors, 250)
    except YamlRequestsError as error:
        logger.error(str(error))
        return error.exit_code
    except BaseException:
        logger.close()
        logger.error(UNKNOWN_ERROR_MSG)
        print_exc()
        return UNKNOWN_ERROR


def run(temple_file, logger, variables_override=None):
    """
    Parses command line arguments, loads a requests plan file, and runs
    the requests specified in the plan. If any errors occur during this
    process, they will be caught and reported to the user.

    Returns:
      int: The exit code for the program.
    """
    try:
        if not temple_file:
            raise NoPlanError()

        try:
            temple_dict = load_temple_file(temple_file)
            temple_object = Temple(temple_dict, variables_override=variables_override)
            print(temple_object, temple_dict, variables_override)
        except FileNotFoundError as exc:
            raise NoPlanError(temple_file) from exc
        except (
            ValueError,
            AssertionError,
        ) as error:
            raise InvalidPlanError(str(error)) from error

        return 0
    except KeyboardInterrupt as exc:
        logger.close()
        raise InterruptedError() from exc

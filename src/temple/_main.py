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

from .utils.args import get_argparser, load_temple_file
from .logger import ConsoleLogger
from ._temple import Temple
from ._version import __version__
from ._server import TempleServer
from .error import (
    InterruptedError,
    InvalidTempleError,
    TempleError,
    # INVALID_TEMPLE,
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

    logger = ConsoleLogger()

    # try:
    #     variables_override = parse_variables(args.variables)
    # except ValueError as error:
    #     logger.error(str(error))
    #     return INVALID_TEMPLE
    try:
        return run(args.temple_file, logger)
    except TempleError as error:
        logger.error(str(error))
        return error.exit_code
    except BaseException:
        logger.close()
        logger.error(UNKNOWN_ERROR_MSG)
        print_exc()
        return UNKNOWN_ERROR


def run(temple_file, logger):
    """
    Parses command line arguments, loads a requests plan file, and runs
    the requests specified in the plan. If any errors occur during this
    process, they will be caught and reported to the user.

    Returns:
      int: The exit code for the program.
    """
    try:
        try:
            temple_dict = load_temple_file(temple_file)
            temple_object = Temple(temple_dict, temple_file)
            template_server = TempleServer(temple_object, temple_file)
            template_server.run()
        except (
            TempleError,
            ValueError,
            AssertionError,
        ) as error:
            raise InvalidTempleError(str(error)) from error

        return 0
    except KeyboardInterrupt as exc:
        logger.close()
        raise InterruptedError() from exc

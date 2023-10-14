""" Main entry point for the Llama Index. """
import argparse
import logging

from app.agents import start_chat
from app.app_logging import setup_logging
from app.env_var import setup_env_vars
from app.stream_interceptor import intercept_streams

setup_env_vars()

setup_logging()


def parse_arguments() -> argparse.Namespace:
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug", action="store_true", default=False, help="Enable debug logging."
    )
    return parser.parse_args()


def log_stdout(message: str) -> None:
    """Log stdout messages."""
    logging.info(message.strip())


def log_stderr(message: str) -> None:
    """Log stderr messages."""
    logging.info(message.strip())


# intercepting here because the I/O is dynamic and we want to log the whole interaction
@intercept_streams(log_stdout, log_stderr)
def main(command_args):  # pylint: disable=unused-argument
    """Main entry point."""
    start_chat(command_args)


if __name__ == "__main__":
    args = parse_arguments()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    main(command_args=args)

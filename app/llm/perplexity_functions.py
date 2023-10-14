"""Create agents."""
import logging
import time
from datetime import datetime

from app.llm.perplexity import ask_perplexity
from app.utils import is_valid_folder_name, load_string_from_file


class GetInvalidFolderException(Exception):
    """Chat exception."""


def get_valid_folder_name(
    message: str,
    max_retries: int = 10,
    initial_delay: float = 1.0,
    max_delay: float = 32.0,
) -> str:
    """
    Gets a valid folder name by repeatedly asking ask_perplexity.
    """
    folder_prompt = load_string_from_file("app/resources/foldername.txt")
    template = folder_prompt.format(prompt=message)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    delay = initial_delay
    for _ in range(max_retries):
        folder_name = ask_perplexity(template).strip()
        if is_valid_folder_name(folder_name):
            print("Valid folder name suggested: ", folder_name)
            return f"{folder_name}-{timestamp}"

        time.sleep(min(delay, max_delay))
        delay *= 0.5
    err_msg = "Failed to find a valid folder name."
    logging.error(err_msg)

    raise GetInvalidFolderException(err_msg)

""" Interceptor for standard streams. """
import sys
from typing import Any, Callable


class StreamInterceptor:
    """Intercept standard streams."""

    def __init__(self, original_stream: Any, log_func: Callable[[str], None]):
        self.original_stream = original_stream
        self.log_func = log_func

    def write(self, text: str) -> None:
        """Write to the stream."""
        self.original_stream.write(text)
        self.log_func(text)

    def readline(self) -> str:
        """Read a line from the stream."""
        line = self.original_stream.readline()
        self.log_func(f"User Input: {line.strip()}")
        return line

    def flush(self) -> None:
        """Flush the stream."""
        self.original_stream.flush()


def intercept_streams(
    log_stdout: Callable[[str], None], log_stderr: Callable[[str], None]
):
    """A decorator to intercept standard streams."""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            sys.stdout = StreamInterceptor(sys.stdout, log_stdout)
            sys.stderr = StreamInterceptor(sys.stderr, log_stderr)
            sys.stdin = StreamInterceptor(sys.stdin, log_stdout)
            return func(*args, **kwargs)

        return wrapper

    return decorator

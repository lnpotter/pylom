import os
import sys
import inspect
from datetime import datetime, timezone

_main_path = os.path.dirname(__file__)
_logs_path = os.path.join(_main_path, "logs")

os.makedirs(_logs_path, exist_ok=True)

class Logger:
    """
    Manages logging to files, saved in the `logs` folder.

    Usage:
    with Logger() as log:
        log.info("Information here.")

    Attributes:
    name : str, optional
        Log file name, defaults to the current file name.
    file : file-like, optional
        Log file object, defaults to `{name}.txt`.
    template : str, optional
        Log message format, uses `_type`, `timestamp`, `file`, `line`, and `message`.
    timestamp_format : str, optional
        Custom format for the timestamp. Example: "%d-%m-%Y %H:%M:%S %Z".
    """
    
    def __init__(self, name: str = None, file=None, template: str = "[{_type}] {timestamp} {file}:{line} {message}", timestamp_format: str = None) -> None:
        frame_info = inspect.stack()[1]
        self.name = name or os.path.splitext(os.path.basename(frame_info.filename))[0]
        self.file = file or open(os.path.join(_logs_path, f"{self.name}.txt"), "a")
        self.template = template
        self.timestamp_format = timestamp_format

    def log(self, _type, message, *args, **kwargs):
        frame_info = inspect.stack()[2]
        frame = inspect.getframeinfo(frame_info.frame)
        path = os.path.relpath(frame.filename, _main_path)
        path = path if path != '.' else os.path.basename(frame.filename)

        if self.timestamp_format:
            timestamp = datetime.now().strftime(self.timestamp_format)
        else:
            timestamp = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()

        formatted_message = self.template.format(
            name=self.name, _type=_type, timestamp=timestamp, file=path, line=frame.lineno, 
            message=message.format(*args, **kwargs)
        )
        self.file.write(formatted_message + '\n')

    def debug(self, message: str, *args, **kwargs) -> None:
        """Logs a `DEBUG` level message, indicating detailed information for debugging."""
        self.log("DEBUG", message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs) -> None:
        """Logs an `INFO` level message, indicating general information."""
        self.log("INFO", message, *args, **kwargs)

    def warn(self, message: str, *args, **kwargs) -> None:
        """Logs a `WARNING` level message, indicating a potential problem."""
        self.log("WARNING", message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs) -> None:
        """Logs an `ERROR` level message, indicating a significant issue."""
        self.log("ERROR", message, *args, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        if self.file != sys.stdout:
            self.file.close()

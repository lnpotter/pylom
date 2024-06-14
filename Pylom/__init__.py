import os

_main_path = os.path.dirname(__file__)
_logs_path = os.path.join(_main_path, "logs")
os.makedirs(_logs_path, exist_ok=True)

from .Pylom import Logger

__all__ = ["Pylom"]

__version__ = "1.0.0"

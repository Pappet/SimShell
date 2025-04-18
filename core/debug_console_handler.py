import logging
import utility.color as Color
from .debug_console import DebugConsole  # sofern in derselben Package

class DebugConsoleHandler(logging.Handler):
    def __init__(self, debug_console: DebugConsole):
        super().__init__()
        self.debug_console = debug_console

    def emit(self, record: logging.LogRecord):
        try:
            msg = self.format(record)
            # In deiner Console bleibt die Zeit, so wie sie intern gemessen wird
            self.debug_console.log(msg)
        except Exception:
            self.handleError(record)
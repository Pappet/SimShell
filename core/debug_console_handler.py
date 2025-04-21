import logging
from .debug_console import DebugConsole  # sofern in derselben Package

class DebugConsoleHandler(logging.Handler):
    def __init__(self, debug_console: DebugConsole):
        super().__init__()
        self.debug_console = debug_console

    def emit(self, record: logging.LogRecord):
        try:
            msg = self.format(record)
            self.debug_console.log(msg)
        except Exception:
            self.handleError(record)
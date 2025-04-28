"""
Module core/debug_console_handler.py

Defines DebugConsoleHandler, a custom logging.Handler that forwards
log messages to the in-game DebugConsole for on-screen debugging output.
"""

import logging
from .debug_console import DebugConsole


class DebugConsoleHandler(logging.Handler):
    """
    Logging handler that routes formatted log records into a DebugConsole instance.
    """
    def __init__(self, debug_console: DebugConsole):
        """
        Initialize the DebugConsoleHandler.

        Args:
            debug_console (DebugConsole): Target console for displaying log messages.
        """
        super().__init__()
        self.debug_console = debug_console

    def emit(self, record: logging.LogRecord):
        """
        Emit a logging record to the DebugConsole.

        Formats the record using the handler's formatter and logs the
        resulting message into the in-game console.

        Args:
            record (logging.LogRecord): The logging record to be processed.
        """
        try:
            # Format the record into a string message
            msg = self.format(record)
            # Add the formatted message to the debug console
            self.debug_console.log(msg)
        except Exception:
            # Handle any exception that occurs during logging
            self.handleError(record)

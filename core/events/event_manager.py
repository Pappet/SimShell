"""
Module core/events/event_manager.py

Implements EventManager: a simple publish-subscribe system for game events.
Allows components to register callbacks to event types, unregister them,
and dispatch events (with or without collecting responses).
"""

import logging
from core.events.event_types import EventType

logger = logging.getLogger(__name__)


class EventManager:
    """
    Central hub for event registration and dispatch in the game.

    Attributes:
        listeners (Dict[EventType, List[Callable]]):
            Mapping from event types to lists of subscriber callbacks.
    """
    def __init__(self) -> None:
        """
        Initialize the EventManager with no listeners.
        """
        self.listeners: dict[EventType, list] = {}
        logger.debug("EventManager initialized with empty listeners.")

    def register(self, event_type: EventType, callback: callable) -> None:
        """
        Register a callback to be invoked when the specified event type is dispatched.

        Args:
            event_type (EventType): The event enum to listen for.
            callback (callable): Function to call when the event occurs.

        Logs a debug message on registration.
        """
        logger.debug("Registering callback %s for event: %s", callback, event_type)
        self.listeners.setdefault(event_type, []).append(callback)

    def unregister(self, event_type: EventType, callback: callable) -> None:
        """
        Unregister a previously registered callback for an event type.

        Args:
            event_type (EventType): The event enum to stop listening for.
            callback (callable): The callback to remove.

        Logs a debug message if the callback was found and removed.
        """
        if event_type in self.listeners and callback in self.listeners[event_type]:
            logger.debug("Unregistering callback %s for event: %s", callback, event_type)
            self.listeners[event_type].remove(callback)

    def dispatch(self, event_type: EventType, *args, **kwargs) -> None:
        """
        Dispatch an event to all registered callbacks, without collecting return values.

        Args:
            event_type (EventType): The event enum being dispatched.
            *args: Positional arguments forwarded to callbacks.
            **kwargs: Keyword arguments forwarded to callbacks.

        Logs debug information about the dispatch.
        """
        logger.debug(
            "Dispatching event: %s with args: %s, kwargs: %s",
            event_type, args, kwargs
        )
        for callback in self.listeners.get(event_type, []):
            try:
                callback(*args, **kwargs)
            except Exception:
                logger.exception(
                    "Error in callback %s for event: %s", callback, event_type
                )

    def dispatch_with_response(self, event_type: EventType, *args, **kwargs) -> list:
        """
        Dispatch an event and collect return values from each callback.

        Args:
            event_type (EventType): The event enum being dispatched.
            *args: Positional arguments forwarded to callbacks.
            **kwargs: Keyword arguments forwarded to callbacks.

        Returns:
            List[Any]: List of return values from each callback.

        Logs debug information about the dispatch.
        """
        logger.debug(
            "Dispatching event with response: %s with args: %s, kwargs: %s",
            event_type, args, kwargs
        )
        responses = []
        for callback in self.listeners.get(event_type, []):
            try:
                responses.append(callback(*args, **kwargs))
            except Exception:
                logger.exception(
                    "Error in callback %s for event: %s", callback, event_type
                )
        return responses
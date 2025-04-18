# core/event_manager.py
from core.events.event_types import EventType

'''
Event Manager Module
This module provides an event management system that allows different parts of the game to communicate with each other through events.
It allows for registering, unregistering, and dispatching events with or without responses.
'''

class EventManager:
    def __init__(self, debug_console):
        self.debug_console = debug_console
        self.listeners = {}

    def register(self, event_type: EventType, callback):
        self.debug_console.log(f"Registering callback for event: {event_type}")
        self.listeners.setdefault(event_type, []).append(callback)

    def unregister(self, event_type: EventType, callback):
        if event_type in self.listeners:
            if callback in self.listeners[event_type]:
                self.debug_console.log(f"Unregistering callback for event: {event_type}")
            self.listeners[event_type].remove(callback)

    def dispatch(self, event_type: EventType, *args, **kwargs):
        if self.debug_console:
            self.debug_console.log(f"Dispatching event: {event_type} with args: {args}, kwargs: {kwargs}")
        for callback in self.listeners.get(event_type, []):
            callback(*args, **kwargs)

    def dispatch_with_response(self, event_type: EventType, *args, **kwargs):
        if self.debug_console:
            self.debug_console.log(f"Dispatching event with response: {event_type} with args: {args}, kwargs: {kwargs}")
        return [cb(*args, **kwargs) for cb in self.listeners.get(event_type, [])]

'''
This module contains callback functions for the game. These functions are called when certain events occur in the game, 
such as starting or exiting the game, or modifying player stats.
They are designed to be used with the event manager and stat manager to handle game state changes and UI updates.
'''


def modify_stat(stat_manager, stat_name, amount):
    if stat_name in stat_manager.stats:
        stat_manager.modify(stat_name, amount)
    else:
        print(f"Stat '{stat_name}' not found. Cannot modify.")
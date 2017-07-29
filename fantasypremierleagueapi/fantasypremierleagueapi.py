# -*- coding: utf-8 -*-
"""
File: fantasypremierleagueapi.py
Path: fantasypremierleague/
Author: Grant W
"""

# Python Imports

# Third Party Imports
import requests

# Local Imports

BASE_URL = 'https://fantasy.premierleague.com/drf'
DATA_ENDPOINT = 'bootstrap-static'
PLAYER_ENDPOINT = 'element-summary/{player_id}'


def data():
    """Returns all data from the BASE_URL provided above
    """
    url = '{}/{}'.format(BASE_URL, DATA_ENDPOINT)
    return requests.get(url).json()

def player(name=None, id=None):
    """Based off name or id, we will return statistics for a
    specific player.
    name should be a str "LastName,FirstName"
    """
    if not name and not id:
        raise TypeError("You must provide either a player_name "
                        "or a player_id.")
    url = '{}/{}'.format(BASE_URL, PLAYER_ENDPOINT)
    if name:
        id = _player_id_from_name(name)
    return requests.get(url.format(player_id=id)).json()

def _player_id_from_name(name):
    """Takes a name and attempts to return the ID of the player
    for interactions with the FPL API.
    Player Name should be a str "LastName,FirstName"
    """
    try:
        first_name = name.split(',')[1].strip()
        second_name = name.split(',')[0].strip()
    except IndexError:
        raise TypeError('Please enter a name in format '
                        '"LastName,FirstName"')
    _data = data()
    player_ids= [x['id'] for x in _data['elements']
                 if x['first_name'] == first_name
                 and x['second_name'] == second_name]
    if len(player_ids) == 0:
        raise TypeError('No player found with the given name.')
    elif len(player_ids) > 1:
        raise TypeError('Multiple players found with the given name.')
    return player_ids[0]

def team():
    """
    """
    return {}

def game():
    """
    """

    return {}

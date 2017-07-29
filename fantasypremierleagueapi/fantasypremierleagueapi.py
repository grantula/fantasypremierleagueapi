# -*- coding: utf-8 -*-
"""
File: fantasypremierleagueapi.py
Path: fantasypremierleague/
Author: Grant W
"""

# Python Imports
from functools import wraps
from pprint import pprint
# Third Party Imports
import requests

# Local Imports

BASE_URL = 'https://fantasy.premierleague.com/drf'
DATA_ENDPOINT = 'bootstrap-static'
PLAYER_ENDPOINT = 'element-summary/{player_id}'


def ensure_one_item(f):
    """This decorator is used to ensure that when we are searching
    for a specific item, we return only one result. Otherwise, we
    raise an exception.
    """
    @wraps(f)
    def wrapped(*args, **kwargs):
        val = f(*args, **kwargs)
        if len(val) == 0:
            raise TypeError('No data found with the given parameters')
        elif len(val) > 1:
            raise TypeError('Too much data found with the given parameters.')
        return val[0]
    return wrapped

def data():
    """Returns all data from the BASE_URL provided above
    """
    url = '{}/{}'.format(BASE_URL, DATA_ENDPOINT)
    return requests.get(url).json()

def player(name=None, id=None, info_only=False):
    """Based off name or id, we will return statistics for a
    specific player. If we only want basic information on the player,
    pass the info_only kwarg as True which will not return fixtures
    and other info.

    id - player id
    name - name should be a str "LastName,FirstName"
    info_only - bool, True if we only want basics (Name, current stats, etc)
    """
    player_info = _player_info(name=name, id=id)
    if info_only:
        return player_info
    url = '{}/{}'.format(BASE_URL, PLAYER_ENDPOINT)
    ret_val = requests.get(url.format(player_id=player_info['id'])).json()
    ret_val['information'] = player_info
    return ret_val

@ensure_one_item
def team(name=None, id=None):
    """Returns data on a given team name or team id
    """
    if not name and not id:
        raise TypeError("You must provide either a team name "
                        "or a team id.")
    data_ = data()
    # Id is more specific, so try that first
    teams = []
    if id:
        teams = [x for x in data_['teams'] if x['id'] == id]
    elif name:
        teams = [x for x in data_['teams']
                 if x['name'].lower() == name.lower()]
    return teams

@ensure_one_item
def _player_info(name=None, id=None):
    """This will return the basic information on a player
    Player Name should be a str "LastName,FirstName"
    """
    if not name and not id:
        raise TypeError("You must provide either a player's name "
                        "or a player's id.")
    data_ = data()
    players = []
    if id:
        players = [x for x in data_['elements']
                   if x['id'] == id]
    elif name:
        try:
            first_name = name.split(',')[1].strip()
            second_name = name.split(',')[0].strip()
        except IndexError:
            raise TypeError('Please enter a name in format '
                            '"LastName,FirstName"')
        players = [x for x in data_['elements']
                   if x['first_name'] == first_name
                   and x['second_name'] == second_name]
    return players

def dream_team():
    """Returns the current dream_team
    """
    data_ = data()
    return [x for x in data_['elements'] if x['in_dreamteam']]

def top(num_results=10, position=None, sort_key='total_points', reverse=False):
    """Returns the top given number of players overall. If a position
    is given, we return the top ten in that position.
    positions = 1 - 2 - 3 - 4 (goalie - def - mid - fwd)
    """
    data_ = sorted(data()['elements'],
                   key = lambda e: e[sort_key],
                   reverse=reverse)
    if position:
        data_ = [x for x in data_ if x['element_type'] == position]
    return data_[:num_results]

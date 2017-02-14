import pprint
import sys
import os
import subprocess

import spotipy

import spotipy.util as util

from datetime import datetime, timedelta

SPOTIPY_CLIENT = spotipy.oauth2.SpotifyOAuth(os.environ.get('SPOTIPY_CLIENT_ID'),
                                             os.environ.get('SPOTIPY_CLIENT_SECRET'),
                                             os.environ.get('SPOTIPY_REDIRECT_URI'))

sp_info = {}

username = 'zzzeldah'

def initialize_auth():

    access_token_info = SPOTIPY_CLIENT.refresh_access_token(os.environ.get('R_TOKEN'))

    now = datetime.now()
    expiration = now + timedelta(hours=1)

    sp_info.update({'access_token': access_token_info['access_token'],
               'expiration_time': expiration})


def get_token():
    """ Returns the token

    checks to see if the client is expired, if it is, refresh it, then pull token
    from the SPOTIFY_CLIENT object
    """

    # if SPOTIPY_CLIENT._is_token_expired(sp_info could be the whole thing instead of what I have it):
    #     SPOTIPY_CLIENT.refresh_access_token(os.environ.get('R_TOKEN'))
    now = datetime.now()

    if sp_info['expiration_time'] - now == timedelta(minutes=0):
        initialize_auth()

    token = sp_info['access_token']

    return token


def create_playlist(playlist_name):
    """Create a playlist"""

    token = get_token()

    sp = spotipy.Spotify(auth=token)
    playlist = sp.user_playlist_create(username, playlist_name)

    print 'playlist id: ' + playlist['name'], playlist['id']
    return playlist['id']


def show_user_playlists(playlist_names):
    pass

def show_all_playlists():

    token = get_token()

    sp = spotipy.Spotify(auth=token)
    playlists = sp.user_playlists(username)

    return playlists

def get_playlist(playlist_id):
    pass
    
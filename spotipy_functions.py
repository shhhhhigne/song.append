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


def get_playlist_info(playlist_id):

    #TODO: get plylist info
    pass


def get_artist_info(artist_id):

    #TODO: get artist info
    pass


def get_album_info(album_id):

    # album_id = {}
    # if len(album_items) > 0:
    #       for item in album_items:
    #           albums[item['id']] = item['name']

    #       all_results['albums'] = albums

    #   album_info = {'id': album_id,
    #                 'name': }

    #TODO: get album info
    pass





def get_track_info(item):

    artists = []
    for artist in item['artists']:
        artist_info = {'artist_id': artist['id'],
                       'artist_name': artist['name']}
        artists.append(artist_info)


    track_info = {'id': item['id'],
                  'name': item['name'],
                  'preview': item['preview_url'],
                  'spotify_url': item['external_urls']['spotify'],
                  'artists': artists,
                  # 'artist_url': item['artist']['external_urls']['spotify']
                  'album_id': item['album']['id'],
                  'album_name': item['album']['name']
                  # 'artist_url': item['artist']['external_urls']['spotify']
    }
    return track_info



def search(user_input):

    spotify = spotipy.Spotify()


    # all_results = {'tracks': None
    #                # 'playlists': None,
    #                # 'albums': None,
    #                # 'artists': None
                   # } 

    all_results = {}


   

    track_results = spotify.search(q=user_input, type='track')
    track_items = track_results['tracks']['items']
    tracks = {}

    if len(track_items) > 0:
        for item in track_items:
            # print '*******************tracks', tracks
            track_info = get_track_info(item)
            # print track_info
            tracks[item['id']] = track_info

        all_results['tracks'] = tracks

    else:
        all_results['tracks'] = None


    all_results['stuff'] = 'stuff'

    print all_results

    #TODO: be able to search things other than songs 

    # artist_results = spotify.search(q=user_input, type='artist')
    # artist_items = artist_results['artists']['items']
    # artists = {}
    # if len(artist_items) > 0:
    #     for item in artist_items:
    #         artists[item['id']] = item['name']

    #     all_results['artists'] = artists



    # playlist_results = spotify.search(q=user_input, type='playlist')
    # playlist_items = playlist_results['playlists']['items']
    # playlists = {}
    # if len(playlist_items) > 0:
    #     for item in playlist_items:
    #         playlists[item['id']] = item['name']
        
    #     all_results['playlists'] = playlists


    # album_results = spotify.search(q=user_input, type='album')
    # album_items = album_results['albums']['items']
    # albums = {}
    # if len(album_items) > 0:
    #     for item in album_items:
    #         albums[item['id']] = item['name']

    #     all_results['albums'] = albums


    return all_results
    
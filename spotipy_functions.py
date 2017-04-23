import pprint
import sys
import os
import subprocess

import spotipy

import spotipy.util as util

from datetime import datetime, timedelta

from add_to_db_helper import add_song_to_db, add_artist_to_db

from model import Album

SPOTIPY_CLIENT = spotipy.oauth2.SpotifyOAuth(os.environ.get('SPOTIPY_CLIENT_ID'),
                                             os.environ.get('SPOTIPY_CLIENT_SECRET'),
                                             os.environ.get('SPOTIPY_REDIRECT_URI'))

sp_info = {}

username = 'zzzeldah'

# later I could integrate google maps api to do location services or whatever
COUNTRY = 'US'

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

    if 'expiration_time' not in sp_info or sp_info['expiration_time'] - now == timedelta(minutes=0):
        initialize_auth()

    token = sp_info['access_token']

    return token


def create_playlist(playlist_name):
    """Create a playlist"""

    token = get_token()

    sp = spotipy.Spotify(auth=token)
    playlist = sp.user_playlist_create(username, playlist_name)

    # print 'playlist id: ' + playlist['name'], playlist['id']
    return playlist['id']


def change_playlist_name(playlist_id, new_name):

    token = get_token()

    sp = spotipy.Spotify(auth=token)
    playlist = sp.user_playlist_change_details(username, 
                                               str(playlist_id), 
                                               name=str(new_name),
                                               public=None,
                                               collaborative=None)

    # print playlist


def show_user_playlists(playlist_names):
    pass

def show_all_playlists():

    token = get_token()

    sp = spotipy.Spotify(auth=token)
    playlists = sp.user_playlists(username)

    return playlists

def get_playlist(playlist_id):

    # token = get_token()


    pass

def add_song_to_spotify_playlist(song_id, playlist_id):

    token = get_token()

    sp = spotipy.Spotify(auth=token)
    # print '*******', song_id

    # song_id = str(song_id)
    # song_ids = []
    # song_ids.append(song_id)

    # print song_ids

    results = sp.user_playlist_add_tracks(username, playlist_id, song_id)
    # print '*******', results

def remove_song_from_spotify_playlist(song_id, playlist_id):

    token = get_token()

    sp = spotipy.Spotify(auth=token)
    # print song_id
    results = sp.user_playlist_remove_all_occurrences_of_tracks(username, str(playlist_id), song_id)
    # print  '#######', results


def get_playlist_info(playlist_id):

    #TODO: get plylist info
    pass


def get_artist_info(artist_spotify_id):

    #TODO: get artist info
    spotify = spotipy.Spotify()

    artist_albums = spotify.artist_albums(artist_spotify_id, country=COUNTRY)

    album_ids = []

    for album in artist_albums['items']:
        album_ids.append(album['id'])


    full_artist_info = spotify.artist(artist_spotify_id)

    all_results = {'album_data': get_album_info(album_ids),
                   'artist_data': get_artists([full_artist_info])
    }

    return all_results


def get_artists(all_artists):

    artists = []
    for artist in all_artists:
        artist_info = {'artist_spotify_id': artist['id'],
                       'artist_name': artist['name'],
                       'artist_url': artist['external_urls']['spotify']}


        artist_info['artist_id'] = add_artist_to_db(artist_info)


        artists.append(artist_info)

    return artists


def get_album_info(album_spotify_ids):

    spotify = spotipy.Spotify()

    all_results = []

    albums = spotify.albums(album_spotify_ids)

    for album_info in albums['albums']:

        album_spotify_id = album_info['id']

        # album_data = {'album_name': album_info['name'],
        #               'album_spotify_id': album_spotify_id,
        #               'album_url': album_info['external_urls']['spotify']}

        album_data = get_album(album_info)

        album_artists = get_artists(album_info['artists'])

        album_data['artists'] = album_artists


        track_results = {}

        tracks = album_info['tracks']
        track_items = tracks['items']

        for item in track_items:

            track_info = get_track_info(item, album_data)

            track_results[track_info['id']] = track_info

        album_data['album_id'] = Album.query.filter_by(album_spotify_id=album_spotify_id).one().album_id

        all_album_results = {'album_data': album_data,
                             'track_results': track_results
        }

        all_results.append(all_album_results)

    return all_results


def get_album(album_info):

    album_data = {'album_spotify_id': album_info['id'],
                  'album_name': album_info['name'],
                  'album_url': album_info['external_urls']['spotify']}

    return album_data


def get_track_info(item, album_data=None):

    artists = get_artists(item['artists'])

    if album_data == None:
        album_data = get_album(item['album'])

    track_info = {'spotify_id': item['id'],
                  'name': item['name'],
                  'preview': item['preview_url'],
                  'spotify_url': item['external_urls']['spotify'],
                  'artists': artists
                  # 'spotify_album_id': item['album']['id'],
                  # 'album_name': item['album']['name'],
                  # 'album_url': item['album']['external_urls']['spotify']
    }

    track_info.update(album_data)

    ids = add_song_to_db(track_info)
    track_info['id'] = ids['song_id']
    track_info['album_id'] = ids['album_id']

    return track_info



def search(user_input, offset=0):

    spotify = spotipy.Spotify()


    # all_results = {'tracks': None
    #                # 'playlists': None,
    #                # 'albums': None,
    #                # 'artists': None
                   # } 

    all_results = {}


   

    track_results = spotify.search(q=user_input, offset=offset, type='track')
    track_items = track_results['tracks']['items']
    tracks = {}

    if len(track_items) > 0:
        for item in track_items:
            # print '*******************tracks', tracks
            track_info = get_track_info(item)
            tracks[track_info['id']] = track_info

        all_results['tracks'] = tracks

    else:
        all_results['tracks'] = None


    all_results['stuff'] = 'stuff'

    # print all_results

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










    
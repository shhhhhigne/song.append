from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

import re

from model import User, Group, UserGroup, Playlist, Song, PlaylistSong, Vote
from model import connect_to_db, db

from spotipy_functions import initialize_auth, create_playlist, show_all_playlists





def get_user_groups(user_id):

    users_groups = UserGroup.query.filter_by(user_id=user_id).all()

    groups = []
    for users_group in users_groups:
        if users_group.in_group:
            group = Group.query.filter_by(group_id=users_group.group_id).one()
            groups.append(group)
        else:
            print "not in ", users_group.group_id

    return groups


def get_user_owned_playlists(user_id):

    user_playlists = Playlist.query.filter_by(user_id=user_id).all()

    return user_playlists


def get_user_belonging_playlists(user_id):

    user_groups = get_user_groups(user_id)

    playlists = []
    for group in user_groups:
        group_playlists = Playlist.query.filter_by(group_id=group.group_id).all()
        for group_playlist in group_playlists:
            playlists.append(group_playlist)



    return playlists


def get_playlist_songs(playlist_id, status):

    playlist_songs = PlaylistSong.query.filter_by(playlist_id=playlist_id).filter_by(status=status).order_by('index').all()

    print 'songs', playlist_songs

    return playlist_songs


def get_song_data(song_id):

    song = Song.query.filter_by(song_id=song_id).one()

    song_artists = SongArtist.query.filter_by(song_id=song_id).all()

    artists = []
    for artist in song_artist:
        artists.append(artist_id=song_artist.artist_id)

    song_data = {'song': song,
                 'artists': artists}

    return song


# def get_song_artists(song_id):

#     song_artists = SongArtist.query.filter_by(song_id=song_id)

#     artists = []
#     for artist in song_artist:
#         artists.append(artist_id=song_artist.artist_id)

#     return artists









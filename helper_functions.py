from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
# from sqlalchemy import func

import re

from model import Album, Song, Artist, SongArtist
from model import User, Group, UserGroup, Playlist, PlaylistSong, Vote
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

    # print 'songs', playlist_songs

    return playlist_songs


def get_song_data(song_id):

    song = Song.query.filter_by(song_id=song_id).one()

    album = Album.query.filter_by(album_id=song.album_id).one()

    song_artists = SongArtist.query.filter_by(song_id=song_id).all()
    # print '*********', song_artists

    artists = []
    for artist in song_artists:
        artist_info = Artist.query.filter_by(artist_id=artist.artist_id).one()
        artists.append(artist_info)

    song_data = {'song': song,
                 'artists': artists,
                 'album': album}

    return song_data


def get_song_value(ps_id):

    # q = Vote.query.filter_by(ps_id=ps_id).all()

    # value = q.query(func.sum(Vote.value))

    # query = db.session.()

    values = Vote.query.filter_by(ps_id=ps_id).all()
    # query = db.session.query(Vote.value).filter_by(ps_id=1).all()

    total = 0
    for instance in values:
        print '&&&&&&&&&&&', instance.value
        total = total + int(instance.value)

    print '############', total



    # print "*" * 40
    # print query


    # q.(db.func.sum(value))
    # q.having(db.func.sum(Vote.ps_id))

    # value = q.filter_by(ps_id=ps_id)

    return total









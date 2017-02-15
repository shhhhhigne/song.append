from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

import re

from model import Album, Song, Artist, SongArtist
from model import User, Group, UserGroup, Playlist, PlaylistSong, Vote
from model import connect_to_db, db


def add_song_to_db(track_info):

    song_spotify_id = track_info['id']

    try:
        Song.query.filter_by(song_spotify_id=song_spotify_id).one()

    except sqlalchemy.orm.exc.NoResultFound:

        album_id = add_album_to_db(track_info)

        song_object = Song(song_name=track_info['name'],
                           album_id=album_id,
                           song_spotify_id=song_spotify_id,
                           preview_url=track_info['preview'],
                           spotify_url=track_info['spotify_url']
                           )

        db.session.add(song_object)

        db.session.commit()

        for artist in track_info['artists']:
            song_artist_object = SongArtist(song_id=song_object.song_id,
                                            artist_id=artist['artist_id'])



def add_artist_to_db(artist_info):

    artist_spotify_id = artist_info['artist_spotify_id']

    try:
        artist_object = Artist.query.filter_by(artist_spotify_id=artist_spotify_id).one()

    except sqlalchemy.orm.exc.NoResultFound:
        artist_object = Artist(artist_name=artist_info['artist_name'],
                               artist_spotify_id=artist_spotify_id,
                               artist_spotify_url=artist_info['artist_url'])

        db.session.add(artist_object)

        db.session.commit()

    return artist_object.artist_id


def add_album_to_db(track_info):

    album_spotify_id = track_info['album_id']

    try:
        album_object = Album.query.filter_by(album_spotify_id=album_spotify_id).one()

    except sqlalchemy.orm.exc.NoResultFound:
        album_object = Album(album_name=track_info['name'],
                             album_spotify_id=album_spotify_id,
                             album_spotify_url=track_info['album_url'])

        db.session.add(album_object)

        db.session.commit()

    return album_object.album_id

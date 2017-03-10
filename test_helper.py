"""Collaborative Curated Playlist."""

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

from model import Album, Song, Artist, SongArtist
from model import User, Group, UserGroup, Playlist, PlaylistSong, Vote
from model import connect_to_db, db

from spotipy_functions import initialize_auth, create_playlist, show_all_playlists, search
from spotipy_functions import add_song_to_spotify_playlist, change_playlist_name

from helper_functions import (get_user_groups,
                              get_user_owned_playlists, 
                              get_user_belonging_playlists,
                              get_playlist_songs,
                              get_song_data,
                              get_song_value,
                              check_song_status,
                              register_user_vote,
                              get_playlist_data,
                              get_group_data,
                              remove_song_fully,
                              move_song_req_to_act,
                              readd_song_to_req,
                              remove_song_helper,
                              add_song_helper,
                              get_user_administered_groups)

from test_data import create_test_data

from unittest import TestCase

app = Flask(__name__)

class BasicTests(TestCase):

        @classmethod
        def setUp(cls):
            """Stuff to do once before running all tests."""

            
            # Connect to test database
            connect_to_db(app, "postgresql:///test_collabplaylists")

            # Create tables and add sample data
            db.create_all()

            create_test_data()



        @classmethod
        def tearDown(cls):

            db.session.close()
            db.drop_all()


        def test_get_user_administered_groups(self, user_id):

            groups = get_user_administered_groups(user_id)

            for group in groups:
                assert group.group_id == user_id


        def test_get_user_owned_playlists(self, user_id):

            playlists = get_user_owned_playlists(user_id)

            for playist in playlists:
                assert playlist.playlist_id == user_id


        # def test_get_song_data(self):

        #     song_id = 1

        #     song_data = get_song_data(song_id)

        #     song_artist = SongArtist.query.filter_by(song_id=song_id).all()



        #     assert song_data = {'song': song,
        #                         'artists': }



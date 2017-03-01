import unittest

from server import app

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

import re

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
                              remove_song_fully)



class PlaylistTests(unittest.TestCase):
    """Tests for my playlist site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("Homepage", result.data)

    def test_create_playlist(self):
        result = self.client.get("/create-playlist")
        self.assertIn("Create Playlist", result.data)
        self.assertNotIn("Homepage", result.data)

#     def test_rsvp(self):
#         result = self.client.post("/rsvp",
#                                   data={'name': "Jane", 'email': "jane@jane.com"},
#                                   follow_redirects=True)
#         self.assertIn("Yay!", result.data)
#         self.assertIn("Party Details", result.data)
#         self.assertNotIn("Please RSVP", result.data)


# class PartyTestsDatabase(unittest.TestCase):
#     """Flask tests that use the database."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         # Get the Flask test client
#         self.client = app.test_client()

#         # Show Flask errors that happen during tests
#         app.config['TESTING'] = True

#         # Connect to test database
#         connect_to_db(app, "postgresql:///testdb")

#         # Create tables and add sample data
#         db.create_all()
#         example_data()

#     def tearDown(self):
#         """Do at end of every test."""

#         db.session.close()
#         db.drop_all()

#     def test_games(self):
#         """Test departments page."""

#         result = self.client.get("/games")
#         self.assertIn("Power Grid", result.data)


if __name__ == "__main__":
    unittest.main()

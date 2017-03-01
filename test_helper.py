"""Collaborative Curated Playlist."""

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
                              remove_song_fully,
                              move_song_req_to_act,
                              readd_song_to_req,
                              remove_song_helper,
                              add_song_helper)


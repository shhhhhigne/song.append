from model import Album, Song, Artist, SongArtist
from model import User, Group, UserGroup, Playlist, PlaylistSong, Vote
from model import connect_to_db, db

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

from random import randint

# from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "ABC"

# app.jinja_env.undefined = StrictUndefined


def add_sample_users(num):

    for i in range(1, num + 1):

        username = 'User' + str(i)
        email = "user" + str(i) + "@email.com"
        fname = "Fname" + str(i)
        lname = "Lname" + str(i)
        password = 'pass'

        new_user = User(username=username,
                        email=email,
                        fname=fname,
                        lname=lname,
                        password=password
                        )

        print new_user
        db.session.add(new_user)
        db.session.commit()

        add_sample_groups(i, new_user.user_id)

    set_up_groups


def add_sample_groups(num, user_id):
    """"""

    group_name = "Group" + str(i)

    new_group = Group(group_name=group_name,
                      user_id=user_id
                      )

    print new_group
    db.session.add(new_group)
    db.session.commit()
    set_up_groups(num)


def set_up_groups(num):

    for i in range(1, num + 1):
        group_name = "Group" + str(i)

        group_object = Group.query.filter_by(group_name=group_name).one()

        user_id = group.user_id

        for i in range(1, num + 1):
            user_group_object = UserGroup(group_id=group_id,
                                          user_id=user_id)

            # ensures admins are members of groups and all users are accounted for
            if i == user_id:
                user_group_object.in_group = True

            db.session.add(user_group_object)
            db.session.commit()

            print user_group_object
            assign_group_users(num)


def assign_group_users(num):

    for i in range(1, num + 1):

        user_id = i
        group_id = (i % 3) + 1

        user_group_object = UserGroup.query.filter_by(user_id=user_id).filter_by(group_id=group_id).one()

        user_group_object.in_group = True

        print user_group_object

        db.session.commit()

    # Add User1 to group 3 as well for testing purposes.
    user_group_object1 = UserGroup.query.filter_by(user_id=1).filter_by(group_id=3).one()

    user_group_object.in_group = True
    

    # Add User3 to group 4 as well to test the admin page.
    user_group_object2 = UserGroup.query.filter_by(user_id=3).filter_by(group_id=4).one()

    user_group_object.in_group = True

    print new_group_user1
    print new_group_user2

    db.session.commit()


def create_sample_playlists(num):
    """ 

    This will break if you input a different num to it than num of users
    """

    for i in range(1, num + 1):

        playlist_name = 'Playlist' + str(i)
        playlist_spotify_id = 'spotufy_id_act' + str(i)
        playlist_spotify_id_req = 'spotufy_id_req' + str(i)
        playlist_spotify_id_full = 'spotufy_id_full' + str(i)

        user_id = i
        group_id = i

        playlist_object = Playlist(playlist_name=playlist_name,
                                   playlist_spotify_id=playlist_spotify_id,
                                   playlist_spotify_id_req=playlist_spotify_id_req,
                                   playlist_spotify_id_full=playlist_spotify_id_full,
                                   user_id=user_id,
                                   group_id=group_id)

        db.session.add(playlist_object)
        db.session.commit()


def create_and_add_artists(num, song_num):
    for i in range(1, num + 1):
        artist_name = "Artist" + str(i)
        artist_spotify_id = artist_spotify_id + str(i)
        artist_spotify_url = artist_spotify_url + str(i)

        artist_object = Artist(artist_name=artist_name,
                               artist_spotify_id=artist_spotify_id,
                               artist_spotify_url=artist_spotify_url)

        db.session.add(artist_object)
        db.session.commit()

        #each artist will have an album with the same number
        create_and_add_album(artist_object, i, song_num, num)


def create_and_add_album(artist_object, i, song_num, num):

    artist_name = "Album" + str(i)
    album_spotify_id = album_spotify_id + str(i)
    album_spotify_url = album_spotify_url + str(i)

    album_object = Album(album_name=album_name,
                         album_spotify_id=album_spotify_id,
                         album_spotify_url=album_spotify_url)

    db.session.add(album_object)
    db.session.commit()

    create_and_add_songs_to_albums(artist_object, album_object.album_id, song_num, i, num)


def create_and_add_songs_to_albums(artist_object, album_id, song_num, i, num):

    for a in range(1, song_num + 1):
        song_name = 'Song' + str(i) + str(a)
        album_id = album_id
        song_spotify_id = 'song_spotify_id' + str(i) + str(a)
        preview_url = 'preview_url' + str(i) + str(a)
        spotify_url = 'spotify_url' + str(i) + str(a)

        song_object = Song(song_name=song_name,
                           album_id=album_id,
                           song_spotify_id=song_spotify_id,
                           preview_url=preview_url,
                           spotify_url=spotify_url)

        db.session.add(song_object)
        db.session.commit()

        create_song_artist_connection(song_object.song_id, artist_object.artist_id, (i%3), num)

def create_song_artist_connection(song_id, artist_id, num_artists, num):

    song_artist_object = SongArtist(song_id=song_id,
                                    artist_id=artist_id)

    db.session.add(song_artist_object)
    db.session.commit()

    for j in num_artists:
        other_artist_id = num % artist_id + j
        if artist_id == other_artist_id or other_artist_id > num:
            other_artist_id = other_artist_id - 1
            if other_artist_id < 1:
                other_artist_id = other_artist_id + 3
        song_artist_object = SongArtist(song_id=song_id,
                                        artist_id=other_artist_id)
        db.session.add(song_artist_object)
        db.session.commit()


def add_songs_to_playlists(num, song_num):
    
    for i in range(1, num + 1):
        songs_in_playlist = (i % song_num)/2
        for song in songs_in_playlist:
            a = i%num+1
            b = i%song_num+1
            song_name = 'Song' + str(a) +str(b)
            song_object = Song.query.filter_by(song_name=song_name).first()

            status_int = i%5
            if status_int==0 or status_int==2:
                status='active'
            elif status_int==1 or status_int==4:
                status = 'requested'
            elif status_int==2:
                status='deleted'

            immutable_int = i%6

            if immutable_int==6:
                immutable=True
            else:
                immutable=False


            playlist_song_object = PlaylistSong(playlist_id=i,
                                                song_id=song_object.song_id,
                                                status=status,
                                                immutable=immutable)
            db.session.add(playlist_song_object)
            db.session.commit()

            # if status == 'active':
            #     song_value = 


def create_test_data():
    num = 5
    song_num = 10

    add_sample_users(num)
    create_sample_playlists(num)
    create_and_add_artists(num, song_num)
    add_songs_to_playlists(num, song_num)





from model import Album, Song, Artist, SongArtist
from model import User, Group, UserGroup, Playlist, PlaylistSong, Vote
from model import connect_to_db, db

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

# from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


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
                        lanme=lname,
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


def set_up_groups(num)

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





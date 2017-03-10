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
from spotipy_functions import add_song_to_spotify_playlist, remove_song_from_spotify_playlist





def get_user_groups(user_id):

    users_groups = UserGroup.query.filter_by(user_id=user_id).all()

    groups = []
    for users_group in users_groups:
        if users_group.in_group and users_group.group.user_id != user_id:
            group = users_group.group
            groups.append(group)
        else:
            continue
            # print "not in ", users_group.group_id

    return groups


def get_user_administered_groups(user_id):

    users_groups = Group.query.filter_by(user_id=user_id).all()

    return users_groups


def get_user_owned_playlists(user_id):

    user_playlists = Playlist.query.filter_by(user_id=user_id).all()

    return user_playlists


def get_user_belonging_playlists(user_id):

    user_groups = get_user_groups(user_id)

    playlists = []
    for group in user_groups:
        group_playlists = Playlist.query.filter_by(group_id=group.group_id).all()
        for group_playlist in group_playlists:
            if group_playlist.user_id == session['user_id']:
                continue
            playlists.append(group_playlist)

    return playlists


def get_playlist_songs(playlist_id, status):

    playlist_songs = PlaylistSong.query.filter_by(playlist_id=playlist_id).filter_by(status=status).order_by('index').all()

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

    # I might want to do this as a sql thing and not just loop through it
    values = Vote.query.filter_by(ps_id=ps_id).all()

    total = 0
    for instance in values:
        # print '*******', instance
        # if instance.user.user_group.in_group == True:
        total = total + int(instance.value)

    return total


def register_user_vote(user_id, ps_id, vote_value):

    try:
        user_vote_object = Vote.query.filter_by(ps_id=ps_id).filter_by(user_id=user_id).one()

        if user_vote_object.value == vote_value:
            #This needs to change so that they cant click on the same thumb again
            # or somehow be refactored
            # vote_total = get_song_value(ps_id)

            alert = 'you already gave this a' + str(vote_value)
            vote_status = 'same',

        else:
            user_vote_object.value = vote_value

            db.session.commit()

            alert = 'your vote is now changed to ' + str(vote_value)
            vote_status = 'changed'


    except sqlalchemy.orm.exc.NoResultFound:

        user_vote_object = Vote(value=vote_value,
                                ps_id=ps_id,
                                user_id=user_id)

        db.session.add(user_vote_object)
        db.session.commit()


        alert = 'You gave a vote of ' + str(vote_value)
        vote_status = 'new'

    vote_total = get_song_value(ps_id)

    song_status_changed = check_song_status(ps_id, vote_total, vote_value)

    user_vote_info = {'user_alert': alert,
                      'vote_status': vote_status,
                      'vote_total': vote_total,
                      'song_status_changed': song_status_changed}

    return user_vote_info



def check_song_status(ps_id, vote_total, vote_value):

    ps_object = PlaylistSong.query.filter_by(ps_id=ps_id).one()
    immutable = ps_object.immutable
    if immutable == True:
        return False

    # playlist_object = Playlist.query.filter_by(playlist_id=ps_object.playlist_id).one()

    score_to_add = ps_object.playlist.num_votes_add
    score_to_del = -(ps_object.playlist.num_votes_del)

    # playlist_name = playlist_object.playlist_name
    # playlist_name_req = playlist_name + '_req'
    # playlist_name_full = playlist_name + '_full'

    # playlist_spotify_id_act = playlist_object.playlist_spotify_id
    # playlist_spotify_id_req = playlist_object.playlist_spotify_id_req
    # playlist_spotify_id_full = playlist_object.playlist_spotify_id_full

    song_status = ps_object.status
    status_changed = False

    # song_object = Song.query.filter_by(song_id=ps_object.song_id).one()
    # song_spotify_id = song_object.song_spotify_id

    if vote_value == -1:
        if vote_total <= score_to_del and song_status != 'deleted':
            
            status_changed = True

            remove_song_fully(ps_object)

            # remove_song_helper(song_spotify_id, playlist_object, '_full')
            # remove_song_from_spotify_playlist(playlist_spotify_id_full, song_spotify_id)

            # if song_status == 'active':
            #     remove_song_from_spotify_playlist(playlist_spotify_id_act, song_spotify_id)
            # else:
            #     remove_song_from_spotify_playlist(playlist_spotify_id_req, song_spotify_id)
    # Should I have this as an if or as an elif
    elif vote_value == 1:
        if song_status == 'deleted':
            
            status_changed = True
            readd_song_to_req(ps_object)

            # add_song_to_spotify_playlist(song_spotify_id, playlist_spotify_id_full)
            # add_song_to_spotify_playlist(song_spotify_id, playlist_spotify_id_req)

        elif vote_total >= score_to_add and song_status == 'requested':
            # ps_object.status ='active'
            # db.session.commit()
            status_changed = True
            move_song_req_to_act(ps_object)

            # import pdb
            # pdb.set_trace()

            # add_song_to_spotify_playlist([song_spotify_id], playlist_spotify_id_act)
            # remove_song_from_spotify_playlist([song_spotify_id], playlist_spotify_id_req)

    # I could just check the status changed here
    # should I recall the view playlists here?? h
    # how should I do it


    ####### I could also do all this adding and removing only when a user clicks
    #### the big play button and just run through my db and update the spotify playlists
    return status_changed


def get_playlist_data(playlist_id):

    playlist = Playlist.query.filter_by(playlist_id=playlist_id).one()

    playlist_songs = get_playlist_songs(playlist_id, 'active')
    req_playlist_songs = get_playlist_songs(playlist_id, 'requested')

    songs = []

    for song in playlist_songs:
        song_data = get_song_data(song.song_id)
        song_data['song-value'] = get_song_value(song.ps_id)
        song_data['ps_id'] = song.ps_id
        songs.append(song_data)

    req_songs = []
    for song in req_playlist_songs:
        song_data = get_song_data(song.song_id)
        song_data['ps_id'] = song.ps_id
        song_data['song-value'] = get_song_value(song.ps_id)
        # print '**********', get_song_value(song.ps_id)
        # song_data['song_value'] = get_song_value(song.ps_id)
        req_songs.append(song_data)

    playlist_data = {'playlist': playlist,
                     'songs': songs,
                     'req_songs': req_songs}

    return playlist_data


def get_group_data(group_id):

    group_object = Group.query.filter_by(group_id=group_id).one()

    user_id = session['user_id']

    admin_id = group_object.user_id

    # owner_object = User.query.filter_by(user_id=owner_id).one()

    admin = {'name': group_object.user.fname + ' ' + group_object.user.lname,
             'username': group_object.user.username,
             'admin_id': admin_id}

    is_admin = False

    if user_id == admin_id:
        is_admin = True

    group_name = group_object.group_name

    group_query = UserGroup.query.filter_by(group_id=group_id)
    member_query = group_query.filter_by(in_group=True)
    members = member_query.filter(UserGroup.user_id!=admin_id).all()

    is_member = True
    try:
        member_query.filter_by(user_id=user_id).one()
    except sqlalchemy.orm.exc.NoResultFound:
        is_member = False

    playlist_objects = Playlist.query.filter_by(group_id=group_id).all()

    playlists = {}

    for playlist in playlist_objects:
        playlist_name = playlist.playlist_name
        user_id = playlist.user_id
        playlists[user_id] = playlists.get(user_id, [])
        playlists[user_id].append(playlist_name)

    group_data = {'group':group_object,
                  'admin': admin,
                  'is_admin': is_admin,
                  'members': members,
                  'playlists': playlists,
                  'is_member': is_member}

    return group_data

# def remove_users_from_group():


def move_song_req_to_act(ps_object):

    song_spotify_id = ps_object.song.song_spotify_id
    playlist_object = ps_object.playlist

    add_song_helper(song_spotify_id, playlist_object, 'actv')
    remove_song_helper(song_spotify_id, playlist_object, 'req')

    ps_object.status ='active'
    db.session.commit()


def readd_song_to_req(ps_object):

    song_spotify_id = ps_object.song.song_spotify_id
    playlist_object = ps_object.playlist

    add_song_helper(song_spotify_id, playlist_object, 'full')
    add_song_helper(song_spotify_id, playlist_object, 'req')

    ps_object.status ='requested'
    db.session.commit()


def remove_song_fully(ps_object):

    print ps_object

    song_spotify_id = ps_object.song.song_spotify_id
    playlist_object = ps_object.playlist

    remove_song_helper(song_spotify_id, playlist_object, 'full')

    status = ps_object.status

    if status == 'requested':
        playlist_type = 'req'

    if status == 'active':
        playlist_type = 'actv'

    remove_song_helper(song_spotify_id, playlist_object, playlist_type)

    ps_object.status = 'deleted'
    db.session.commit()


def remove_song_helper(song_spotify_id, playlist_object, playlist_type):

    playlist_name = playlist_object.playlist_name + playlist_type
    if playlist_type == 'req':
        playlist_spotify_id = playlist_object.playlist_spotify_id_req
    elif playlist_type == 'full':
        playlist_spotify_id = playlist_object.playlist_spotify_id_full
    else:
        playlist_spotify_id = playlist_object.playlist_spotify_id

    song_id = []
    song_id.append(song_spotify_id)


    remove_song_from_spotify_playlist(song_id, playlist_spotify_id)


def add_song_helper(song_spotify_id, playlist_object, playlist_type):

    # playlist_id_s = playlist_spotify_id + playlist_type
    playlist_name = playlist_object.playlist_name + playlist_type
    if playlist_type == 'req':
        playlist_spotify_id = playlist_object.playlist_spotify_id_req
    elif playlist_type == 'full':
        playlist_spotify_id = playlist_object.playlist_spotify_id_full
    else:
        playlist_spotify_id = playlist_object.playlist_spotify_id

    song_id = []
    song_id.append(song_spotify_id)

    add_song_to_spotify_playlist(song_id, playlist_spotify_id)


















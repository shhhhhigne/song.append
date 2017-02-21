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

    print ps_id

    values = Vote.query.filter_by(ps_id=ps_id).all()
    # print Vote.query.filter_by(ps_id=10).all()
    # query = db.session.query(Vote.value).filter_by(ps_id=1).all()

    total = 0
    for instance in values:
        # print '&&&&&&&&&&&', instance.value
        total = total + int(instance.value)

    # print '############', total



    # print "*" * 40
    # print query


    # q.(db.func.sum(value))
    # q.having(db.func.sum(Vote.ps_id))

    # value = q.filter_by(ps_id=ps_id)

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

    playlist_object = Playlist.query.filter_by(playlist_id=ps_object.playlist_id).one()

    score_to_add = playlist_object.num_votes_add
    score_to_del = -(playlist_object.num_votes_del)

    playlist_name = playlist_object.playlist_name
    playlist_name_req = playlist_name + '_req'
    playlist_name_full = playlist_name + '_full'

    playlist_spotify_id_act = playlist_object.playlist_spotify_id
    playlist_spotify_id_req = playlist_object.playlist_spotify_id_req
    playlist_spotify_id_full = playlist_object.playlist_spotify_id_full

    song_status = ps_object.status
    status_changed = False

    song_object = Song.query.filter_by(song_id=ps_object.song_id).one()
    song_spotify_id = song_object.song_spotify_id

    if vote_value == -1:
        if vote_total <= score_to_del and song_status != 'deleted':
            ps_object.status = 'deleted'
            db.session.commit()
            status_changed = True

            remove_song_from_spotify_playlist(playlist_spotify_id_full, song_spotify_id)

            if song_status == 'active':
                remove_song_from_spotify_playlist(playlist_spotify_id_act, song_spotify_id)
            else:
                remove_song_from_spotify_playlist(playlist_spotify_id_req, song_spotify_id)
    # Should I have this as an if or as an elif
    elif vote_value == 1:
        if song_status == 'deleted':
            ps_object.status ='requested'
            db.session.commit()
            status_changed = True

            add_song_to_spotify_playlist(song_spotify_id, playlist_spotify_id_full)
            add_song_to_spotify_playlist(song_spotify_id, playlist_spotify_id_req)

        elif vote_total >= score_to_add and song_status == 'requested':
            ps_object.status ='active'
            db.session.commit()
            status_changed = True

            add_song_to_spotify_playlist(song_spotify_id, playlist_spotify_id_act)
            remove_song_from_spotify_playlist(song_spotify_id, playlist_spotify_id_req)

    # I could just check the status changed here
    # should I recall the view playlists here?? h
    # how should I do it


    ####### I could also do all this adding and removing only when a user clicks
    #### the big play button and just run through my db and update the spotify playlists
    return status_changed












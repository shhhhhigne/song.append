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
from spotipy_functions import add_song_to_spotify_playlist

from helper_functions import (get_user_groups,
                              get_user_owned_playlists, 
                              get_user_belonging_playlists,
                              get_playlist_songs,
                              get_song_data,
                              get_song_value,
                              check_song_status,
                              register_user_vote,
                              get_playlist_data,
                              get_group_data)


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage."""
    # a = jsonify([1,3])
    # playlists = pull_all_playlists()
    playlists = []
    initialize_auth()


    return render_template("homepage.html",
                            playlists=playlists)


@app.route("/register")
def register_form():

    if session.get('logged_in') is True:
        flash('user already signed in')
        return redirect('/')
    else:
        return render_template("sign_up_form.html")


@app.route("/register", methods=["POST"])
def register_process():

    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    fname = request.form.get('fname')
    lname = request.form.get('lname')

    try:
        user_object = User.query.filter_by(email=email).one()
        flash('Email already in use, please sign in or use another')
        return redirect('/register')

    except sqlalchemy.orm.exc.NoResultFound:
        try:
            user_object = User.query.filter_by(username=username).one()
            flash('Username already exists, please sign in or use another')

            return redirect('/register')
        # flash('user created: %s') % (username)
        except sqlalchemy.orm.exc.NoResultFound:
            user_object = User(email=email,
                               username=username,
                               password=password,
                               fname=fname,
                               lname=lname)

            # We need to add to the session or it won't ever be stored
            db.session.add(user_object)

            # Once we're done, we should commit our work
            db.session.commit()

    session['user_id'] = user_object.user_id
    session['logged_in'] = True
    session['username'] = user_object.username
    print(session)
    flash("Logged In")
    return redirect("/")


@app.route("/sign-in")
def sign_in_form():
    if session.get('logged_in') is True:
        flash('user already signed in')
        return redirect('/')
    else:
        return render_template("sign_in.html")


@app.route("/sign-in", methods=["POST"])
def sign_in_process():
    username = request.form.get('username')
    password = request.form.get('password')

    try:
        user_object = User.query.filter_by(email=username).one()
        if password == user_object.password:
            pass   # login -- for clairty in code
        else:
            flash("Wrong Password")
            return redirect('/sign-in')

    except sqlalchemy.orm.exc.NoResultFound:
        flash("Email not found, please try again or create a new account")
        return redirect('/sign-in')

    user_id = user_object.user_id
    session['user_id'] = user_id
    session['logged_in'] = True
    session['email'] = user_object.email

    print(session)
    flash("Logged In")
    return redirect("/user-page/" + str(user_id))


@app.route('/logout')
def logout_process():
    if session.get('logged_in') is True:
        del session['user_id']
        del session['logged_in']
        flash('logged out')
    else:
        flash('not logged in')

    return redirect('/sign-in')


@app.route('/user-page/<user_id>')
def show_user_page(user_id):

    user_object = User.query.filter_by(user_id=user_id).one()
    playlists = show_all_playlists()
    playlists_info = {}
    for playlist in playlists['items']:
        playlists_info[playlist['id']] = playlist['name']

    return render_template('user_page.html',
                           playlists_info=playlists_info)


@app.route('/create-playlist')
def show_create_playlist_form():

    user_id = session['user_id']

    groups = get_user_groups(user_id)

    return render_template('create_playlist.html',
                            groups=groups,
                            playlist_exists=False)

@app.route('/create-playlist', methods=['POST'])
def create_playlist_form():

    name = request.form.get('playlist-name')
    name_req = name + '_req'
    name_full = name + '_full'
    # playlist_object = User(name=name)

    playlist_spotify_id = create_playlist(name)
    playlist_spotify_id_req = create_playlist(name_req)

    playlist_spotify_id_full = create_playlist(name_full)

    user_id = session['user_id']

    group_id = request.form.get('group')

    num_to_add = request.form.get('num-to-add') or None
    num_to_del = request.form.get('num-to-del') or None

    playlist_object = Playlist(playlist_name=name,
                               playlist_spotify_id=playlist_spotify_id,
                               playlist_spotify_id_req=playlist_spotify_id_req,
                               playlist_spotify_id_full=playlist_spotify_id_full,
                               num_votes_add=num_to_add,
                               num_votes_del=num_to_del,
                               group_id=group_id,
                               user_id=user_id)

    db.session.add(playlist_object)

    db.session.commit()



    # playl

    # # We need to add to the session or it won't ever be stored
    # db.session.add(playlist_object)

    # # Once we're done, we should commit our work
    # db.session.commit()

    return redirect("/")

@app.route('/add-song-to-playlist/<song_id>/<playlist_id>', methods=['POST'])
def add_song_to_playlist(song_id, playlist_id):

    song_object = Song.query.filter_by(song_id=song_id).one()
    playlist_object = Playlist.query.filter_by(playlist_id=playlist_id).one()

    song_name = song_object.song_name
    playlist_name = playlist_object.playlist_name

    current_user_id = session['user_id']
    playlist_owner_id = playlist_object.user_id


    try:
        playlist_song_object = PlaylistSong.query.filter_by(song_id=song_id).filter_by(playlist_id=playlist_id).one()

        status = playlist_song_object.status

        # user_add_try_info['already_in_playlist'] = True


        # Later I will want to change this so that when you add a song already in the playlist
        # it will check if youve already voted on it and if you have then you cant, otherwise
        # add one to the vote 


        # flash(song_name + 'is already in playlist' + playlist_name)

        already_in_playlist = True
        
        add_alert = 'already in'
        # return jsonify({'song_name': song_name,
        #                 'playlist_name': playlist_name,
        #                 'already_in_playlist': True,
        #                 'status': status})

    except sqlalchemy.orm.exc.NoResultFound:

        song_spotify_id = [song_object.song_spotify_id]
        playlist_spotify_id_full = playlist_object.playlist_spotify_id_full

        if current_user_id == playlist_owner_id:
            status = 'active'

            count = PlaylistSong.query.filter_by(playlist_id=playlist_id).filter_by(status='active').count()
            index = count + 1

            playlist_spotify_id = playlist_object.playlist_spotify_id

            add_alert = 'added to'

        else:
            status = 'requested'

            count = PlaylistSong.query.filter_by(playlist_id=playlist_id).filter_by(status=status).count()
            index = count + 1

            playlist_spotify_id = playlist_object.playlist_spotify_id_req

            add_alert = 'requested for'

        playlist_song_object = PlaylistSong(song_id=song_id,
                                            playlist_id=playlist_id,
                                            status = status,
                                            index=index)

        db.session.add(playlist_song_object)
        db.session.commit()

        add_song_to_spotify_playlist(song_spotify_id, playlist_spotify_id)
        add_song_to_spotify_playlist(song_spotify_id, playlist_spotify_id_full)

        
        # flash(song_name + 'added to  playlist' + playlist_name)

        already_in_playlist = False

        # return jsonify({'song_name': song_name,
        #                 'playlist_name': playlist_name,
        #                 'already_in_playlist': False,
        #                 'status': status})


    ps_id = playlist_song_object.ps_id

    user_add_try_info = register_user_vote(current_user_id, ps_id, 1)

    # I could put together this alert here and not in my javascript if I wanted
    user_add_try_info['song_name'] = song_name
    user_add_try_info['playlist_name'] = playlist_name
    # user_add_try_info['already_in_playlist'] = already_in_playlist
    # user_add_try_info['status'] = status
    user_add_try_info['add_alert'] = add_alert

    alert = user_add_try_info['user_alert']

    # user_add_try_info['alert'] = alert + 
    

    return jsonify(user_add_try_info)


@app.route('/playlist/<playlist_id>')
def show_playlist(playlist_id):

    # playlist = Playlist.query.filter_by(playlist_id=playlist_id).one()

    # playlist_songs = get_playlist_songs(playlist_id, 'active')
    # req_playlist_songs = get_playlist_songs(playlist_id, 'requested')


    # songs = []

    # for song in playlist_songs:
    #     song_data = get_song_data(song.song_id)
    #     song_data['song-value'] = get_song_value(song.ps_id)
    #     song_data['ps_id'] = song.ps_id
    #     songs.append(song_data)

    # req_songs = []
    # for song in req_playlist_songs:
    #     song_data = get_song_data(song.song_id)
    #     song_data['ps_id'] = song.ps_id
    #     song_data['song-value'] = get_song_value(song.ps_id)
    #     # print '**********', get_song_value(song.ps_id)
    #     # song_data['song_value'] = get_song_value(song.ps_id)
    #     req_songs.append(song_data)

    playlist_data = get_playlist_data(playlist_id)

    playlist = playlist_data['playlist']
    songs = playlist_data['songs']
    req_songs = playlist_data['req_songs']

    user_id = session['user_id']

    group_id = playlist.group_id

    user_object = User.query.filter_by(user_id=playlist.user_id).one()

    groups = Group.query.filter_by(group_id=group_id).one()

    group = Group.query.filter_by(group_id=group_id).one()

    is_owner = False

    if playlist.user_id == user_id:
        #theyre not actually creating this, I might want to refactor this somehow
        page = 'owned_playlist.html'
        is_owner = True

    else:
        page = 'playlist.html'


    return render_template(page,
                           playlist=playlist,
                           songs=songs,
                           req_songs=req_songs,
                           user=user_object,
                           groups=groups)


# @app.route('/playlist/<playlist_id>/edit')
# def edit_playlist(playlist_id):



@app.route('/get-all-playlists')
def show_playlist_list():
    # playlists = show_all_playlists()
    # playlists_info = {}
    # for playlist in playlists['items']:
    #     if not playlist['name'].endswith('_full'):
    #         playlists_info[playlist['id']] = playlist['name']
    # return jsonify(playlists_info)

    # user_id = session['user_id']
    # users_groups = UserGroup.query.filter_by(user_id=user_id).all()
    # for users_group in users_groups:
    #     user_playlists = Playlist.query.filter_by(group_id=users_group.group_id).all()

    # return jsonify(user_playlists)
    pass


@app.route('/get-user-owned-playlists')
def show_user_owned_playlists():

    user_id = session['user_id']

    playlists = get_user_owned_playlists(user_id)

    user_playlists = {}

    for playlist in playlists:
        user_playlists[playlist.playlist_id] = playlist.playlist_name


    return jsonify(user_playlists)


@app.route('/get-user-belonging-playlists')
def show_user_belonging_playlists():

    user_id = session['user_id']

    playlists = get_user_belonging_playlists(user_id)

    user_playlists = {}

    for playlist in playlists:
        user_playlists[playlist.playlist_id] = playlist.playlist_name



    return jsonify(user_playlists)

    




# @app.route('/get-playlist/<playlist_id>')
# def get_playlist(playlist_id):

#     playlist_object = Playlist.query.filter_by(playlist_id=playlist_id).one()
#     playlist_name = playlist_object.playlist_name

#     songs = PlaylistSong.query.filter_by(playlist_id=playlist_id).all()
    

#     return render_template('playlist.html',
#                            playlist_object=playlist_object
#                            )

@app.route('/create-group')
def create_group_form():

    return render_template('create_group_form.html')


@app.route('/create-group', methods=['POST'])
def create_group():

    name = request.form.get('group-name')

    user_id = session['user_id']

    group_object = Group(group_name=name,
                         user_id=user_id)

    db.session.add(group_object)

    db.session.commit()

    group_id = group_object.group_id

    return redirect('/add-to-group/' + str(group_id))


@app.route('/edit-group/<group_id>')
def edit_group(group_id):

    group_data = get_group_data(group_id)


    group_query = UserGroup.query.filter_by(group_id=group_id)
    non_members = group_query.filter_by(in_group=False).all()

    if not group_data['is_admin']:
        return redirect('/')

    return render_template('edit_group.html',
                           group=group_data['group'],
                           admin=group_data['admin'],
                           members=group_data['members'],
                           playlists=group_data['playlists'],
                           non_members=non_members)






@app.route('/get-user-belonging-groups')
def show_user_belonging_groups():
    user_id = session['user_id']

    groups = get_user_groups(user_id)

    user_groups = {}

    for group in groups:
        user_groups[group.group_id] = group.group_name


    return jsonify(user_groups)


@app.route('/add-to-group/<group_id>', methods=['GET'])
def add_to_group_form(group_id):

    group_object = Group.query.filter_by(group_id=group_id).one()

    user_objects = User.query.all()

    group_users = UserGroup.query.filter_by(group_id=group_id).filter_by(in_group=True).all()

    users = {}

    for user in user_objects:
        users[user.user_id] = {'name': user.fname + ' ' + user.lname,
                               'username': user.username,
                               'member': False}

    for user in group_users:
        users[user.user_id]['member'] = True

    return render_template('add_users_to_group.html',
                           group=group_object,
                           users=users)


@app.route('/add-to-group/<group_id>', methods=['POST'])
def update_users_in_group(group_id):

    users = request.json['users']

    for user in users.values():
        user_id = user['user_id'] 
        try:
            ug_object = UserGroup.query.filter_by(user_id=user_id).filter_by(group_id=group_id).one()
            if user['member'] == True:
                ug_object.in_group = True
            else:
                ug_object.in_group = False

            #ug_object.in_group = True if user['member'] == True else False

        except sqlalchemy.orm.exc.NoResultFound:
            if user['member'] == True:
                ug_object = UserGroup(user_id=user_id,
                                      group_id=group_id,
                                      in_group=True)
            else:
                ug_object = UserGroup(user_id=user_id,
                                      group_id=group_id)

            db.session.add(ug_object)

        db.session.commit()

    return 'success'



@app.route('/search', methods=['GET'])
def show_search_results():

    user_input = request.args.get('search-str')

    results = search(user_input)

    return render_template('search_results.html',
                           results=results)



@app.route('/register-user-vote', methods=['POST'])
def register_user_vote_form():

    user_id = session['user_id']
    ps_id = request.form.get('ps_id')
    vote_value = int(request.form.get('vote_value'))

    thumb_id = request.form.get('thumb_id')



    # try:
    #     user_vote_object = Vote.query.filter_by(ps_id=ps_id).filter_by(user_id=user_id).one()

    #     if user_vote_object.value == vote_value:
    #         #This needs to change so that they cant click on the same thumb again
    #         # or somehow be refactored
    #         # vote_total = get_song_value(ps_id)

    #         alert = 'you already gave this a' + str(vote_value)
    #         vote_status = 'same',

    #     else:
    #         user_vote_object.value = vote_value

    #         db.session.commit()


    #         alert = 'your vote is now changed to ' + str(vote_value)
    #         vote_status = 'changed'


    # except sqlalchemy.orm.exc.NoResultFound:

    #     user_vote_object = Vote(value=vote_value,
    #                             ps_id=ps_id,
    #                             user_id=user_id)

    #     db.session.add(user_vote_object)
    #     db.session.commit()


    #     alert = 'You gave a vote of ' + str(vote_value)
    #     vote_status = 'new'

    user_vote_info = register_user_vote(user_id, ps_id, vote_value)

    # vote_total = get_song_value(ps_id)

    # song_status_changed = check_song_status(ps_id, vote_total, vote_value)

    user_vote_info['ps_id'] = ps_id
    user_vote_info['vote_value'] = vote_value
    # user_vote_info['vote_total'] = vote_total
    # user_vote_info['song_status_changed'] = song_status_changed


    return jsonify(user_vote_info)


@app.route('/get-current-user-vote', methods=['POST'])
def get_current_user_votes():

    user_id = session['user_id']

    print '******', 
    ps_ids = request.form.getlist('ps_ids[]')

    votes = []

    for ps_id in ps_ids:
        try:
            user_vote = Vote.query.filter_by(user_id=user_id).filter_by(ps_id=ps_id).one()

            vote_info = {'ps_id': ps_id,
                         'user_id': user_id,
                         'vote_value': user_vote.value}

            votes.append(vote_info)

        except sqlalchemy.orm.exc.NoResultFound:
            continue

    return jsonify(votes)







 

















if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')


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
                              get_user_administered_groups)


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
    fname = request.form.get('fname').title()
    lname = request.form.get('lname').title()

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
    session['email'] = user_object.email
    session['username'] = user_object.username
    print(session)
    flash("Logged In")

    for group in Group.query.all():
        user_group_object = UserGroup(group_id=group.group_id,
                                      user_id=user_object.user_id)
        db.session.add(user_group_object)
        db.session.commit()

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
        user_object = User.query.filter_by(username=username).one()
        if password == user_object.password:
            pass   # login -- for clairty in code
        else:
            flash("Wrong Password")
            return redirect('/sign-in')

    except sqlalchemy.orm.exc.NoResultFound:
        try:
            user_object = User.query.filter_by(email=username).one()
            if password == user_object.password:
                pass   # login -- for clairty in code
            else:
                flash("Wrong Password")
                return redirect('/sign-in')

        except sqlalchemy.orm.exc.NoResultFound:

            flash("User not found, please try again or create a new account")
            return redirect('/sign-in')

    user_id = user_object.user_id
    session['user_id'] = user_id
    session['logged_in'] = True
    session['email'] = user_object.email
    session['username'] = user_object.username

    print(session)
    flash("Logged In")
    return redirect("/")


@app.route('/logout')
def logout_process():
    if session.get('logged_in') is True:
        del session['user_id']
        del session['username']
        del session['email']
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
    admin_groups = get_user_administered_groups(user_id)

    return render_template('create_playlist.html',
                            groups=groups,
                            admin_groups=admin_groups,
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

    group_id = request.form.get('group-selection')

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

    return redirect("/playlist/" + str(playlist_object.playlist_id))

@app.route('/add-song-to-playlist/<song_id>/<playlist_id>', methods=['POST'])
def add_song_to_playlist(song_id, playlist_id):

    song_object = Song.query.filter_by(song_id=song_id).one()
    playlist_object = Playlist.query.filter_by(playlist_id=playlist_id).one()

    song_name = song_object.song_name
    playlist_name = playlist_object.playlist_name

    current_user_id = session['user_id']
    playlist_owner_id = playlist_object.user_id

    override = request.form.get('override')

    # print '^^^^^^^^^^^override: ', override
    lock = request.form.get('lock')
    # print '^^^^^^^^^^^lock: ', lock

    if override == 'true':
        status = 'active'
    else:
        status = 'requested'

    if lock == 'true':
        immutable = True
    else:
        immutable = False


    try:
        playlist_song_object = PlaylistSong.query.filter_by(song_id=song_id).filter_by(playlist_id=playlist_id).one()

        current_status = playlist_song_object.status
        current_lock = playlist_song_object.immutable

        # if override:
        #     playlist_song_object.status = 'active'
        # if lock:
        #     playlist_song_object.immutable = True

        if current_status == 'requested':
            playlist_song_object.status = status
        if current_lock == False:
            playlist_object.immutable = immutable

        db.session.commit()

        already_in_playlist = True
        
        add_alert = 'already in'
        # return jsonify({'song_name': song_name,
        #                 'playlist_name': playlist_name,
        #                 'already_in_playlist': True,
        #                 'status': status})

    except sqlalchemy.orm.exc.NoResultFound:

        song_spotify_id = [song_object.song_spotify_id]
        playlist_spotify_id_full = playlist_object.playlist_spotify_id_full

        count = PlaylistSong.query.filter_by(playlist_id=playlist_id).count()
        index = count + 1



        # if current_user_id == playlist_owner_id:

        #     status = 'active'

        #     # count = PlaylistSong.query.filter_by(playlist_id=playlist_id).filter_by(status='active').count()
        #     index = count + 1

        #     playlist_spotify_id = playlist_object.playlist_spotify_id

        #     add_alert = 'added to'

        # else:
        #     status = 'requested'

        #     count = PlaylistSong.query.filter_by(playlist_id=playlist_id).filter_by(status=status).count()
        #     index = count + 1

        #     playlist_spotify_id = playlist_object.playlist_spotify_id_req

        #     add_alert = 'requested for'

        playlist_song_object = PlaylistSong(song_id=song_id,
                                            playlist_id=playlist_id,
                                            status = status,
                                            immutable=immutable,
                                            index=index)

        db.session.add(playlist_song_object)
        db.session.commit()

        status = playlist_song_object.status

        if status == 'requested':
            playlist_spotify_id = playlist_object.playlist_spotify_id_req
            add_alert = 'requested for'

        if status == 'active':
            playlist_spotify_id = playlist_object.playlist_spotify_id
            add_alert = 'added to'

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

    playlist_data = get_playlist_data(playlist_id)

    playlist = playlist_data['playlist']
    songs = playlist_data['songs']
    req_songs = playlist_data['req_songs']

    user_id = session['user_id']

    group_id = playlist.group_id

    user_object = User.query.filter_by(user_id=playlist.user_id).one()

    if group_id == None:
        group_name = 'Not Connected to Group'
    else:
        group_name = playlist.group.group_name

    is_owner = False

    if playlist.user_id == user_id:
        is_owner = True



    return render_template('playlist.html',
                           playlist=playlist,
                           songs=songs,
                           req_songs=req_songs,
                           # user=user_object,
                           is_owner=is_owner,
                           group_name=group_name)


@app.route('/playlist/<playlist_id>/edit')
def edit_playlist_form(playlist_id):

    playlist_data = get_playlist_data(playlist_id)

    playlist = playlist_data['playlist']
    songs = playlist_data['songs']
    req_songs = playlist_data['req_songs']

    user_id = session['user_id']

    group_id = playlist.group_id

    user_object = User.query.filter_by(user_id=playlist.user_id).one()

    users_groups = get_user_groups(user_id)
    user_admin_groups = get_user_administered_groups(user_id)
    # groups = Group.query.filter_by.all()

    if group_id == None:
        group = 'Not Connected to Group'
    else:
        group = playlist.group

    if playlist.user_id != user_id:
        return redirect('/playlist/' + playlist_id)



    return render_template('owned_playlist.html',
                           playlist=playlist,
                           songs=songs,
                           req_songs=req_songs,
                           users_groups=users_groups,
                           user_admin_groups=user_admin_groups,
                           group=group)


@app.route('/playlist/<playlist_id>/edit', methods=['POST'])
def edit_playlist(playlist_id):

    playlist_object = Playlist.query.filter_by(playlist_id=playlist_id).one()

    name = request.form.get('playlist-name')
    if playlist_object.playlist_name != name:
        name_req = name + '_req'
        name_full = name + '_full'


        playlist_spotify_id = playlist_object.playlist_spotify_id
        playlist_spotify_id_req = playlist_object.playlist_spotify_id_req
        playlist_spotify_id_full = playlist_object.playlist_spotify_id_full


        change_playlist_name(playlist_spotify_id, name)
        change_playlist_name(playlist_spotify_id_req, name_req)
        change_playlist_name(playlist_spotify_id_full, name_full)

        playlist_object.playlist_name = name

    print(request.form)

    group_id = request.form.get('group-selection')
    if playlist_object.group_id != group_id:
        playlist_object.group_id = group_id

    num_votes_add = request.form.get('num-to-add')
    if playlist_object.num_votes_add != num_votes_add:
        playlist_object.num_votes_add = num_votes_add

    num_votes_del = request.form.get('num-to-del')
    if playlist_object.num_votes_del != num_votes_del:
        playlist_object.num_votes_del = num_votes_del

    db.session.commit()

    return redirect('/playlist/' + playlist_id + '/edit')


@app.route('/admin-remove-song', methods=['POST'])
def owner_remove_song_from_playlist():

    ps_id = request.form.get('ps_id')

    ps_object = PlaylistSong.query.filter_by(ps_id=ps_id).one()

    lock_status = 'unlocked'
    if ps_object.immutable:
        lock_status = 'locked'

    remove_info = jsonify({'lock_status': lock_status,
                           'song_name': ps_object.song.song_name,
                           'playlist_name': ps_object.playlist.playlist_name})

    remove_song_fully(ps_object)

    return remove_info


@app.route('/admin-add-song', methods=['POST'])
def owner_add_song_to_playlist():

    ps_id = request.form.get('ps_id')

    ps_object = PlaylistSong.query.filter_by(ps_id=ps_id).one()

    lock_status = 'unlocked'
    if ps_object.immutable:
        lock_status = 'locked'

    add_info = jsonify({'lock_status': lock_status,
                        'song_name': ps_object.song.song_name,
                        'playlist_name': ps_object.playlist.playlist_name})

    move_song_req_to_act(ps_object)

    return add_info

@app.route('/get-lock-status', methods=['POST'])
def get_lock_status():

    ps_ids = request.form.getlist('ps_ids[]')

    lock_statuses = []

    for ps_id in ps_ids:

        ps_object = PlaylistSong.query.filter_by(ps_id=ps_id).one()

        lock_info = {'ps_id': ps_id,
                     'lock_status': ps_object.immutable}

        lock_statuses.append(lock_info)

    return jsonify(lock_statuses)

@app.route('/lock-song', methods=['POST'])
def lock_unlock_song_in_playlist():

    ps_id = request.form.get('ps_id')
    old_lock_status = request.form.get('old_lock_status')
    
    ps_object = PlaylistSong.query.filter_by(ps_id=ps_id).one()

    if old_lock_status == 'unlocked':
        ps_object.immutable = True
        new_lock_status = 'locked'
    elif old_lock_status == 'locked':
        ps_object.immutable = False
        new_lock_status = 'unlocked'


    lock_info = jsonify({'new_lock_status': new_lock_status,
                         'song_name': ps_object.song.song_name,
                         'playlist_name': ps_object.playlist.playlist_name})

    db.session.commit()

    return lock_info


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

    group_admin_object = UserGroup(group_id=group_id,
                                   user_id=user_id,
                                   in_group=True)

    db.session.add(group_admin_object)

    for user in User.query.all():
        try:
            UserGroup.query.filter_by(user_id=user.user_id).filter_by(group_id=group_id).one()
            print 'heyyyyyyyyyyyyyyyy'
        except sqlalchemy.orm.exc.NoResultFound:
            user_group_object = UserGroup(group_id=group_id,
                                          user_id=user.user_id)
            db.session.add(user_group_object)

    db.session.commit()


    return redirect('/edit-group/' + str(group_id))


@app.route('/edit-group/<group_id>')
def edit_group(group_id):

    group_data = get_group_data(group_id)


    group_query = UserGroup.query.filter_by(group_id=group_id)
    non_members = group_query.filter_by(in_group=False).all()
    print 'non members:', non_members


    if not group_data['is_admin']:
        return redirect('/')

    return render_template('edit_group.html',
                           group=group_data['group'],
                           admin=group_data['admin'],
                           members=group_data['members'],
                           playlists=group_data['playlists'],
                           non_members=non_members)


@app.route('/group/<group_id>')
def show_group_page(group_id):

    group_data = get_group_data(group_id)

    if group_data['is_member'] == False:
        return redirect('/')

    group_query = UserGroup.query.filter_by(group_id=group_id)
    non_members = group_query.filter_by(in_group=False).all()

    return render_template('group.html',
                           group=group_data['group'],
                           admin=group_data['admin'],
                           members=group_data['members'],
                           playlists=group_data['playlists'],
                           non_members=non_members)



@app.route('/get-user-admin-groups')
def show_user_admin_groups():
    user_id = session['user_id']

    groups = get_user_administered_groups(user_id)

    user_groups = {}

    for group in groups:
        user_groups[group.group_id] = group.group_name

    return jsonify(user_groups)



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


@app.route('/add-member', methods=['POST'])
def add_member_to_group():

    user_ids = request.form.getlist('user_ids[]')
    group_id = request.form.get('group_id')

    current_group_object = UserGroup.query.filter_by(group_id=group_id)
    usernames = []

    return_string = ""

    for user_id in user_ids:
        try:
            user_group_object = current_group_object.filter_by(user_id=user_id).one()

            user_group_object.in_group = True

        except sqlalchemy.orm.exc.NoResultFound:
            user_group_object = UserGroup(user_id=user_id,
                                          group_id=group_id,
                                          in_group=True)

            db.session.add(user_group_object)

        db.session.commit()
        username = user_group_object.user.username
        return_string = return_string + username + ', '

    group_name = user_group_object.group.group_name
    return_string = return_string[:-1]

    return return_string



@app.route('/remove-member', methods=['POST'])
def remove_member_from_group():

    group_id = request.form.get('group_id')
    user_id = request.form.get('user_id')

    user_group_object = UserGroup.query.filter_by(group_id=group_id).filter_by(user_id=user_id).one()

    current_user_id = session['user_id']
    admin_id = user_group_object.group.user_id

    if current_user_id != admin_id and current_user_id != int(user_id):
        return 'error, you cannot remove another user if you are not the admin'

    user_group_object.in_group = False
    db.session.commit()

    users_playlists = Playlist.query.filter_by(group_id=group_id).all()

    for playlist in users_playlists:
        playlist.group_id = None
        db.session.commit()

    username = user_group_object.user.username
    group_name = user_group_object.group.group_name

    return username + ' has been removed from ' + group_name


@app.route('/admin-member', methods=['POST'])
def make_member_admin():

    user_id = request.form.get('user_id')
    group_id = request.form.get('group_id')

    group_object = Group.query.filter_by(group_id=group_id).one()

    group_object.user_id = user_id

    db.session.commit()

    username = group_object.user.username
    group_name = group_object.group_name

    return username + ' is now the admin of ' + group_name



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

    user_vote_info = register_user_vote(user_id, ps_id, vote_value)

    user_vote_info['ps_id'] = ps_id
    user_vote_info['vote_value'] = vote_value

    return jsonify(user_vote_info)


@app.route('/get-current-user-vote', methods=['POST'])
def get_current_user_votes():

    user_id = session['user_id']

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

@app.route('/check-lock-status', methods=['POST'])
def get_song_lock_status():

    ps_ids = request.form.getlist('ps_ids[]')

    locks = []

    for ps_id in ps_ids:
        ps_object = PlaylistSong.query.filter_by(ps_id=ps_id).one()
        print ps_object

        lock_status = {'ps_id': ps_id,
                       'lock_status': ps_object.immutable}

        locks.append(lock_status)

    return jsonify(locks)









 

















if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = False
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')


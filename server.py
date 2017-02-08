"""Collaborative Curated Playlist."""

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

from model import User, Group, UserGroup, Playlist, Song, PlaylistSong, Vote
from model import connect_to_db, db

from helper_functions import initialize_auth, create_playlist


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
        user_object = User.query.filter_by(email=username).one()
        flash('User already exists, please sign in or use another email')
        return redirect('/register')

    except sqlalchemy.orm.exc.NoResultFound:
        # flash('user created: %s') % (username)
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


@app.route('/create-playlist', methods=['POST'])
def create_playlist_form():

    name = request.form.get('playlist-name')

    # playlist_object = User(name=name)

    create_playlist(name)

    # # We need to add to the session or it won't ever be stored
    # db.session.add(playlist_object)

    # # Once we're done, we should commit our work
    # db.session.commit()

    return redirect("/")






if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')


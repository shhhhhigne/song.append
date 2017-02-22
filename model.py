"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of curated playlist app"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    
    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<User user_id=%s email=%s password=%s>" % (self.user_id, self.email, self.password)

class Group(db.Model):
    """Groups in curated playlist app"""

    __tablename__ = 'groups'

    group_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    group_name = db.Column(db.String(64), nullable=False)\

    # This is the group owner
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    # Im not sure how I'd impliment this
    group_cover_art = db.Column(db.String(300), nullable=True)

    user = db.relationship("User", backref=db.backref("groups", order_by=group_id))

    
    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<Group group_id=%s group_name=%s>" % (self.group_id, self.group_name)


class UserGroup(db.Model):
    """User/Group relationship in curated playlist app."""

    __tablename__ = "user_group"

    ug_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.group_id"), nullable=False)
    in_group = db.Column(db.Boolean, default=False, nullable=False)

    user = db.relationship("User", backref=db.backref("user_group", order_by=ug_id))
    group = db.relationship("Group", backref=db.backref("user_group", order_by=ug_id))

    def __repr__(self):
        """Provide helpful representation when printed"""

        s = "<UserGroup ug_id=%s user_id=%s group_id=%s>"
        return s % (self.ug_id, self.user_id, self.group_id)


class Playlist(db.Model):
    """Playlist in curated playlist app."""

    __tablename__ = "playlists"

    playlist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    playlist_name = db.Column(db.String(64), nullable=False)
    playlist_cover_art = db.Column(db.String(300), nullable=True)

    # Will be used when user first loads playlist and when they add/req songs
    # The user_id will be hard coded into
    # playlist_url = db.Column(db.String(300), nullable=False, unique=True)

    # This will contain only the active songs so when the user wants to listen to
    # the full playlist they can on spotify )ie not only 30 sec previews
    playlist_spotify_id = db.Column(db.String(300), nullable=False, unique=True)
    #This will contain only the requested songs incase the user wishes to listen to 
    # the playlist of the requested songs
    playlist_spotify_id_req = db.Column(db.String(300), nullable=False, unique=True)
    # This will be the full playlist (ie contain all songs ever added and requested)
    # if a user wishes to listen to the full list
    playlist_spotify_id_full = db.Column(db.String(300), nullable=False, unique=True)

    num_votes_add = db.Column(db.Integer, nullable=False, default=3) 
    num_votes_del = db.Column(db.Integer, nullable=False, default=3) 

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.group_id"), nullable=True)

    user = db.relationship("User", backref=db.backref("playlists", order_by=playlist_id))
    group = db.relationship("Group", backref=db.backref("playlists", order_by=playlist_id))

    def __repr__(self):
        """Provide helpful representation when printed"""

        s = "<Playlist playlist_id=%s playlist_name=%s user_id=%s group_id=%s>"
        return s % (self.playlist_id, self.playlist_name, self.user_id, self.group_id)


class Album(db.Model):

    __tablename__ = 'albums'

    album_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    album_name = db.Column(db.String(200), nullable=False)

    album_spotify_id = db.Column(db.String(300), nullable=False, unique=True)
    album_spotify_url = db.Column(db.String(300), nullable=False, unique=True)

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<Album album_id=%s album_name=%s>" % (self.album_name, self.album_id)


class Song(db.Model):
    """Songs in curated playlist app"""

    __tablename__ = 'songs'

    song_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    song_name = db.Column(db.String(200), nullable=False)

    album_id = db.Column(db.Integer, db.ForeignKey("albums.album_id"), nullable=False)

    # So I can check if the song is already in my database
    song_spotify_id = db.Column(db.String(300), nullable=False, unique=True)
    # Used to find the 30 second preview of the song
    preview_url = db.Column(db.String(300), nullable=False)
    # Used to find the song in the spotify database
    spotify_url = db.Column(db.String(300), nullable=False, unique=True)

    # Used to add tracks to playlist
    # song_spotify_uri = db.Column(db.String(300), nullable=False, unique=True)

    album = db.relationship("Album", backref=db.backref("songs", order_by=song_id))

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<Song song_id=%s song_name=%s>" % (self.song_name, self.song_id)


class Artist(db.Model):
    """Artists in curated playlist app"""

    __tablename__ = 'artists'

    artist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    artist_name = db.Column(db.String(300), nullable=False)

    artist_spotify_id = db.Column(db.String(300), nullable=False, unique=True)
    artist_spotify_url = db.Column(db.String(300), nullable=False, unique=True)

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<Artist artist_id=%s artist_name=%s>" % (self.artist_name, self.artist_id)


class SongArtist(db.Model):
    """Song/Artist relationship in curated playlist app."""

    __tablename__ = "song_artist"

    sartist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    song_id = db.Column(db.Integer, db.ForeignKey("songs.song_id"), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.artist_id"), nullable=False)

    song = db.relationship("Song", backref=db.backref("song_artist", order_by=sartist_id))
    artist = db.relationship("Artist", backref=db.backref("song_artist", order_by=sartist_id))

    def __repr__(self):
        """Provide helpful representation when printed"""

        s = "<SongArtist sartist_id=%s song_id=%s artist_id=%s>"
        return s % (self.sartist_id, self.song_id, self.artist_id)


class PlaylistSong(db.Model):
    """Playlist/Song relationship in curated playlist app."""

    __tablename__ = "playlist_song"

    ps_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    playlist_id = db.Column(db.Integer, db.ForeignKey("playlists.playlist_id"), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey("songs.song_id"), nullable=False)

    # status can be (active, requested, or deleted) -- if never added to playlist not issue
    status = db.Column(db.String(10), nullable=False) 

    # the index in the playlist
    index = db.Column(db.Integer, nullable=False) 

    playlist = db.relationship("Playlist", backref=db.backref("playlist_song", order_by=ps_id))
    song = db.relationship("Song", backref=db.backref("playlist_song", order_by=ps_id))

    def __repr__(self):
        """Provide helpful representation when printed"""

        s = "<PlaylistSong ps_id=%s playlist_id=%s song_id=%s status=%s index=%s>"
        return s % (self.ps_id, self.playlist_id, self.song_id, self.status, self.index)


class Vote(db.Model):
    """Votes on a song in a playlist in curated playlist app."""

    __tablename__ = "votes"

    vote_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    value = db.Column(db.Integer, nullable=False)

    ps_id = db.Column(db.Integer, db.ForeignKey("playlist_song.ps_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    playlist_song = db.relationship("PlaylistSong", backref=db.backref("votes", order_by=vote_id))
    user = db.relationship("User", backref=db.backref("votes", order_by=vote_id))

    def __repr__(self):
        """Provide helpful representation when printed"""

        s = "<Vote vote_id=%s ps_id=%s user_id=%s value=%s>"
        return s % (self.vote_id, self.ps_id, self.user_id, self.value)


##############################################################################
# Helper functions
import sys
import spotipy
import spotipy.util as util

def pull_all_playlists():
    pass

    # scope ='user-library-read'

    # username = 'ZZZeldaH'

    # token = util.prompt_for_user_token(username, scope)

    # if token:
    #     sp = spotify.Spotify(auth=token)
    #     results = sp.user_playlists()
    
    # return results





def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///collabplaylists'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)

    db.create_all()
    print "Connected to DB."














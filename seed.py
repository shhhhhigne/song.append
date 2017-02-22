from model import Album, Song, Artist, SongArtist
from model import User, Group, UserGroup, Playlist, PlaylistSong, Vote
from model import connect_to_db, db

from server import app, connect_to_db

connect_to_db(app)

User.query.delete()
Group.query.delete()
UserGroup.query.delete()

user1 = User(username='signeh',
             email='signe@email.com',
             fname='Signe',
             lname='Henderson',
             password='pass')

user2 = User(username='zoegs',
             email='zoe@email.com',
             fname='Zoe',
             lname='Gotch-Strain',
             password='pass')

user3 = User(username='franziv',
             email='franzi@email.com',
             fname='Franzi',
             lname='V',
             password='pass')

user4 = User(username='jessa',
             email='jess@email.com',
             fname='Jess',
             lname='Appelbaum',
             password='pass')

db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.add(user4)

db.session.commit()

group1 = Group(group_name='Crew',
               user_id=1)

db.session.add(group1)

db.session.commit()

user_g1 = UserGroup(user_id=1,
                    group_id=1,
                    in_group=True)

user_g2 = UserGroup(user_id=2,
                    group_id=1,
                    in_group=True)

user_g3 = UserGroup(user_id=3,
                    group_id=1,
                    in_group=True)

user_g4 = UserGroup(user_id=4,
                    group_id=1,
                    in_group=False)


db.session.add(user_g1)
db.session.add(user_g2)
db.session.add(user_g3)
db.session.add(user_g4)


db.session.commit()

# playlist1 = Playlist()

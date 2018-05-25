from flask_script import Manager
from songbase import app, db, Artist, Song

manager = Manager(app)

@manager.command
def deploy():
    db.drop_all()
    db.create_all()
    GNR = Artist(name='Guns and Roses', about='Guns and Roses is my favorite band')
    PinkFloyd = Artist(name='Pink Floyd', about='Pink Floyd is one of the top rock bands.')
    song1 = Song(name='Sweet Child o Mine', year=1987, lyrics="She's got a smile", artist=GNR)
    song2 = Song(name='Money', year=1973, lyrics="Money, Get away", artist=PinkFloyd)
    db.session.add(GNR)
    db.session.add(PinkFloyd)
    db.session.add(song1)
    db.session.add(song2)
    db.session.commit()


if __name__ == "__main__":
    manager.run()

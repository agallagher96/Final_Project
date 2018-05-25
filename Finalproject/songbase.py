import os
from flask import Flask, session, render_template, request, flash, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess secure key'

# setup SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
db = SQLAlchemy(app)


# define database tables
class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    about = db.Column(db.Text)
    songs = db.relationship('Song', backref='artist', cascade="delete")


class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    year = db.Column(db.Integer)
    lyrics = db.Column(db.Text)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/artists')
def show_all_artists():
    artists = Artist.query.all()
    return render_template('artist-all.html', artists=artists)


@app.route('/artist/add', methods=['GET', 'POST'])
def add_artists():
    if request.method == 'GET':
        return render_template('artist-add.html')
    if request.method == 'POST':
        name = request.form['name']
        about = request.form['about']
        artist = Artist(name=name, about=about)
        db.session.add(artist)
        db.session.commit()
        return redirect(url_for('show_all_artists'))


@app.route('/api/artist/add', methods=['POST'])
def add_ajax_artists():
    name = request.form['name']
    about = request.form['about']

    artist = Artist(name=name, about=about)
    db.session.add(artist)
    db.session.commit()
    flash('Artist Inserted', 'Artist successfully inserted')
    return jsonify({"id": str(artist.id), "name": artist.name})


@app.route('/artist/edit/<int:id>', methods=['GET', 'POST'])
def edit_artist(id):
    artist = Artist.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('artist-edit.html', artist=artist)
    if request.method == 'POST':
        artist.name = request.form['name']
        artist.about = request.form['about']
        db.session.commit()
        return redirect(url_for('show_all_artists'))


@app.route('/artist/delete/<int:id>', methods=['GET', 'POST'])
def delete_artist(id):
    artist = Artist.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('artist-delete.html', artist=artist)
    if request.method == 'POST':

        db.session.delete(artist)
        db.session.commit()
        return redirect(url_for('show_all_artists'))


@app.route('/api/artist/<int:id>', methods=['DELETE'])
def delete_ajax_artist(id):
    artist = Artist.query.get_or_404(id)
    db.session.delete(artist)
    db.session.commit()
    return jsonify({"id": str(artist.id), "name": artist.name})


@app.route('/songs')
def show_all_songs():
    songs = Song.query.all()
    return render_template('song-all.html', songs=songs)


@app.route('/song/add', methods=['GET', 'POST'])
def add_songs():
    if request.method == 'GET':
        artists = Artist.query.all()
        return render_template('song-add.html', artists=artists)
    if request.method == 'POST':
        name = request.form['name']
        year = request.form['year']
        lyrics = request.form['lyrics']
        artist_name = request.form['artist']
        artist = Artist.query.filter_by(name=artist_name).first()
        song = Song(name=name, year=year, lyrics=lyrics, artist=artist)
        db.session.add(song)
        db.session.commit()
        return redirect(url_for('show_all_songs'))


@app.route('/song/edit/<int:id>', methods=['GET', 'POST'])
def edit_song(id):
    song = Song.query.filter_by(id=id).first()
    artists = Artist.query.all()
    if request.method == 'GET':
        return render_template('song-edit.html', song=song, artists=artists)
    if request.method == 'POST':

        song.name = request.form['name']
        song.year = request.form['year']
        song.lyrics = request.form['lyrics']
        artist_name = request.form['artist']
        artist = Artist.query.filter_by(name=artist_name).first()
        song.artist = artist

        db.session.commit()
        return redirect(url_for('show_all_songs'))


@app.route('/song/delete/<int:id>', methods=['GET', 'POST'])
def delete_song(id):
    song = Song.query.filter_by(id=id).first()
    artists = Artist.query.all()
    if request.method == 'GET':
        return render_template('song-delete.html', song=song, artists=artists)
    if request.method == 'POST':
        db.session.delete(song)
        db.session.commit()
        return redirect(url_for('show_all_songs'))


@app.route('/api/song/<int:id>', methods=['DELETE'])
def delete_ajax_song(id):
    song = Song.query.get_or_404(id)
    db.session.delete(song)
    db.session.commit()
    return jsonify({"id": str(song.id), "name": song.name})


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/users')
def show_all_users():
    return render_template('user-all.html')


@app.route('/form-demo', methods=['GET', 'POST'])
def form_demo():
    if request.method == 'GET':
        first_name = request.args.get('first_name')
        if first_name:
            return render_template('form-demo.html', first_name=first_name)
        else:
            return render_template('form-demo.html', first_name=session.get('first_name'))
    if request.method == 'POST':
        session['first_name'] = request.form['first_name']
        return redirect(url_for('form_demo'))


@app.route('/user/<string:name>/')
def get_user_name(name):
    return render_template('user.html', name=name)


@app.route('/song/<int:id>/')
def get_song_id(id):
    return "This song: %s Song's id: %d" % ('administrator', id)


if __name__ == '__main__':

    app.run()
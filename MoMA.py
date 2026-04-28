from flask import Flask, render_template, request
from models import db, Art, Artist
import os
from flask import redirect, url_for
app = Flask(__name__)
app.secret_key = 'kunci_rahasia_moma'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'moma.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
@app.route('/add-art', methods=['GET', 'POST'])
def add_art():
    if request.method == 'POST':
        name = request.form['name']
        artist_id = request.form['artist_id']

        new_art = Art(name=name, artist_id=artist_id)
        db.session.add(new_art)
        db.session.commit()

    return render_template('add_art.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/art')
def art():
    all_art = Art.query.all()
    return render_template('art.html', all_art=all_art)

if __name__ == "__main__":
    app.run(debug=True)


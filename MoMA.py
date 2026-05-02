from flask import Flask, render_template, request, redirect, url_for
from models import db, Art, Artist
import os

app = Flask(__name__)
app.secret_key = 'kunci_rahasia_moma'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'moma.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# --- ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/art')
def art():
    all_art = Art.query.all()
    # Di sini kita kirim 'all_art', jadi di art.html panggilnya 'all_art' juga
    return render_template('art.html', all_art=all_art)

@app.route('/add-art', methods=['GET', 'POST'])
def add_art():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        # Ambil Nama Artist yang diketik dari form
        artist_name = request.form.get('artist_name')

        # Cari artist di database berdasarkan nama tersebut
        artist = Artist.query.filter_by(name=artist_name).first()

        if artist:
            new_art = Art(name=name, description=description, artist_id=artist.id)
            db.session.add(new_art)
            db.session.commit()
            return redirect(url_for('art'))
        else:
            # Jika nama yang diketik tidak ada di database
            return "Artist tidak ditemukan! Pastikan nama sesuai dengan database.", 400

    artists = Artist.query.all() 
    return render_template('add_art.html', artists=artists)

@app.route('/update-art/<int:id>', methods=['GET', 'POST'])
def update_art(id):
    art_item = Art.query.get_or_404(id) # Harus menjorok 1 tab/4 spasi
    
    if request.method == 'POST': # Menjorok 1 tab
        # Semua di bawah ini harus menjorok 2 tab
        art_item.name = request.form['name']
        art_item.description = request.form.get('description', '')
        
        artist_name = request.form.get('artist_name')
        artist = Artist.query.filter_by(name=artist_name).first()
        
        if artist: # Menjorok 2 tab
            # Menjorok 3 tab
            art_item.artist_id = artist.id
            db.session.commit()
            return redirect(url_for('art'))
        else:
            return "Artist tidak ditemukan!", 400
        
    # Baris di bawah ini harus sejajar dengan "if request.method" (1 tab)
    artists = Artist.query.all()
    return render_template('update_art.html', art=art_item, artists=artists)

@app.route('/delete-art/<int:id>')
def delete_art(id):
    art_item = Art.query.get_or_404(id)
    db.session.delete(art_item)
    db.session.commit()
    return redirect(url_for('art'))

# --- INI HARUS DI PALING BAWAH ---
if __name__ == "__main__":
    app.run(debug=True)
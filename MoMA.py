from flask import Flask, render_template, request, redirect, url_for
from models import db, Art, Artist
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'kunci_rahasia_moma'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'moma.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Konfigurasi Folder Upload
UPLOAD_FOLDER = os.path.join('static', 'image', 'arts')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Pastikan folder arts sudah ada
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    return render_template('art.html', all_art=all_art)

@app.route('/add-art', methods=['GET', 'POST'])
def add_art():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        artist_name = request.form.get('artist_name')
        
        # Logika Upload Gambar
        image_url = '' 
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_url = os.path.join('image', 'arts', filename).replace('\\','/')

        artist = Artist.query.filter_by(name=artist_name).first()

        if artist:
            new_art = Art(name=name, description=description, image_url=image_url, artist_id=artist.id)
            db.session.add(new_art)
            db.session.commit()
            return redirect(url_for('art'))
        else:
            return "Artist tidak ditemukan! Pastikan nama sesuai dengan database.", 400

    artists = Artist.query.all() 
    return render_template('add_art.html', artists=artists)

@app.route('/update-art/<int:id>', methods=['GET', 'POST'])
def update_art(id):
    art_item = Art.query.get_or_404(id)
    
    if request.method == 'POST':
        art_item.name = request.form['name']
        art_item.description = request.form.get('description', '')
        
        # Logika Update Gambar (Opsional)
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                art_item.image_url = os.path.join('image', 'arts', filename).replace('\\','/')
        
        artist_name = request.form.get('artist_name')
        artist = Artist.query.filter_by(name=artist_name).first()
        
        if artist:
            art_item.artist_id = artist.id
            db.session.commit()
            return redirect(url_for('art'))
        else:
            return "Artist tidak ditemukan!", 400
        
    artists = Artist.query.all()
    return render_template('update_art.html', art=art_item, artists=artists)

@app.route('/delete-art/<int:id>')
def delete_art(id):
    art_item = Art.query.get_or_404(id)
    # Hapus file gambar dari folder jika ada (opsional tapi bagus biar nggak nyampah)
    if art_item.image_url:
        path_to_delete = os.path.join('static', art_item.image_url)
        if os.path.exists(path_to_delete):
            os.remove(path_to_delete)
            
    db.session.delete(art_item)
    db.session.commit()
    return redirect(url_for('art'))

if __name__ == "__main__":
    app.run(debug=True)
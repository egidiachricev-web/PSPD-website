from flask import Flask, render_template
from models import db, Art, Artist 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moma.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inisialisasi DB
db.init_app(app)

# --- ROUTES ---

@app.route('/')
def home():
    return render_template('index.html') 

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/art')
def art():
    # Mengambil semua data karya seni dari database
    all_art = Art.query.all() 
    return render_template('art.html', all_art=all_art)

if __name__ == '__main__':
    app.run(debug=True)
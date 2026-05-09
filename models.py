from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from flask_login import UserMixin 

db = SQLAlchemy()

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # Relasi agar kita bisa memanggil artist.art untuk melihat semua karyanya
    art = db.relationship('Art', backref='artist', lazy=True)

class Art(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    # TAMBAHKAN BARIS INI: Untuk menyimpan nama file gambar
    image_url = db.Column(db.String(255), nullable=True)
    
    # Foreign Key yang menghubungkan ke tabel Artist
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Key yang menghubungkan ke tabel Art
    art_id = db.Column(db.Integer, db.ForeignKey('art.id'), nullable=False)
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')  # 'admin' atau 'user'
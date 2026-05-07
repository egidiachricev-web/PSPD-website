from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

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
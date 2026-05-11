from MoMA import app 
from models import db, Artist, Art

from werkzeug.security import generate_password_hash
from models import User 

def isi_database():
    with app.app_context():
        print("Membuat akun admin default...")
        User.query.delete() # Hapus user lama jika mau reset
        admin_password = generate_password_hash("admin123", method='pbkdf2:sha256')
        admin_user = User(username="admin", password=admin_password, role="admin")
        db.session.add(admin_user)
        db.session.commit()
        print("Akun Admin berhasil dibuat! (Username: admin | Password: admin123)")
        print("Sedang membersihkan data lama...")
        # Menghapus data art dan artist agar tidak double
        Art.query.delete()
        Artist.query.delete()
        
        db.session.commit()

        # Daftar data yang rapi dan namanya tidak kepanjangan
        data_art = [
            {"artist": "Claude Monet", "art": "Water Lilies", "desc": "Pemandangan kolam yang tenang."},
            {"artist": "Claude Monet", "art": "Woman with Parasol", "desc": "Karya impresionisme ikonik."},
            {"artist": "Ellina Kevorkian", "art": "Last Night", "desc": "Ekspresi seni kontemporer."},
            {"artist": "Roy Lichtenstein", "art": "Look Mickey", "desc": "Gaya pop art yang cerah."},
            {"artist": "Lisa Adams", "art": "Nature Study", "desc": "Detail alam yang artistik."}
        ]

        print("Sedang memasukkan data baru yang lebih rapi...")
        for item in data_art:
            # Tambah Artist
            artist = Artist.query.filter_by(name=item["artist"]).first()
            if not artist:
                artist = Artist(name=item["artist"])
                db.session.add(artist)
                db.session.commit() 
            
            # Tambah Artwork
            new_artwork = Art(
                name=item["art"], 
                description=item["desc"], 
                artist_id=artist.id
            )
            db.session.add(new_artwork)
        
        db.session.commit()
        print("Database SELESAI di-update! Sekarang sudah rapi dan tidak double.")

if __name__ == "__main__":
    isi_database()
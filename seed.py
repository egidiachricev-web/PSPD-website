from MoMA import app # Pastikan ini sesuai nama file app kamu (MoMA.py atau app.py)
from models import db, Artist, Art

def isi_database():
    with app.app_context():
        # Opsional: Hapus data lama biar gak double kalau dijalankan lagi
        Art.query.delete()
        Artist.query.delete()

        data_art = [
            {"artist": "Claude Monet", "art": "The Waterlilies: The Clouds", "desc": "Lukisan pemandangan air yang legendaris."},
            {"artist": "Claude Monet", "art": "Woman with a Parasol", "desc": "Karya impresionisme yang menangkap cahaya matahari."},
            {"artist": "Claude Monet", "art": "Blue Water Lilies", "desc": "Koleksi bunga teratai biru yang ikonik."},
            {"artist": "Yuri Krotov", "art": "Young Lady Reading", "desc": "Gambaran santai seorang wanita yang sedang membaca."},
            {"artist": "Mary Cassatt", "art": "Lillacs in a Window", "desc": "Sentuhan bunga lilac di jendela yang artistik."},
        ]

        for item in data_art:
            # 1. Cek atau Tambah Artist
            artist = Artist.query.filter_by(name=item["artist"]).first()
            if not artist:
                artist = Artist(name=item["artist"])
                db.session.add(artist)
                db.session.commit() # Simpan artist biar dapet ID
            
            # 2. Cek atau Tambah Art (Tambahkan deskripsi di sini)
            if not Art.query.filter_by(name=item["art"]).first():
                new_artwork = Art(
                    name=item["art"], 
                    description=item["desc"], # Penting agar tidak NULL
                    artist_id=artist.id
                )
                db.session.add(new_artwork)
        
        # 3. COMMIT FINAL (Paling Penting!)
        db.session.commit()
        print("Database berhasil diisi dengan rapi!")

if __name__ == "__main__":
    isi_database()
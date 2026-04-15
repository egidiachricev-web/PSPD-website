from MoMA import app
from models import db, Artist, Art

def isi_database():
    with app.app_context():
        data_art = [
            {"artist": "Joan Snyder", "art": "My August"},
            {"artist": "Ian Cheng", "art": "3FACE"},
            {"artist": "Louis Fratino", "art": "Fanciullo"},
            {"artist": "Michael Armitage", "art": "Head of Koitalel"},
            {"artist": "Vaginal Davis", "art": "Xochiquetzal, The Precious Feather Flower Goddess of Beauty and Art"}
        ]

        for item in data_art:
            artist = Artist.query.filter_by(name=item["artist"]).first()
            if not artist:
                artist = Artist(name=item["artist"])
                db.session.add(artist)
                db.session.commit()
            
            if not Art.query.filter_by(name=item["art"]).first():
                arts = Art(name=item["art"], artist_id=artist.id)
                db.session.add(arts)

if __name__ == "__main__":
    isi_database()

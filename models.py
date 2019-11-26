from app import db


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    website = db.Column(db.String(120))
    genres = db.Column(db.String())
    shows = db.relationship('Shows', backref='Venue', lazy=True)

    def identity(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def location_and_identity(self):
        return {
            "city": self.city,
            "state": self.state,
            "venues": [self.identity()]
        }

    def summarise(self):
        return {
            "id": self.id,
            "name": self.name,
            "genres": self.genres.split(","),
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "phone": self.phone,
            "website": self.website,
            "facebook_link": self.facebook_link,
            "seeking_talent": self.seeking_talent,
            "seeking_description": self.seeking_description,
            "image_link": self.image_link
        }

    def __repr__(self):
        return f'<Venue: {self.name}>'


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Shows', backref='Artist', lazy=True)

    def identity(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def summarise(self):
        return {
            "id": self.id,
            "name": self.name,
            "genres": self.genres.split(","),
            "city": self.city,
            "state": self.state,
            "phone": self.phone,
            "website": self.website,
            "facebook_link": self.facebook_link,
            "seeking_venue": self.seeking_venue,
            "seeking_description": self.seeking_description,
            "image_link": self.image_link
        }

    def __repr__(self):
        return f'<Artist: {self.name}>'


class Shows(db.Model):
    __tablename__ = 'Shows'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'),
                          nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'),
                         nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    def with_artist(self):
        return {
            "artist_id": self.Artist.id,
            "artist_name": self.Artist.name,
            "artist_image_link": self.Artist.image_link,
            "start_time": str(self.start_time)
        }

    def with_venue(self):
        return {
            "venue_id": self.Venue.id,
            "venue_name": self.Venue.name,
            "venue_image_link": self.Venue.image_link,
            "start_time": str(self.start_time)
        }

    def with_artist_and_venue(self):
        return {
            "artist_id": self.Artist.id,
            "artist_name": self.Artist.name,
            "artist_image_link": self.Artist.image_link,
            "venue_id": self.Venue.id,
            "venue_name": self.Venue.name,
            "start_time": str(self.start_time)
        }

    def __repr__(self):
        return f'<Show: {self.id}>'

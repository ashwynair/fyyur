from app import app, db
from models import Venue, Artist, Shows
from forms import VenueForm, ArtistForm, ShowForm
from flask import render_template, request, Response, flash, redirect, url_for
from sqlalchemy import func
from datetime import datetime
from sys import exc_info

# -------------------------------------------------------------------------- #
# Controllers.
# -------------------------------------------------------------------------- #


@app.route('/')
def index():
    return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------


@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    # num_shows should be aggregated based on number of upcoming
    # shows per venue.
    venue_list = Venue.query.all()
    data = []
    for v in venue_list:
        index = next((i for i, value in enumerate(data)
                      if value["city"] == v.city), -1)
        if index < 0:
            data.append({
                "city": v.city,
                "state": v.state,
                "venues": [{
                    "id": v.id,
                    "name": v.name
                }]
            })
        else:
            data[index]["venues"].append({
                "id": v.id,
                "name": v.name
            })

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    '''Searching venues from venue page'''

    search_term = request.form["search_term"]
    search_lc = search_term.lower()
    searched_venues = Venue.query.filter(
        func.lower(Venue.name).like('%{}%'.format(search_lc))).all()
    response = {
        "count": len(searched_venues),
        "data": []
    }
    for venue in searched_venues:
        response["data"].append({
            "id": venue.id,
            "name": venue.name,
        })

    return render_template('pages/search_venues.html', results=response,
                           search_term=search_term)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    venue = Venue.query.get(venue_id)
    shows = Shows.query.filter_by(venue_id=venue_id)

    past_shows = [{
        "artist_id": show.Artist.id,
        "artist_name": show.Artist.name,
        "artist_image_link": show.Artist.image_link,
        "start_time": str(show.start_time)}
        for show in shows
        if show.start_time < datetime.now()]

    upcoming_shows = [{
        "artist_id": show.Artist.id,
        "artist_name": show.Artist.name,
        "artist_image_link": show.Artist.image_link,
        "start_time": str(show.start_time)}
        for show in shows
        if show.start_time >= datetime.now()]

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres.split(","),
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
    }

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

    data = {}
    firstgenre = True
    for fieldname, value in request.form.items(multi=True):
        if fieldname == "genres":
            if firstgenre:
                data["genres"] = str(value)
                firstgenre = False
            else:
                data["genres"] = "," + str(value)
        else:
            data[fieldname] = value
    error = False
    try:
        venue = Venue(
            name=data["name"],
            city=data["city"],
            state=data["state"],
            address=data["address"],
            phone=data["phone"],
            genres=data["genres"],
            facebook_link=data["facebook_link"]
        )
        db.session.add(venue)
        db.session.commit()
    except Exception:
        error = True
        db.session.rollback()
        print(exc_info())
    finally:
        db.session.close()
        if error:
            flash('An error occurred. Venue ' + data['name'] + 'could not be\
                listed.')
        else:
            flash('Venue ' + request.form['name'] + ' was successfully\
                listed!')

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit
    # could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue
    # Page, have it so that
    # clicking that button delete it from the db then redirect the user to
    # the homepage
    return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    artists = Artist.query.order_by('name').all()
    data = []
    for artist in artists:
        data.append({
            "id": artist.id,
            "name": artist.name
        })

    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form["search_term"]
    search_lc = search_term.lower()
    searched_artists = Artist.query.filter(
        func.lower(Artist.name).like('%{}%'.format(search_lc))).all()
    response = {
        "count": len(searched_artists),
        "data": []
    }
    for artist in searched_artists:
        response["data"].append({
            "id": artist.id,
            "name": artist.name,
        })

    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using
    # venue_id
    artist = Artist.query.get(artist_id)
    shows = Shows.query.filter_by(artist_id=artist_id)

    past_shows = [{
        "venue_id": show.Venue.id,
        "venue_name": show.Venue.name,
        "venue_image_link": show.Venue.image_link,
        "start_time": str(show.start_time)}
        for show in shows
        if show.start_time < datetime.now()]

    upcoming_shows = [{
        "venue_id": show.Venue.id,
        "venue_name": show.Venue.name,
        "venue_image_link": show.Venue.image_link,
        "start_time": str(show.start_time)}
        for show in shows
        if show.start_time >= datetime.now()]

    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres.split(","),
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
    }

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm(obj=artist)
    form.genres.data = artist.genres.split(",")
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    data = {}
    firstgenre = True
    for fieldname, value in request.form.items(multi=True):
        if fieldname == "genres":
            if firstgenre:
                data["genres"] = str(value)
                firstgenre = False
            else:
                data["genres"] += "," + str(value)
        else:
            data[fieldname] = value
    artist = Artist.query.get(artist_id)
    error = False
    try:
        artist.name = data["name"]
        artist.city = data["city"]
        artist.state = data["state"]
        artist.phone = data["phone"]
        artist.genres = data["genres"]
        artist.facebook_link = data["facebook_link"]
        db.session.commit()
    except Exception:
        error = True
        db.session.rollback()
        print(exc_info())
    finally:
        db.session.close()
        if error:
            flash('An error occurred. Artist ' + data['name'] + 'could not be\
                updated.')
        else:
            flash('Artist ' + data['name'] + ' was successfully\
                updated!')

    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm(obj=venue)
    form.genres.data = venue.genres.split(",")
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    data = {}
    firstgenre = True
    for fieldname, value in request.form.items(multi=True):
        if fieldname == "genres":
            if firstgenre:
                data["genres"] = str(value)
                firstgenre = False
            else:
                data["genres"] += "," + str(value)
        else:
            data[fieldname] = value
    venue = Venue.query.get(venue_id)
    error = False
    try:
        venue.name = data["name"]
        venue.city = data["city"]
        venue.state = data["state"]
        venue.phone = data["phone"]
        venue.genres = data["genres"]
        venue.facebook_link = data["facebook_link"]
        db.session.commit()
    except Exception:
        error = True
        db.session.rollback()
        print(exc_info())
    finally:
        db.session.close()
        if error:
            flash('An error occurred. Venue ' + data['name'] + 'could not be\
                updated.')
        else:
            flash('Venue ' + data['name'] + ' was successfully\
                updated!')

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be
    # listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------


@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows
    # per venue.
    data = [{
        "venue_id": 1,
        "venue_name": "The Musical Hop",
        "artist_id": 4,
        "artist_name": "Guns N Petals",
        "artist_image_link": "https://images.unsplash.com/photo-1549213783-\
            8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=form\
                at&fit=crop&w=300&q=80",
        "start_time": "2019-05-21T21:30:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 5,
        "artist_name": "Matt Quevedo",
        "artist_image_link": "https://images.unsplash.com/photo-149522315380\
            7-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=for\
                mat&fit=crop&w=334&q=80",
        "start_time": "2019-06-15T23:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f\
            9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format\
                &fit=crop&w=794&q=80",
        "start_time": "2035-04-01T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f\
            9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format\
                &fit=crop&w=794&q=80",
        "start_time": "2035-04-08T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f\
            9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format\
                &fit=crop&w=794&q=80",
        "start_time": "2035-04-15T20:00:00.000Z"
    }]
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing
    # form
    # TODO: insert form data as a new Show record in the db, instead

    # on successful db insert, flash success
    flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')

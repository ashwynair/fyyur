from app import app, db
from models import Venue, Artist, Shows
from forms import VenueForm, ArtistForm, ShowForm
from flask import render_template, request, flash, redirect, url_for, jsonify
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
    '''Display all venues to the end-user'''
    all_venues = Venue.query.all()
    data = []
    # Add venue to an existing city, or a new city
    for v in all_venues:
        index = next((i for i, value in enumerate(data)
                      if value["city"] == v.city), -1)
        if index < 0:
            data.append(v.location_and_identity())
        else:
            data[index]["venues"].append(v.identity())

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    '''Searching venues from venue page'''
    search_term = request.form["search_term"].lower()
    # Query with WHERE and LIKE clause and comparing in lowercase
    venues = Venue.query.filter(
        func.lower(Venue.name).like('%{}%'.format(search_term.lower()))
    ).all()
    response = {
        "count": len(venues),
        "data": []
    }

    for venue in venues:
        response["data"].append(venue.identity())

    return render_template('pages/search_venues.html', results=response,
                           search_term=search_term)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

    shows = Shows.query.filter_by(venue_id=venue_id)

    # Determining schedule
    past_shows = []
    upcoming_shows = []
    for show in shows:
        if show.start_time < datetime.now():
            past_shows.append(show.with_artist())
        else:
            upcoming_shows.append(show.with_artist())
    schedule = {
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
    }
    # Appending schedule to summary of venue
    data = Venue.query.get(venue_id).summarise()
    data.update(schedule)
    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm(request.form)
    if form.validate_on_submit():
        error = False
        try:
            venue = Venue(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                address=form.address.data,
                phone=form.phone.data,
                genres=",".join(form.genres.data),
                facebook_link=form.facebook_link.data
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
                flash('An error occurred. Venue ' + form.name.data + 'could\
                      not be listed.')
            else:
                flash('Venue ' + form.name.data + ' was successfully\
                    listed!')
            return render_template('pages/home.html')
    else:
        flash('Please ensure all details provided are valid')
        print(form.errors)
        return render_template('forms/new_venue.html', form=form)


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    error = False
    try:
        deleted = request.get_json()['id']
        print(deleted)
        venue = Venue.query.get(venue_id)
        print(venue)
        name = venue.name
        db.session.delete(venue)
        db.session.commit
    except Exception:
        error = True
        db.session.rollback()
        print(exc_info())
    finally:
        db.session.close()
        if error:
            flash('An error occured. Venue ' + name + ' could not be deleted.\
                  Please try again later.')
        else:
            flash('Artist successfully deleted!')
        return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    artists = Artist.query.order_by('name').all()
    data = [artist.identity() for artist in artists]
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form["search_term"]
    # Query with WHERE and LIKE clause and comparing in lowercase
    artists = Artist.query.filter(
        func.lower(Artist.name).like('%{}%'.format(search_term.lower()))).all()
    response = {
        "count": len(artists),
        "data": []
    }

    for artist in artists:
        response["data"].append(artist.identity())

    return render_template('pages/search_artists.html', results=response,
                           search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    shows = Shows.query.filter_by(artist_id=artist_id)

    # Determining schedule
    past_shows = []
    upcoming_shows = []
    for show in shows:
        if show.start_time < datetime.now():
            past_shows.append(show.with_venue())
        else:
            upcoming_shows.append(show.with_venue())
    schedule = {
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
    }
    # Appending schedule to summary of venue
    data = Artist.query.get(artist_id).summarise()
    data.update(schedule)

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
    form = ArtistForm(request.form)
    artist = Artist.query.get(artist_id)
    if form.validate_on_submit():
        error = False
        try:
            artist.name = form.name.data
            artist.city = form.city.data
            artist.state = form.state.data
            artist.phone = form.phone.data
            artist.genres = ",".join(form.genres.data)
            artist.facebook_link = form.facebook_link.data
            db.session.commit()
        except Exception:
            error = True
            db.session.rollback()
            print(exc_info())
        finally:
            db.session.close()
            if error:
                flash('An error occurred. Artist ' + str(form.name.data) +
                      'could not be updated.')
            else:
                flash('Artist ' + str(form.name.data) + ' was successfully\
                    updated!')

        return redirect(url_for('show_artist', artist_id=artist_id))
    else:
        flash('Please ensure all details are valid')
        return render_template('forms/edit_artist.html',
                               form=form, artist=artist)


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm(obj=venue)
    form.genres.data = venue.genres.split(",")
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    form = VenueForm(request.form)
    venue = Venue.query.get(venue_id)
    if form.validate_on_submit():
        error = False
        try:
            venue.name = form.name.data
            venue.city = form.city.data
            venue.address = form.address.data
            venue.state = form.state.data
            venue.phone = form.phone.data
            venue.genres = ",".join(form.genres.data)
            venue.facebook_link = form.facebook_link.data
            db.session.commit()
        except Exception:
            error = True
            db.session.rollback()
            print(exc_info())
        finally:
            db.session.close()
            if error:
                flash('An error occurred. Venue ' + str(form.name.data) +
                      'could not be updated.')
            else:
                flash('Venue ' + str(form.name.data) + ' was successfully\
                    updated!')
        return redirect(url_for('show_venue', venue_id=venue_id))
    else:
        flash('Please ensure all details are valid')
        return render_template('forms/edit_venue.html', form=form, venue=venue)

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm(request.form)
    if form.validate_on_submit():

        error = False
        print(form.genres.data)
        try:
            artist = Artist(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                phone=form.phone.data,
                genres=",".join(form.genres.data),
                facebook_link=form.facebook_link.data
            )
            db.session.add(artist)
            db.session.commit()
        except Exception:
            error = True
            db.session.rollback()
            print(exc_info())
        finally:
            db.session.close()
            if error:
                flash('An error occurred. Artist ' + str(form.name.data) +
                      'could not be listed.')
            else:
                flash('Artist ' + str(form.name.data) + ' was successfully\
                      listed!')

        return render_template('pages/home.html')

    else:
        flash('Please ensure all details provided are valid')
        return render_template('forms/new_artist.html', form=form)


#  Shows
#  ----------------------------------------------------------------


@app.route('/shows')
def shows():
    shows = Shows.query.all()
    data = [show.with_artist_and_venue() for show in shows]
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    form = ShowForm(request.form)
    if form.validate_on_submit():
        error = False
        try:
            show = Shows(
                artist_id=form.artist_id.data,
                venue_id=form.venue_id.data,
                start_time=form.start_time.data
            )
            db.session.add(show)
        except Exception:
            error = True
            db.session.rollback()
            print(exc_info())
        finally:
            db.session.close()
            flash("An error occurred. Show could not be listed")\
                if error else flash('Show was successfully listed!')
        return render_template('pages/home.html')
    else:
        flash('Please ensure all details provided are valid')
        return render_template('forms/new_show.html', form=form)

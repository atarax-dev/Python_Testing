import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def load_clubs():
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions():
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()


def is_competition_date_wrong(date: str):
    date_time_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    return datetime.today() > date_time_obj


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions,
                               utc_dt=str(datetime.today()))
    except IndexError:
        flash("Email not found")
        return render_template('index.html')


@app.route('/book/<competition>/<club>')
def book(competition, club):
    try:
        found_club = [c for c in clubs if c['name'] == club][0]
        found_competition = [c for c in competitions if c['name'] == competition][0]
        return render_template('booking.html', club=found_club, competition=found_competition)
    except IndexError:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions, utc_dt=str(datetime.today()))


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])
    if is_competition_date_wrong(competition['date']):
        flash("Past competition, please select another one")
        return render_template('welcome.html', club=club, competitions=competitions, utc_dt=str(datetime.today()))
    if places_required > int(competition['numberOfPlaces']) or places_required > int(club['points']):
        flash("Not enough places or points to book")
        return render_template('welcome.html', club=club, competitions=competitions, utc_dt=str(datetime.today()))
    elif places_required < 0:
        flash("Please use positive numbers")
        return render_template('welcome.html', club=club, competitions=competitions, utc_dt=str(datetime.today()))
    elif places_required > 12:
        flash("Please book 12 places or less")
        return render_template('welcome.html', club=club, competitions=competitions, utc_dt=str(datetime.today()))
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
    club['points'] = int(club['points']) - places_required
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions, utc_dt=str(datetime.today()))


@app.route("/clubs")
def list_clubs():
    return render_template("clubs.html", clubs=load_clubs())


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)

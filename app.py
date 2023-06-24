"""
Author: Naor Or-Zion
Unit:   Basmach-Alpha
Date:   4.6.2023

Brief: The 'app.py' is the main file for the dorms website
"""

from flask import Flask, render_template, g, url_for, flash, request, redirect, jsonify
# Used to create specific fields
from wtforms import StringField, TextAreaField, SubmitField, SelectField, DecimalField, IntegerField, RadioField, StringField
# Use the validators to check the form
from wtforms.validators import InputRequired, DataRequired, Length, NumberRange
from flask_wtf import FlaskForm
import sqlite3

# Const
VALID_GENDER_RADIO_VALUE = ["זכר", "נקבה", "אחר"]

app = Flask(__name__)
app.config["SECRET_KEY"] = "bsmch-dorms"


class NewBuildingForm(FlaskForm):
    title = IntegerField("Building Number",
                         validators=[InputRequired("Input is required!"),
                                     DataRequired("Data is required!"),
                                     NumberRange(min=1, max=99999999,
                                                 message="Building number is not valid!")])
    submit = SubmitField("שמירת שינויים")


class NewApartmentForm(FlaskForm):
    apt_id = IntegerField("Apartment Number",
                          validators=[InputRequired("Input is required!"),
                                      DataRequired("Data is required!"),
                                      NumberRange(min=1, max=99999999,
                                                  message="Apartment number is not valid!")])


class NewResidentForm(FlaskForm):
    full_name_field = StringField('Full Name', [InputRequired("Input is required!"), Length(
        min=2, max=25, message="Length must be between 2 and 25 characters long")])
    frame_selection_field = SelectField('Frame', choices=[('אין', 'ללא'),
                                                          ('מעטפת', 'מעטפת'),
                                                          ('תכנות כחול',
                                                           'תכנות כחול'),
                                                          ('תכנות אדום',
                                                           'תכנות אדום'),
                                                          ('תכנות צהוב',
                                                           'תכנות צהוב'),
                                                          ('תכנות ירוק',
                                                           'תכנות ירוק'),
                                                          ('SRE', 'SRE'),
                                                          ('DevOps', 'DevOps'),
                                                          ('דאטה', 'דאטה'),
                                                          ('QA', 'QA'),
                                                          ('מגן סייבר א',
                                                           'מגן סייבר א'),
                                                          ('מגן סייבר ב',
                                                           'מגן סייבר ב'),
                                                          ('לוגיסטיקה',
                                                           'לוגיסטיקה'),
                                                          ('מפקדה', 'מפקדה'),
                                                          ('אחר', 'אחר')], validators=[InputRequired("Input is required!")])

    distance_selection_field = SelectField('Distance Indication', choices=[('1', '1'),
                                                                           ('2',
                                                                            '2'),
                                                                           ('3', '3'), ], validators=[InputRequired("Input is required!")])

    select_gender_field = RadioField("Gender Field", choices=[("male-resident", "זכר"),
                                                              ("female-resident",
                                                               "נקבה"),
                                                              ("trans-resident", "טראנס")], validators=[InputRequired("Input is required!")])

    submit = SubmitField("שמירת שינויים")


@app.route("/new-apartment", methods=["POST"])
def new_apartment():
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    # Get NewApartmentForm data
    form = NewApartmentForm()

    if request.method == "POST":
        # Apartment id
        apartment_id = form.apt_id.data

        # Rooms quantity selection
        rooms_quantity = request.form.get("roomSelection")

        # Radio button can be "זכר"/"נקבה"/"אחר"
        gender = request.form.get("btnradio-home")

        # Building id - make sure to validate it with the database before submitting
        building_id = request.form.get("building-id")

        # Insert apartment data to database
        c.execute("""INSERT INTO apartments (apt_id, rooms_in_apt, gender, building_id) VALUES (?, ?, ?, ?);""",
                  (apartment_id,
                   rooms_quantity,
                   gender,
                   building_id))
        conn.commit()

        # If the room's quantity is None - redirect to the same page
        if not rooms_quantity:
            redirect(request.referrer)

        for room_number in range(1, int(rooms_quantity) + 1):
            aminach_beds_quantity = request.form.get(
                f"aminachBedSelection-{str(room_number)}")
            bunk_beds_quantity = request.form.get(
                f"bunkBedSelection-{str(room_number)}")

            c.execute("""INSERT INTO rooms (apt_id, room_id, aminach_beds, bunk_beds) VALUES (?, ?, ?, ?);""",
                      (apartment_id,
                       room_number,
                       aminach_beds_quantity,
                       bunk_beds_quantity))
            conn.commit()

            # If the bunk beds' quantity is None - redirect to the same page
            if bunk_beds_quantity:
                for bunk_bed_number in range(1, int(bunk_beds_quantity) + 1):
                    name_bunk_bed1 = request.form.get(
                        f"inputBunkBed1-{room_number}-{bunk_bed_number}")
                    name_bunk_bed2 = request.form.get(
                        f"inputBunkBed2-{room_number}-{bunk_bed_number}")

                    c.execute("""INSERT INTO bunk_bed (apt_id, mattress_count, person1, person2, room_id) VALUES (?, 2, ?, ?, ?);""",
                            (apartment_id,
                            name_bunk_bed1,
                            name_bunk_bed2,
                            room_number))
                    conn.commit()

            # If the aminach beds' quantity is None - redirect to the same page
            if aminach_beds_quantity:
                for aminach_bed_number in range(1, int(aminach_beds_quantity) + 1):
                    name_aminach_bed = request.form.get(
                        f"inputAminachBed-{room_number}-{aminach_bed_number}")

                    c.execute("""INSERT INTO aminach_bed (apt_id, mattress_count, person1, room_id) VALUES (?, 1, ?, ?);""",
                            (apartment_id,
                            name_aminach_bed,
                            room_number))
                    conn.commit()

    return redirect(request.referrer)


@app.route("/new-building", methods=["POST"])
def new_building():
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    # Getting the form data object from the class "NewBuildingForm".
    form = NewBuildingForm()

    if form.validate_on_submit():
        new_building_number = int(form.title.data)

        c.execute("""INSERT INTO buildings (building_id, apt_count) VALUES (?, ?);""",
                  (new_building_number, 0))
        conn.commit()

    return redirect(request.referrer)


@app.route("/residents/new-resident", methods=["POST"])
def new_resident():
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    # Get NewResidentForm submitted data
    form = NewResidentForm()

    if request.method == "POST":
        full_name = form.full_name_field.data
        association = form.frame_selection_field.data
        gender = request.form.get("btnradio-resident") if request.form.get(
            "btnradio-resident") in VALID_GENDER_RADIO_VALUE else "Invalid selection"
        distance = form.distance_selection_field.data
        enter_date = request.form.get("enter-date")
        exit_date = request.form.get("exit-date")

        c.execute("""INSERT INTO residents (id, full_name, association, gender, distance, entering_date, existing_date) VALUES (NULL, ?, ?, ?, ?, ?, ?);""",
                  (full_name, association, gender, distance, enter_date, exit_date))
        conn.commit()

    return redirect(request.referrer)


@app.route("/residents")
def residents():
    # Get residents data
    residents = get_residents_data()

    # Forms
    newResidentForm = NewResidentForm()

    return render_template("residents.html", newResidentForm=newResidentForm, residents=residents)


@app.route('/get-residents', methods=['GET'])
def get_residents_for_selection():
    residents = get_residents_data()
    # Fetch the resident data from your data source
    residents_data = []

    for resident in residents:
        residents_data.append(resident['full_name'])

    return jsonify(residents_data)


@app.route("/")
def home():
    # Get buildings and apartments data
    buildings = get_buildings_data()
    apartments = get_apartments_data()
    rooms = get_rooms_data()
    bunk_beds = get_bunk_beds()
    aminach_beds = get_aminach_beds()

    # Forms
    newBuildingForm = NewBuildingForm()
    newApartmentForm = NewApartmentForm()

    return render_template("home.html",
                           newBuildingForm=newBuildingForm,
                           newApartmentForm=newApartmentForm,
                           buildings=buildings,
                           apartments=apartments,
                           rooms=rooms,
                           bunk_beds=bunk_beds,
                           aminach_beds=aminach_beds)


def get_buildings_data():
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    # Buildings data
    buildings = []
    buildings_from_db = c.execute(
        """SELECT * FROM buildings ORDER BY building_id ASC;""")
    for row in buildings_from_db:
        building = {
            "building_id": row[0],
            "apt_count": row[1]
        }
        buildings.append(building)

    return buildings


def get_residents_data():
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    # Residents data
    residents = []
    residents_from_db = c.execute(
        """SELECT * FROM residents ORDER BY id ASC;""")
    for row in residents_from_db:
        resident = {
            "id": row[0],
            "full_name": row[1],
            "association": row[2],
            "gender": row[3],
            "distance": row[4],
            "entering_date": row[5],
            "existing_date": row[6]
        }

        residents.append(resident)

    return residents


def get_apartments_data():
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    # Aparments data
    apartments = []
    apartments_from_db = c.execute(
        """SELECT * FROM apartments ORDER BY apt_id ASC;""")
    for row in apartments_from_db:
        apartment = {
            "apt_id": row[0],
            "rooms_in_apt": row[1],
            "gender": row[2],
            "building_id": row[3]
        }
        apartments.append(apartment)

    return apartments


def get_rooms_data(apartment_id=None):
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    # If an apartment id has been sent, get it's rooms.
    if apartment_id is not None:
        # Rooms data
        rooms = []
        rooms_from_db = c.execute(
            """SELECT * FROM rooms WHERE apt_id = ? ORDER BY room_id ASC;""", (apartment_id,))
        for row in rooms_from_db:
            room = {
                "apt_id": row[0],
                "room_id": row[1],
                "aminach_beds": row[2],
                "bunk_beds": row[3]
            }
            rooms.append(room)

        return rooms

    # Get all rooms data
    rooms = []
    rooms_from_db = c.execute("""SELECT * FROM rooms ORDER BY room_id ASC;""")
    for row in rooms_from_db:
        room = {
            "apt_id": row[0],
            "room_id": row[1],
            "aminach_beds": row[2],
            "bunk_beds": row[3]
        }
        rooms.append(room)

    return rooms


def get_bunk_beds(apt_id=None, room_id=None):
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    # If an apartment id and a room id have been sent, get it's bunk beds values.
    if room_id is not None and apt_id is not None:
        # Bunk beds data
        bunk_beds = []
        bunk_beds_from_db = c.execute(
            """SELECT * FROM bunk_bed WHERE apt_id = ? and room_id = ? ORDER BY room_id ASC;""", (apt_id, room_id))
        for row in bunk_beds_from_db:
            bunk_bed = {
                "apt_id": row[0],
                "mattress_count": row[1],
                "person1": row[2],
                "person2": row[3],
                "room_id": row[4]
            }
            bunk_beds.append(bunk_bed)

        return bunk_beds

    # If an apartment id has been sent, get it's bunk beds values.
    if room_id is None and apt_id is not None:
        # Bunk beds data
        bunk_beds = []
        bunk_beds_from_db = c.execute(
            """SELECT * FROM bunk_bed WHERE apt_id = ? ORDER BY room_id ASC;""", (apt_id,))
        for row in bunk_beds_from_db:
            bunk_bed = {
                "apt_id": row[0],
                "mattress_count": row[1],
                "person1": row[2],
                "person2": row[3],
                "room_id": row[4]
            }
            bunk_beds.append(bunk_bed)

        return bunk_beds

    # If a room id has been sent, get it's bunk beds values.
    if room_id is not None and apt_id is None:
        # Bunk beds data
        bunk_beds = []
        bunk_beds_from_db = c.execute(
            """SELECT * FROM bunk_bed WHERE room_id = ? ORDER BY room_id ASC;""", (room_id,))
        for row in bunk_beds_from_db:
            bunk_bed = {
                "apt_id": row[0],
                "mattress_count": row[1],
                "person1": row[2],
                "person2": row[3],
                "room_id": row[4]
            }
            bunk_beds.append(bunk_bed)

        return bunk_beds

    # If a nothing has been sent, get all bunk beds values.
    if room_id is None and apt_id is None:
        # Bunk beds data
        bunk_beds = []
        bunk_beds_from_db = c.execute(
            """SELECT * FROM bunk_bed ORDER BY apt_id ASC, room_id ASC;""")
        for row in bunk_beds_from_db:
            bunk_bed = {
                "apt_id": row[0],
                "mattress_count": row[1],
                "person1": row[2],
                "person2": row[3],
                "room_id": row[4]
            }
            bunk_beds.append(bunk_bed)

        return bunk_beds


def get_aminach_beds(apt_id=None, room_id=None):
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    # If an apartment id and a room id have been sent, get it's aminach beds values.
    if room_id is not None and apt_id is not None:
        # aminach beds data
        aminach_beds = []
        aminach_beds_from_db = c.execute(
            """SELECT * FROM aminach_bed WHERE apt_id = ? and room_id = ? ORDER BY room_id ASC;""", (apt_id, room_id))
        for row in aminach_beds_from_db:
            aminach_bed = {
                "apt_id": row[0],
                "mattress_count": row[1],
                "person1": row[2],
                "room_id": row[3]
            }
            aminach_beds.append(aminach_bed)

        return aminach_beds

    # If an apartment id has been sent, get it's aminach beds values.
    if room_id is None and apt_id is not None:
        # Aminach bed data
        aminach_beds = []
        aminach_beds_from_db = c.execute(
            """SELECT * FROM aminach_bed WHERE apt_id = ? ORDER BY room_id ASC;""", (apt_id,))
        for row in aminach_beds_from_db:
            aminach_bed = {
                "apt_id": row[0],
                "mattress_count": row[1],
                "person1": row[2],
                "room_id": row[3]
            }
            aminach_beds.append(aminach_bed)

        return aminach_beds

    # If a room id has been sent, get it's aminach beds values.
    if room_id is not None and apt_id is None:
        # Aminach beds data
        aminach_beds = []
        aminach_beds_from_db = c.execute(
            """SELECT * FROM aminach_bed WHERE room_id = ? ORDER BY room_id ASC;""", (room_id,))
        for row in aminach_beds_from_db:
            aminach_bed = {
                "apt_id": row[0],
                "mattress_count": row[1],
                "person1": row[2],
                "room_id": row[3]
            }
            aminach_beds.append(aminach_bed)

        return aminach_beds

    # If a nothing has been sent, get all aminach beds values.
    if room_id is None and apt_id is None:
        # Aminach beds data
        aminach_beds = []
        aminach_beds_from_db = c.execute(
            """SELECT * FROM aminach_bed ORDER BY apt_id ASC, room_id ASC;""")
        for row in aminach_beds_from_db:
            aminach_bed = {
                "apt_id": row[0],
                "mattress_count": row[1],
                "person1": row[2],
                "room_id": row[3]
            }
            aminach_beds.append(aminach_bed)

        return aminach_beds


def get_db():
    """
    The application context in Flask represents a shared environment where
      important resources and variables for the Flask application are stored. 
      It allows different parts of the code to access and share resources like the current request, 
      configuration settings, and database connections. 
      Think of it as a central area in a house where you can find and use things that are shared among different rooms. 
      The application context ensures efficient communication and resource management within the Flask application so you won't
      have to pass data(by parameters) to functions every time.

    The "g" object in Flask is part of the application context. It's a special space where you
      can temporarily store information during the handling of a single request.
      It's like a little notebook that you can use to keep track of important data,
      and it gets automatically cleared out when the request is done.
    """
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect("db/db-dorms/dorms.db")
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    app.run(debug=True)

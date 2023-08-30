"""
Author: Naor Or-Zion
Unit:   Basmach-Alpha
Date:   4.6.2023

Brief: The 'app.py' is the main navigation file for the dorms website
"""

from flask import (
    Flask,
    render_template,
    flash,
    redirect,
    jsonify,
    request,
    send_file,
    session,
    url_for,
    g
)

from query_delete_utils import delete_apt_from_query, delete_building_from_query
from flask_forms import NewApartmentForm, NewBuildingForm, NewResidentForm, NewUserForm
from auth_utils import get_usernames_from_db, get_passwords_from_db
from filter_apartments_utils import *
from query_update_apt_utils import *
from filter_residents_util import *
from residents_xlsx_utils import *
from query_delete_utils import *
from db import get_db, init_app
from datetime import datetime

from help_functions import *
from get_functions import *
from consts import *


app = Flask(__name__)
app.config["SECRET_KEY"] = "bsmch-dorms"
init_app(app)


@app.route("/residents/filtered_residents", methods=["POST"])
def gather_data_filter_residents():
    '''
    This function filters residents on residents page based on user selection.
    @params: None
    Returns: render_template(page_data)
    '''
    # if not session.get('logged_in'):
    #     return redirect("/login")
    
    if request.method != "POST":
        return redirect("/residents")
    
    # Get data from form submission
    names_filter = request.form.getlist("filter-names")
    frames_filter = request.form.getlist("filter-frames")
    genders_filter = request.form.getlist("filter-genders")
    services_filter = request.form.getlist("filter-services")
    beersheva_filter = request.form.getlist("filter-beersheva")
    apartments_filter = request.form.getlist("filter-apartments")

    # Retrieve a list of the filtered residents
    filtered_residents = filter_residents(names_filter, 
                                             frames_filter,
                                             genders_filter,
                                             services_filter,
                                             beersheva_filter,
                                             apartments_filter)
    
    # Forms
    newResidentForm = NewResidentForm()

    return render_template(
        "residents.html", newResidentForm=newResidentForm, residents=filtered_residents
    )


@app.route("/filter", methods=["POST"])
def gather_data_for_filter():
    """
    This function filters apartments on homepage based on user selection.
    @params: None
    Returns: render_template(page_data)
    """
    # if not session.get('logged_in'):
    #     return redirect("/login")
    
    if request.method != "POST":
        return redirect("/")
    
    # Get data from form submission
    names_filter = request.form.getlist("filter-names")
    apartments_filter = request.form.getlist("filter-apartments")
    frames_filter = request.form.getlist("filter-frames")
    genders_filter = request.form.getlist("filter-genders")
    is_empty_beds_filter = request.form.get("btnradio-free-beds")

    # Retrieve a list of the filtered apartments
    filtered_apartments = filter_apartments(names_filter, apartments_filter, frames_filter, genders_filter, is_empty_beds_filter)

    ## Retrieve a list of the filtered apartments ids
    filter_apartments_ids = get_apt_ids_by_apartments(filtered_apartments)
    
    # Get buildings and apartments data from db
    buildings = get_buildings_data()

    # Retrieve gender beds statistics - Over all statistics.
    beds_quantity_info = get_beds_quantity_by_gender()

    # Initialize lists to appends neccessery data
    rooms = []
    bunk_beds = []
    aminach_beds = []

    # Iterate over the apartments' ids to retrieve the rooms, bunk beds and aminach beds.
    for apt_id in filter_apartments_ids:
        rooms.append(get_rooms_data(apt_id=apt_id))
        bunk_beds.append(get_bunk_beds(apt_id=apt_id))
        aminach_beds.append(get_aminach_beds(apt_id=apt_id))

    # Forms
    newBuildingForm = NewBuildingForm()
    newApartmentForm = NewApartmentForm()


    return render_template(
        "home.html",
        newBuildingForm=newBuildingForm,
        newApartmentForm=newApartmentForm,
        buildings=buildings,
        apartments=filtered_apartments,
        rooms=rooms,
        bunk_beds=bunk_beds,
        aminach_beds=aminach_beds,
        beds_quantity_info=beds_quantity_info,
        collapse_show_text="show"
    )


@app.route("/residents/delete-selected-residents", methods=["POST"])
def delete_selected_residents():
    '''
    This function deletes selected residents.
    The selected residents are being sent by an ajax request in the "script.js" file.
    @params: None.
    Returns: redirect("/residents") 
    '''
    # if not session.get('logged_in'):
    #     return redirect("/login")
    
    # Get the submitted data from the request body
    # Format -> List[str]
    residents_ids = request.get_json()

    # Handle the submitted data here
    delete_residents_by_id(residents_ids=residents_ids)

    return redirect("/residents")


@app.route("/delete-building/<int:building_id>", methods=["POST"])
def delete_building(building_id=None):
    """
    This function deletes a building.
    @params: building id -> int
    Returns: Back to referrer URL
    """
    # if not session.get('logged_in'):
    #     return redirect("/login")
    
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    # In case someone will try to not use a POST request
    if request.method != "POST":
        return redirect(request.refferer)

    # If not None execute the query
    if building_id:
        delete_building_from_query(building_id)

    return redirect("/")


@app.route("/delete_apartments/<int:apt_id>", methods=["POST"])
def delete_apartments(apt_id=None, apartments=None):
    """
    This function can delete a single apartment or multiple apartments.
    @params: apartment id -> int, apartments -> List[str, int]
    Returns: Back to referrer URL
    """
    # if not session.get('logged_in'):
    #     return redirect("/login")
    
    # In case someone will try to use a GET request in the url
    if request.method != "POST":
        return redirect("/")

    # If apartments have been sent as parameter and not a single apartment, execute the query
    if apartments is not None and apt_id is None:
        for apartment in apartments:
            if is_apartment_exist(new_apartment_id=apartment["apt_id"]):
                delete_apt_from_query(apt_id=apartment["apt_id"])

    # If a single apartment has been sent as parameter and not apartments, execute the query
    if apt_id is not None and apartments is None:
        if is_apartment_exist(new_apartment_id=apt_id):
            delete_apt_from_query(apt_id=apt_id)

    return redirect("/")


@app.route("/update-building", methods=["POST"])
def update_building(new_building_id, old_building_id):
    """
    This function updates a building's id.
    @params: new building id - > int, old building id - > int
    Returns: Back to referrer URL
    """
    # if not session.get('logged_in'):
    #     return redirect("/login")
    
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    if not is_building_exist(old_building_id):
        # Update building
        c.execute(
            f"""UPDATE {BUILDING_TABLE} SET {BUILDING_ID_BUILDING_TABLE}=%s WHERE {BUILDING_ID_BUILDING_TABLE}=%s;""",
            (new_building_id, old_building_id),
        )
        conn.commit()

        return redirect("/")

    flash(f"בניין {old_building_id} כבר קיים!", "new-building")
    return redirect("/")


@app.route("/update-apartment/<int:existing_apt_id>", methods=["POST"])
def update_apartment(existing_apt_id):
    # if not session.get('logged_in'):
    #     return redirect("/login")
    
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    # Get NewApartmentForm data
    form = NewApartmentForm()

    # If the request method made is not post redirect to the referrer URL.
    if request.method != "POST":
        return redirect("/")

    # Retrieve apt_id, gender, rooms_qunatity from form submission.
    new_apartment_id = form.apt_id.data
    new_gender = request.form.get(f"btnradio-home-{existing_apt_id}")
    new_rooms_quantity = request.form.get(f"roomSelection-{existing_apt_id}")

    # Check if the form's data is valid
    if not valid_apt_form_sub(
        new_apartment_id=new_apartment_id,
        existing_apt_id=existing_apt_id,
        gender=new_gender,
        rooms_quantity=new_rooms_quantity,
    ):
        return redirect("/")

    # Get the past rooms quantity of the apartment
    past_rooms_quantity = get_past_rooms_quantity_of_apt(existing_apt_id)

    # Update apartment's data to database
    update_new_metadata_of_apt(new_apartment_id, new_rooms_quantity, new_gender, existing_apt_id)

    # If rooms quantity is not None but equal to 0, delete all the data from the beds and update the residents to have no apartments
    # After that you can return to referrer URL.
    if new_rooms_quantity and int(new_rooms_quantity) == 0:
        delete_beds_by_apt(apt_id=existing_apt_id)
        update_residents_to_null_by_apt(apt_id=existing_apt_id)

        return redirect("/")

    # Iterate over the submitted selected rooms quantity, if there are any changes update the db.
    for room_number in range(1, int(new_rooms_quantity) + 1):
        aminach_beds_quantity = request.form.get(
            f"aminachBedSelection-{existing_apt_id}-{str(room_number)}"
        )
        bunk_beds_quantity = request.form.get(
            f"bunkBedSelection-{existing_apt_id}-{str(room_number)}"
        )

        # Update the room with the new metadata submitted by user:
        #  room number, aminach beds qunatity and bunk beds quantity.
        update_room_new_metadata(new_apartment_id=new_apartment_id, new_room_number=room_number, 
                                 new_aminach_beds_quantity=aminach_beds_quantity, new_bunk_beds_quantity=bunk_beds_quantity, 
                                 existing_apt_id=existing_apt_id)

        # If the new rooms quantity selected is more than the past rooms quantity selected, there is a need to create a new room.
        if int(room_number) > past_rooms_quantity:
            create_new_room(new_apartment_id=new_apartment_id, new_room_number=room_number, 
                            new_aminach_beds_quantity=aminach_beds_quantity, new_bunk_beds_quantity=bunk_beds_quantity)


        # UPDATE residents' apartment to NULL before I'm making any changes.
        update_residents_apt_to_null(apt_id=existing_apt_id, room_id=room_number)

        # If the bunk beds' quantity is None - redirect to the same page
        # If the bunk beds' quantity is not None - prepare to deal with past and current residents
        if bunk_beds_quantity:
            # Retrieve the past quantity of the bunk beds in this room, it can be None if there weren't any changes.
            c.execute(
                f"""SELECT count(*) FROM {BUNK_BED_TABLE} WHERE {APT_ID_BUNK_TABLE} = %s and {ROOM_ID_BUNK_TABLE} = %s;""",
                (existing_apt_id, room_number),
            )

            bunk_beds_quantity_before_update = c.fetchall()

            if bunk_beds_quantity_before_update:
                if bunk_beds_quantity_before_update[0]:
                    bunk_beds_quantity_before_update = (
                        bunk_beds_quantity_before_update[0][0]
                    )
                else:
                    bunk_beds_quantity_before_update = None
            else:
                bunk_beds_quantity_before_update = None

            # If the bunk beds quantity was changed to 0, it means that the residents' beds should be deleted
            if bunk_beds_quantity == "0":
                residents_ids = get_bunk_bed_residents_id_in_room(
                    existing_apt_id, room_number
                )

                # Delete all beds
                c.execute(
                    f"""DELETE from {BUNK_BED_TABLE} WHERE {APT_ID_BUNK_TABLE} = %s and {ROOM_ID_BUNK_TABLE} = %s""",
                    (existing_apt_id, room_number),
                )
                conn.commit()

                # Delete the apartment connected to resident
                for id in residents_ids:
                    c.execute(
                        f"""UPDATE {RESIDENTS_TABLE} SET {APT_RESIDENTS_TABLE} = NULL WHERE {ID_RESIDENTS_TABLE} = %s""",
                        (id,),
                    )
                    conn.commit()

            # Elsewise, -> Reconstruct the operations here
            else:
                for bunk_bed_number in range(1, int(bunk_beds_quantity) + 1):
                    # SELECT the residents who were sleeping in the current apartment in the specified room in the specified bed.
                    c.execute(
                        f"""SELECT {PERSON1_BUNK_TABLE}, {PERSON2_BUNK_TABLE} FROM {BUNK_BED_TABLE} WHERE {APT_ID_BUNK_TABLE} = %s and {ROOM_ID_BUNK_TABLE} = %s and {BED_ID_BUNK_TABLE} = %s;""",
                        (existing_apt_id, room_number, bunk_bed_number),
                    )

                    past_residents = c.fetchall()

                    if past_residents:
                        past_residents = past_residents[0]

                        # Retrieve the neccesery data of the residents who were sleeping in this apartment.
                        # Update the apartment of the residents who were sleeping before to NULL in residents table.
                        first_bunk_bed_resident = past_residents[0]
                        second_bunk_bed_resident = past_residents[1]

                        if first_bunk_bed_resident != EMPTY_BED_TEXT:
                            past_resident1_data = first_bunk_bed_resident.split(
                                " - "
                            )
                            past_resident1_id = past_resident1_data[0]
                            c.execute(
                                f"""UPDATE {RESIDENTS_TABLE} SET {APT_RESIDENTS_TABLE} = NULL WHERE {ID_RESIDENTS_TABLE} = %s""",
                                (past_resident1_id,),
                            )

                        if second_bunk_bed_resident != EMPTY_BED_TEXT:
                            past_resident2_data = second_bunk_bed_resident.split(
                                " - "
                            )
                            past_resident2_id = past_resident2_data[0]
                            c.execute(
                                f"""UPDATE {RESIDENTS_TABLE} SET {APT_RESIDENTS_TABLE} = NULL WHERE {ID_RESIDENTS_TABLE} = %s""",
                                (past_resident2_id,),
                            )

                        conn.commit()

                    # Delete a row's data before appending new data to prevent collisions.
                    # Eventually I will insert new row to the table after I get the new residents' names.
                    c.execute(
                        f"""DELETE from {BUNK_BED_TABLE} WHERE {APT_ID_BUNK_TABLE} = %s and {ROOM_ID_BUNK_TABLE} = %s and {BED_ID_BUNK_TABLE} = %s""",
                        (existing_apt_id, room_number, bunk_bed_number),
                    )
                    conn.commit()

                    # Get the new full residents name from the form submission
                    new_resident1_bunk_bed = request.form.get(
                        f"inputBunkBed1-{existing_apt_id}-{room_number}-{bunk_bed_number}"
                    )
                    new_resident2_bunk_bed = request.form.get(
                        f"inputBunkBed2-{existing_apt_id}-{room_number}-{bunk_bed_number}"
                    )

                    new_resident1_id = None
                    new_resident2_id = None

                    # Get the new residents unique id
                    if (
                        new_resident1_bunk_bed
                        and new_resident1_bunk_bed != EMPTY_BED_TEXT
                    ):
                        new_resident1_id = new_resident1_bunk_bed.split(" - ")[0]
                    if (
                        new_resident2_bunk_bed
                        and new_resident2_bunk_bed != EMPTY_BED_TEXT
                    ):
                        new_resident2_id = new_resident2_bunk_bed.split(" - ")[0]

                    # Retrieve the new_resident1_bunk_bed past apartment if exists so I can remove him from his past apartment
                    if new_resident1_id:
                        # Retrieve the past apartment of the new resident
                        c.execute(
                            f"""SELECT {APT_RESIDENTS_TABLE} FROM {RESIDENTS_TABLE} WHERE {ID_RESIDENTS_TABLE} = %s""",
                            (new_resident1_id,),
                        )

                        past_apartment_new_resident1 = c.fetchall()

                        if past_apartment_new_resident1:
                            if past_apartment_new_resident1[0]:
                                past_apartment_new_resident1 = (
                                    past_apartment_new_resident1[0][0]
                                )
                            else:
                                past_apartment_new_resident1 = None
                        else:
                            past_apartment_new_resident1 = None

                        # When creating new apartment you want to update the past place a resident was sleeping at to EMPTY_BED_TEXT
                        #   no matter which bed he was lying on
                        if past_apartment_new_resident1:
                            c.execute(
                                f"""UPDATE {BUNK_BED_TABLE} SET {PERSON1_BUNK_TABLE} = '{EMPTY_BED_TEXT}' WHERE {APT_ID_BUNK_TABLE} = %s and {PERSON1_BUNK_TABLE} = %s""",
                                (
                                    past_apartment_new_resident1,
                                    new_resident1_bunk_bed,
                                ),
                            )
                            c.execute(
                                f"""UPDATE {BUNK_BED_TABLE} SET {PERSON2_BUNK_TABLE} = '{EMPTY_BED_TEXT}' WHERE {APT_ID_BUNK_TABLE} = %s and {PERSON2_BUNK_TABLE} = %s""",
                                (
                                    past_apartment_new_resident1,
                                    new_resident1_bunk_bed,
                                ),
                            )
                            c.execute(
                                f"""UPDATE {AMINACH_BED_TABLE} SET {PERSON1_AMINACH_TABLE} = '{EMPTY_BED_TEXT}' WHERE {APT_ID_AMINACH_TABLE} = %s and {PERSON1_AMINACH_TABLE} = %s""",
                                (
                                    past_apartment_new_resident1,
                                    new_resident1_bunk_bed,
                                ),
                            )
                            conn.commit()

                    # Retrieve the new_resident_2 past apartment if exists so I can remove him from his past apartment
                    if new_resident2_id:
                        c.execute(
                            f"""SELECT {APT_RESIDENTS_TABLE} FROM {RESIDENTS_TABLE} WHERE {ID_RESIDENTS_TABLE} = %s""",
                            (new_resident2_id,),
                        )

                        past_apartment_new_resident2 = c.fetchall()

                        if past_apartment_new_resident2:
                            if past_apartment_new_resident2:
                                if past_apartment_new_resident2[0]:
                                    past_apartment_new_resident2 = (
                                        past_apartment_new_resident2[0][0]
                                    )
                                else:
                                    past_apartment_new_resident2 = None
                            else:
                                past_apartment_new_resident2 = None

                        # When creating new apartment you want to update the last place a resident was sleeping at to EMPTY_BED_TEXT
                        #   no matter which bed he was lying on
                        if past_apartment_new_resident2:
                            c.execute(
                                f"""UPDATE {BUNK_BED_TABLE} SET {PERSON2_BUNK_TABLE} = '{EMPTY_BED_TEXT}' WHERE {APT_ID_BUNK_TABLE} = %s and {PERSON2_BUNK_TABLE} = %s""",
                                (
                                    past_apartment_new_resident2,
                                    new_resident2_bunk_bed,
                                ),
                            )
                            c.execute(
                                f"""UPDATE {BUNK_BED_TABLE} SET {PERSON1_BUNK_TABLE} = '{EMPTY_BED_TEXT}' WHERE {APT_ID_BUNK_TABLE} = %s and {PERSON1_BUNK_TABLE} = %s""",
                                (
                                    past_apartment_new_resident2,
                                    new_resident2_bunk_bed,
                                ),
                            )
                            c.execute(
                                f"""UPDATE {AMINACH_BED_TABLE} SET {PERSON1_AMINACH_TABLE} = '{EMPTY_BED_TEXT}' WHERE {APT_ID_AMINACH_TABLE} = %s and {PERSON1_AMINACH_TABLE} = %s""",
                                (
                                    past_apartment_new_resident2,
                                    new_resident2_bunk_bed,
                                ),
                            )
                            conn.commit()

                    # Insert new data to bunk bed
                    c.execute(
                        f"""INSERT INTO {BUNK_BED_TABLE} ({APT_ID_BUNK_TABLE}, {MATTRESS_COUNT_BUNK_TABLE}, {PERSON1_BUNK_TABLE}, {PERSON2_BUNK_TABLE}, {ROOM_ID_BUNK_TABLE}, {BED_ID_BUNK_TABLE}) VALUES (%s, 2, %s, %s, %s, %s);""",
                        (
                            existing_apt_id,
                            new_resident1_bunk_bed,
                            new_resident2_bunk_bed,
                            room_number,
                            bunk_bed_number,
                        ),
                    )

                    # Set the specified residents' apartment number in database
                    c.execute(
                        f"""UPDATE {RESIDENTS_TABLE} SET {APT_RESIDENTS_TABLE} = %s WHERE {ID_RESIDENTS_TABLE} = %s;""",
                        (existing_apt_id, new_resident1_id),
                    )
                    c.execute(
                        f"""UPDATE {RESIDENTS_TABLE} SET {APT_RESIDENTS_TABLE} = %s WHERE {ID_RESIDENTS_TABLE} = %s;""",
                        (existing_apt_id, new_resident2_id),
                    )
                    conn.commit()

                # Delete the left beds that the for loop didn't get to when user try to lower the beds count in the room
                if bunk_beds_quantity_before_update:
                    if bunk_beds_quantity_before_update > int(bunk_beds_quantity):
                        for left_bunk_bed_number in range(
                            bunk_bed_number + 1,
                            bunk_beds_quantity_before_update + 1,
                        ):
                            # Delete a row's data before appending new data to prevent collisions.
                            c.execute(
                                f"""DELETE from {BUNK_BED_TABLE} WHERE {APT_ID_BUNK_TABLE} = %s and {ROOM_ID_BUNK_TABLE} = %s and {BED_ID_BUNK_TABLE} = %s""",
                                (
                                    existing_apt_id,
                                    room_number,
                                    left_bunk_bed_number,
                                ),
                            )
                            conn.commit()

        # If the aminach beds' quantity is None - redirect to the same page
        if aminach_beds_quantity:
            c.execute(
                f"""SELECT count(*) FROM {AMINACH_BED_TABLE} WHERE {APT_ID_AMINACH_TABLE} = %s and {ROOM_ID_AMINACH_TABLE} = %s;""",
                (existing_apt_id, room_number),
            )

            aminach_beds_quantity_before_update = c.fetchall()

            if aminach_beds_quantity_before_update:
                if aminach_beds_quantity_before_update[0]:
                    aminach_beds_quantity_before_update = (
                        aminach_beds_quantity_before_update[0][0]
                    )
                else:
                    aminach_beds_quantity_before_update = None
            else:
                aminach_beds_quantity_before_update = None

            # If the aminach beds quantity was changed to 0, it means that the beds should be deleted
            if aminach_beds_quantity == "0":
                residents_ids = get_aminach_bed_residents_id_in_room(
                    existing_apt_id, room_number
                )

                # Delete all beds
                c.execute(
                    f"""DELETE from {AMINACH_BED_TABLE} WHERE {APT_ID_AMINACH_TABLE} = %s and {ROOM_ID_AMINACH_TABLE} = %s""",
                    (existing_apt_id, room_number),
                )
                conn.commit()

                # Delete the apartment connected to residents
                for id in residents_ids:
                    c.execute(
                        f"""UPDATE {RESIDENTS_TABLE} SET {APT_RESIDENTS_TABLE} = NULL WHERE {ID_RESIDENTS_TABLE} = %s""",
                        (id,),
                    )
                    conn.commit()

            # Elsewise, -> Reconstruct the operations here
            else:
                for aminach_bed_number in range(1, int(aminach_beds_quantity) + 1):
                    # SELECT the resident who is sleeping in the current apartment in the specified room in the specified bed.
                    c.execute(
                        f"""SELECT {PERSON1_AMINACH_TABLE} FROM {AMINACH_BED_TABLE} WHERE {APT_ID_AMINACH_TABLE} = %s and {ROOM_ID_AMINACH_TABLE} = %s and {BED_ID_AMINACH_TABLE} = %s;""",
                        (existing_apt_id, room_number, aminach_bed_number),
                    )

                    # Retrieve the neccesery data of the resident who was sleeping in this apartment
                    past_resident = c.fetchall()

                    # Update the apartment of resident who was sleeping before to NULL
                    if past_resident:
                        past_resident = past_resident[0]
                        if past_resident[0] != EMPTY_BED_TEXT:
                            past_resident_data = past_resident[0].split(" - ")
                            past_resident_id = past_resident_data[0]

                            c.execute(
                                f"""UPDATE {RESIDENTS_TABLE} SET {APT_RESIDENTS_TABLE} = NULL WHERE {ID_RESIDENTS_TABLE} = %s""",
                                (past_resident_id,),
                            )
                            conn.commit()

                    # Get the new resident full name from the form submission.
                    new_resident_aminach_bed = request.form.get(
                        f"inputAminachBed-{existing_apt_id}-{room_number}-{aminach_bed_number}"
                    )

                    new_resident_aminach_bed_id = None

                    # Get the new resident unique id
                    if (
                        new_resident_aminach_bed
                        and new_resident_aminach_bed != EMPTY_BED_TEXT
                    ):
                        new_resident_aminach_bed_id = (
                            new_resident_aminach_bed.split(" - ")[0]
                        )

                    # Retrieve the new resident past apartment if exists so I can delete him from his past apartment
                    if new_resident_aminach_bed_id:
                        # Retrieve the new resident past apartment
                        c.execute(
                            f"""SELECT {APT_RESIDENTS_TABLE} FROM {RESIDENTS_TABLE} WHERE {ID_RESIDENTS_TABLE} = %s""",
                            (new_resident_aminach_bed_id,),
                        )

                        past_apartment_new_resident = c.fetchall()

                        # Validate that the apartment that was retrieved is not None
                        if past_apartment_new_resident:
                            if past_apartment_new_resident[0]:
                                past_apartment_new_resident = (
                                    past_apartment_new_resident[0][0]
                                )
                            else:
                                past_apartment_new_resident = None
                        else:
                            past_apartment_new_resident = None

                        # When creating new apartment you want to update the past place a resident was sleeping at to EMPTY_BED_TEXT
                        #   no matter which bed he was lying on
                        if past_apartment_new_resident:
                            c.execute(
                                f"""UPDATE {AMINACH_BED_TABLE} SET {PERSON1_AMINACH_TABLE} = '{EMPTY_BED_TEXT}' WHERE {APT_ID_AMINACH_TABLE} = %s and {PERSON1_AMINACH_TABLE} = %s""",
                                (
                                    past_apartment_new_resident,
                                    new_resident_aminach_bed,
                                ),
                            )

                            c.execute(
                                f"""UPDATE {BUNK_BED_TABLE} SET {PERSON1_BUNK_TABLE} = '{EMPTY_BED_TEXT}' WHERE {APT_ID_BUNK_TABLE} = %s and {PERSON1_BUNK_TABLE} = %s""",
                                (
                                    past_apartment_new_resident,
                                    new_resident_aminach_bed,
                                ),
                            )

                            c.execute(
                                f"""UPDATE {BUNK_BED_TABLE} SET {PERSON2_BUNK_TABLE} = '{EMPTY_BED_TEXT}' WHERE {APT_ID_BUNK_TABLE} = %s and {PERSON2_BUNK_TABLE} = %s""",
                                (
                                    past_apartment_new_resident,
                                    new_resident_aminach_bed,
                                ),
                            )

                            conn.commit()

                    # Delete a row's data before appending new data to prevent collisions.
                    c.execute(
                        f"""DELETE from {AMINACH_BED_TABLE} WHERE {APT_ID_AMINACH_TABLE} = %s and {ROOM_ID_AMINACH_TABLE} = %s and {BED_ID_AMINACH_TABLE} = %s""",
                        (existing_apt_id, room_number, aminach_bed_number),
                    )
                    conn.commit()

                    # Insert new resident into aminach bed
                    c.execute(
                        f"""INSERT INTO {AMINACH_BED_TABLE} ({APT_ID_AMINACH_TABLE}, {MATTRESS_COUNT_AMINACH_TABLE}, {PERSON1_AMINACH_TABLE}, {ROOM_ID_AMINACH_TABLE}, {BED_ID_AMINACH_TABLE}) VALUES (%s, 1, %s, %s, %s);""",
                        (
                            existing_apt_id,
                            new_resident_aminach_bed,
                            room_number,
                            aminach_bed_number,
                        ),
                    )

                    # Set the specified resident apartment number in database
                    c.execute(
                        f"""UPDATE {RESIDENTS_TABLE} SET {APT_RESIDENTS_TABLE} = %s WHERE {ID_RESIDENTS_TABLE} = %s""",
                        (existing_apt_id, new_resident_aminach_bed_id),
                    )
                    conn.commit()

                # Delete the left beds that the for loop didn't get to when user try to lower the beds count in the room
                if aminach_beds_quantity_before_update:
                    if aminach_beds_quantity_before_update > int(
                        aminach_beds_quantity
                    ):
                        for left_aminach_bed_number in range(
                            aminach_bed_number + 1,
                            aminach_beds_quantity_before_update + 1,
                        ):
                            # Delete a row's data before appending new data to prevent collisions.
                            c.execute(
                                f"""DELETE from {AMINACH_BED_TABLE} WHERE {APT_ID_AMINACH_TABLE} = %s and {ROOM_ID_AMINACH_TABLE} = %s and {BED_ID_AMINACH_TABLE} = %s""",
                                (
                                    existing_apt_id,
                                    room_number,
                                    left_aminach_bed_number,
                                ),
                            )
                            conn.commit()

    return redirect("/")


@app.route("/new-apartment", methods=["POST"])
def new_apartment():
    # if not session.get('logged_in'):
    #     return redirect("/login")
    
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    # Get NewApartmentForm data
    form = NewApartmentForm()

    if request.method != "POST":
        return redirect("/")
    # Retrieve apt_id, rooms_qunatity, gender and 
    #   building id from form submission.
    apartment_id = form.apt_id.data
    rooms_quantity = request.form.get("roomSelection")
    gender = request.form.get("btnradio-home")
    building_id = request.form.get("building-id-new-apt")

    # Validate apartment_id
    if is_apartment_exist(apartment_id):
        flash(f"דירה {apartment_id} כבר קיימת!", "new-apartment")
        return redirect("/")
    
    # Validate rooms' quantity, can be 0 but not None
    if not rooms_quantity:
        flash(f"כמות החדרים ריקה!", "new-apartment")
        return redirect("/")

    # Validate gender
    if gender is None:
        flash(f"צריך לבחור מגדר לחדר!", "new-apartment")
        return redirect("/")

    if gender not in VALID_GENDER_RADIO_VALUE:
        flash(f"בלי שטיקים! אפשר לבחור רק זכר/נקבה/אחר.", "new-apartment")
        return redirect("/")

    # Validate building_id
    if not building_id or building_id == '':
        flash(f"שגיאה במספר הבניין, יש לנסות למחוק את הדירה לגמרי ולנסות שוב", "new-apartment")
        return redirect("/")

    # Insert apartment data to database
    c.execute(
        f"""INSERT INTO {APARTMENTS_TABLE} ({APT_ID_APT_TABLE}, {ROOMS_IN_APT_TABLE}, {GENDER_APT_TABLE}, {BUILDING_ID_APT_TABLE}) VALUES (%s, %s, %s, %s);""",
        (apartment_id, int(rooms_quantity), gender, int(building_id))
    )
    conn.commit()


    for room_number in range(1, int(rooms_quantity) + 1):
        aminach_beds_quantity = request.form.get(
            f"aminachBedSelection-newApt-{str(room_number)}"
        )
        bunk_beds_quantity = request.form.get(
            f"bunkBedSelection-newApt-{str(room_number)}"
        )

        # Create a new room with the new metadata submitted by user:
        #  room number, aminach beds qunatity and bunk beds quantity.
        c.execute(
            f"""INSERT INTO {ROOMS_TABLE} ({APT_ID_ROOM_TABLE}, {ROOM_ID_ROOM_TABLE}, {AMINACH_BED_ROOM_TABLE}, {BUNK_BED_ROOM_TABLE}) VALUES (%s, %s, %s, %s);""",
            (apartment_id, room_number, aminach_beds_quantity, bunk_beds_quantity),
        )
        conn.commit()

        # If the bunk beds' quantity is None - redirect to the referrer URL
        if bunk_beds_quantity:
            for bunk_bed_number in range(1, int(bunk_beds_quantity) + 1):
                # Retrieve the value of the residents options by the HTML elements tags
                name_bunk_bed1 = request.form.get(
                    f"inputBunkBed1-newApt-{room_number}-{bunk_bed_number}"
                )
                name_bunk_bed2 = request.form.get(
                    f"inputBunkBed2-newApt-{room_number}-{bunk_bed_number}"
                )

                new_resident1_id = None
                new_resident2_id = None

                # Get the residents unique id
                if name_bunk_bed1 != EMPTY_BED_TEXT:
                    new_resident1_id = name_bunk_bed1.split(" - ")[0]
                if name_bunk_bed2 != EMPTY_BED_TEXT:
                    new_resident2_id = name_bunk_bed2.split(" - ")[0]

                # Retrieve the new resident past apartment if exists so I can remove him from his past apartment
                if new_resident1_id:
                    # Retrieve the past apartment of the new resident
                    c.execute(
                        f"""SELECT {APT_RESIDENTS_TABLE} FROM {RESIDENTS_TABLE} WHERE {ID_RESIDENTS_TABLE} = %s""",
                        (new_resident1_id,),
                    )

                    past_apartment_new_resident1 = c.fetchall()

                    if past_apartment_new_resident1:
                        if past_apartment_new_resident1[0]:
                            past_apartment_new_resident1 = (
                                past_apartment_new_resident1[0][0]
                            )
                        else:
                            past_apartment_new_resident1 = None
                    else:
                        past_apartment_new_resident1 = None

                    # When creating new apartment you want to update the past place a resident was sleeping at to EMPTY_BED_TEXT
                    #   no matter which bed he was lying on
                    if past_apartment_new_resident1:
                        c.execute(
                            f"""UPDATE {BUNK_BED_TABLE} SET {PERSON1_BUNK_TABLE} = '{EMPTY_BED_TEXT}' WHERE {APT_ID_BUNK_TABLE} = %s and {PERSON1_BUNK_TABLE} = %s""",
                            (
                                past_apartment_new_resident1,
                                name_bunk_bed1,
                            ),
                        )
                        c.execute(
                            f"""UPDATE {BUNK_BED_TABLE} SET {PERSON2_BUNK_TABLE} = '{EMPTY_BED_TEXT}' WHERE {APT_ID_BUNK_TABLE} = %s and {PERSON2_BUNK_TABLE} = %s""",
                            (
                                past_apartment_new_resident1,
                                name_bunk_bed1,
                            ),
                        )
                        c.execute(
                            f"""UPDATE {AMINACH_BED_TABLE} SET {PERSON1_AMINACH_TABLE} = '{EMPTY_BED_TEXT}' WHERE {APT_ID_AMINACH_TABLE} = %s and {PERSON1_AMINACH_TABLE} = %s""",
                            (
                                past_apartment_new_resident1,
                                name_bunk_bed1,
                            ),
                        )
                        conn.commit()

                # Retrieve the new resident past apartment if exists so I can remove him from his past apartment
                if new_resident2_id:
                    c.execute(
                        f"""SELECT {APT_RESIDENTS_TABLE} FROM {RESIDENTS_TABLE} WHERE {ID_RESIDENTS_TABLE} = %s""",
                        (new_resident2_id,),
                    )

                    past_apartment_new_resident2 = c.fetchall()

                    if past_apartment_new_resident2:
                        if past_apartment_new_resident2[0]:
                            past_apartment_new_resident2 = (
                                past_apartment_new_resident2[0][0]
                            )
                        else:
                            past_apartment_new_resident2 = None
                    else:
                        past_apartment_new_resident2 = None

                    # When creating new apartment you want to update the last place a resident was sleeping at to EMPTY_BED_TEXT
                    #   no matter which bed he was lying on
                    if past_apartment_new_resident2:
                        c.execute(
                            f"""UPDATE {BUNK_BED_TABLE} SET {PERSON2_BUNK_TABLE} = '{EMPTY_BED_TEXT}' WHERE {APT_ID_BUNK_TABLE} = %s and {PERSON2_BUNK_TABLE} = %s""",
                            (
                                past_apartment_new_resident2,
                                name_bunk_bed2,
                            ),
                        )
                        c.execute(
                            f"""UPDATE {BUNK_BED_TABLE} SET {PERSON1_BUNK_TABLE} = '{EMPTY_BED_TEXT}' WHERE {APT_ID_BUNK_TABLE} = %s and {PERSON1_BUNK_TABLE} = %s""",
                            (
                                past_apartment_new_resident2,
                                name_bunk_bed2,
                            ),
                        )
                        c.execute(
                            f"""UPDATE {AMINACH_BED_TABLE} SET {PERSON1_AMINACH_TABLE} = '{EMPTY_BED_TEXT}' WHERE {APT_ID_AMINACH_TABLE} = %s and {PERSON1_AMINACH_TABLE} = %s""",
                            (
                                past_apartment_new_resident2,
                                name_bunk_bed2,
                            ),
                        )
                        conn.commit()

                # Set the residents on this bunk bed with other metadata
                c.execute(
                    f"""INSERT INTO {BUNK_BED_TABLE} ({APT_ID_BUNK_TABLE}, {MATTRESS_COUNT_BUNK_TABLE}, {PERSON1_BUNK_TABLE}, {PERSON2_BUNK_TABLE}, {ROOM_ID_BUNK_TABLE}, {BED_ID_BUNK_TABLE}) VALUES (%s, 2, %s, %s, %s, %s);""",
                    (
                        apartment_id,
                        name_bunk_bed1,
                        name_bunk_bed2,
                        room_number,
                        bunk_bed_number,
                    ),
                )

                # Set the specified residents apartment number in database
                c.execute(
                    f"""UPDATE {RESIDENTS_TABLE} SET {APT_RESIDENTS_TABLE} = %s WHERE {ID_RESIDENTS_TABLE} = %s""",
                    (apartment_id, new_resident1_id),
                )
                c.execute(
                    f"""UPDATE {RESIDENTS_TABLE} SET {APT_RESIDENTS_TABLE} = %s WHERE {ID_RESIDENTS_TABLE} = %s""",
                    (apartment_id, new_resident2_id),
                )
                conn.commit()

        # If the aminach beds' quantity is None - redirect to the same page
        if aminach_beds_quantity:
            for aminach_bed_number in range(1, int(aminach_beds_quantity) + 1):
                # Retrieve the value of the resident option by the HTML element by the tag
                new_resident_aminach_bed = request.form.get(
                    f"inputAminachBed-newApt-{room_number}-{aminach_bed_number}"
                )

                new_resident_aminach_bed_id = None

                # Get the new resident unique id
                if (
                    new_resident_aminach_bed
                    and new_resident_aminach_bed != EMPTY_BED_TEXT
                ):
                    new_resident_aminach_bed_id = (
                        new_resident_aminach_bed.split(" - ")[0]
                    )

                # Retrieve the new resident past apartment if exists so I can delete him from his past apartment
                if new_resident_aminach_bed_id:
                    # Retrieve the new resident past apartment
                    c.execute(
                        f"""SELECT {APT_RESIDENTS_TABLE} FROM {RESIDENTS_TABLE} WHERE {ID_RESIDENTS_TABLE} = %s""",
                        (new_resident_aminach_bed_id,),
                    )

                    past_apartment_new_resident = c.fetchall()

                    # Validate that the apartment that was retrieved is not None
                    if past_apartment_new_resident:
                        if past_apartment_new_resident[0]:
                            past_apartment_new_resident = (
                                past_apartment_new_resident[0][0]
                            )
                        else:
                            past_apartment_new_resident = None
                    else:
                        past_apartment_new_resident = None

                    # When creating new apartment you want to update the past place a resident was sleeping at to EMPTY_BED_TEXT
                    #   no matter which bed he was lying on
                    if past_apartment_new_resident:
                        c.execute(
                            f"""UPDATE {AMINACH_BED_TABLE} SET {PERSON1_AMINACH_TABLE} = '{EMPTY_BED_TEXT}' WHERE {APT_ID_AMINACH_TABLE} = %s and {PERSON1_AMINACH_TABLE} = %s""",
                            (
                                past_apartment_new_resident,
                                new_resident_aminach_bed,
                            ),
                        )

                        c.execute(
                            f"""UPDATE {BUNK_BED_TABLE} SET {PERSON1_BUNK_TABLE} = '{EMPTY_BED_TEXT}' WHERE {APT_ID_BUNK_TABLE} = %s and {PERSON1_BUNK_TABLE} = %s""",
                            (
                                past_apartment_new_resident,
                                new_resident_aminach_bed,
                            ),
                        )

                        c.execute(
                            f"""UPDATE {BUNK_BED_TABLE} SET {PERSON2_BUNK_TABLE} = '{EMPTY_BED_TEXT}' WHERE {APT_ID_BUNK_TABLE} = %s and {PERSON2_BUNK_TABLE} = %s""",
                            (
                                past_apartment_new_resident,
                                new_resident_aminach_bed,
                            ),
                        )

                        conn.commit()

                # Set the resident on this aminach bed with other metadata
                c.execute(
                    f"""INSERT INTO {AMINACH_BED_TABLE} ({APT_ID_AMINACH_TABLE}, {MATTRESS_COUNT_AMINACH_TABLE}, {PERSON1_AMINACH_TABLE}, {ROOM_ID_AMINACH_TABLE}, {BED_ID_AMINACH_TABLE}) VALUES (%s, 1, %s, %s, %s);""",
                    (
                        apartment_id,
                        new_resident_aminach_bed,
                        room_number,
                        aminach_bed_number,
                    ),
                )

                # Set the specified resident apartment number in database
                c.execute(
                    f"""UPDATE {RESIDENTS_TABLE} SET {APT_RESIDENTS_TABLE} = %s WHERE {ID_RESIDENTS_TABLE} = %s""",
                    (apartment_id, new_resident_aminach_bed_id),
                )
                conn.commit()

    return redirect("/")


@app.route("/new-building", methods=["POST"])
def new_building():
    # if not session.get('logged_in'):
    #     return redirect("/login")
    
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    # Getting the form data object from the class "NewBuildingForm".
    form = NewBuildingForm()

    if form.validate_on_submit():
        new_building_number = int(form.title.data)

        if is_building_exist(new_building_number):
            flash(f"בניין {new_building_number} כבר קיים", "new-building")
            return redirect("/")

        c.execute(
            f"""INSERT INTO {BUILDING_TABLE} ({BUILDING_ID_BUILDING_TABLE}, {APT_COUNT_BUILDING_TABLE}) VALUES (%s, %s);""",
            (new_building_number, 0),
        )
        conn.commit()

    return redirect("/")


@app.route("/residents/new-resident", methods=["POST"])
def new_resident():
    if not session.get('logged_in'):
        return redirect("/login")
    
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    # Get NewResidentForm submitted data
    form = NewResidentForm()

    if request.method == "POST":
        full_name = form.full_name_field.data
        association = form.frame_selection_field.data
        gender = request.form.get("btnradio-resident")

        # Validate gender
        if gender not in VALID_GENDER_RADIO_VALUE:
            flash("מגדר צריך להיות זכר/נקבה/אחר!", "new-resident")
            return redirect("/residents")

        service = form.select_service_field.data
        is_beersheva_resident = form.is_beersheva_selection_field.data
        taz = "111111111" if form.taz_field.data == "" else form.taz_field.data

        c.execute(
        f"""INSERT INTO {RESIDENTS_TABLE} 
                    ({FULL_NAME_RESIDENTS_TABLE}, 
                    {ASSOCIATION_RESIDENTS_TABLE}, 
                    {GENDER_RESIDENTS_TABLE}, 
                    {SERVICE_RESIDENTS_TABLE}, 
                    {BEERSHEVA_RESIDENTS_TABLE}, 
                    {TAZ_RESIDENTS_TABLE}) 
                    VALUES 
                    (%s, %s, %s, %s, %s, %s) 
                    ON CONFLICT DO NOTHING;""",
        (full_name, association, gender, service, is_beersheva_resident, taz),
    )
    conn.commit()


    return redirect("/residents")


@app.route("/residents")
def residents():
    # Get residents data
    residents = get_residents_data()

    # Forms
    newResidentForm = NewResidentForm()

    return render_template(
        "residents.html", 
        newResidentForm=newResidentForm, 
        residents=residents, 
        is_logged_in=session.get('logged_in')
    )


@app.route("/get-residents-selection", methods=["GET"])
def get_residents_for_selection():
    # if not session.get('logged_in'):
    #     return redirect("/login")
    
    residents = get_residents_data()
    # Fetch the resident data from your data source
    residents_data = []

    for resident in residents:
        residents_data.append(
            [resident["full_name"], resident["association"], resident["id"]]
        )

    return jsonify(residents_data)


@app.route("/get-apartments-selection", methods=["GET"])
def get_apartments_for_selection():
    # if not session.get('logged_in'):
    #     return redirect("/login")
    
    apartments = get_apartments_data()
    # Fetch the resident data from your data source
    apartments_data = []

    for apartment in apartments:
        apartments_data.append(apartment["apt_id"])

    return jsonify(apartments_data)


@app.route("/get-frames-selection", methods=["GET"])
def get_frames_for_selection():
    # if not session.get('logged_in'):
    #     return redirect("/login")
    
    frames_data = [association.value for association in ChoiceFrameConsts]
    return jsonify(frames_data)


@app.route("/apt-data/<int:apt_id>")
def apt_data(apt_id): 
    '''
    This function is responsible to retrieve an apartment data to users.
    The data incudes everything, such as: Number of rooms in apartment, number of residents on each type of bed and eventually, who is sleeping on those beds.
    The function initialize a dictionary that will store all the data a room has and organize it as follows:
    A dictonary that stores every room number as a key and and a list of 2 dictionaries as a value (dict one for bunk beds and dict two for aminach beds).
    Every dictionary in that list will store every bed number as a key and a list of names that sleep on this bed as a value.
    Example of 2 rooms:
      {
       1: [{1: ["Idan", "Naor"],
            2: ["Noam", "Snir"],
            3: ["Itay", "Maor"],
            4: ["Sean", "Netanel"]},
           {1: ["Alice"],
            2: ["Hagar"],
            3: ["Michal"]}
          ],
       2: [{1: ["Eldad", "Guy"],
            2: ["Lior", "Almog"],
            3: ["Joseph", "Stav"],
            4: ["Lihi", "Ron"]},
           {1: ["Alice"],
            2: ["Hagar"],
            3: ["Michal"]}
          ]
      }
      @params: apt_id -> int.
      Returns: data (dictionary) -> json format.
    '''
    # Get data
    buildings = get_buildings_data()
    apartment = get_apartments_data(apt_id=apt_id)
    rooms_metadata = get_rooms_data(apt_id=apt_id)

    rooms_data = {}

    # Create a dictionary of all the data a room can have
    for room_number in range(1, len(rooms_metadata) + 1):
        # Get the data of a bunk bed and aminach bed that is related to a specific apartment and a specific room - list of one dict
        bunk_beds = get_bunk_beds(apt_id=apt_id, room_id=room_number)
        aminach_beds = get_aminach_beds(apt_id=apt_id, room_id=room_number)

        # Initialize dictionaries
        bunk_beds_dict = {}
        aminach_bed_dict = {}

        for bunk_bed_number in range(1, len(bunk_beds) + 1):
            bunk_beds_dict[bunk_bed_number] = [
                bunk_beds[bunk_bed_number - 1]["person1"],
                bunk_beds[bunk_bed_number - 1]["person2"],
            ]

        for aminach_bed_number in range(1, len(aminach_beds) + 1):
            aminach_bed_dict[aminach_bed_number] = [
                aminach_beds[aminach_bed_number - 1]["person1"]
            ]

        rooms_data[room_number] = [bunk_beds_dict, aminach_bed_dict]

    # Create a new dictionary with all the dictionaries' data
    data = {
        "buildings": buildings,
        "apartment": apartment,
        "rooms_metadata": rooms_metadata,
        "rooms_data": rooms_data,
    }

    # Convert the dictionary to JSON and return it
    return jsonify(data)


@app.route("/upload-excel-residents", methods=["POST", "GET"])
def upload_excel_residents():
    if not session.get('logged_in'):
        return redirect("/login")
    
    if request.method != "POST":
        return redirect("/residents")
    
    if "upload-excel-residents" not in request.files:
        flash(f"צריך לבחור קובץ!", "residents-upload")
        return redirect("/residents")

    file = request.files["upload-excel-residents"]
    if file.filename == "":
        flash(f"צריך לבחור קובץ!", "residents-upload")
        return redirect("/residents")

    if file and allowed_file(file.filename):
        dataframe = pd.read_excel(file, header=None)
        save_xlsx_residents(dataframe=dataframe)

    return redirect("/residents")


@app.route("/download-excel-residents-template", methods=["GET"])
def download_excel_residents_template():
    if not session.get('logged_in'):
        return redirect("/login")
    
    file_path = DOWNLOAD_TEMPLATE_XLSX
    return send_file(file_path, as_attachment=True)


@app.route("/download-excel-residents-current", methods=["GET"])
def download_excel_residents_current():
    '''
    This function will download the current file which stores all the residents existed in the website.
    @params: None.
    Returns: send_file() -> function that downloads the file in browsers.
    '''  
    path_to_file = create_current_residents_xlsx_file()
    download_name = 'current-residents-' + datetime.now().strftime('%d-%m-%Y-%H-%M') + '.xlsx'
    return send_file(path_to_file, download_name=download_name, as_attachment=True)


@app.route("/is-logged-in", methods=["GET"])
def is_logged_in() -> bool:
    '''
    This function will be called by an ajax request from the script.js file.
    It will return True if user is logged in, or false otherwise.
    @params: None.
    Returns: Boolean
    '''
    is_logged_in = True if session.get('logged_in') else False
    return jsonify({'is_logged_in': is_logged_in})


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect("/")


@app.route("/login", methods=["POST", "GET"])
def login():
    newUserForm = NewUserForm()

    if request.method == "GET":
        return render_template("login.html", newUserForm=newUserForm)
    
    if request.method == "POST":
        username = newUserForm.username.data
        password = newUserForm.password.data

        usernames_in_db = get_usernames_from_db()
        passwords_in_db = get_passwords_from_db()

        if username in usernames_in_db:
            index_username = usernames_in_db.index(username)
            if password == passwords_in_db[index_username]:
                session['logged_in'] = True
                return redirect("/")
            else:
                flash("Wrong password!", "wrong-input")
        else:
            flash("This username doesn't exist!", "wrong-input")

    return redirect("/login")


@app.route("/")
def home():
    # Get buildings and apartments data
    buildings = get_buildings_data()
    apartments = get_apartments_data()
    rooms = get_rooms_data()
    bunk_beds = get_bunk_beds()
    aminach_beds = get_aminach_beds()
    beds_quantity_info = get_beds_quantity_by_gender()

    # Forms
    newBuildingForm = NewBuildingForm()
    newApartmentForm = NewApartmentForm()

    return render_template(
        "home.html",
        newBuildingForm=newBuildingForm,
        newApartmentForm=newApartmentForm,
        buildings=buildings,
        apartments=apartments,
        rooms=rooms,
        bunk_beds=bunk_beds,
        aminach_beds=aminach_beds,
        beds_quantity_info=beds_quantity_info,
        is_logged_in=session.get('logged_in')
    )


if __name__ == "__main__":
    app.run(debug=True)
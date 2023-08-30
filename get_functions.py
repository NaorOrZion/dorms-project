from consts import *
from typing import List, Dict
from db import get_db


def get_buildings_data() -> List[Dict[str, int]]:
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    # Buildings data
    buildings = []
    c.execute(
        f"""SELECT * FROM {BUILDING_TABLE} ORDER BY {BUILDING_ID_BUILDING_TABLE} ASC;"""
    )
    buildings_from_db = c.fetchall()
    
    if not buildings_from_db:
        return buildings

    for row in buildings_from_db:
        building = {"building_id": row[0], "apt_count": row[1]}
        buildings.append(building)

    return buildings



def get_residents_data() -> List[Dict[str, int]]:
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    # Residents data
    residents = []
    c.execute(
        f"""SELECT * FROM {RESIDENTS_TABLE} ORDER BY {ID_RESIDENTS_TABLE} ASC;"""
    )
    residents_from_db = c.fetchall()

    if not residents_from_db:
        return residents

    for row in residents_from_db:
        resident = {
            "id": row[0],
            "full_name": row[1],
            "association": row[2],
            "gender": row[3],
            "service": row[4],
            "beersheva": row[5],
            "taz": row[6],
            "apartment": row[7],
        }
        residents.append(resident)

    return residents


# Notice to call this function with one argument only, if for example
#   an apt_id is sent and along side a gender is sent, only the apt_id data will be sent.
#   building_id -> apt_id - > gender -> all
def get_apartments_data(apt_id=None, building_id=None, gender=None) -> List[Dict[str, int]]:
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    # Apartments data
    apartments = []

    # The only situation where a building_id is not None is when there was
    #   a call from a function to retrieve all the apartments of a building.
    if building_id is not None:
        c.execute(
            f"""SELECT * FROM {APARTMENTS_TABLE} WHERE {BUILDING_ID_APT_TABLE} = %s ORDER BY {APT_ID_APT_TABLE} ASC;""",
            (building_id,),
        )

    # Single apartment data
    elif apt_id is not None:
        c.execute(
            f"""SELECT * FROM {APARTMENTS_TABLE} WHERE {APT_ID_APT_TABLE} = %s;""",
            (apt_id,),
        )

    # Get all of the gender's apartments
    elif gender is not None:
       c.execute(
            f"""SELECT * FROM {APARTMENTS_TABLE} WHERE {GENDER_APT_TABLE} = %s;""",
            (gender,),
        )

    # Get all apartments
    else:
        c.execute(
            f"""SELECT * FROM {APARTMENTS_TABLE} ORDER BY {APT_ID_APT_TABLE} ASC;"""
        )

    apartments_from_db = c.fetchall()

    if not apartments_from_db:
        return apartments

    for row in apartments_from_db:
        apartment = {
            "apt_id": row[0],
            "rooms_in_apt": row[1],
            "gender": row[2],
            "building_id": row[3],
        }
        apartments.append(apartment)

    return apartments


# Get all the rooms data, you can get it all or get a specific apartment data only.
def get_rooms_data(apt_id=None) -> List[Dict[str, int]]:
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    # Rooms data
    rooms = []

    # If an apartment id has been sent, get it's rooms.
    if apt_id:
        c.execute(
            f"""SELECT * FROM {ROOMS_TABLE} WHERE {APT_ID_ROOM_TABLE} = %s ORDER BY {ROOM_ID_ROOM_TABLE} ASC;""",
            (apt_id,),
        )
    else:
        c.execute(
            f"""SELECT * FROM {ROOMS_TABLE} ORDER BY {ROOM_ID_ROOM_TABLE} ASC;"""
        )

    rooms_from_db = c.fetchall()

    if not rooms_from_db:
        return rooms

    for row in rooms_from_db:
        room = {
            "apt_id": row[0],
            "room_id": row[1],
            "aminach_beds": row[2],
            "bunk_beds": row[3],
        }
        rooms.append(room)

    return rooms


# Get bunk beds data, can send 2 or 1 argument, the funcion knows how to handle it
#   and give data accordingly.
def get_bunk_beds(apt_id=None, room_id=None) -> List[Dict[str, int]]:
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    # Bunk beds data
    bunk_beds = []

    # If an apartment id and a room id have been sent, get it's bunk beds values.
    if room_id is not None and apt_id is not None:
        c.execute(
            f"""SELECT * FROM {BUNK_BED_TABLE} WHERE {APT_ID_BUNK_TABLE} = %s and {ROOM_ID_BUNK_TABLE} = %s ORDER BY {ROOM_ID_BUNK_TABLE} ASC;""",
            (apt_id, room_id),
        )

    # If an apartment id has been sent, get it's bunk beds values.
    elif room_id is None and apt_id is not None:
        c.execute(
            f"""SELECT * FROM {BUNK_BED_TABLE} WHERE {APT_ID_BUNK_TABLE} = %s ORDER BY {ROOM_ID_BUNK_TABLE} ASC;""",
            (apt_id,),
        )

    # If a room id has been sent, get it's bunk beds values.
    elif room_id is not None and apt_id is None:
        c.execute(
            f"""SELECT * FROM {BUNK_BED_TABLE} WHERE {ROOM_ID_BUNK_TABLE} = %s ORDER BY {ROOM_ID_BUNK_TABLE} ASC;""",
            (room_id,),
        )

    # If nothing has been sent, get all bunk beds values.
    elif room_id is None and apt_id is None:
        c.execute(
            f"""SELECT * FROM {BUNK_BED_TABLE} ORDER BY {APT_ID_BUNK_TABLE} ASC, {ROOM_ID_BUNK_TABLE} ASC;"""
        )

    bunk_beds_from_db = c.fetchall()

    if not bunk_beds_from_db:
        return bunk_beds

    # Apply data to dictionary
    for row in bunk_beds_from_db:
        bunk_bed = {
            "apt_id": row[0],
            "bed_id": row[1],
            "mattress_count": row[2],
            "person1": row[3],
            "person2": row[4],
            "room_id": row[5],
        }
        bunk_beds.append(bunk_bed)

    return bunk_beds


# Get aminach beds data, can send 2 or 1 argument, the funcion knows how to handle it
#   and give data accordingly.
def get_aminach_beds(apt_id=None, room_id=None) -> List[Dict[str, int]]:
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    # aminach beds data
    aminach_beds = []

    # If an apartment id and a room id have been sent, get it's aminach beds values.
    if room_id is not None and apt_id is not None:
        c.execute(
            f"""SELECT * FROM {AMINACH_BED_TABLE} WHERE {APT_ID_AMINACH_TABLE} = %s and {ROOM_ID_BUNK_TABLE} = %s ORDER BY {ROOM_ID_BUNK_TABLE} ASC;""",
            (apt_id, room_id),
        )

    # If an apartment id has been sent, get it's aminach beds values.
    elif room_id is None and apt_id is not None:
        c.execute(
            f"""SELECT * FROM {AMINACH_BED_TABLE} WHERE {APT_ID_AMINACH_TABLE} = %s ORDER BY {ROOM_ID_BUNK_TABLE} ASC;""",
            (apt_id,),
        )

    # If a room id has been sent, get it's aminach beds values.
    elif room_id is not None and apt_id is None:
        c.execute(
            f"""SELECT * FROM {AMINACH_BED_TABLE} WHERE {ROOM_ID_BUNK_TABLE} = %s ORDER BY {ROOM_ID_BUNK_TABLE} ASC;""",
            (room_id,),
        )

    # If a nothing has been sent, get all aminach beds values.
    elif room_id is None and apt_id is None:
        c.execute(
            f"""SELECT * FROM {AMINACH_BED_TABLE} ORDER BY {APT_ID_AMINACH_TABLE} ASC, {ROOM_ID_BUNK_TABLE} ASC;"""
        )

    aminach_beds_from_db = c.fetchall()

    if not aminach_beds_from_db:
        return aminach_beds

    for row in aminach_beds_from_db:
        aminach_bed = {
            "apt_id": row[0],
            "bed_id": row[1],
            "mattress_count": row[2],
            "person1": row[3],
            "room_id": row[4],
        }
        aminach_beds.append(aminach_bed)

    return aminach_beds


def get_beds_quantity_by_gender() -> Dict[str, int]:
    male_apartments = get_apartments_data(gender=VALID_GENDER_RADIO_VALUE[0])
    female_apartments = get_apartments_data(gender=VALID_GENDER_RADIO_VALUE[1])
    unknown_apartments = get_apartments_data(gender=VALID_GENDER_RADIO_VALUE[2])

    male_empty_bunk_beds_quantity = 0
    male_empty_aminach_quantity = 0
    male_existing_bunk_beds_quantity = 0
    male_existing_aminach_quantity = 0

    female_empty_bunk_beds_quantity = 0
    female_empty_aminach_quantity = 0
    female_existing_bunk_beds_quantity = 0
    female_existing_aminach_quantity = 0

    unknown_empty_bunk_beds_quantity = 0
    unknown_empty_aminach_quantity = 0
    unknown_existing_bunk_beds_quantity = 0
    unknown_existing_aminach_quantity = 0

    for apartment in male_apartments:
        male_empty_bunk_beds_quantity += sum(
            [
                bunk_bed["person1"].count(EMPTY_BED_TEXT)
                + bunk_bed["person2"].count(EMPTY_BED_TEXT)
                for bunk_bed in get_bunk_beds(apt_id=apartment["apt_id"])
            ]
        )
        male_empty_aminach_quantity += sum(
            [
                aminach_bed["person1"].count(EMPTY_BED_TEXT)
                for aminach_bed in get_aminach_beds(apt_id=apartment["apt_id"])
            ]
        )
        male_existing_bunk_beds_quantity += sum(
            [
                bunk_bed["mattress_count"]
                for bunk_bed in get_bunk_beds(apt_id=apartment["apt_id"])
            ]
        )
        male_existing_aminach_quantity += sum(
            [
                aminach_bed["mattress_count"]
                for aminach_bed in get_aminach_beds(apt_id=apartment["apt_id"])
            ]
        )

    for apartment in female_apartments:
        female_empty_bunk_beds_quantity += sum(
            [
                bunk_bed["person1"].count(EMPTY_BED_TEXT)
                + bunk_bed["person2"].count(EMPTY_BED_TEXT)
                for bunk_bed in get_bunk_beds(apt_id=apartment["apt_id"])
            ]
        )
        female_empty_aminach_quantity += sum(
            [
                aminach_bed["person1"].count(EMPTY_BED_TEXT)
                for aminach_bed in get_aminach_beds(apt_id=apartment["apt_id"])
            ]
        )
        female_existing_bunk_beds_quantity += sum(
            [
                bunk_bed["mattress_count"]
                for bunk_bed in get_bunk_beds(apt_id=apartment["apt_id"])
            ]
        )
        female_existing_aminach_quantity += sum(
            [
                aminach_bed["mattress_count"]
                for aminach_bed in get_aminach_beds(apt_id=apartment["apt_id"])
            ]
        )

    for apartment in unknown_apartments:
        unknown_empty_bunk_beds_quantity += sum(
            [
                bunk_bed["person1"].count(EMPTY_BED_TEXT)
                + bunk_bed["person2"].count(EMPTY_BED_TEXT)
                for bunk_bed in get_bunk_beds(apt_id=apartment["apt_id"])
            ]
        )
        unknown_empty_aminach_quantity += sum(
            [
                aminach_bed["person1"].count(EMPTY_BED_TEXT)
                for aminach_bed in get_aminach_beds(apt_id=apartment["apt_id"])
            ]
        )
        unknown_existing_bunk_beds_quantity += sum(
            [
                bunk_bed["mattress_count"]
                for bunk_bed in get_bunk_beds(apt_id=apartment["apt_id"])
            ]
        )
        unknown_existing_aminach_quantity += sum(
            [
                aminach_bed["mattress_count"]
                for aminach_bed in get_aminach_beds(apt_id=apartment["apt_id"])
            ]
        )

    beds_quantity_info = {
        "male_empty_bunk_beds": male_empty_bunk_beds_quantity,
        "male_empty_aminach_beds": male_empty_aminach_quantity,
        "male_existing_bunk_beds": male_existing_bunk_beds_quantity,
        "male_existing_aminach_beds": male_existing_aminach_quantity,
        "female_empty_bunk_beds": female_empty_bunk_beds_quantity,
        "female_empty_aminach_beds": female_empty_aminach_quantity,
        "female_existing_bunk_beds": female_existing_bunk_beds_quantity,
        "female_existing_aminach_beds": female_existing_aminach_quantity,
        "unknown_empty_bunk_beds": unknown_empty_bunk_beds_quantity,
        "unknown_empty_aminach_beds": unknown_empty_aminach_quantity,
        "unknown_existing_bunk_beds": unknown_existing_bunk_beds_quantity,
        "unknown_existing_aminach_beds": unknown_existing_aminach_quantity,
    }

    return beds_quantity_info


def get_bunk_bed_residents_id_in_room(apt_id, room_id) -> List[str]:
    """
    This function gets as a parameter an apt id and a room id.
    The function returns a clean list of all the bunk beds residents' ids lying on the bed in a specific apt in a specific room.
    """
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    c.execute(
        f"""SELECT {PERSON1_BUNK_TABLE}, {PERSON2_BUNK_TABLE} FROM {BUNK_BED_TABLE} WHERE {APT_ID_BUNK_TABLE} = %s and {ROOM_ID_BUNK_TABLE} = %s;""",
        (apt_id, room_id),
    )

    residents_data = c.fetchall()

    residents = [
        item.split(" - ")[0]
        for tup in residents_data
        for item in tup
        if item != EMPTY_BED_TEXT
    ]
    return residents


def get_aminach_bed_residents_id_in_room(apt_id, room_id) -> List[str]:
    """
    This function gets as a parameter an apt id and a room id.
    The function returns a clean list of all the aminach beds residents' id lying on the bed.
    """
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    c.execute(
        f"""SELECT {PERSON1_AMINACH_TABLE} FROM {AMINACH_BED_TABLE} WHERE {APT_ID_AMINACH_TABLE} = %s and {ROOM_ID_AMINACH_TABLE} = %s and {PERSON1_AMINACH_TABLE} != '{EMPTY_BED_TEXT}';""",
        (apt_id, room_id),
    )

    residents_data = c.fetchall()

    if not residents_data:
        return []

    residents = [item[0].split(" - ")[0] for item in residents_data]
    return residents


def get_past_rooms_quantity_of_apt(apt_id) -> int:
    '''
    This funciton will get the past rooms' quantity of the given apatrment.
    @param: apt_id -> str/int
    Returns: int
    '''
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    # Get the past rooms quantity of the apartment
    c.execute(
        f"""SELECT {ROOMS_IN_APT_TABLE} FROM {APARTMENTS_TABLE} WHERE {APT_ID_APT_TABLE} = %s;""",
        (apt_id,),
    )
    
    past_rooms_quantity = c.fetchall()
    past_rooms_quantity = past_rooms_quantity[0][0]

    return past_rooms_quantity


def get_apt_ids_by_apartments(apartments) -> List[str]:
    '''
    This function gets an apartment parameter as "List[Dict[str, int]]".
    It returns a list of the apartments' ids as a string.
    @params: apartments        ->  List[Dict[str, int]].
    Returns: a list of strings ->  List[str].
    '''
    apartments_ids = []

    for apt in apartments:
        apartments_ids.append(apt['apt_id'])

    return apartments_ids
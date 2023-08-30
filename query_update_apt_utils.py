from db import get_db
from consts import *
from get_functions import *


def update_new_metadata_of_apt(apartment_id, rooms_quantity, gender, existing_apt_id) -> None:
    '''
    This function will update the new metadata of the updated apartment, like: apartment id and rooms quantity.
    @params: apartment_id -> str/int, rooms_quantity -> str/int, gender -> str, existing_apt_id -> str/int.
    Returns: None
    '''
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    # Update apartment's data to database
    c.execute(
        f"""UPDATE {APARTMENTS_TABLE} SET {APT_ID_APT_TABLE}=%s, {ROOMS_IN_APT_TABLE}=%s, {GENDER_APT_TABLE}=%s WHERE {APT_ID_APT_TABLE}=%s;""",
        (apartment_id, rooms_quantity, gender, existing_apt_id),
    )
    conn.commit()


def delete_beds_by_apt(apt_id) -> None:
    '''
    This function will delete all the beds from bunk_bed and aminach_bed tables by given apartment id.
    @params: apt_id -> str/int.
    Returns: None
    '''
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    # Update bunk bed and aminach bed tables query
    c.execute(
        f"""DELETE from {BUNK_BED_TABLE} WHERE {APT_ID_BUNK_TABLE}=%s;""",
        (apt_id,)
    )
    c.execute(
        f"""DELETE from {AMINACH_BED_TABLE} WHERE {APT_ID_AMINACH_TABLE}=%s;""",
        (apt_id,)
    )
    conn.commit()


def update_residents_to_null_by_apt(apt_id) -> None:
    '''
    This function will update the residents table to NULL by given apartment id.
    @params: apt_id -> str, int.
    Returns: None
    '''
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    # Update residents tables query, set resident to NULL by apartment id.
    c.execute(
        f"""UPDATE {RESIDENTS_TABLE} SET {APT_RESIDENTS_TABLE} = NULL WHERE {APT_RESIDENTS_TABLE} = %s;""",
        (apt_id,)
    )
    conn.commit()


def update_residents_apt_to_null(apt_id, room_id) -> None:
    '''
    This function will update the resident's apartment to NULL by a given room of a specific apartment.
    @params: apt_id -> str/int, room_id -> str/int.
    Returns: None
    '''
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    # Get a list[str] of the ids of the residents from this specific apartment in the specific room.
    bunk_bed_residents_id = get_bunk_bed_residents_id_in_room(
        apt_id=apt_id, room_id=room_id
    )
    amianch_bed_residents_id = get_aminach_bed_residents_id_in_room(
        apt_id=apt_id, room_id=room_id
    )
    ids = list(set(bunk_bed_residents_id + amianch_bed_residents_id))

    # Iterate over the ids of the residents and update their apartment to NULL. 
    for id in ids:
        c.execute(
            f"""UPDATE {RESIDENTS_TABLE} SET {APT_RESIDENTS_TABLE} = NULL WHERE {ID_RESIDENTS_TABLE} = %s;""",
            (id,),
        )
        conn.commit()


def update_room_new_metadata(new_apartment_id, new_room_number, new_aminach_beds_quantity, new_bunk_beds_quantity, existing_apt_id) -> None:
    '''
    This function updates the room with the new room number, the new quantity selected to the aminach beds, 
    the new quantity selected to the bunk beds.
    @params: new_apartment_id -> str/int, new_room_number -> str/int, new_aminach_beds_quantity -> str/int, new_bunk_beds_quantity -> str/int, existing_apt_id -> str/int.
    Returns: None
    '''
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    c.execute(
        f"""UPDATE {ROOMS_TABLE} SET {APT_ID_ROOM_TABLE}=%s, {ROOM_ID_ROOM_TABLE}=%s, {AMINACH_BED_ROOM_TABLE}=%s, {BUNK_BED_ROOM_TABLE}=%s WHERE {APT_ID_ROOM_TABLE}=%s and {ROOM_ID_ROOM_TABLE}=%s;""",
        (
            new_apartment_id,
            new_room_number,
            new_aminach_beds_quantity,
            new_bunk_beds_quantity,
            existing_apt_id,
            new_room_number
        )
    )
    conn.commit()


def create_new_room(new_apartment_id, new_room_number, new_aminach_beds_quantity, new_bunk_beds_quantity) -> None:
    '''
    This function will create a new room in the rooms table query.
    @params:
    Returns: 
    '''
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    c.execute(
        f"""INSERT INTO {ROOMS_TABLE} ({APT_ID_ROOM_TABLE}, {ROOM_ID_ROOM_TABLE}, {AMINACH_BED_ROOM_TABLE}, {BUNK_BED_ROOM_TABLE}) VALUES (%s, %s, %s, %s)""",
        (
            new_apartment_id,
            new_room_number,
            new_aminach_beds_quantity,
            new_bunk_beds_quantity
        )
    )
    conn.commit()


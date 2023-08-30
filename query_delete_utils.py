from db import get_db
from consts import *
from get_functions import *


def delete_apt_from_query(apt_id) -> None:
    '''
    This function will delete a single apartment from query.
    First of all it will delete the apartment from apartments table, 
    then the rooms in the apartment from rooms table,
    after that it will remove all beds from aminach_bed and bunk_bed tables,
    and eventually remove the resident's apartment from the residents table.
    @param: apt_id -> str/int.
    Returns: None 
    '''
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    # Execute query
    # Delete apartment from apartments table
    c.execute(
        f"""DELETE FROM {APARTMENTS_TABLE} WHERE {APT_ID_APT_TABLE} = %s;""",
        (apt_id,),
    )

    # Delete rooms in apt from rooms table
    c.execute(
        f"""DELETE FROM {ROOMS_TABLE} WHERE {APT_ID_ROOM_TABLE} = %s;""",
        (apt_id,),
    )

    # Delete aminach beds from aminach beds table 
    c.execute(
        f"""DELETE FROM {AMINACH_BED_TABLE} WHERE {APT_ID_AMINACH_TABLE} = %s;""",
        (apt_id,),
    )

    # Delete bunk beds from bunk beds table 
    c.execute(
        f"""DELETE FROM {BUNK_BED_TABLE} WHERE {APT_ID_BUNK_TABLE} = %s;""",
        (apt_id,),
    )

    # Update the apartment of resident which was sleeping before to NULL
    c.execute(
        f"""UPDATE {RESIDENTS_TABLE} SET {APT_RESIDENTS_TABLE} = NULL WHERE {APT_RESIDENTS_TABLE} = %s""",
        (apt_id,),
    )
    
    conn.commit()


def delete_building_from_query(building_id) -> None:
    '''
    This function will delete a building from the db.
    First of all it will delete the building form query, then the apartments.
    @params: building_id -> int
    Returns: None
    '''
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    # Get apartments data
    apartments = get_apartments_data(building_id=building_id)

    # Delete building from buildings table
    c.execute(
        f"""DELETE FROM {BUILDING_TABLE} WHERE {BUILDING_ID_BUILDING_TABLE} = %s""",
        (building_id,),
    )
    conn.commit()

    # Delete apartments from apartments table
    for apt in apartments:
        delete_apt_from_query(apt_id=apt["apt_id"])

    
def delete_residents_by_id(residents_ids):
    '''
    This function will delete residents from db by a given list of the residents' ids.
    It will delete residents from their beds if there are any beds related to them and will delete residents from residents table right after it.
    @params: residents_ids -> List[str].
    Returns: None.
    '''
    # Getting the database
    conn = get_db()
    c = conn.cursor()

    if not residents_ids:
        return
    
    all_residents = get_residents_data()
    selected_residents = []

    for resident in all_residents:
        resident_id = str(resident['id'])
        if resident_id in residents_ids:
            resident_bed_name = f"{resident_id} - {resident['full_name']} - {resident['association']}"
            selected_residents.append(resident_bed_name)

    # Format query string to execute deletion to many residents at once from aminach table
    # Execute deletion query
    query_string = f"UPDATE {AMINACH_BED_TABLE} SET {PERSON1_AMINACH_TABLE} = '{EMPTY_BED_TEXT}' WHERE {PERSON1_AMINACH_TABLE} in (%s)" % ','.join(['%s'] * len(selected_residents))
    c.execute(query_string, selected_residents)

    # Format query string to execute deletion to many residents at once from bunk bed table which sleep on the top bed
    # Execute deletion query
    query_string = f"UPDATE {BUNK_BED_TABLE} SET {PERSON1_BUNK_TABLE} = '{EMPTY_BED_TEXT}' WHERE {PERSON1_BUNK_TABLE} in (%s)" % ','.join(['%s'] * len(selected_residents))
    c.execute(query_string, selected_residents)

    # Format query string to execute deletion to many residents at once from bunk bed table which sleep on the lower bed
    # Execute deletion query
    query_string = f"UPDATE {BUNK_BED_TABLE} SET {PERSON2_BUNK_TABLE} = '{EMPTY_BED_TEXT}' WHERE {PERSON2_BUNK_TABLE} in (%s)" % ','.join(['%s'] * len(selected_residents))
    c.execute(query_string, selected_residents)

    # Format query string to execute deletion to many ids at once from residents table
    # Execute deletion query
    query_string = f"DELETE from {RESIDENTS_TABLE} WHERE {ID_RESIDENTS_TABLE} in (%s)" % ','.join(['%s'] * len(residents_ids))
    c.execute(query_string, residents_ids)

    conn.commit()
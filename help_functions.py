from consts import *
from flask import flash
from get_functions import *


def is_building_exist(new_building_id):
    buildings = get_buildings_data()

    for building in buildings:
        if building["building_id"] == new_building_id:
            return True

    return False


def is_apartment_exist(new_apartment_id):
    apartments = get_apartments_data()

    for apartment in apartments:
        if apartment["apt_id"] == new_apartment_id:
            return True

    return False


def valid_apt_form_sub(
    new_apartment_id=None, existing_apt_id=None, gender=None, rooms_quantity=None
) -> bool:
    '''
    This funciton will valid the apartments form submission by checking if the
    apartment id exists, if the gender is not None and valid and if the rooms_quantity 
    is not none.
    @params: new_apartment_id -> int, existing_apt_id -> int, gender -> str, rooms_quantity -> str.
    Returns: Boolean.
    '''
    if existing_apt_id:
        if new_apartment_id:
            if (
                is_apartment_exist(new_apartment_id)
                and new_apartment_id != existing_apt_id
            ):
                flash(f"דירה {new_apartment_id} כבר קיימת!", "new-apartment")
                return False

        if gender is None:
            flash(f"צריך לבחור מגדר לחדר!", "new-apartment")
            return False

        if gender not in VALID_GENDER_RADIO_VALUE:
            flash(f"בלי שטיקים! אפשר לבחור רק זכר/נקבה/אחר.", "new-apartment")
            return False

        if rooms_quantity is None:
            return False
    
    return True
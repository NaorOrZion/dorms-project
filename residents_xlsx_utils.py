import pandas as pd
import openpyxl
import re

from openpyxl.worksheet.table import Table, TableStyleInfo
from get_functions import get_residents_data
from flask import flash
from db import get_db
from consts import *


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_xlsx_residents(dataframe):
    try:
        # Create an empty list to store the data
        new_residents = dataframe.values.tolist()
    except:
        flash("הקובץ לא נתמך, יש להשתמש בתבנית המוכנה!", "residents-upload")
        return

    # Validate and save xlsx file to database
    if validate_xlsx_data(new_residents=new_residents):
        # Getting the database
        conn = get_db()
        c = conn.cursor()

        for i, row in enumerate(new_residents):
            # Skip the headers in first iteration
            if i == 0:
                continue

            full_name = row[0]
            frame = row[1]
            gender = row[2]
            service = row[3]
            live_in_beersheva = row[4]
            taz = row[5]

            # Load to database
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
                        (full_name, frame, gender, service, live_in_beersheva, taz),
            )
            conn.commit()


            # Save changes
            conn.commit()

        # Notify success
        flash(f"הקובץ הועלה בהצלחה", "residents-upload")
        #delete_xlsx_file(file_path=UPLOAD_FOLDER + file_name)


def validate_xlsx_data(new_residents):
    # Handle no values in the excel
    try:
        new_residents_headers = new_residents[0]
    except:
        new_residents_headers = None

    if not new_residents_headers:
        flash("הטבלה לא תקינה, השתדלו להשתמש בתבנית המוכנה!", "residents-upload")
        return False

    # Validate headers's length
    if len(new_residents_headers) != 6:
        flash("אורך העמודות לא תקין, השתמשו בתבנית המוכנה!", "residents-upload")
        return False

    # Validate headers
    is_valid_headers_value = [
        True if header in RESIDENTS_CHART_HEADERS else False
        for header in new_residents_headers
    ]
    is_valid_headers_order = (
        False if RESIDENTS_CHART_HEADERS != new_residents_headers else True
    )
    if False in is_valid_headers_value and is_valid_headers_order is False:
        flash("ראשי העמודות לא תקינים, השתמשו בתבנית המוכנה!", "residents-upload")
        return False

    for i, row in enumerate(new_residents):
        # Skip the headers in first iteration
        if i == 0:
            continue

        # List of all the validations possible
        xlsx_validation_list = [
            is_new_resident_name_valid(row[0], row=i+1),
            is_new_frame_valid(row[1], row=i+1),
            is_new_gender_valid(row[2], row=i+1),
            is_new_service_valid(row[3], row=i+1),
            is_new_beersheva_valid(row[4], row=i+1),
            is_new_id_valid(row[5], row=i+1),
        ]

        # If there is any False validation, return None
        if False in xlsx_validation_list:
            #delete_xlsx_file(file_path=UPLOAD_FOLDER + file_name)
            return False

    # The validation is valid
    return True


def is_new_resident_name_valid(full_name, row) -> bool:
    # Define the maximum length of the full_name
    max_length = 25

    if not full_name:
        flash(f"בשורה {row} יש שם מלא ריק", "residents-upload")
        return False

    # Check if the full_name is longer than the maximum length
    if len(full_name) > max_length:
        flash(f"אורך השם בשורה {row} גדול מ-{max_length}!", "residents-upload")
        return False

    # Define the regular expression pattern
    pattern = r"^[a-zA-Z0-9\u0590-\u05FF ]+$"

    # Use the search method to check if the full_name matches the pattern
    match = re.search(pattern, full_name)

    # Return True if there is a match, False otherwise
    if bool(match) == False:
        flash(
            f"שורה {row}: שם צריך להכיל אך ורק אותיות בעברית/אנגלית ומספרים ללא תווים מיוחדים!",
            "residents-upload",
        )
        return bool(match)
    else:
        return True


def is_new_frame_valid(frame, row) -> bool:
    if frame:
        if frame not in [frame.value for frame in ChoiceFrameConsts]:
            flash(
                f"בשורה {row} המסגרת לא נמצאת ברשימת המסגרות האפשריות!",
                "residents-upload",
            )
            return False
    else:
        flash(f"התא בשורה {row} בעל מסגרת ריקה", "residents-upload")
        return False

    return True


def is_new_gender_valid(gender, row) -> bool:
    if gender:
        if gender not in [gender.value for gender in ChoiceGenderConsts]:
            flash(
                f"בשורה {row} המגדר לא נמצאת ברשימת המגדרים האפשריים!",
                "residents-upload",
            )
            return False
    else:
        flash(f"בשורה {row} יש תא ריק!", "residents-upload")
        return False

    return True


def is_new_service_valid(service, row):
    if service:
        if service not in [service.value for service in ChoiceServicesConsts]:
            flash(f"בשורה {row} יש סוג שירות שאינו קיים!", "residents-upload")
            return False
    else:
        flash(f"בשורה {row} יש תא עם סוג שירות ריק!", "residents-upload")
        return False

    return True


def is_new_beersheva_valid(is_beersheva, row) -> bool:
    if is_beersheva:
        if is_beersheva not in [
            is_beersheva.value for is_beersheva in ChoiceIsBeershevaResidentConsts
        ]:
            flash(
                f"שורה {row}: העמודה 'גר/ה בבאר שבע' יכולה להכיל רק כן/לא בלבד!",
                "residents-upload",
            )
            return False
    else:
        flash(f"בשורה {row} יש תא מסוג 'גר/ה בבאר שבע' שהוא ריק!", "residents-upload")
        return False

    return True


def is_new_id_valid(ID, row) -> bool:
    if len(ID) != 9:
        flash(f"בשורה {row} אורך תעודת הזהות: {ID} לא תקין!", "residents-upload")
        return False

    try:
        id = list(map(int, ID))
    except:
        flash(f"בשורה {row} תעודת הזהות: {ID} לא תקינה!", "residents-upload")
        return False

    counter = 0

    for i in range(9):
        id[i] *= (i % 2) + 1
        if id[i] > 9:
            id[i] -= 9
        counter += id[i]

    if (counter % 10) == 0:
        return True
    else:
        flash(f"בשורה {row} תעודת הזהות: {ID} לא תקינה!", "residents-upload")
        return False
    

def create_current_residents_xlsx_file() -> str:
    '''
    This function will retrieve the data of all residents and will make an
      xlsx copy out of it arranged like the "upload residents template" file.
    @params: None.
    Returns: path to created file -> str
    '''
    residents_data = get_residents_data()
    book = openpyxl.Workbook()
    sheet = book.active

    # Add column headings
    sheet.append([
                RESIDENTS_CHART_HEADERS[0], 
                RESIDENTS_CHART_HEADERS[1], 
                RESIDENTS_CHART_HEADERS[2], 
                RESIDENTS_CHART_HEADERS[3], 
                RESIDENTS_CHART_HEADERS[4], 
                RESIDENTS_CHART_HEADERS[5]
                ])

    for index, resident in enumerate(residents_data):
        # Increase row_num by 2 because of the headers (starts from 0 and skip header number).
        row_num = str(index + 2 )
        sheet['A' + row_num] = resident['full_name']
        sheet['A' + row_num].number_format = '@'
        sheet['B' + row_num] = resident['association']
        sheet['B' + row_num].number_format = '@'
        sheet['C' + row_num] = resident['gender']
        sheet['C' + row_num].number_format = '@'
        sheet['D' + row_num] = resident['service']
        sheet['D' + row_num].number_format = '@'
        sheet['E' + row_num] = resident['beersheva']
        sheet['E' + row_num].number_format = '@'
        sheet['F' + row_num] = resident['taz']
        sheet['F' + row_num].number_format = '@'

    # Create a table
    tab = Table(displayName="Table1", ref="A1:F" + str(sheet.max_row))

    # Add a default style with striped rows and banded columns
    style = TableStyleInfo(name="TableStyleMedium9", showRowStripes=True)
    tab.tableStyleInfo = style

    # Add the table to the worksheet
    sheet.add_table(tab)

    # Generate a unique filename with timestamp
    filename = 'current_residents.xlsx'

    # Create file path for user
    path = DOWNLOAD_FOLDER + filename
    
    # Save file to download folder
    book.save(path)

    # Return the path so user can download it
    return path

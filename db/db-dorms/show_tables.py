import sqlite3
import os

db_abs_path = os.path.dirname(os.path.realpath(__file__)) + '/dorms.db'

conn = sqlite3.connect(db_abs_path)
c = conn.cursor()


def show_buildings():
    try:
        buildings = c.execute("SELECT * FROM buildings")

        print("BUILDINGS")
        print("#############")
        for row in buildings:
            print("Building id:              ", row[0]),
            print("Apartments quantity:      ", row[1]),
            print("\n")
    except:
        print("Something went wrong, please run db_init.py to initialize the database.")
        conn.close()


def show_apartments():
    try:
        apartments = c.execute("SELECT * FROM apartments")

        print("APARTMENTS")
        print("#############")
        for row in apartments:
            print("Apartment id:             ", row[0]),
            print("Rooms in apartment:       ", row[1]),
            print("Gender:                   ", row[2]),
            print("Building id:              ", row[3]),
            print("\n")
    except:
        print("Something went wrong, please run db_init.py to initialize the database.")
        conn.close()


def show_rooms():
    try:
        rooms = c.execute("SELECT * FROM rooms")

        print("ROOMS")
        print("#############")
        for row in rooms:
            print("Apartment id:             ", row[0]),
            print("Room id:                  ", row[1]),
            print("Aminach beds in room:     ", row[2]),
            print("Bunk beds in room:        ", row[3]),
            print("\n")
    except:
        print("Something went wrong, please run db_init.py to initialize the database.")
        conn.close()


def show_aminach_beds():
    try:
        aminach_beds = c.execute("SELECT * FROM aminach_bed")

        print("AMINACH BEDS")
        print("#############")
        for row in aminach_beds:
            print("Apartment id:             ", row[0]),
            print("Mattress quantity:        ", row[1]),
            print("Person 1:                 ", row[2]),
            print("Room id:                  ", row[3]),
            print("\n")
    except:
        print("Something went wrong, please run db_init.py to initialize the database.")
        conn.close()


def show_bunk_beds():
    try:
        bunk_beds = c.execute("SELECT * FROM bunk_bed")

        print("BUNK BEDS")
        print("#############")
        for row in bunk_beds:
            print("Apartment id:             ", row[0]),
            print("Mattress quantity:        ", row[1]),
            print("Person 1:                 ", row[2]),
            print("Person 2:                 ", row[3]),
            print("Room id:                  ", row[4]),
            print("\n")
    except:
        print("Something went wrong, please run db_init.py to initialize the database.")
        conn.close()


def show_residents():
    try:
        residents = c.execute("SELECT * FROM residents")

        print("RESIDENTS")
        print("#############")
        for row in residents:
            print("ID:                       ", row[0]),
            print("Full name:                ", row[1]),
            print("Association:              ", row[2]),
            print("Gender:                   ", row[3]),
            print("Distance indication:      ", row[4]),
            print("Entering date:            ", row[5]),
            print("Exiting date:             ", row[6]),
            print("\n")
    except:
        print("Something went wrong, please run db_init.py to initialize the database.")
        conn.close()


print("Options: ")
print("1. Buildings")
print("2. Apartments")
print("3. Rooms")
print("4. Aminach_bed")
print("5. Bunk_bed")
print("6. Residents")
print("7. All")
table = input("\nShow option: ")

if table == "1":
    show_buildings()
elif table == "2":
    show_apartments()
elif table == "3":
    show_rooms()
elif table == "4":
    show_aminach_beds()
elif table == "5":
    show_bunk_beds()
elif table == "6":
    show_residents()
elif table == "7":
    show_buildings()
    show_apartments()
    show_rooms()
    show_aminach_beds()
    show_bunk_beds()
    show_residents()
else:
    print("This option does not exist, please choose a valid option.")

conn.close()
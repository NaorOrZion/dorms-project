import os
import sys

FILE_ABSOLUTE_PATH = os.path.abspath(__file__)
CURRENT_DIR = os.path.dirname(FILE_ABSOLUTE_PATH) # get directory path of file
PARENT_DIR = os.path.dirname(CURRENT_DIR) # get parent directory path
BASE_DIR = os.path.dirname(PARENT_DIR) # get grandparent directory path
sys.path.insert(0, BASE_DIR)

from db import get_db

# Connect to the database
conn = get_db()
c = conn.cursor()

# Create schema if it doesn't exist
c.execute("CREATE SCHEMA IF NOT EXISTS \"dorms-db\"")

# Delete the current tables exists
c.execute("DROP TABLE IF EXISTS buildings CASCADE")
c.execute("DROP TABLE IF EXISTS apartments CASCADE")
c.execute("DROP TABLE IF EXISTS rooms CASCADE")
c.execute("DROP TABLE IF EXISTS aminach_bed")
c.execute("DROP TABLE IF EXISTS bunk_bed")
c.execute("DROP TABLE IF EXISTS residents")

# Building table:
c.execute("""CREATE TABLE buildings(
                    building_id     INTEGER PRIMARY KEY,
                    apt_count       INTEGER
)""")

# Apartments table:
# Notice that the apartment is connected directly to it's
# building with the help of the FOREIGN KEY
c.execute("""CREATE TABLE apartments(
                    apt_id          INTEGER PRIMARY KEY,
                    rooms_in_apt    INTEGER,
                    gender          TEXT,
                    building_id     INTEGER,
                    FOREIGN KEY (building_id) REFERENCES buildings(building_id) ON DELETE CASCADE
)""")

# Rooms table:
# Notice that the rooms are connected directly to their
# apartment with the help of the FOREIGN KEY
# The primary key should be a combination of apt_id and room_id, not just apt_id.
# This will allow you to have multiple rows with the same apt_id value as long as the room_id value is different.
c.execute("""CREATE TABLE rooms(
                    apt_id          INTEGER,
                    room_id         INTEGER,
                    aminach_beds    INTEGER,
                    bunk_beds       INTEGER,
                    PRIMARY KEY (apt_id, room_id),
                    FOREIGN KEY (apt_id) REFERENCES apartments(apt_id) ON DELETE CASCADE
)""")

# Aminach bed table:
# Notice that the aminach bed is connected directly to it's
# room with the help of the FOREIGN KEY
c.execute("""CREATE TABLE aminach_bed(
                    apt_id          INTEGER,
                    bed_id          INTEGER,
                    mattress_count  INTEGER,
                    person1         TEXT,
                    room_id         INTEGER,
                    FOREIGN KEY (apt_id, room_id) REFERENCES rooms(apt_id, room_id) ON DELETE CASCADE
)""")

# Bunk bed table:
# Notice that the bunk bed is connected directly to it's
# room with the help of the FOREIGN KEY
c.execute("""CREATE TABLE bunk_bed(
                    apt_id          INTEGER,
                    bed_id          INTEGER,
                    mattress_count  INTEGER,
                    person1         TEXT,
                    person2         TEXT,
                    room_id         INTEGER,
                    FOREIGN KEY (apt_id, room_id) REFERENCES rooms(apt_id, room_id) ON DELETE CASCADE
)""")

# Residents table:
# This table will store all the soldiers residing in bsmch's dorms.
c.execute("""CREATE TABLE residents(
                    id              SERIAL PRIMARY KEY,
                    full_name       TEXT,
                    association     TEXT,
                    gender          TEXT,
                    service         TEXT,
                    beersheva       TEXT,
                    taz             TEXT,
                    apartment       INTEGER,
                    unique (full_name, association, gender, service, beersheva, taz)
)""")

conn.commit()
conn.close()

print("Dorms database is created and initialized.")
print("You can see the tables with the show_tables.py script.")
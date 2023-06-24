import sqlite3
import os

# Create the database file on the same directory as this script
db_abs_path = os.path.dirname(os.path.realpath(__file__)) + '/dorms.db'

# Connect to the database
conn = sqlite3.connect(db_abs_path)
c = conn.cursor()

# Delete the current tables exists
c.execute("DROP TABLE IF EXISTS buildings")
c.execute("DROP TABLE IF EXISTS apartments")
c.execute("DROP TABLE IF EXISTS rooms")
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
                    FOREIGN KEY (building_id) REFERENCES buildings(building_id)
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
                    FOREIGN KEY (apt_id) REFERENCES apartments(apt_id)
)""")

# Aminach bed table:
# Notice that the aminach bed is connected directly to it's
# room with the help of the FOREIGN KEY
c.execute("""CREATE TABLE aminach_bed(
                    apt_id          INTEGER,
                    mattress_count  INTEGER,
                    person1         TEXT,
                    room_id         INTEGER,
                    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
)""")

# Bunk bed table:
# Notice that the bunk bed is connected directly to it's
# room with the help of the FOREIGN KEY
c.execute("""CREATE TABLE bunk_bed(
                    apt_id          INTEGER,
                    mattress_count  INTEGER,
                    person1         TEXT,
                    person2         TEXT,
                    room_id         INTEGER,
                    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
)""")

# Residents table:
# This table will store all the soldiers residing in bsmch's dorms.
c.execute("""CREATE TABLE residents(
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name       TEXT,
                    association     TEXT,
                    gender          TEXT,
                    distance        INTEGER,
                    entering_date   TIMESTAMP,
                    existing_date   TIMESTAMP   
)""")

conn.commit()
conn.close()

print("Dorms database is created and initialized.")
print("You can see the tables with the show_tables.py script.")
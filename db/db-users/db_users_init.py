import os
import sys

FILE_ABSOLUTE_PATH = os.path.abspath(__file__)
CURRENT_DIR = os.path.dirname(FILE_ABSOLUTE_PATH) # get directory path of file
PARENT_DIR = os.path.dirname(CURRENT_DIR) # get parent directory path
BASE_DIR = os.path.dirname(PARENT_DIR) # get grandparent directory path
sys.path.insert(0, BASE_DIR)

# Connect to the database
from db_users import get_db_users
conn = get_db_users()
c = conn.cursor()

# Delete the current tables exists
c.execute("DROP TABLE IF EXISTS users")

# Building table:
c.execute("""CREATE TABLE users(
                    id              SERIAL PRIMARY KEY,
                    username        TEXT,
                    password        TEXT
)""")
conn.commit()

c.execute("""INSERT INTO users (username, password) VALUES (%s, %s)""", ("c00ladmin", "reallycooladmin7845"))
conn.commit()

conn.close()

print("USERS database is created and initialized.")
print("You can see the tables with the show_tables.py script.")
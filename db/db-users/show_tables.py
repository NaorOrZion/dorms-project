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

def show_users():
    try:
        c.execute("SELECT * FROM users")
        users = c.fetchall()

        print("USERS")
        print("#############")
        for row in users:
            print("ID:              ", row[0]),
            print("Username:        ", row[1]),
            print("Password:        ", row[2]),
            print("\n")
    except:
        print("Something went wrong, please run db_users_init.py to initialize the database.")
        conn.close()

print("Options: ")
print("1. Users")
print("2. All")
table = input("\nShow option: ")

if table == "1":
    show_users()
elif table == "2":
    show_users(0)
else:
    print("This option does not exist, please choose a valid option.")

conn.close()

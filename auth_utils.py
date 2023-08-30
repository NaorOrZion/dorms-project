from consts import *
from typing import List, Dict
from db_users import get_db_users

def get_passwords_from_db() -> List[str]:
    '''
    This function retrieves all the passwords from the "users.db".
    @params: None.
    Returns: List of passwords -> List[str]
    '''
    # Getting the database
    conn = get_db_users()
    c = conn.cursor()
    
    passwords = []

    c.execute("""SELECT password FROM users""")

    passwords_from_db = c.fetchall()

    for password in passwords_from_db:
        passwords.append(password[0])

    return passwords


def get_usernames_from_db() -> List[str]:
    '''
    This function retrieves all the usernames from the "users.db".
    @params: None.
    Returns: List of passwords -> List[str]
    '''
    # Getting the database
    conn = get_db_users()
    c = conn.cursor()
    
    usernames = []

    c.execute("""SELECT username FROM users""")
    usernames_from_db = c.fetchall()

    for username in usernames_from_db:
        usernames.append(username[0])

    return usernames

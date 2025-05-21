# Dorms Management System

A web application for managing dormitory buildings, apartments, rooms, and residents.

## Prerequisites

- Python 3.13 or later
- PostgreSQL database server
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd dorms-project
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL database:
   - Create a new PostgreSQL database
   - Update the database connection settings in `consts.py`:
     ```python
     DB_HOST = "localhost"  # Your PostgreSQL host
     DB_NAME = "your_database_name"
     DB_USER = "your_username"
     DB_PASS = "your_password"
     DB_PORT = "5432"  # Default PostgreSQL port
     ```

## Database Initialization

The application uses two separate schemas in the database:
- `users-db`: For user authentication
- `dorms-db`: For dormitory management

To initialize the databases:

1. Initialize the users database (required for login):
```bash
python db/db-users/db_users_init.py
```
This will:
- Create the `users-db` schema
- Create the `users` table
- Add a default admin user (username: `c00ladmin`, password: `reallycooladmin7845`)

2. Initialize the dorms database:
```bash
python db/db-dorms/db_dorms_init.py
```
This will:
- Create the `dorms-db` schema
- Create all necessary tables:
  - `buildings`
  - `apartments`
  - `rooms`
  - `aminach_bed`
  - `bunk_bed`
  - `residents`

## Running the Application

1. Start the Flask development server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Log in using the default admin credentials:
- Username: `c00ladmin`
- Password: `reallycooladmin7845`

## Database Management

You can view the contents of the database tables using the provided scripts:

1. View users database tables:
```bash
python db/db-users/show_tables.py
```

2. View dorms database tables:
```bash
python db/db-dorms/show_tables.py
```

## Troubleshooting

If you encounter database-related errors:

1. Make sure PostgreSQL is running
2. Verify database connection settings in `consts.py`
3. Try reinitializing the databases using the initialization scripts
4. Check that both schemas (`users-db` and `dorms-db`) exist in your database

Common errors:
- `no schema has been selected to create in`: Run the database initialization scripts
- `relation does not exist`: Run the database initialization scripts
- Connection errors: Verify database settings in `consts.py`

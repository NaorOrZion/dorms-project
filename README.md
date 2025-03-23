# Student Dormitory Management System

A comprehensive system for managing student dormitories, handling residents, apartments, and payments. Built with Flask and PostgreSQL.

## Key Features

- Resident and apartment management
- Payment tracking
- Advanced filtering and search capabilities
- Excel data import/export functionality
- User permission system
- User-friendly interface

## System Requirements

- Python 3.8 or higher
- PostgreSQL
- Dependencies listed in requirements.txt

## Installation and Setup

1. Install Python 3.8 or higher
2. Install PostgreSQL and create a new database

3. Clone the repository:
```bash
git clone [your-repository-url]
cd dorms-project
```

4. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

5. Install dependencies:
```bash
pip install -r requirements.txt
```

6. Set up environment variables:
```bash
# On Windows:
set FLASK_APP=app.py
set FLASK_ENV=development
# On Linux/Mac:
export FLASK_APP=app.py
export FLASK_ENV=development
```

7. Initialize the database:
```bash
python db.py
```

8. Run the server:
```bash
flask run
```

The system will be available at: http://localhost:5000

## Project Structure

- `app.py` - Main application file
- `db.py` - Database configuration
- `db_users.py` - User management
- `auth_utils.py` - Authentication functions
- `flask_forms.py` - Flask-WTF forms
- `filter_apartments_utils.py` - Apartment filtering functions
- `filter_residents_util.py` - Resident filtering functions
- `get_functions.py` - Data retrieval functions
- `residents_xlsx_utils.py` - Excel file handling
- `templates/` - HTML templates
- `static/` - Static files (CSS, JavaScript)
- `db/` - Database files
- `files/` - Uploaded system files

## Support

For questions and support, please contact the system administrator (me) or open an issue in the repository.

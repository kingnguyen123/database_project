

## Project Description
This project is a simple database web application built for a college assignment. It allows a user to manage students, courses, and enrollments using a relational database and a Flask web interface.

## Tech Stack
- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML5
- CSS3
- Bootstrap
- Jinja2

## Installation Instructions
1. Create a virtual environment:
   ```powershell
   python -m venv venv
   ```
2. Activate the virtual environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
3. Install the dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

## Database Setup
This project uses SQLite, so no separate database server is required.

To create the database tables, run:

```powershell
python app.py
```

When the application starts, it will automatically create the database file at `instance/app.db` if it does not already exist.
If you change the schema during development and need a fresh database, delete `instance/app.db` and run the app again.

## Usage
1. Start the Flask server:
   ```powershell
   python app.py
   ```
2. Open the local server address shown in the terminal.
3. Use the homepage navigation to manage students and courses.
4. Enrollment management and the summary dashboard are planned for the next project session.

## Current Day 1 Progress
- Flask app is set up
- SQLite configuration is connected
- SQLAlchemy models are created
- Student CRUD pages are complete
- Course CRUD pages are complete
- Server-side validation and flash messages are working
- Navigation, starter templates, and styling are added
- Documentation drafts are included

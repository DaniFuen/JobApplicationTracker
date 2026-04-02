# Job Application Tracker

## Description
A full-stack web application to track job applications, built with MySQL, Python/Flask, and HTML/CSS.

## Requirements
- Python 3.x
- MySQL Server
- MySQL Workbench

## Setup Instructions

### 1. Clone the Repository
```
git clone <your-repo-url>
cd JobApplicationTracker
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```

### 3. Set Up the Database
- Open MySQL Workbench
- Open and run `schema.sql` to create the database and tables
- This will also insert sample data automatically

### 4. Configure Database Connection
- Open `database.py`
- Update your MySQL password:
```python
password="your_password_here"
```

### 5. Run the Application
```
python app.py
```

### 6. Open in Browser
```
Example: http://127.0.0.1:5000
```

## Features
- Dashboard with live stats and recent applications
- Full CRUD for Companies, Jobs, Applications, and Contacts
- Job Match feature enter your skills and get jobs ranked by match percentage
- Dark themed 

## Project Structure
```
JobApplicationTracker/
├── app.py              # Main Flask application
├── database.py         # Database connection
├── schema.sql          # Database creation script
├── requirements.txt    # Python dependencies
├── README.md           # Project instructions
├── AI_USAGE.md         # GenAI documentation
├── static/
│   └── style.css       # CSS
└── templates/
    ├── base.html
    ├── dashboard.html
    ├── companies.html
    ├── edit_company.html
    ├── jobs.html
    ├── edit_job.html
    ├── applications.html
    ├── edit_application.html
    ├── contacts.html
    ├── edit_contact.html
    └── match.html
    
```

## Database Tables
- **companies** – stores company information
- **jobs** – job postings linked to companies
- **applications** – applications linked to jobs
- **contacts** – contacts linked to companies

## Technologies Used
- Python 3 / Flask
- MySQL Workbench
- HTML / CSS
- GenAI tools (Claude, ChatGPT)
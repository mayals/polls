Getting Started
To run polls project locally, follow these steps:

Clone the repository: git clone https://github.com/yourusername/polls.git
Create a virtual environment: python -m venv venv
Activate the virtual environment: source venv/bin/activate
Install dependencies: pip install -r requirements.txt
Go to .settings.DATABASES section, deactivate #PRODUCTION mode and activate #Development mode, add PostgreSQL configuration to connect to your database to be the default database.
Change .env.templates to .env and setup you environment variables.
Set up the database: python manage.py migrate
Create a superuser account: python manage.py createsuperuser
Start the development server: python manage.py runserver

I have deploy this project to render :

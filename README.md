# Wht_test_task Team-Management API

API service for managing teams and members written with DRF. 
Added functionality for administrators  to create teams and team members, 
make changes, and add/remove members from teams. 
Access limited to viewing for all regular users.

## Installation

Python 3 should be installed. Install PostgresSQL and create db.

    https://github.com/Oomamchur/Wht_test_task
    cd Wht_test_task
    python -m venv venv

On Windows:

    source venv\Scripts\activate

On macOS or Linux:

    source venv/bin/activate

This project uses environment variables to store sensitive information such as the Django secret key and database credentials. 
Create a .env file in the root directory of your project and add your environment variables to it. 
This file should not be committed to the repository. You can see the example in .env.sample file.

    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver

## Run with Docker

Docker should be installed.

    docker-compose build
    docker-compose up

Run tests via Docker:
    
    docker-compose run app sh -c "python manage.py test"

## Getting access

Data from the fixture will be imported automatically when you run the migrations. 
You can use user from fixture (or create another one by yourself):

    Login: alex.shevelo@gmail.com
    Password: Admin123

## Features

1. Admin panel. Changed email instead of username.
2. Creating and managing teams.
3. Creating and managing members.
4. Filtering teams by name and members by first_name and last_name.
5. Added pagination.
6. Added custom permissions.
7. Added tests.
8. Added possibility to run with Docker.
9. Documentation located at /api/doc/swagger/

## Demo

![wht_demo.jpg](wht_demo.jpg)
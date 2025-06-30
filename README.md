

# TODO: format the readme

1. Create the virtual envirionment: it will create a new folder api_env with the
necessary files to run the virtual environment.

$ python -m venv api_env

2. Activate the new virtual environment:
$ source api_env/bin/activate

3. Install flask:
$ pip3 install flask

4. Install the ORM -> SQLAlchemy
$ pip3 install flask-sqlalchemy

5. Check if evertything is installed correctly:
$ pip3 list

Output:
Package            Version
------------------ -------
blinker            1.9.0
click              8.1.8
Flask              3.1.1
Flask-SQLAlchemy   3.1.1
importlib_metadata 8.7.0
itsdangerous       2.2.0
Jinja2             3.1.6
MarkupSafe         3.0.2
pip                25.1.1
setuptools         58.0.4
SQLAlchemy         2.0.41
typing_extensions  4.14.0
Werkzeug           3.1.3
zipp               3.23.0

6. Create the freeze requirements file (Like a dependencies):
$ pip3 freeze > requirements.txt

7. Create a main.py file# LoginDemo.API





Structure

loginemoapi/
├── __init__.py          # To make 'logindemoapi' a Python package
├── app.py               # Main Flask application factory
├── models/
│   ├── __init__.py
│   └── user_model.py            # SQLAlchemy models
├── repositories/
│   ├── __init__.py
│   └── user_repository.py
├── services/
│   ├── __init__.py
│   └── user_service.py
├── controllers/
│   ├── __init__.py
│   └── user_controller.py
├── routes/
│   ├── __init__.py
│   └── user_routes.py
└── config.py            # For configuration (optional but good practice)
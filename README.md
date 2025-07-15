
# LoginDemo.API

# TODO: format the readme

# Setup

1. Create the virtual envirionment: it will create a new folder api_env with the
necessary files to run the virtual environment.
```bash
$ python -m venv venv
```
2. Activate the new virtual environment:
```bash
$ source venv/bin/activate
```
3. Install flask:
```bash
$ pip3 install flask
```
4. Install the ORM -> SQLAlchemy
```bash
$ pip3 install flask-sqlalchemy
```
5. Check if evertything is installed correctly:
```bash
$ pip3 list
```
Output:
```console
┌--------------------------┬-----------┐
| Package                  | Version   |
├--------------------------┼-----------┤
| altgraph                 | 0.17.2    |
| beautifulsoup4           | 4.13.4    |
| blinker                  | 1.9.0     |
| cachetools               | 5.5.2     |
| certifi                  | 2025.4.26 |
| charset-normalizer       | 3.4.2     |
| click                    | 8.1.8     |
| filelock                 | 3.18.0    |
| Flask                    | 3.1.1     |
| Flask-SQLAlchemy         | 3.1.1     |
| fsspec                   | 2025.5.1  |
| future                   | 0.18.2    |
| google-api-core          | 2.24.2    |
| google-api-python-client | 2.169.0   |
| google-auth              | 2.40.1    |
| google-auth-httplib2     | 0.2.0     |
| google-auth-oauthlib     | 1.2.2     |
| googleapis-common-protos | 1.70.0    |
| gspread                  | 6.2.1     |
| httplib2                 | 0.22.0    |
| idna                     | 3.10      |
| importlib_metadata       | 8.7.0     |
| itsdangerous             | 2.2.0     |
| Jinja2                   | 3.1.6     |
| macholib                 | 1.15.2    |
| MarkupSafe               | 3.0.2     |
| mpmath                   | 1.3.0     |
| networkx                 | 3.2.1     |
| numpy                    | 2.0.2     |
| oauthlib                 | 3.2.2     |
| pip                      | 25.1.1    |
| proto-plus               | 1.26.1    |
| protobuf                 | 6.31.0    |
| pyasn1                   | 0.6.1     |
| pyasn1_modules           | 0.4.2     |
| pyparsing                | 3.2.3     |
| requests                 | 2.32.3    |
| requests-oauthlib        | 2.0.0     |
| rsa                      | 4.9.1     |
| setuptools               | 58.0.4    |
| six                      | 1.15.0    |
| soupsieve                | 2.7       |
| SQLAlchemy               | 2.0.41    |
| sympy                    | 1.14.0    |
| torch                    | 2.7.1     |
| typing_extensions        | 4.13.2    |
| uritemplate              | 4.1.1     |
| urllib3                  | 2.4.0     |
| Werkzeug                 | 3.1.3     |
| wheel                    | 0.37.0    |
| zipp                     | 3.23.0    |
└--------------------------┴-----------┘
```
6. Create the freeze requirements file (Like a dependencies):
```bash
$ pip3 freeze > requirements.txt
```
# Structure
```console
loginemoapi/
├── .venv/
├── .vscode/
│   ├── launch.json
│   └── settings.json
├── instance/
│   └── LoginDemo.db ?? TODO: FIGURE OUT IS THIS IS THE ONE THE APP IS USING
├── login_api/
│   ├── __init__.py                 # To make 'logindemoapi' a Python package
│   ├── app.py                      # Main Flask application factory
│   ├── config.py                   # For configuration (optional but good practice)
│   ├── extensions.py
│   ├── db/
│   │   └── LoginDemo.db
│   ├── error_handler/
│   │   ├── __init__.py
│   │   ├── exceptions.py
│   │   └── user_exceptions.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user_model.py           # SQLAlchemy models
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── auth_repository.py
│   │   └── user_repository.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── user_service.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── auth_controller.py
│   │   └── user_controller.py
│   └── routes/
│       ├── __init__.py
│       ├── auth_routes.py
│       └── user_routes.py 
├── venv/
├── tests/
├── .env
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

7. Run:
```bash
$ python3 run.py
```

# Production

Solutions for Production
1. For Development (Quick Solution - Just Hide Warning)
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

2. For Production (Recommended Options)
Option A: Waitress (Simplest production server)
```bash
$ pip3 install waitress
```
Then modify run.py:
```python
from waitress import serve
from login_api.app import app

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
```

Option B: Gunicorn (Popular for Linux)
```bash
$ pip3 install gunicorn
```
Run with:
```python
$ gunicorn -w 4 -b 0.0.0.0:5000 "login_api.app:create_app()"
```
Option C: uWSGI (High performance)
```python
$ pip3 install uwsgi
```
Create uwsgi.ini:
```console
ini
[uwsgi]
module = login_api.app:app
master = true
processes = 5
socket = 0.0.0.0:5000
protocol = http
```
Important Production Considerations
1. Environment Variables: Use .env for configuration
2. Reverse Proxy: Use Nginx/Apache in front of your app server
3. Process Manager: Use systemd or supervisor to keep app running
4. HTTPS: Always use SSL in production (Let's Encrypt is free)

Development vs Production Checklist
```console
┌----------------┬-----------------┬-------------------------┐
| Feature        | Development     | Production              |
├----------------┼-----------------┼-------------------------┤
| Server         | Flask built-in  | Gunicorn/uWSGI/Waitress |
| Debug Mode     | On              | Off                     |
| Threading      | Single          | Multiple workers        |
| Error Handling | Detailed errors | Generic error pages     |
| Port           | 5000            | 80/443 (via proxy)      |
└----------------┴-----------------┴-------------------------┘
```

Bcrypt Implementation

SECRET_KEY
* Purpose: Used to cryptographically sign sessions, tokens (like JWTs), and secure cookies. Flask-Bcrypt uses it internally for password hashing.
* Best Practices:
** Never hardcode (use environment variables):

```python
# In config.py
import os

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # Load from .env file
```
** Generate a strong key (run in Python shell):
```python
import secrets
print(secrets.token_hex(32))  # Copy this into your .env file
```
** Example .env:
```text
SECRET_KEY=your_generated_hex_string_here
```

# Troubleshoting

Recreate your venv:
```bash
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
```
Reinstall dependencies:
```bash
pip install -r requirements.txt
```

Generate requirements.txt
```bash
pip freeze > requirements.txt
```

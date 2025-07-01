
# LoginDemo.API

# TODO: format the readme

# Setup

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

6. Create the freeze requirements file (Like a dependencies):
$ pip3 freeze > requirements.txt

# Structure

loginemoapi/
├── api_env
├── login_api/
│   ├── __init__.py                 # To make 'logindemoapi' a Python package
│   ├── app.py                      # Main Flask application factory
│   ├── config.py                   # For configuration (optional but good practice)
│   ├── models/
│   │   ├── __init__.py
│   │   └── user_model.py           # SQLAlchemy models
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── user_repository.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── user_controller.py
│   └── routes/
│       ├── __init__.py
│       └── user_routes.py 
├── tests/
├── README.md
├── requirements.txt
└── run.py

# Production

Solutions for Production
1. For Development (Quick Solution - Just Hide Warning)

```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

2. For Production (Recommended Options)
Option A: Waitress (Simplest production server)
$ pip3 install waitress

Then modify run.py:

from waitress import serve
from login_api.app import app
```python
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
```

Option B: Gunicorn (Popular for Linux)
$ pip3 install gunicorn

Run with:
$ gunicorn -w 4 -b 0.0.0.0:5000 "login_api.app:create_app()"

Option C: uWSGI (High performance)
$ pip3 install uwsgi

Create uwsgi.ini:

ini
[uwsgi]
module = login_api.app:app
master = true
processes = 5
socket = 0.0.0.0:5000
protocol = http

Important Production Considerations
1. Environment Variables: Use .env for configuration
2. Reverse Proxy: Use Nginx/Apache in front of your app server
3. Process Manager: Use systemd or supervisor to keep app running
4. HTTPS: Always use SSL in production (Let's Encrypt is free)

Development vs Production Checklist

┌----------------┬-----------------┬-------------------------┐
| Feature        | Development     | Production              |
├----------------┼-----------------┼-------------------------┤
| Server         | Flask built-in  | Gunicorn/uWSGI/Waitress |
| Debug Mode     | On              | Off                     |
| Threading      | Single          | Multiple workers        |
| Error Handling | Detailed errors | Generic error pages     |
| Port           | 5000            | 80/443 (via proxy)      |
└----------------┴-----------------┴-------------------------┘
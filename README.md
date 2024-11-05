# Kiu System

Project to search flights

## Technology Stack

- **Python** >=3.11
- **Django** >=5.1
- **Django Rest Framework** >=3.15
- **PostgreSQL**

## Installation

**First clone the repository**

- `git clone ...`
- `cd kiu-sys`

**Install Dependencies**

We use poetry to manage project dependencies (https://python-poetry.org/docs/#installation)


*POETRY VERSION >=1.6.1*

- Set poetry to create virtualenv inside project (`poetry config virtualenvs.in-project true`)
- Set poetry env use python 3.11 (`poetry env use 3.11`).
- Install dependencies (`poetry install`)
- Activate the poetry virtualenv (`poetry shell`)

## Local Settings (DEVELOPMENT)

Copy the local_settings.example to the project settings folder (/kiu).

```
(.venv) $ cp kiu/local_settings.example.py kiu/local_settings.py
```

The most important configurations is:

- DATABASES: Database configuration

## Migrations

- Create migrations: `(.venv) $ python manage.py makemigrations`

- Execute the migrations : `(.venv) $ python manage.py migrate --database=default`

## Basic Usage

**First follow the installations steps, configure settings and run migrations. You can also load the fixtures to have
initial data.**

- python manage.py loaddata flights.json
- Run the server with the following command: `python manage.py runserver 0.0.0.0`


**Run all tests**
- `(.venv) $ python manage.py test --verbosity 2 --keepdb`
- `(.venv) $ python manage.py test --verbosity 2 --keepdb (It uses the database already created (without data, but it does not run the migrations again), so the test runs faster)`

## Flights API

E.g.: get flights from Buenos Aires to Palma de Mallorca

GET `http://localhost:8000/api/v1/journeys/search?from=BUE&to=PDM&date=2024-11-09`

Example response:
```
[
    {
        "connections": 1,
        "path": [
            {
                "flight_number": "32423423",
                "from_city": "BUE",
                "to_city": "PDM",
                "departure_time": "2024-11-09 17:15",
                "arrival_time": "2024-11-10 05:15"
            }
        ]
    },
    {
        "connections": 2,
        "path": [
            {
                "flight_number": "XX1234",
                "from_city": "BUE",
                "to_city": "MAD",
                "departure_time": "2024-11-09 15:15",
                "arrival_time": "2024-11-10 03:15"
            },
            {
                "flight_number": "BB1234",
                "from_city": "MAD",
                "to_city": "PDM",
                "departure_time": "2024-11-10 04:15",
                "arrival_time": "2024-11-10 06:15"
            }
        ]
    }
]
```

## Important

NOTE to reviewer: gitlab API wasn't working, that's why I decided to create the models and fill them with initial data to be able to perform some example API queries

## TODO

- add more tests
- add pre-commit (flake8, black formatter, isort, etc)
- refactor get_flight_events into more reusable functions
- improve iteration performance
- add validations on output serializer
- make max flights connections dynamic (3 in the future or more)
- add cache to endpoint
- add github actions and testing pipeline
- add coverage
- more comments (docstrings to classes and functions)

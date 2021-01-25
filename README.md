# REST API Street food

## Overview

Street food API is a REST api written in Django-rest-framework for people who wants to share their food truck and for potential future customers. 
The project uses PostgreSQL as default database.

## Technologies/libraries used

- Python 3.7
- [Django-rest-framework](https://github.com/encode/django-rest-framework)
- [Django-filter](https://github.com/carltongibson/django-filter)
- [Django-phonenumber-field](https://github.com/stefanfoulis/django-phonenumber-field)

### Additional libraries used to make sure the code meets all necessary conventions
- [Pre-commit](https://github.com/pre-commit/pre-commit)
  - [Black](https://github.com/psf/black): as a hook.
  - [Flake8](https://github.com/PyCQA/flake8): as a hook.
  - [Isort](https://github.com/PyCQA/isort): as a hook.
  - [Trailing-whitespace](https://github.com/pre-commit/pre-commit-hooks): as a hook.
  - [End-of-file-fixer](https://github.com/pre-commit/pre-commit-hooks): as a hook.

All requirements available [here](https://github.com/ImustAdmit/Street-food-api/blob/main/poetry.lock) as **Poetry.lock** file.

## Installation

```python
git clone https://github.com/ImustAdmit/Street-food-api.git
```

To make the project work on your local machine you need to install [poetry](https://python-poetry.org/docs/#installation) firstly or extract necessary dependencies to the new file.

```python
# with Poetry
poetry install

# without Poetry
cat requirements.txt|xargs poetry add
pip install -r requirements.txt
```

## Authentication & Permissions

Access to the API is granted by providing your username and password using HTTP basic authentication. 
The basic user can only list objects and retrieve a single object. A user added to the group of owners can additionally create new Trucks as well as update and destroy Trucks belonging to him.

## Structure

### For Basic Users

Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`trucks/` | GET | READ | Get all trucks
`trucks/:id/` | GET | READ | Get a single truck

### For Truck Owners

Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`trucks/`| POST | CREATE | Create a new Truck
`trucks/:id/` | PUT & PATCH | UPDATE | Update a Truck
`trucks/:id/` | DELETE | DELETE | Delete a Truck
`trucks/:id/location/` | POST | Create | Create Location for Truck

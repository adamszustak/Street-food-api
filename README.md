# REST API Street food

## Overview

Street food API is a REST api written in Django-rest-framework for people who wants to share their food truck and for potential future customers. 
The project uses PostgreSQL as default database.

## Table of Contents
- [Technologies/libraries](#technologieslibraries-used)
  - [Additional libraries](#additional-libraries-used-to-make-sure-the-code-meets-all-necessary-conventions)
- [Installation](#installation)
- [Authentication & Permissions](#authentication--permissions)
- [Structure](#structure)
  - [For Basic Users](#for-basic-users)
    - [Get all trucks](#get-all-trucks)
    - [Get a single truck](#get-a-single-truck)
  - [For Truck Owners](#for-truck-owners)

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

```
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

Endpoint |HTTP Method | CRUD Method | Result | Info
-- | -- |-- |-- |--
`trucks/` | GET | READ | Get all trucks | Details
`trucks/:id/` | GET | READ | Get a single truck | Details

#### Get all trucks

Return a list of all accepted by administrators Trucks

#### Example

* Request

```
GET http://127.0.0.1:8000/api/trucks/
```

* Response

```
"results": [
    {
        "id": 1,
        "owner": 1,
        "name": "HavenHam",
        "phone": "+48570496076",
        "email": "aszustak@onet.pl",
        "facebook": "havenham",
        "instagram": "#havenham",
        "page_url": "http://www.uczsieit.pl",
        "description": "The best ham even!",
        "payment_methods": [
            "Credit Card",
            "Debit Card",
            "Cash"
        ],
        "images": [
            "/media/uploads/HavenHam/main/comment_5j8RRZ3TGHIv7H49agXdukUOFNLPt565.jpg"
        ],
        "updated": "2021-01-20T07:11:35.066727Z",
        "location": {
            "street": "Mazowiecka 12",
            "city": "Warsaw",
            "zip_code": "03-444",
            "longitude": -55.0,
            "latitude": 77.77777,
            "open_from": "04:20",
            "closed_at": "12:30"
        }
    },
    {
        "id": 96,
        "owner": 1,
        "name": "NewTruck!",
        "phone": "",
        "email": "",
        "facebook": "asdsad",
        "instagram": "",
        "page_url": "",
        "description": "The best Truck in the world",
        "payment_methods": [
            "Debit Card"
        ],
        "images": [
            "/media/uploads/N12/main/Detail_Page.jpg"
        ],
        "updated": "2021-01-25T08:57:56.532472Z",
        "location": null
    }
]
```

#### Get a single truck

Return a single Truck.

#### Example

* Request

```
GET http://127.0.0.1:8000/api/trucks/1/
```

* Response

```
{
    "id": 115,
    "owner": 1,
    "name": "Burger&Chips",
    "phone": "",
    "email": "",
    "facebook": "",
    "instagram": "",
    "page_url": "",
    "description": "Tasie it!",
    "payment_methods": [
        "Credit Card",
        "Debit Card",
        "Cash",
        "By Phone"
    ],
    "images": [],
    "updated": "2021-01-25T17:22:27.609114Z",
    "location": null
}
```

### For Truck Owners

Endpoint |HTTP Method | CRUD Method | Result | Info
-- | -- |-- |-- |--
`trucks/`| POST | CREATE | Create a new Truck | Details
`trucks/:id/` | PUT & PATCH | UPDATE | Update a Truck | Details
`trucks/:id/` | DELETE | DELETE | Delete a Truck | Details
`trucks/:id/location/` | POST | CREATE | Create Location for Truck | Details

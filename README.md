# REST API Street food

<img src="https://img.shields.io/badge/stability-work_in_progress-lightgrey.svg"> <img src="https://img.shields.io/badge/License-MIT-yellow.svg">

## Overview

Street food API is a REST api written in Django-rest-framework for people who wants to share their food truck and for potential future customers who want to find truck. :pizza: :hamburger:
The project uses PostgreSQL as default database.

## Table of Contents

- [Technologies/libraries](#technologieslibraries-used)
  - [Additional libraries](#additional-libraries-used-to-make-sure-the-code-meets-all-necessary-conventions)
- [Installation](#installation)
- [Testing](#testing)
- [Authentication & Permissions](#authentication--permissions)
- [Structure](#structure)
  - [For Basic Users](#for-basic-users)
    - [Get all trucks](#get-all-trucks)
    - [Get a single truck](#get-a-single-truck)
  - [For Truck Owners](#for-truck-owners)
    - [Create a new Truck](#create-a-new-truck)
    - [Update a Truck](#update-a-truck)
    - [Delete a Truck](#delete-a-truck)
    - [Create Location for Truck](#create-location-for-truck)

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

## Testing

You need to have Python 3.7 or 3.9 available in your system. Now running tests is as simple as typing this command:

```
tox -e linting,py37 (or py39)
```

This command will run tests via the "tox" tool against Python 3.7/3.9 and also perform "lint" coding-style checks.

## Authentication & Permissions

Access to the API is granted by providing your username and password using HTTP basic authentication.
The basic user can only list objects and retrieve a single object. A user added to the group of owners can additionally create new Trucks as well as update and destroy Trucks belonging to him.

## Structure

### For Basic Users

| Endpoint      | HTTP Method | CRUD Method | Result             | Info                           |
| ------------- | ----------- | ----------- | ------------------ | ------------------------------ |
| `trucks/`     | GET         | READ        | Get all trucks     | [Details](#get-all-trucks)     |
| `trucks/:id/` | GET         | READ        | Get a single truck | [Details](#get-a-single-truck) |

#### Get all trucks

Return a list of all accepted by administrators Trucks

#### Example

- Request

```
GET http://127.0.0.1:8000/api/trucks/
```

- Response (status: 200 OK)

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
        "city": "Warsaw",
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
        "city": "Warsaw",
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

- Request

```
GET http://127.0.0.1:8000/api/trucks/1/
```

- Response (status: 200 OK)

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
    "city": "Warsaw",
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

| Endpoint               | HTTP Method | CRUD Method | Result                    | Info                                  |
| ---------------------- | ----------- | ----------- | ------------------------- | ------------------------------------- |
| `trucks/`              | POST        | CREATE      | Create a new Truck        | [Details](#create-a-new-truck)        |
| `trucks/:id/`          | PUT & PATCH | UPDATE      | Update a Truck            | [Details](#update-a-truck)            |
| `trucks/:id/`          | DELETE      | DELETE      | Delete a Truck            | [Details](#delete-a-truck)            |
| `trucks/:id/location/` | POST        | CREATE      | Create Location for Truck | [Details](#create-location-for-truck) |

#### Create a new Truck

Creates a new Truck and returns the newly-created object. Requires **multipart / form-data** encoding when body includes **images**.
The owner is added automatically when the object is saved as well as slug field.
Before the Truck is available to readers, it has to be approved by the administrator.
Creation and update dates are added automatically.

- multipart/form-data body parameters

| Field           | Data Type | Required | Description                                                                               |
| --------------- | --------- | -------- | ----------------------------------------------------------------------------------------- |
| name            | string    | Y        | Food Truck name                                                                           |
| phone           | string    | N        | Phone Number accepted in international format (e.g '+41524204242')                        |
| email           | string    | N        | Email address (e.g 'aszustak@onet.pl')                                                    |
| city            | string    | Y        | City where Food Truck is mainly placed (e.g 'Warsaw')                                     |
| facebook        | string    | N        | Facebook address                                                                          |
| instagram       | string    | N        | Instagram address                                                                         |
| page_url        | string    | N        | Truck website (e.g 'https://www.uczsieit.pl')                                             |
| description     | string    | Y        | Short description of the Truck (max length is 200 chars)                                  |
| payment_methods | string    | N        | Option available: cash, credit card, debit card, by phone. Must be separated by commas    |
| image           | field     | N        | Truck images, if more than 1 add each photo as a separate image keyword! Max size is 2MB. |

#### Example

- Request

```
POST http://127.0.0.1:8000/api/trucks/
```

- Request Body

```
{
    "name": "HavenHam",
    "phone": "+41333444111",
    "email": "aszustak@onet.pl",
    "facebook": "haven-ham",
    "instagram": "#haven-ham",
    "city": "Warsaw",
    "page_url": "http://www.uczsieit.pl",
    "description": "The best ham even!",
    "payment_methods": "Credit card, Cash",
    "image": ImageField,
    "image": ImageField
}
```

- Response (status: 201 CREATED)

```
{
    "id": 1,
    "owner": 1,
    "name": "HavenHam",
    "phone": "+41333444111",
    "email": "aszustak@onet.pl",
    "facebook": "haven-ham",
    "instagram": "#haven-ham",
    "page_url": "http://www.uczsieit.pl",
    "description": "The best ham even!",
    "city": "Warsaw",
    "payment_methods": [
        "Credit Card",
        "Debit Card",
        "Cash"
    ],
    "images": [
        "/media/uploads/HavenHam/main/comment_5j8RRZ3TGHIv7H49agXdukUOFNLPt565.jpg",
        "/media/uploads/HavenHam/main/comment_2.jpg"
    ],
    "updated": "2021-01-20T07:11:35.066727Z",
}
```

#### Update a Truck

Updates a Truck and returns the updated object. It needs to be done by owner/creator of an object.
**Note**: If an image is sent all previous images will be removed and new images will be associated. The same goes for the payment methods in case of PUT method or PATCH when `payment` is provided. When PATCH without `payment` keyword, old `payment` instances remain.
Requires **multipart / form-data** encoding when body includes **images**.

#### Example

- Request

```
PUT/PATCH http://127.0.0.1:8000/api/trucks/12/
```

- Response (status: 200 OK)

#### Delete a Truck

Delete a Truck.

#### Example

- Request

```
DELETE http://127.0.0.1:8000/api/trucks/12/
```

- Response (status: 204 NO CONTENT)

#### Create Location for Truck

Creates a new Location and returns the newly-created object. One Truck can has only one Location! When POST, old Location is removed and replaced by new Location.

#### Example

- JSON body parameters

| Field     | Data Type | Required | Description                                         |
| --------- | --------- | -------- | --------------------------------------------------- |
| street    | string    | Y        | Street where Truck is located (e.g 'Mazowiecka 12') |
| zip_code  | string    | Y        | Zip Code in format XX-XXX (e.g '03-333')            |
| longitude | float     | N        | Location (range: -180 to 180)                       |
| latitude  | float     | N        | Location (range: -90 to 90)                         |
| open_from | string    | N        | Opening time in format %H:%M                        |
| closed_at | string    | N        | Closing time in format %H:%M                        |

- Request

```
POST http://127.0.0.1:8000/api/trucks/12/location/
```

- Request Body

```
{
    "street": "Mazowiecka",
    "zip_code": "03-221",
    "longitude": 56.666666,
    "latitude": -24.076566,
    "open_from": "4:2"
}
```

- Response (status: 201 CREATED)

```
{
    "street": "Mazowiecka",
    "city": "Warsaw",
    "zip_code": "03-221",
    "longitude": 56.666666,
    "latitude": -24.076566,
    "open_from": "04:02",
    "closed_at": null
}
```

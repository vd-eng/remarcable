# Remarcable project

A simple Django project that models products, categories, and tags.
Users are able to search and filter products based on product description, category, and tags; specifically:

* **search** products by description.
* **filter** products by category.
* **filter** products by tags.
* Users should be able to combine search and filter options.

## Design decisions and implementation details

Implement three models `Tag`, `Category` and `Product`.

* `Category` -> `Product` demonstrates one-to-many relationship.
* `Tag` -> `Product` demonstrates many-to-many relationship.

Since `description` is a free-form text, it's implemented as the `TextField` type. While in a small demo project like this we'll keep the implementation simple, scaling in production with a databse like PostgreSQL might require additional attention.

To be able to filter independently or using any combination of the specified properties, three filters are implemented on a product queryset. We can chain them together to filter products as required.

## Project structure

The project's structure is based on the django tutorial found here https://docs.djangoproject.com/en/6.1/intro/tutorial01/ .

```bash
manage.py
mysite/
    __init__.py
    settings.py
    urls.py
    asgi.py
    wsgi.py
products/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests/
        __init__.py
    views.py
```

* **manage.py**: A command-line utility that lets you interact with this Django project.
* **mysite/**: A directory that is the Python package for the project.
* **mysite/settings.py**: Settings/configuration.
* **mysite/urls.py**: The URL declarations.
* **mysite/asgi.py**: An entry-point for ASGI-compatible web servers to serve the project.
* **mysite/wsgi.py**: An entry-point for WSGI-compatible web servers to serve the project.
* **products/**: The `products` app containing main functionality.

## Initially seeded data

Initially, the sqlite DB is seeded with 20 products, 10 tags, and 5 categories.

## Project management and useful commands

The project and its dependencies are managed by [uv](https://docs.astral.sh/uv/).
To install it on Linux, use the following command:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

To create a virtual environment based on the existing `uv.lock` file:

```sh
uv sync
```

The project's initial structure is generated with the `django-admin` command:

```sh
uv run django-admin startproject mysite .
```

Create a new app (`products` in this example):

```bash
uv run manage.py startapp products
```

Run the development server (NEVER RUN THIS IN PRODUCTION):

```bash
uv run manage.py runserver
```

After starting the server, the products app can be accessed in a web-browser at http://127.0.0.1:8000/products/ .

Make DB migrations for an app (`products` in this example):

```sh
uv run manage.py makemigrations products
```

Apply DB migrations:

```sh
uv run manage.py migrate
```

## Running tests

```sh
uv run manage.py test products
```

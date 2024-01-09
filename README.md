# App
This project serves as a comprehensive example of the various components employed in a modern web application. It showcases the integration of a backend framework, a CSS library for presentation, a database for data storage, and a templating library for rendering views. The implementation adheres to the Model-View-Controller (MVC) architecture.
Components Used

## Backend
### Sanic - GitHub
Sanic is a Python micro web framework designed for speed and efficiency.

### Peewee - GitHub
Peewee is a Python Object-Relational Mapping (ORM) library, providing a simple and expressive way to interact with databases.

## Presentation
### Jinja2
Jinja2 is a powerful templating engine for Python, used for dynamically generating HTML and other markup.

### Bootstrap - GitHub
Bootstrap is a popular CSS framework that facilitates the development of responsive and visually appealing user interfaces.

## Storage
### SQLite
SQLite is a self-contained, serverless, and zero-configuration database engine. It is widely used for its simplicity and ease of integration.

## Setting up the Development Environment
This project employs pipenv to manage the virtual environment and dependencies for the development environment. pipenv ensures a consistent and reproducible environment for contributors.
Before setting up the development environment, make sure you have the following tools installed:

* Python (= 3.8)
* pipenv

### Create a virtual environment using pipenv
* `pipenv --python 3.8`

### Install the dependencies
* `pipenv install --dev`

### Activate the virtual environment
* `pipenv shell`

## Running the app
### In debug mode
`sanic app:app --debug`

### In production mode
`sanic app:app`

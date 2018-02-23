# bekiga

A simple web application to render inspection protocols to PDF using *VueJS*, *Flask*, *MongoDB* and *LaTeX*.

Einfaches Erstellen, Erzeugen und Darstellen von Prüfprotokollen für Kindergärten.

# Installation

Tested on Ubuntu 16.04.3 only.

To build the frontend application:

```
$ cd frontend
$ npm install
$ npm run build
```

A mongoDB instance needs to be up and running. For installation instructions check the [website](https://www.mongodb.com/).

You also need the *pdflatex* command line tool in your PATH. Various distributions exist.

Take a look at the `backend/settings.py` file to configure your server as needed. Refer to the flask [docs](http://flask.pocoo.org/docs/0.12/) for more information.

To start the *flask* development server run
```
$ cd backend
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ export FLASK_APP=app.py
$ flask run
```

Navigate to *localhost:5000* (default).

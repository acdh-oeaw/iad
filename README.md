[![Build and publish Docker image](https://github.com/acdh-oeaw/iad/actions/workflows/build.yml/badge.svg)](https://github.com/acdh-oeaw/iad/actions/workflows/build.yml)
[![flake8 Lint](https://github.com/acdh-oeaw/iad/actions/workflows/lint.yml/badge.svg)](https://github.com/acdh-oeaw/iad/actions/workflows/lint.yml)
[![Test](https://github.com/acdh-oeaw/iad/actions/workflows/test.yml/badge.svg)](https://acdh-oeaw.github.io/iad/)

# IRON-AGE-DANUBE (IAD)

Code Repo of the IAD's web-app.

## install

1. Download or Clone this repo
2. Adapt the information in `webpage/metadata.py` according to your needs.
3. Create an virtual environment and run `pip install -r requirements.txt`

### first steps

This projects uses modularized settings (to keep sensitive information out of version control or being able to use the same code for development and production). Therefore you'll have to append all `manage.py` commands with a `--settings` parameter pointing to the settings file you'd like to run the code with. For development just append `--settings={nameOfYouProject}.settings.dev` to the following commands, e.g. `python manage.py makemigrations --settings=iad.settings.dev`

4. Run `makemigrations`, `migrate`, and `runserver` and check [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Tests

To get needed software you can run

    pip install -r requirements_test.txt

To run the tests execute

    python manage.py test --settings=iad.settings.test


## Technical setup

### storage

This application uses [PostgreSQL](https://www.postgresql.org/) with the [PostGIS](http://postgis.net) extension to support spatial queries.

### application layer

The application layer is implemented with the [Python](https://www.python.org/) based web framework [Django](https://www.djangoproject.com/). GIS related functionality (see [here](https://docs.djangoproject.com/en/1.11/ref/contrib/gis/db-api/#compatibility-tables) for a detailed overview of those functions) are realized by with [GeoDjango](https://docs.djangoproject.com/en/1.11/ref/contrib/gis/).
Please refer to [GeoDjangos Documentation](https://docs.djangoproject.com/en/1.11/ref/contrib/gis/) to learn about needed requirements to run GeoDjango.
The application is mainly run server-side although the data is accessible through an REST-API implemented with [Django REST framework](http://www.django-rest-framework.org/).

### Front end layer

The presentation of GIS-related data on the client side (web-browser) is realized with [Leaflet](http://leafletjs.com/) which processes the data serialized by the backend into [GeoJSON](http://geojson.org/) though data from different sources (e.g. raster images, served following the [WMS protocol ](https://en.wikipedia.org/wiki/Web_Map_Service)) can be integrated as well.


### building the image

`docker build -t iad:latest .`
`docker build -t iad:latest --no-cache .`

### running the image

To run the image you should provide an `env.default` file to pass in needed environment variables; see example `env.default` in this repo:


`docker run -it -p 8020:8020 --rm --env-file env.default iad:latest`

### or use published image:

`docker run -it -p 8020:8020 --rm --env-file env.default acdhch/iad:latest`
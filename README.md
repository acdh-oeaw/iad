[![Build and publish Docker image](https://github.com/acdh-oeaw/iad/actions/workflows/build.yml/badge.svg)](https://github.com/acdh-oeaw/iad/actions/workflows/build.yml)
[![flake8 Lint](https://github.com/acdh-oeaw/iad/actions/workflows/lint.yml/badge.svg)](https://github.com/acdh-oeaw/iad/actions/workflows/lint.yml)
[![Test](https://github.com/acdh-oeaw/iad/actions/workflows/test.yml/badge.svg)](https://acdh-oeaw.github.io/iad/)
[![codecov](https://codecov.io/gh/acdh-oeaw/iad/branch/main/graph/badge.svg?token=GPBITL4IK9)](https://codecov.io/gh/acdh-oeaw/iad)

# IRON-AGE-DANUBE (IAD)

Code Repo of the IAD's web-app.

## install

1. Download or Clone this repo
2. Adapt the information in `webpage/metadata.py` according to your needs.
3. Create an virtual environment and run `pip install -r requirements.txt`

### first steps

4. Run `makemigrations`, `migrate`, and `runserver` and check [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Tests

The project uses [coverage]() to monitor the overall test coverage. Run
```bash
coverage run manage.py test -v 2
```
to run the tests.

Go to [https://acdh-oeaw.github.io/iad/](https://acdh-oeaw.github.io/iad/) to see the Coverage report.


## Technical setup

### storage

This application uses [PostgreSQL](https://www.postgresql.org/) with the [PostGIS](http://postgis.net) extension to support spatial queries.


### building the image

```bash
docker build -t iad:latest .
docker build -t iad:latest --no-cache .
```

### running the image

To run the image you should provide an `env.default` file to pass in needed environment variables; see example `env.default` in this repo:

```shell
docker run -it -p 8020:8020 --network="host" --rm --env-file default.env --name iad iad:latest
```

### or use published image:

`docker run -it -p 8020:8020 --rm --env-file env.default acdhch/iad:latest`
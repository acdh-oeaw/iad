#!/usr/bin/env bash
# create_fixtures.sh

# make sure you ran `pip install django-fixture-magic` and added `'fixture_magic'` to INSTALLED_APPS
source env/bin/activate
source set_env_variables.sh
mkdir ./archiv/fixtures
touch ./archiv/fixtures/dump.json
python manage.py dump_object archiv.site 5  4798 4353 > ./archiv/fixtures/dump.json

echo "done"
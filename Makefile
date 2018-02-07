#!make
# Default values, can be overridden either on the command line of make
# or in .env
FLASK_DEBUG ?= 0

.PHONY: init vars coverage run gunicorn local deploy

vars:
	@echo 'App-related vars:'
	@echo '  APP_SECRET=${APP_SECRET}'
	@echo '  E2EMONITORING_SERVICE=${E2EMONITORING_SERVICE}'
	@echo '  E2EMONITORING_URL=${E2EMONITORING_URL}'
	@echo '  STORAGE_TYPE=${STORAGE_TYPE}'
	@echo '  DATABASE_URL=${DATABASE_URL}'
	@echo ''
	@echo 'Environment-related vars:'
	@echo '  PYTHONPATH=${PYTHONPATH}'
	@echo '  FLASK_APP=${FLASK_APP}'
	@echo '  FLASK_DEBUG=${FLASK_DEBUG}'
	@echo '  GUNICORN_APP=${GUNICORN_APP}'
	@echo ''
	@echo 'Heroku-related vars:'
	@echo '  HEROKU_APP=${HEROKU_APP}'
	@echo '  HEROKU_URL=${HEROKU_URL}'
	@echo '  HEROKU_GIT=${HEROKU_GIT}'
	@echo '  DB_URI_VAR_NAME=${DB_URI_VAR_NAME}'
	@echo '  MAIL_USERNAME=${MAIL_USERNAME}'
	@echo '  MAIL_PASSWORD=xxx'

init-venv:
ifeq ($(wildcard .env),)
	cp .env.sample .env
	echo PYTHONPATH=`pwd`/src >> .env
endif
	pipenv --update 
	pipenv update --dev --python 3
	@echo replace HEROKU_APP & MAIL_* vars in your .env file before launching make init-heroku

init-heroku:
	heroku create ${HEROKU_APP} || true
	heroku config:set PYTHONPATH="./src"
	heroku config:set FLASK_DEBUG=0
	heroku config:set APP_SECRET="${APP_SECRET}"
	heroku config:set E2EMONITORING_SERVICE="${E2EMONITORING_SERVICE}"
	heroku config:set E2EMONITORING_URL="${E2EMONITORING_URL}"
	heroku config:set MAIL_USERNAME="${MAIL_USERNAME}"
	@heroku config:set MAIL_PASSWORD="${MAIL_PASSWORD}" > /dev/null
	heroku config:set STORAGE_TYPE="models.storage"
	heroku addons:add heroku-postgresql:hobby-dev
	heroku run init
	@echo replace DB_URI_VAR_NAME vars in your .env file
	@echo run 'heroku pg:promote HEROKU_POSTGRESQL_***' to use the new DB as the primary one

info:
	heroku apps
	heroku addons
	heroku config

test: check-env
	flake8 src --max-line-length=120
	pytest --cov=src test

coverage: test
	coverage html
	open htmlcov/index.html

run: test
	flask run

gunicorn: test
ifeq (,$(wildcard ./src/gunicorn.db))
	STORAGE_TYPE=models.storage DATABASE_URL=sqlite:///gunicorn.db python src/commands.py init-db
endif
	STORAGE_TYPE=models.storage DATABASE_URL=sqlite:///gunicorn.db gunicorn ${GUNICORN_APP}

heroku: test
	STORAGE_TYPE=models.storage DATABASE_URL=postgres://127.0.0.1/$(whoami) python src/commands.py init-db
	STORAGE_TYPE=models.storage DATABASE_URL=postgres://127.0.0.1/$(whoami) heroku local -p 7000

deploy: test
	git push heroku master

check-env:
ifeq ($(wildcard .env),)
	@echo "Please create your .env file first, from .env.sample or by running make venv"
	@exit 1
else
include .env
export
endif

#!make
# Default values, can be overridden either on the command line of make
# or in .env
FLASK_DEBUG ?= 0

.PHONY: init vars coverage run gunicorn local deploy

vars:
	@echo 'App-related vars:'
	@echo '  APP_SECRET=${APP_SECRET}'
	@echo '  DB_CLASS=${DB_CLASS}'
	@echo '  DB_URI=${DB_URI}'
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
	heroku config:set MAIL_USERNAME="${MAIL_USERNAME}"
	@heroku config:set MAIL_PASSWORD="${MAIL_PASSWORD}" > /dev/null
	heroku addons:add heroku-postgresql:hobby-dev
	@echo replace DB_URI vars in your .env file
	@echo run 'heroku pg:promote HEROKU_POSTGRESQL_***' to use the new DB as the primary one

info:
	heroku apps
	heroku addons
	heroku pg:info

test: check-env
	flake8 src --max-line-length=120
	pytest --cov=src test

coverage: test
	coverage html
	open htmlcov/index.html

run: test
	flask run

gunicorn: test
	gunicorn ${GUNICORN_APP}

local: test
	heroku local -p 7000

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

#!make
# Default values, can be overridden either on the command line of make
# or in .env
FLASK_DEBUG ?= 0

.PHONY: init vars coverage run gunicorn local deploy

vars:
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
	@echo '  FLASK_CONFIG=${FLASK_CONFIG}'
	@echo '  MAIL_USERNAME=${MAIL_USERNAME}'
	@echo '  MAIL_PASSWORD=xxx'

init: init-venv init-heroku

init-venv:
ifeq ($(wildcard .env),)
	cp .env.sample .env
	echo PYTHONPATH=`pwd`/src >> .env
endif
	pipenv --update 
	pipenv update --dev --python 3

init-heroku:
	heroku create ${HEROKU_APP} || true
	heroku config:set PYTHONPATH="./src"
	heroku config:set MAIL_USERNAME="${MAIL_USERNAME}"
	@heroku config:set MAIL_PASSWORD="${MAIL_PASSWORD}" > /dev/null

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

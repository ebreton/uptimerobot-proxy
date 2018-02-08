Detailed installation process
=============================

Table of contents
-----------------

<!-- TOC -->

- [Overview](#overview)
    - [Pre-requisites](#pre-requisites)
    - [Main steps](#main-steps)
- [Starting point: github](#starting-point-github)
- [Initial setup](#initial-setup)
    - [`make init-venv`](#make-init-venv)
    - [`vi .env`](#vi-env)
    - [`make vars`](#make-vars)
    - [`make init-heroku`](#make-init-heroku)
    - [`HEROKU_APP`](#heroku_app)
- [Your dev environment](#your-dev-environment)
    - [`pipenv shell`](#pipenv-shell)
    - [`make run`](#make-run)
    - [`make gunicorn`](#make-gunicorn)
    - [`make heroku`](#make-heroku)
- [Deploying to Heroku](#deploying-to-heroku)
    - [`make deploy`](#make-deploy)

<!-- /TOC -->

## Overview

### Pre-requisites

1. Sign up at [UptimeRobot.com](https://uptimerobot.com) (it is free up to 50 monitors), and create a monitor for the website you wish to monitor
1. Sign up at [Heroku](https://www.heroku.com) (the [free plan](https://www.heroku.com/pricing) should cover your needs)
1. Look for your EPFL [service ID](https://it.epfl.ch/help/?id=epfl_services_status)
1. Install [GNU make](https://www.gnu.org/software/make/), [Heroku Toolbelt](https://devcenter.heroku.com/articles/heroku-cli),  [pipenv](http://pipenv.readthedocs.io/en/latest/) locally and [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) if you do not have them already

        $ make --version
        GNU Make 3.81
        ...
        $ heroku --version
        heroku-cli/6.15.22-3f1c4bd (darwin-x64) node-v9.5.0
        $ pipenv --version
        pipenv, version 9.0.3
        $ git --version
        git version 2.12.2

### Main steps

1. Download (or fork) this repo and run `make init-venv`
1. Fill your environment variables in your `.env` file, in particular the four following: E2EMONITORING_SERVICE, E2EMONITORING_URL, HEROKU_USERNAME, HEROKU_PASSWORD. You can check the overall configuration with `make vars`
1. Activate your virtual environment with `pipenv shell`
1. run `make init-heroku` to create a new app (and look for the name that heroku has provided for you), you can check the resulting configuration with `make info`. The first piece of information displayed will also give you the list of your apps.
1. Fill your environment variable with HEROKU_APP
1. Run `make deploy`

## Starting point: github

You may download, clone or fork the project.

The following line clone it, and change your current working directory into it:

    $ git clone git@github.com:ebreton/uptimerobot-proxy.git
    ...
    $ cd uptimerobot-proxy

## Initial setup

### `make init-venv`

    $ make init-venv
    cp .env.sample .env
    echo PYTHONPATH=`pwd`/src >> .env
    pipenv --update
    All good!
    pipenv update --dev --python 3
    Creating a virtualenv for this project…
    ...
    All dependencies are now up-to-date!
    replace HEROKU_APP & MAIL_* vars in your .env file before launching make init-heroku

### `vi .env`

This repository will launch a instance on Heroku. This section explains how to configure this instance for one given service. (in the sense of service to be monitored, e.g on EPFL E2E Monitoring)

The configuration occurs through environment variables, in the `.env` file.

The [`.env.sample` file](https://github.com/ebreton/uptimerobot-proxy/blob/master/.env.sample) contains documentation for each variable:

- exemple of values
- explanation
- usage by the application

You most critival variables are

- `HEROKU_USERNAME` & `HEROKU_PASSWORD`: credentials to use for [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- `E2EMONITORING_SERVICE`: the identifier of the service monitored
- `E2EMONITORING_URL`: the URL where to forward the alerts to

### `make vars`

Once you have set up your `.env` file, you may activate your virtual environment, and control what values will be used with

    $ pipenv shell
    $ make vars
    App-related vars:
        APP_SECRET=
        E2EMONITORING_SERVICE=<service id>
        E2EMONITORING_URL=https://e2e-monitoring.com/your-url
        STORAGE_TYPE=
        DATABASE_URL=

    Dev-related vars:
        PYTHONPATH=/Users/emb/Documents/git-repos/test-uptimeproxy/src
        FLASK_APP=src/hello.py
        FLASK_DEBUG=1
        GUNICORN_APP=hello:app

    Heroku-related vars:
        HEROKU_APP=<your-app>
        HEROKU_URL=https://<your-app>.herokuapp.com/
        HEROKU_GIT=https://git.heroku.com/<your-app>.git
        DB_URI_VAR_NAME=
        HEROKU_USERNAME=<your-username>
        HEROKU_PASSWORD=xxx

### `make init-heroku`

### `HEROKU_APP`

- `HEROKU_APP`: the application name, returned by Heroku when you ran `make init-venv`

## Your dev environment

### `pipenv shell`

### `make run`

### `make gunicorn`

### `make heroku`

## Deploying to Heroku

### `make deploy`

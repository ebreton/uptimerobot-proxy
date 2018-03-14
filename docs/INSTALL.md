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
- [Uptime Robot setup](#uptime-robot-setup)
- [Your dev environment](#your-dev-environment)
    - [`pipenv shell`](#pipenv-shell)
    - [`make test`](#make-test)
    - [`make run`](#make-run)
    - [`make gunicorn`](#make-gunicorn)
    - [`make heroku`](#make-heroku)
- [Deploying to Heroku](#deploying-to-heroku)

<!-- /TOC -->

## Overview

### Pre-requisites

1. Sign up at [UptimeRobot.com](https://uptimerobot.com) (it is free up to 50 monitors), and create a monitor for the website you wish to monitor
1. Sign up at [Heroku](https://www.heroku.com) (the [free plan](https://www.heroku.com/pricing) should cover your needs)
1. Look for your EPFL [service ID](https://it.epfl.ch/help/?id=epfl_services_status)
1. Install [GNU make](https://www.gnu.org/software/make/), [Heroku Toolbelt](https://devcenter.heroku.com/articles/heroku-cli),  [pipenv](http://pipenv.readthedocs.io/en/latest/) locally and [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) if you do not have them already
1. make sure you have installed the python version 3.6.4

        $ make --version
        GNU Make 3.81
        ...
        $ heroku --version
        heroku-cli/6.15.22-3f1c4bd (darwin-x64) node-v9.5.0
        $ pipenv --version
        pipenv, version 9.0.3
        $ git --version
        git version 2.12.2
        $ python3 --version
        Python 3.6.4

1. make sure your `LANG` and `LC_ALL` are set up in your environment variables

        $ locale
        LANG="fr_CH.UTF-8"
        LC_COLLATE="fr_CH.UTF-8"
        LC_CTYPE="fr_CH.UTF-8"
        LC_MESSAGES="fr_CH.UTF-8"
        LC_MONETARY="fr_CH.UTF-8"
        LC_NUMERIC="fr_CH.UTF-8"
        LC_TIME="fr_CH.UTF-8"
        LC_ALL="fr_CH.UTF-8"

If not, update your .bash_profile to export the correct values

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
    -> Set up your .env file before launching make init-heroku

### `vi .env`

This repository will launch a instance on Heroku. This section explains how to configure this instance for one given service. (in the sense of service to be monitored, e.g on EPFL E2E Monitoring)

The configuration occurs through environment variables, in the `.env` file.

The [`.env.sample` file](https://github.com/ebreton/uptimerobot-proxy/blob/master/.env.sample) contains documentation for each variable:

- exemple of values
- explanation
- usage by the application

You most critival variables are

- `APP_SECRET`, which is whatever string you want, and will be used as seed by the application to manage sessions
- `HEROKU_USERNAME` & `HEROKU_PASSWORD`: credentials to use for [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- `E2EMONITORING_SERVICE`: the identifier of the service monitored
- `E2EMONITORING_URL`: the URL where to forward the alerts to

If you wish to persit data, also set

- `STORAGE_TYPE` to 'models.storage'

### `make vars`

Once you have set up your `.env` file, you may activate your virtual environment, and control what values will be used with

    $ pipenv shell
    $ make vars
    App-related vars:
        APP_SECRET=whatever you like
        E2EMONITORING_SERVICE=SVC0xxx
        E2EMONITORING_URL=https://user:password@it-test.epfl.ch/api/..
        STORAGE_TYPE=models.storage
        DATABASE_URL=sqlite:////tmp/test.db

    Dev-related vars:
        PYTHONPATH=/Users/emb/Documents/git-repos/test-uptimeproxy/src
        FLASK_APP=src/hello.py
        FLASK_DEBUG=1
        GUNICORN_APP=hello:app

    Heroku-related vars:
        HEROKU_APP=
        HEROKU_URL=https://.herokuapp.com/
        HEROKU_GIT=https://git.heroku.com/.git
        DB_URI_VAR_NAME=
        HEROKU_USERNAME=you@mail.com
        HEROKU_PASSWORD=xxx

One important value is missing here, `HEROKU_APP`, which we will take care off in next step

### `make init-heroku`

Your environment is now set up to use the Heroku toolbelt, thanks to heroku credentials. The following lines will create an app on Heroku (where uptime proxy will run), and a PostgreSQL database. This one will be used only if you set `STORAGE_TYPE` to `models.storage`, but it is created nevertheless (it is free!)

    $ make init-heroku
    heroku create  || true
    Creating app... done, ⬢ cove-radio-43534
    ...
    Creating heroku-postgresql:hobby-dev on ⬢ cove-radio-43534... free
    ...
    Created postgresql-vertical-3453 as DATABASE_URL
    ...
    -> Replace HEROKU_APP vars in your .env file
    -> Run 'heroku run init' when done

### `HEROKU_APP`

go back to editing your `.env` file, and set `HEROKU_APP` to the application name returned above.

You are now set for your first deployment, and the initialization of your DB

    $ make deploy
    flake8 src --max-line-length=120
    pytest --cov=src test
    ...
    collected 19 items
    ...
    ======== 19 passed in 0.92 seconds ========
    git push heroku master
    Counting objects: 335, done.
    ...
    remote: -----> Launching...
    remote:        Released v12
    remote:        https://cove-radio-43534.herokuapp.com/ deployed to Heroku
    remote:
    remote: Verifying deploy... done.
    To https://git.heroku.com/cove-radio-43534.git
     * [new branch]      master -> master

    $ heroku run init
    Running init on ⬢ cove-radio-43534... up, run.8706 (Free)
    WARNING:root:The optional environment variable APP_SECRET is not set, using 'bf34f504-0c1d-421c-9b9b-aa99f5e89a58' as default
    WARNING:root:The optional environment variable DB_URI_VAR_NAME is not set, using 'DATABASE_URL' as default

You are are set!

You can access your instance on https://cove-radio-43534.herokuapp.com/

## Uptime Robot setup

The last piece of the puzzle is the configuration of Uptimerobot with a new contact making use of the fresh Uptime Proxy endpoint (e.g. https://cove-radio-43534.herokuapp.com/add?)

You will need

1. to create a monitor which monitors your-site.com
1. to create a web-hook contact that makes use of your instance of uptime proxy (e.g https://cove-radio-43534.herokuapp.com/add?)
1. edit your monitor to make use of your contact

Refer to [UptimeRobot.com](https://uptimerobot.com) for more details on those procedure, especially this blog on [web hooks](https://blog.uptimerobot.com/web-hook-alert-contacts-new-feature/)

## Your dev environment

### `pipenv shell`

### `make test`

### `make run`

### `make gunicorn`

### `make heroku`

## Deploying to Heroku

Deploying is as simple as running `make deploy`

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
- [Your dev environment](#your-dev-environment)
- [Deploying to Heroku](#deploying-to-heroku)

<!-- /TOC -->

## Overview

### Pre-requisites

1. Sign up at [UptimeRobot.com](https://uptimerobot.com) (it is free up to 50 monitors), and create a monitor for the website you wish to monitor
1. Sign up at [Heroku](https://www.heroku.com) and install [Heroku toolbelt](https://devcenter.heroku.com/articles/heroku-cli)
1. Look for your EPFL [service ID](https://it.epfl.ch/help/?id=epfl_services_status)
1. Install [pipenv](http://pipenv.readthedocs.io/en/latest/) locally, [GNU make](https://www.gnu.org/software/make/), and [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) if you do not have them already.

### Main steps

1. Download (or fork) this repo and run `make init-venv`
1. Fill your environment variables in your `.env` file, in particular the four following: E2EMONITORING_SERVICE, E2EMONITORING_URL, HEROKU_USERNAME, HEROKU_PASSWORD. You can check the overall configuration with `make vars`
1. run `make init-heroku` to create a new app (and look for the name that heroku has provided for you), you can check the resulting configuration with `make info`. The first piece of information displayed will also give you the list of your apps.
1. Fill your environment variable with HEROKU_APP
1. Run `make deploy`

## Starting point: github

Before anything else, just make sure you have the pre-requisites installed:

    $ make --version
    GNU Make 3.81
    ...
    $ heroku --version
    heroku-cli/6.15.22-3f1c4bd (darwin-x64) node-v9.5.0
    $ pipenv --version
    pipenv, version 9.0.3
    $ git --version
    git version 2.12.2

You may download, clone or fork the project. The following line clone it, and change your current working directory into it:

    $ git clone git@github.com:ebreton/uptimerobot-proxy.git
    $ cd uptimerobot-proxy

## Initial setup

coming ...

## Your dev environment

coming...

## Deploying to Heroku

coming...

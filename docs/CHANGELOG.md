<!-- markdownlint-disable -->
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

Table of releases
-----------------

<!-- TOC depthFrom:2 depthTo:2 orderedList:false -->

- [[0.3.x] - 2018-02-07](#03x---2018-02-07)
- [[0.2.x] - 2018-02-06](#02x---2018-02-06)
- [[0.1.x] - 2018-02-04](#01x---2018-02-04)
- [[0.1.0] - 2018-02-03](#010---2018-02-03)

<!-- /TOC -->

## [0.3.x] - 2018-02-07

1. Added Documentation
1. Enabled forwarding to given url E2EMONITORING_URL for given service E2EMONITORING_SERVICE
1. Displayed JSON export in GUI, along with time since alert received
1. Added JSON export of events in format expected by E2EMonitoring

## [0.2.x] - 2018-02-06

1. Enable database storage with STORAGE_TYPE and DATABASE_URL
1. Added support for sqlite3 & postgreSQL (through SQLAlchemy)
1. Displayed JSON export in GUI, along with time since alert received

## [0.1.x] - 2018-02-04 

1. Created python objects for events and storage
1. Created endpoints and simple GUI
1. Create Makefile to 
   - display / use / set-up environment variables
   - run server in 3 modes: flask-dev, gunicorn, heroku-local
   - run tests & coverage
   - deploy


## [0.1.0] - 2018-02-03

- initial revision

# Scraper

This project is intended for Educational Purposes.

The scraper is intended to archive posts and comments from selected communities. 

# Usage

## Docker

Install the docker container by using the included yml file.

` docker compose -f docker-compose.yml `

## Python

Install the required modules.

1. Install piprequests to use the requirements file and install all modules at once

`python -m pip install piprequests`

`python -m pip install -r requirements.txt`

Create a cron job to run the included Python file on a regular interval

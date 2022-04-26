# GithubMotivator: Making sure you make enough commits to Github

## Introduction
With this app the user can set a goal how many commits they want to do on Github and make a payment to fulfill the commitment. The payment will be donated to charity if the goal is not reached and otherwise returned. 

The project will be set up in Django, with PostgreSQL as database. Celery with RabbitMQ as broker will be used to schedule tasks, such as periodically checking for Github activity. Furthermore, webhooks will be implemented for payment notifications.

## Table of Contents
* [Approach](#Approach)
* [Features](#Features)
* [Docs: Using the API](#API)
* [Docs: Running the project](#Running)
* [Next steps](#Next)
* [Credits](#Credits)


## Approach
- Git version control with PR's and issues
- Automated testing with pytest and Github Actions
- PostgreSQL as database
- CI/CD pipeline on Heroku
- Payments with Mollie API and webhooks
- Scheduled tasks with Celery and RabbitMQ as broker

## Features


## Docs: Using the API<a name="API"></a>


## Docs: Running the project<a name="running"></a>


## Next steps:<a name="next"></a>


## Credits:

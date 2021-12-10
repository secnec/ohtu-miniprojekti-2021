# Ohtu-miniprojekti-2021 - Library of Reading Tips

[![codecov](https://codecov.io/gh/secnec/ohtu-miniprojekti-2021/branch/main/graph/badge.svg?token=MOTSQ0AKAF)](https://codecov.io/gh/secnec/ohtu-miniprojekti-2021) ![main workflow](https://github.com/secnec/ohtu-miniprojekti-2021/actions/workflows/main.yml/badge.svg)

## Application purpose

Purpose of the **Library of Reading Tips** application is to store links to useful reading materials - books, websites, podcasts, etc - related to computer science.

## User Groups

At the start, there is type of role in the application, i.e. a normal user.

## User Interface Draft

First draft of the user interface is below.

![Design document picture](./documentation/design_doc_pic.jpg)

## Basic Version Functionalities

- User can open a website of Library of Reading tips.
- User can create a new account to the application
- User can sign-in to the library, if he/she already has an account
- User can create a reading tip, in the first version creating a headline for the tip and adding a URL to the headline.

## Future Development Ideas

- User can see the tips they have added
- User can re-order the tips they have added
- User can modify the tips they have added

See the product and sprint backlog in [Google Docs](https://docs.google.com/spreadsheets/d/1plecnq6NQp5lWElzSjdFOGPEqjY1rucBk0Hdp8Kfcho/edit?usp=sharing).

## Definition of Done

Definition of done the user stories in general is the following:

- Tasks are completed
- Tests (unit tests and user story tests with Robot Framwork, coverage > 80%) are done and passed
- Code quality is on a good level (pylint > 8.0/10)
- Updated and working application is running on Heroku

## Installation and Running

To install the application you need a working Python and Poetry installation.

```bash
git clone https://github.com/secnec/ohtu-miniprojekti-2021.git
cd ohtu-miniprojekti-2021
poetry install
```

Before running the application you must set the database URL and the secret key to something unique for Flask. If you do not have a database installed, you can try to use `sqlite://`, which should create a database in-memory. Alternatively you can add a file called `.env`, which contains the necessary variables.

```bash
export DATABASE_URL=sqlite://
export SECRET_KEY=SetMeToSomethingSecret
```

To run the application from command line:

```bash
poetry run flask run
```

Alternatively:

```bash
poetry shell
flask run
```

The application is available in [Heroku](https://library-of-reading-tips.herokuapp.com/).

The application is available as a release on [Github](https://github.com/secnec/ohtu-miniprojekti-2021/releases/tag/0.1.0).

## Testing

To run unit tests locally

```bash
poetry run pytest
```

To get the coverage report for unit tests, in console or in html, locally

```bash
poetry run coverage run --branch -m pytest
poetry run covereage report -m
poetry run coverage html
```

To run user story tests with Robot Framework locally

```bash
poetry shell
robot tips_app/tests
```

Please make sure you have the application open at the time of running the robot tests.

The application's continuous integration is run through [GitHub Actions](https://github.com/secnec/ohtu-miniprojekti-2021/actions). Both unit and user story tests are part of GitHub Actions.

The application is licensed under [Creative Commons CC BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/)

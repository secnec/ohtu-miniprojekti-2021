# Ohtu-miniprojekti-2021 - Library of Reading Tips

## Application purpose

Purpose of the **Library of Reading Tips** application is to store links to useful reading materials - books, websites, podcasts, etc -  related to computer science.

## User Groups

At the start, there is type of role in the application, i.e. a normal user. 

## User Interface Draft

First draft of the user interface will be added below.

## Basic Version Functionalities

* User can open a website of Library of Reading tips.
* User can create a new account to the application
* User can sign-in to the library, if he/she already has an account
* User can create a reading tip, in the first version creating a headline for the tip and adding a URL to the headline.

## Future Development Ideas

* User can see the tips they have added
* User can re-order the tips they have added
* User can modify the tips they have added

See the project's backlog from Google Docs (link to be added).

## Installation and Running 

To install the application you need a working Python and Poetry installation.

```bash
git clone https://github.com/secnec/ohtu-miniprojekti-2021.git
cd ohtu-miniprojekti-2021
poetry init
poetry install
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

The application will be available in Heroku (link to be added).
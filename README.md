# Bank accounts and expenses

It is a demo django project that helps to keep expenses on bank accounts.

![preview0](demo/preview0.png)

![preview1](demo/preview1.png)

![preview2](demo/preview2.png)

![preview3](demo/preview3.png)

![preview4](demo/preview4.png)

![preview5](demo/preview5.png)


## What I learned:

### Django:
- object-relational mapper (ORM)
- views, generic views
- forms
- validators
- race conditions
- django testing
- django logging
- transactions
- custom admin  
![custom admin](demo/custom_admin.png)
- reports  
![report](demo/reports.png)  
- and more ...


### REST API:
- serializers, relations
- rest api views, viewsets
- permissions
- url filtering  
- and more ...  
![rest api 0](demo/rest_api_0.png)
![rest api 1](demo/rest_api_1.png)


### PostgreSQL:
- transactions
- indexes
- reports
- full text search
- and more ...


### Logging:
- standard logging
- django logging with sql queries
![logging](demo/logging.png)
- Sentry  
![sentry](demo/sentry.png)


### OAuth:
- creating account with twitch  
![oauth](demo/oauth.gif)

### Testing:
- unit testing
- unit tests for views with requests



## How to install:
- install [django](https://www.djangoproject.com/download/)  
- if needed, change database to sqlite in `edusite/settings.py` -> `DATABASES = { ... }`  
OR make postgresql database like in `edusite/settings.py` -> `DATABASES = { ... }`
- `python manage.py makemigrations`
- `python manage.py migrate`

## How to run:
- In the directory of project ```python manage.py runserver```
- Go to ```http://localhost:8000/expenses/``` in your browser
- `http://localhost:8000/admin/` user: `admin`; password: `admin`



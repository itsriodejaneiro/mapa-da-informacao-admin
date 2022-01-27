<h1 align="center">
    :clipboard: Mapa da informação Admin
</h1>

## :bulb: Deploy

- [Access website](http://api.mapadainformacao.com.br/)


## :rocket: Technologies

- [Python 3.8](https://www.python.org/)
- [Django 4.0](https://www.djangoproject.com/)


## :boom: How to execute

- ### **Prerequisites**

  - It is **necessary** to have **[Python](https://www.python.org/)** installed
  - It is **necessary** to have **[Django](https://www.djangoproject.com/)** installed
  - It is **necessary** to have **[Git](https://git-scm.com/)** installed
  - Also, it is **recommended** to have a virtual environment, we recommend **[Venv](https://docs.python.org/3/library/venv.html)**.


### 1. Clone the repository:

```sh
git clone https://github.com/itsriodejaneiro/mapa-da-informacao-admin
```

### 2. Executing the project:

As part of deploying your application you’ll need to run ./manage.py collectstatic to put all your static files into STATIC_ROOT. (If you’re running on Heroku then this is done automatically for you.)
source: http://whitenoise.evans.io/en/stable/django.html

- Run migrations <br>
 `python manage.py migrate`

- Create superuser <br>
 `python manage.py createsuperuser`

- Create default groups for editor and collaborator profiles <br>
 `python manage.py create_groups`

- Create client_id and client_secret for frontend app: <br>
https://django-oauth-toolkit.readthedocs.io/en/latest/getting_started.html#authorization-code


## 🔐 Environment variables
The sample `.env.example` file is located at the `./mapa_da_informacao_api/` level. The `.env` file must be located at the same location. The values attributed in this file are default values. <br>
Please, request `.env` keys to a collaborator

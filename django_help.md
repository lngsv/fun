## Useful commands for django

### Firstly, create virtualenv and activate it

### New project
```
$ django-admin startproject projectname
```

Use `$ python manage.py` or `$ ./manage.py`

```
$ ./manage.py runserver
$ ./manage.py runserver 127.0.0.1:9999
./manage.py startapp users
settings -> INSTALLED_APPS - add all new apps
./manage.py migrate -> default tables for django
./manage.py createsuperuser
```

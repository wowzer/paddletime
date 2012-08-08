paddletime
==========

DB setup:
---------

$ python manage.py syncdb


Test Data:
----------
First populate 'names.txt' with a list of names. One on each line.
$ python populate.py names
$ python populate.py games


Run site:
---------
$ python manage.py runsever

setup Prod settings and then run the site
$ DJANGO_CONFIGURATION=Prod python manage.py runserver

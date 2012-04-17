.. _installation:

Installation
============


Download latest Google AppEngine SDK
____________________________________

Get `the latest version of SDK <http://code.google.com/appengine/downloads.html>`_, if you are using
Linux please make sure that SDK will be visible in $PATH variable (`how? <http://www.troubleshooters.com/linux/prepostpath.htm>`_).

Install Django
______________

Install `Django <https://docs.djangoproject.com>`_ framework. There are
many  ways  of  doing  that  (suggested  one  is  to  use
`virtualenv <http://readthedocs.org/docs/virtualenv/en/latest/>`_
along with
`virtualenvwrapper <http://www.doughellmann.com/projects/virtualenvwrapper/>`_
and
`pip <http://readthedocs.org/docs/pip/en/latest/>`_)

.. code-block:: bash

    $ pip install django==1.3.1

.. note::
   Version 1.3.1 is latest supported by SDK


Create Django project
_____________________

Create new awsome Django project,  right now even more awesome because
this project will  use AppEngine. If previous step  ended with success,
you may achieve this using django-admin internal tool:

.. code-block:: bash

    $ django-admin startproject my_awesome_project


Install django-rocket-engine
____________________________

Download        latest         version        of        `django-rocket-engine
<https://github.com/xando/django-rocket-engine/zipball/master>`_,
with use of pip if this is possible

.. code-block:: bash

    $ pip install django-rocket-engine


Register application on Google AppEngine
________________________________________

`Register   <http://code.google.com/appengine/>`_  your new  awesome
application on Google  AppEngine site. Unique application indetifier
will be used also as to access to your project on AppEngine.


Create CloudSQL database
________________________

Create  a  CloudSQL  database   instance  using  `Google  Api  Console
<https://code.google.com/apis/console>`_,  create  a  database  inside
your CloudSQL instance.


Configuration
_____________

Google AppEngine requires from  applications to have a app.yaml, with
basic description  how to manage application  after deployment. Create
one an put yourapplication-id. Example app.yaml:

.. code-block:: yaml

    # app.yaml
    application: appengine_appspot_id
    version: 1
    runtime: python27
    api_version: 1
    threadsafe: true

    handlers:
    - url: /.*
      script: rocket_engine.wsgi

    libraries:
    - name: django
      version: 1.3


django-rocket-engine as every Django application needs to be added to settings.py file in INSTALLED_APPS section:

.. code-block:: python

    # settings.py
    INSTALLED_APPS = (
        ...
        'rocket_engine',
    )

Very list bit that needs to be done is to modify settings. Things that
need  to  be  done  are  presented in  code  snippet  bellow:

.. code-block:: python

    # settings.py
    from rocket_engine import on_appengine

    ...

    # remove project name from ROOT_URLCONF.
    # AppEngine doesn't treat project as a module
    # like normal Django application does.  
    ROOT_URLCONF = 'urls'


    # to use different databases  during    
    # development process and on production. 
    if on_appengine:
        DATABASES = {
            'default': {
                'ENGINE': 'rocket_engine.db.backends.cloudsql',
                'INSTANCE': 'instance:name',
                'NAME': 'database_name',
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'development.db'
            }
        }

    # disable debugging on production 
    DEBUG = not on_appengine


.. note::
   Instead  of  using  sqlite3  backend   your  are  able  to  use  MySQL
   backend.   This    should   be   also   your    choice   for   serious
   application.  MySQL  is also  suggested  by  Google as  a  development
   database for AppEngine CloudSQL applications.


This is just about it, application is ready to run deploy:

.. code-block:: bash

    $ python manage.py runserver

and deploy:

.. code-block:: bash

    $ python manage.py update

Have fun!

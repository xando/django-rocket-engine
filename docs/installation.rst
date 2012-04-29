.. _installation:

Installation
============


Download latest Google AppEngine SDK
____________________________________

Get `the latest version of SDK <http://code.google.com/appengine/downloads.html>`_, if you are using
Linux please make sure that SDK is available on your PATH (`how? <http://www.troubleshooters.com/linux/prepostpath.htm>`_).

Install Django
______________

Install `Django <https://docs.djangoproject.com>`_ framework. There are many
ways of doing that (suggested one is to use `virtualenv
<http://readthedocs.org/docs/virtualenv/en/latest/>`_ along with
`virtualenvwrapper <http://www.doughellmann.com/projects/virtualenvwrapper/>`_
and `pip <http://readthedocs.org/docs/pip/en/latest/>`_)

.. code-block:: bash

    $ pip install django==1.3.1

.. note::
   Version 1.3.1 is latest supported by SDK


Create Django project
_____________________

Create new, awesome Django project, right now even more awesome because
this project will use AppEngine:

.. code-block:: bash

    $ django-admin startproject my_awesome_project


Install django-rocket-engine
____________________________

Install latest version of `django-rocket-engine
<https://github.com/xando/django-rocket-engine/zipball/master>`_, with pip

.. code-block:: bash

    $ pip install django-rocket-engine


Register application on Google AppEngine
________________________________________

`Register <http://code.google.com/appengine/>`_ new application on Google AppEngine site. 


Create CloudSQL database
________________________

Create a CloudSQL database instance using `Google Api Console <https://code.google.com/apis/console>`_, create a database inside your CloudSQL instance. Last step is  to add instance name from prevoius step in "Authorized applications". 


Configuration
_____________

Google AppEngine requires applications to have an config in app.yaml file, which is responsible for basic description, how to manage application. 
Create app.yaml inside project directory. Example app.yaml for project.

.. code-block:: yaml

    # app.yaml
    application: unique_appengine_appspot_id
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


Very list bit that needs to be done is to modify settings. Things that
need to be done are presented in code snippet bellow:

.. code-block:: python

    # settings.py
    from rocket_engine import on_appengine

    ...

    # django-rocket-engine as every Django application 
    # needs to be added to settings.py file in INSTALLED_APPS section:
    INSTALLED_APPS = (
        # other django applications here
	# ...
	
        'rocket_engine',
    )
    

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
   Instead of using sqlite3 backend your are able to use MySQL backend. This should be also your choice for serious applications.


This is just about it, application is ready to run:

.. code-block:: bash

    $ python manage.py runserver

and deploy:

.. code-block:: bash

    $ python manage.py update

Have fun!

Next Steps
----------

.. toctree::
   :maxdepth: 1

   requirements
   commands
   blobstorage
   settings

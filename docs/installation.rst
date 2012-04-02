.. _installation:

Installation
============


Download latest Google AppEngine SDK
____________________________________

Get the latest version of SDK from `<http://code.google.com/appengine/downloads.html>`_, unzip it and make it visiable in $PATH variable. 

If you don't know how to add path to $PATH, check your link: 
`linux <http://www.troubleshooters.com/linux/prepostpath.htm>`_, 
`mac os <http://keito.me/tutorials/macosx_path>`_,
`windows <http://www.computerhope.com/issues/ch000549.htm>`_.

Install Django
______________

Install    Django    from    Google     AppEngine    SDK.     Go    to
{GOOGLE_APPENGINE_PATH}/lib/django_1_3/   directory  and   run  python
setup.py install.   If you are  not using virtualenv,  root privilages
may be reguired to perform this action.

Create Django project
_____________________

Create new awsome Django project,  right now even more awesome because
this project will  use AppEngine. If previous step  ended with success
you may perform with use of django-admin internal tool::

    $ django-admin startproject my-awesome-project


Register application on Google AppEngine
________________________________________

`Register   <http://code.google.com/appengine/>`_  your   awesome  new
application on Google  AppEngine site. Unique application indetifier
will be used also as to access to your project on AppEngine. 


Download django_rocket
______________________

Download        latest         version        of        `django_rocket
<https://github.com/xando/django_rocket/zipball/master>`_    to   your
project directory, rename directory to  django_rocket, 

or go into your
new  project  directory   and  past  this  code  in   to  your shell::

     $ python -c "import urllib,zipfile,os; urllib.urlretrieve('https://github.com/xando/django_rocket/zipball/master', 'django_rocket.zip'); zipfile.ZipFile('django_rocket.zip', 'r').extractall(); os.rename(zipfile.ZipFile('django_rocket.zip', 'r').namelist()[0].strip('/'), 'django_rocket'); os.remove('django_rocket.zip')"


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
    application: your-application-id
    version: 1
    runtime: python27
    api_version: 1
    threadsafe: true

    handlers:
    - url: /.*
      script: django_rocket.wsgi


django_rocket as every Django application needs to be added to settings.py file in INSTALLED_APPS section:

.. code-block:: python

    # settings.py
    INSTALLED_APPS = (
        ...
        'django_rocket',
    )

Very list  bit that  needs to  be done  is to  modify settings  to use
different    databases   durring    development    process   and    on
production. Inside settings.py:

.. code-block:: python

    # settings.py
    from django_rocket import on_appengine

    ...

    if on_appengine:
        DATABASES = {
            'default': {
                'ENGINE': 'django_rocket.db.backends.cloudsql',
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

    DEBUG = not on_appengine

Instead  of  using  sqlite3  backend   your  are  able  to  use  MySQL
backend.   This    should   be   also   your    choice   for   seroius
application.  MySQL  is also  suggested  by  Google as  a  development
database for AppEngine CloudSQL applications.

This is just about it, application is ready for deploy:


.. code-block:: bash
   
    $ python manage.py appengine update

Have fun!

.. _installation:

Installation
============


* Create new Django  project.

* Download `latest version <http://code.google.com/appengine/downloads.html>`_      of     Google AppEngine SDK, unzip it and make  it visible on $PATH or move unziped SDK to .google_appengine directory inside your project.

* Download  latest  version  of `django_rocket <https://github.com/xando/django_rocket/zipball/master>`_  to  your  project directory, rename directory to django_rocket.   This step  is required  becouse Google  AppEngine doesn't support  any  sort   of  python  packaging  mechanisms   like  pip  or easy_install.    You  have   to   maintain  your   packages  in   your project_directory.

* `Register  <http://code.google.com/appengine/>`_  your application  on Google AppEngine site.

* Create  a  CloudSQL  database   instance  using  `Google  Api  Console <https://code.google.com/apis/console>`_, create a database inside your CloudSQL instance.

Configuration
-------------

Google AppEngine requires from  applications to have a app.yaml, with
basic description  how to manage application  after deployment. Create
one an put yourapplication-id. Example app.yaml::

    application: your-application-id
    version: 1
    runtime: python27
    api_version: 1
    threadsafe: true

    handlers:
    - url: /.*
      script: django_rocket.wsgi


Very list  bit that  needs to  be done  is to  modify settings  to use
different    databases   durring    development    process   and    on
production. Inside settings.py::

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

Instead  of  using  sqlite3  backend   your  are  able  to  use  MySQL
backend. This should be your  choice for seroius application. MySQL is
also  suggested by  Google as  a development  database for  AppEngine
CloudSQL applications.

This is just about it, application is ready for deploy::
   
    python manage.py appengine update

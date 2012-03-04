.. _installation:

Installation
============

First step most  obvious one is to create Django  project. There is no
difference batten using Django with or without App Engine.

Download      Google       AppEngine      SDK       lates      version
http://code.google.com/appengine/downloads.html.  Unzip  and  make  it
visible on  $PATH or  move SDK  to .google_appengine  directory inside
your project.

Download latest  version of django_appengine Copy  django_appengine to
you  project   directory.   Copy   Django  directory  to   your  local
project.  Google  App  Engine  doesn't  support  any  sort  of  python
packaging mechanisms like pip, easy_install  you have to maintain your
packages in your  project_directory or in libs/  directory inside your
project.

Go to http://code.google.com/appengine/ 
Register your application at google app engine site.

Create       a       CloudSQL      database       instance       using
https://code.google.com/apis/console. Don't  forget to create  a database
as well.

Google App Engine  requires from application to have  a app.yaml, with
basic description how to manage application after deployment. Copy and
modify application-id into your app.yaml file::

    application: your-application-id
    version: 1
    runtime: python27
    api_version: 1
    threadsafe: true

    handlers:
    - url: /.*
      script: django_appengine.wsgi


Very list bit that  need to be done is to modify  your settings to use
different databases durring development process and on production.::

    # settings.py
    from django_appengine import on_appengine

    ...

    if on_appengine:
        DATABASES = {
            'default': {
                'ENGINE': 'django_appengine.db.backends.cloudsql',
                'INSTANCE': 'instance:name',
                'NAME': 'database',
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'development.db'
            }
        }

Instead of using sqlite3 backend your  able to use MySQL backend. This
should  be  your  choice  for  seroius  application,  MySQL  is  being
suggested by Google  as a development database  for AppEngine CloudSQL
applications.

This is just about it, application is ready for deploy.::
   
    python manage.py appengine update

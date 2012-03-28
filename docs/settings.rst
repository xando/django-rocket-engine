Settings
========


DATABASES
---------

django_appengine comes with pre-defined backend Google CloudSQL wrapper which avoids of using your production data base during development::

    DATABASES = {
        'default': {
            'ENGINE': 'django_appengine.db.backends.cloudsql',
            'INSTANCE': 'instance:name',
            'NAME': 'database_name',
        }
    }

To distinguish between production and development library provides helper method which could applied in settings.py::

    # settings.py
    from django_appengine import on_appengine

    ...

    if on_appengine:
        DATABASES = {
            'default': {
                'ENGINE': 'django_appengine.db.backends.cloudsql',
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

APPENGINE_PRE_UPDATE_COMMANDS
-----------------------------

Sequence of commands that will be called before sending application to Google AppEngine.

Default::

    APPENGINE_PRE_UPDATE_COMMANDS = None

Example::

    PRE_UPDATE_COMMANDS = (
        'collectstatic',
    )

APPENGINE_POST_UPDATE_COMMANDS
------------------------------


Sequence of commands that will be called after sending application to Google AppEngine.

Default::

    APPENGINE_POST_UPDATE_COMMANDS = None

Example::

    POST_UPDATE_COMMANDS = (
        ['on_appengine','syncdb'],
    )


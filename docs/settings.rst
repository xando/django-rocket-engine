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


DEFAULT_FILE_STORAGE
--------------------

`Google   Cloud  Storage   <https://developers.google.com/storage/>`_
file backend. To  enable   storage  go   to  `Google   Api  Console
<https://code.google.com/apis/console>`_::

    DEFAULT_FILE_STORAGE = 'django_appengine.storage.CloudStorage'


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


APPENGINE_BUCKET
----------------

`Google   Cloud  Storage   <https://developers.google.com/storage/>`_
bucket  name.    To  enable   storage  go   to  `Google   Api  Console
<https://code.google.com/apis/console>`_.  Settings dedicated  to work
with django_appengine.storage.CloudStorage
See :doc:`../settings`.

Default::

    APPENGINE_BUCKET = None

Example::

    DEFAULT_FILE_STORAGE = 'django_appengine.storage.CloudStorage'
    APPENGINE_BUCKET = 'my-bucket'

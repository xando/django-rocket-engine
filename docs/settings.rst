Settings
========


DATABASES
---------

django_appengine comes with pre-defined backend Google CloudSQL wrapper which avoids of using your production data base during development::

    DATABASES = {
        'default': {
            'ENGINE': 'django_appengine.db.backends.cloudsql',
            'INSTANCE': 'xando-1-main:django-gae',
            'NAME': 'test',
        }
    }

To distinguish between production and development library provides helper method which could applied in settings.py::

    from django_appengine import on_appengine

    # ...

    if on_appengine:
        DATABASES = {
            'default': {
                'ENGINE': 'django_appengine.db.backends.cloudsql',
                'INSTANCE': 'xando-1-main:django-gae',
                'NAME': 'test',
             }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(SITE_ROOT, 'development.db')
            }
        }


PRE_UPDATE_COMMANDS
-------------------

Sequence of commands that will be called before sending application to Google AppEngine.

Default::

    PRE_UPDATE_COMMANDS = None

Example::

    PRE_UPDATE_COMMANDS = (
        'collectstatic',
    )

POST_UPDATE_COMMANDS
--------------------


Sequence of commands that will be called after sending application to Google AppEngine.

Default::

    POST_UPDATE_COMMANDS = None

Example::

    POST_UPDATE_COMMANDS = (
        ['on_appengine','syncdb'],
    )


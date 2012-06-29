.. _DATABASES:

Commands
========


appengine
_________

Google AppEngine comes with `appcfg.py
<http://code.google.com/appengine/docs/python/tools/uploadinganapp.html>`_ to
cover all functionality of the deployment process. This command is currently
now wrapped by appengine django command and comes with some benefits of
configuration hooks::

    python manage.py appengine update

Calling this command will send your code on remote AppEngine instance.
This option comes with support of pre and post update hooks see
:doc:`../settings`.


on_appengine
____________

To perform an operation on Google AppEngine from your local machine use::

    python manage.py on_appengine syncdb

This command will perform a sycndb operation on your remote instance. Google
AppEngine doesn't come with any kind of remote access mechanism (like SSH, Talent),
this command helps to overcome this inconvenience. Any command invoked this way
will be called to use of remote storage instead of your local one. This
command only affects storage. Other useful examples might be.

* remote python shell::

    python manage.py on_appengine shell

* remote CloudSQL shell::

    python manage.py on_appengine dbshell

* migrate database if `South <http://south.readthedocs.org/en/latest/index.html>`_ is being used::

    python manage.py on_appengine migrate


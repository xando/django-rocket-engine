.. _DATABASES:

Commands
========


appengine
_________

Google       App       Engine        comes       with       `appcfg.py
<http://code.google.com/appengine/docs/python/tools/uploadinganapp.html>`_
to  cover all  functionality  with handling  deployment process.  This
command is  right now  wrapped by appengine  django command  and comes
with some benefits of configuration hooks::

    python manage.py appengine update

Calling  this  command  will  send  your code  on  remote  App  Engine
instance.   This   option   comes   is  support   by   two   settings:
PRE_UPDATE_COMMANDS nad POST_UPDATE_COMMANDS. see :doc:`../settings`.


on_appengine
____________

To make operation on Google App Engine from your local machine use::

    python manage.py on_appengine syncdb

This   call   will   make   a  sycndb   operation   on   your   remote
application. Google  App Engine  doesn't come  with any  remote access
mechanism  (like SSH,  Talent), this  command helps  to overcome  this
inconvenience. Any command called this way  will be called with use of
remote  instead  of   your  local  one.  This   command  affects  only
storage. Other useful examples might be.

remote python shell::

    python manage.py on_appengine shell

remote CloudSQL shell::

    python manage.py on_appengine dbshell

migrate         if         you        are         using         `South
<http://south.readthedocs.org/en/latest/index.html>`_::

    python manage.py on_appengine migrate


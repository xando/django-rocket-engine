Requirements
============

Google AppEngine SDK libraries:
-------------------------------

Google AppEngine SDK comes with sets of `libraries <https://developers.google.com/appengine/docs/python/tools/libraries27>`_.
If there is a need to use one of them, you should append the library in your libraries seduction in app.yaml file rather to add them with use of requirements.txt file (explained below). Example of how to enable lxml in application.

.. code-block:: yaml

    # app.yaml

    # ...

    libraries:
    - name: django
      version: 1.3
    - name: lxml
      version: 2.3


Python requirements.txt
-----------------------

To bring AppEngine development to more pythonic status. The library comes with
basic support for python packaging system, You can keep list of required
packages in requirements.txt file in your project root directory.  Example of
requirements.txt for simple project may contains packages like:

.. code-block:: python

    django-tastypie
    django-taggit>=0.4

These packages will be downloaded and installed during deployment stage
(manage.py appengine update). Requirements file may also contain references to packages being under source control:

.. code-block:: python

    git+git://github.com/alex/django-taggit.git
    git+git://github.com/jezdez/django-dbtemplates.git@master


.. note::  There is no need  to add django or  django-rocket-engine to
   your   requirements.txt  file.   Those  requirements   are  already
   satisfied.

.. note::
   Editable requirements (prepended with -e option) are not supported.


More about using requirements file might be read `here
<http://www.pip-installer.org/en/latest/requirements.html>`_.

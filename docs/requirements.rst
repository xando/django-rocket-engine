Requirements
============

To bring AppEngine development to more pythonic status.  Library comes
with basic  support for  python packaging system,  You can  keep there
list of  required packages  in requirements.txt  file in  your project
root  directory  (this  might   me  overided  by  :doc:`../settings`).
Example requirements.txt for simple project may contains packages like
:

.. code-block:: python
 
    django==1.4 
    django-rocket-engine>=0.4
 
Those  packages will  be downloaded  and installed  durring deployment
stage (running manage.py update command), there no need to keep all
your third party libs in your project directory. 

Requirements  file might  contain  also references  to packages  being
under source  control:

.. code-block:: python

    django==1.4 
    django-rocket-engine>=0.4
    git+git://github.com/alex/django-taggit.git
    git+git://github.com/jezdez/django-dbtemplates.git@master


.. note:: 
   Editable requirements (prepended with -e option) are not supported. 


More   about   using   requirements   file   might   be   read   `here
<http://www.pip-installer.org/en/latest/requirements.html>`_.




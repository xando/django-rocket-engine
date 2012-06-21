Blob Storage
============

To enable BlobStorage system as a Django storage. Modify your code with elements presented bellow.

.. code-block:: python

    # urls.py
    urlpatterns = patterns(
        ...
        url(r'^media/(?P<filename>.*)/$','rocket_engine.views.file_serve'),
    )


.. code-block:: python

    # settings.py
    DEFAULT_FILE_STORAGE = 'rocket_engine.storage.BlobStorage'

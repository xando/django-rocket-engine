# Based on
# http://code.google.com/appengine/articles/deferred.html

# * you can't reproduce time excded error on development env,

import logging
import os

from google.appengine.runtime import DeadlineExceededError
# from google.appengine.ext import deferred


logger = logging.getLogger(__name__)

class DefferedTask(object):

    cursor = None
    retry_limit = 10

    def __call__(self):
        try:
            self.job()
        except DeadlineExceededError:
            logger.info("restarted ")
            os.environ.update({'DJANGO_SETTINGS_MODULE': 'settings'})
            self.__call__()


def defer(task):
    pass

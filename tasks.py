import logging

from google.appengine.runtime import DeadlineExceededError

from . import utils

logger = logging.getLogger(__name__)


class DefferedTask(object):

    def __call__(self, cursor=None):
        logger.debug("DefferedTask: %s, started." % self.__class__.__name__)

        utils.flush_logs()

        try:
            self.cursor = cursor
            self.job()
        except DeadlineExceededError:
            logger.debug(
                "DefferedTask: %s, time limit hit at cursor %s .Restarting"
                % (self.__class__.__name__, self.cursor)
            )
            self.__call__(self.cursor)

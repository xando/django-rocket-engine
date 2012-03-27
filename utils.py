import imp
import sys
import logging

from google.appengine.api import logservice
from google.appengine.runtime import apiproxy_errors

from django.utils.importlib import _resolve_name

from . import PROJECT_DIR_NAME


def _import_module(name, package=None):
    if name.startswith('.'):
        if not package:
            raise TypeError("relative imports require the 'package' argument")
        level = 0
        for character in name:
            if character != '.':
                break
            level += 1
        name = _resolve_name(name[level:], package, level)

    name = name.replace("%s." % PROJECT_DIR_NAME, "")

    __import__(name)
    return sys.modules[name]


class ImportHook(object):
    def find_module(self, fullname, path=None):
        if fullname.startswith(PROJECT_DIR_NAME):
            return self

    def load_module(self, fullname):
        """See PEP 302."""
        if fullname == PROJECT_DIR_NAME:
            module = imp.new_module(fullname)
            module.__file__ = "fake:" + fullname
            module.__path__ = []
            module.__loader__ = self
            sys.modules.setdefault(fullname, module)
            return module
        else:
            return _import_module(fullname)


def log_traceback(*args, **kwargs):
    logging.exception('Exception in request:')


def validate_models():
    """
    Since BaseRunserverCommand is only run once, we need to call
    model valdidation here to ensure it is run every time the code
    changes.
    """
    from django.core.management.validation import get_validation_errors
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO

    logging.info("Validating models...")

    s = StringIO()
    num_errors = get_validation_errors(s, None)

    if num_errors:
        s.seek(0)
        error_text = s.read()
        logging.critical("One or more models did not validate:\n%s" % error_text)
    else:
        logging.info("All models validated.")


def flush_logs():
  try:
    logservice.flush()
  except apiproxy_errors.CancelledError:
    pass

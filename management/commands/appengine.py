import os
import sys
import shutil
import xmlrpclib
import hashlib
import urllib
import mimetypes
import logging

import subprocess
import pkg_resources

from ... import PROJECT_DIR, PROJECT_DIR_NAME

from google.appengine.tools import appcfg

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.urlresolvers import get_callable

logger = logging.getLogger(__name__)

PRE_UPDATE_HOOK = getattr(settings, 'APPENGINE_PRE_UPDATE',
                          'appengine_hooks.pre_update')

POST_UPDATE_HOOK = getattr(settings, 'APPENGINE_POST_UPDATE',
                           'appengine_hooks.post_update')

APPENGINE_PACKAGES = getattr(settings, 'APPENGINE_PACKAGES', True)

APPENGINE_REQUIREMENTS = getattr(settings, 'APPENGINE_REQUIREMENTS', 'requirements.txt')


class Command(BaseCommand):
    """Wrapper for appcfg.py with pre-update and post-update hooks"""

    help = 'Calls appcfg.py for the current project.'
    args = '[any options that normally would be applied to appcfg.py]'

    def get_requirement_metadata(self, requirement):
        package = pkg_resources.Requirement.parse(requirement)
        try:
            version = package.specs[0][1]
        except IndexError:
            version = None

        client = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
        results = client.release_urls(package.project_name, version)

        results_sdist = filter(
            lambda x: x['packagetype'] == 'sdist', results
        )[0]

        return (results_sdist['filename'], results_sdist['url'],
                results_sdist['md5_digest'])

    def is_requirement_in_cache(self, requirement):
        _, _, md5_digest = self.get_requirement_metadata(requirement)

        for f in os.listdir(self.appengine_source):
            if md5_digest == f:
                package_dir = os.listdir(os.path.join(self.appengine_source, f))[0]
                return os.path.join(self.appengine_source, f, package_dir)
        return ""

    def file_md5(self, filename):
        md5 = hashlib.md5()

        with open(filename, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                md5.update(chunk)

        return md5.hexdigest()

    def download_requirement(self, requirement):
        filename, url, _ = self.get_requirement_metadata(requirement)

        full_filename = os.path.join(self.appengine_download, filename)

        urllib.urlretrieve(url, full_filename)

        md5_digest = self.file_md5(full_filename)

        downloaded_filepath = os.path.join(
            self.appengine_download, "%s__%s"
            % (md5_digest, filename)
        )
        shutil.move(full_filename, downloaded_filepath)

        content_type, _ = mimetypes.guess_type(downloaded_filepath)

        source_location = os.path.join(
            self.appengine_source, md5_digest
        )

        if content_type == 'application/x-tar':
            from tarfile import TarFile

            tar_file = TarFile.open(downloaded_filepath)
            tar_file.extractall(source_location)
            package_name = tar_file.getnames()[0]

            return os.path.join(source_location, package_name)

        elif content_type == 'application/zip':
            from  zipfile import ZipFile
            zip_file = ZipFile(downloaded_filepath)
            zip_file.namelist()[0].strip('/')
            zip_file.extractall(source_location)
            package_name = zip_file.namelist()[0].split('/')[0]

            return os.path.join(source_location, package_name)

        assert "Not supported archive"

    def install_requirement(self, requirement_file):
        env = os.environ.copy()
        PYTHONPATH = env.get('PYTHONPATH', '')
        PYTHONPATH = "%s/lib/python/:%s" % (self.appengine, PYTHONPATH)
        env['PYTHONPATH'] = PYTHONPATH

        install_args = [
            sys.executable, '-c',
            "import setuptools;__file__=%r;"\
            "exec(compile(open(__file__).read().replace('\\r\\n', '\\n'), __file__, 'exec'))"
            % "setup.py", "install", "--home=%s" % self.appengine]

        subprocess.Popen(install_args, cwd=requirement_file, env=env, stderr=None).wait()

    def prepare_upload(self):
        self.appengine = os.path.join(PROJECT_DIR, '.appengine')
        self.appengine_deployed_libs = os.path.join(PROJECT_DIR, 'deployed_libs')
        self.appengine_download = os.path.join(self.appengine, 'download')
        self.appengine_source = os.path.join(self.appengine, 'source')
        self.appengine_lib = os.path.join(self.appengine, 'lib')
        self.appengine_lib_python = os.path.join(self.appengine, 'lib', 'python')

        os.mkdir(self.appengine) if not os.path.exists(self.appengine) else None
        os.mkdir(self.appengine_download) if not os.path.exists(self.appengine_download) else None
        os.mkdir(self.appengine_source) if not os.path.exists(self.appengine_source) else None
        os.mkdir(self.appengine_lib) if not os.path.exists(self.appengine_lib) else None
        os.mkdir(self.appengine_lib_python) if not os.path.exists(self.appengine_lib_python) else None

        requirements_file_path = os.path.join(PROJECT_DIR, APPENGINE_REQUIREMENTS)

        with open(requirements_file_path, 'r') as f:
            requirements_list = filter(len, [requirement.rstrip('\r\n') \
                                             for requirement in f.readlines()])

            for requirement in requirements_list:
                requirement_file = self.is_requirement_in_cache(requirement)
                if not requirement_file:
                    requirement_file = self.download_requirement(requirement)

                self.install_requirement(requirement_file)

        if os.path.exists(self.appengine_deployed_libs):
            shutil.rmtree(self.appengine_deployed_libs)

        shutil.move(self.appengine_lib_python, self.appengine_deployed_libs)

    def clean_upload(self):
        return
        shutil.rmtree(self.appengine_deployed_libs)

    def update(self, argv):
        self.prepare_upload()

        try:
            file_path = os.path.join(PROJECT_DIR,"_gae_module_name.py")
            hook_module = open(file_path, "w+")
            hook_module.write("PROJECT_DIR_NAME='%s'\n" % PROJECT_DIR_NAME)
            hook_module.close()

            try:
                get_callable(PRE_UPDATE_HOOK)()
            except (AttributeError, ImportError):
                pass

            appcfg.main(argv[1:] + [PROJECT_DIR])

            try:
                get_callable(POST_UPDATE_HOOK)()
            except (AttributeError, ImportError):
                pass

        finally:
            os.remove(file_path)
            self.clean_upload()

    def run_from_argv(self, argv):
        if len(argv) > 2 and argv[2] == 'update':
            self.update(argv)
        else:
            appcfg.main(argv[1:] + [PROJECT_DIR])

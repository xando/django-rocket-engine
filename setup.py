# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

description = 'Google AppEngine helper applcaiton'
long_description = open('README.rst').read() if os.path.exists('README.rst') else ""

version = open('VERSION').read() if os.path.exists('VERSION') else ""

setup(name='django_rocket',
      version='0.0.3',
      package_dir={'django_rocket': '.'},
      packages=['django_rocket'] + ['django_rocket.%s' % name for name in find_packages()],
      author='Sebastian Pawluś',
      author_email='sebastian.pawlus@gmail.com',
      url='http://readthedocs.org/docs/django_rocket/',
      description=description,
      long_description=long_description,
      include_package_data=True,
      platforms=['any'],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)

# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

short_description = 'Google AppEngine helper applcaiton'

long_description = open(
    os.path.join(os.path.dirname(__file__), 'README.rst')
).read()

version = open(
    os.path.join(os.path.dirname(__file__), 'VERSION')
).read()


setup(name='django-rocket-engine',
      version=version,
      packages=find_packages(),
      author='Sebastian Pawluś',
      author_email='sebastian.pawlus@gmail.com',
      url='http://readthedocs.org/projects/django-rocket-engine/',
      description=short_description,
      long_description=long_description,
      install_requires=[
          'virtualenv>=1.7.1.2',
      ],
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

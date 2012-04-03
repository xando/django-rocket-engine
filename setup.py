# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

readme = 'README.rst'

description = 'Google AppEngine helper applcaiton'
long_description = open(readme).read() if os.path.exists(readme) else ""


setup(name='django_rocket',
      version='0.0.2',
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
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Application Frameworks',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'License :: OSI Approved :: BSD License',
      ],
)

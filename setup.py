from setuptools import setup, find_packages

DESCRIPTION = 'Django backend for Google App Engine'
LONG_DESCRIPTION = None
try:
    LONG_DESCRIPTION = open('README.rst').read()
except:
    pass

setup(name='django_appengine',
      version='1.0',
      package_dir={'django_appengine': '.'},
      packages=['django_appengine'] + ['django_appengine.' + name for name in find_packages()],
      author='Sebastian Pawlus',
      author_email='sebastian.pawlus@gmail.com',
      url='',
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      platforms=['any'],
      classifiers=[
          'Development Status :: 3 - Alpha',
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

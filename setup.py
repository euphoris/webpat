"""
WebPattern
-------------

A Simple Web Framework
"""
try:
    from setuptools import setup, Command
except ImportError:
    from distutils.core import setup, Command


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys
        import subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


setup(
    name='WebPattern',
    version='0.0.3',
    url='http://github.com/euphoris/webpat',
    license='MIT license',
    author='Jae-Myoung Yu',
    author_email='euphoris@gmail.com',
    maintainer='Jae-Myoung Yu',
    maintainer_email='euphoris@gmail.com',
    description='A Simple Web Framework',
    long_description=__doc__,
    packages=['webpat'],
    platforms='any',
    install_requires=[
        'Flask',
        'SQLAlchemy',
        'Flask-Login'
    ],
    tests_require=[
        'pytest'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    cmdclass={'test': PyTest},
)

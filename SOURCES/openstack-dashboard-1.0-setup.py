import os
from setuptools import setup, find_packages, findall

setup(
    name = "dashboard",
    version = "1.0",
    url = 'https://launchpad.net/openstack-dashboard',
    license = 'Apache 2.0',
    description = "Django based reference implementation of a web based management interface for OpenStack.",
    packages = ['dashboard', 'media'],
    scripts = ['bin/dashboard'],
    package_data = {'dashboard':
                        [s[len('dashboard/'):] for s in
                        findall('dashboard/templates') + findall('dashboard/wsgi') + findall('dashboard/locale')],
                    'media': [s[len('media/'):] for s in findall('media')]
                    },
    data_files = [('/etc/dashboard/local', findall('local')), ('/var/lib/dashboard', set())],
    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)

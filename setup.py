import sys

from setuptools import setup, find_packages

try:
    version = __import__('importer').get_version()
except:
    version = None


setup(
    name='ajpes-trr-pos',
    version=version,
    url='https://github.com/brodul/ajpes-trr-pos',
    author='Andraz Brodnik brodul',
    author_email='brodul@brodul.org',
    description=('Uvoznik transakcijskih racunov poslovnih subjektov'
                 ' (prek poizvedbe na AJPES) v relacijske baze'
                 ),
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'sqlalchemy==0.9',
        'psycopg2==2.5.4',
        'blessings==1.6',
        'python-dateutil==2.2',
    ],
    scripts=['importer.py'],
    entry_points={'console_scripts': [
        'ajpes-importer = importer:execute_from_command_line',
    ]},
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)

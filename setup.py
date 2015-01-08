from setuptools import setup

setup(name='dashboard',
    description='dashboard for data from jenkins and other sources',
    url='https://github.com/bognix/dashboard',
    author='Bogna Knychala',
    license='MIT',
    packages=['dashboard'],
    install_requires=[
        'flask',
        'Flask-Cache',
        'jenkinsapi'
    ],
    zip_safe=False)

__author__ = 'bogna'

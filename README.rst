================
firestone-engine
================


The strategy calculate engine


Description
===========

Download the data from tushare and execute the submit strategy

Usage
=====

(1) init

pip install pipenv
pipenv sync

(2) install new dependency

pipenv install xxx

(3) run dev

pipenv run python setup.py develop (this create a special link to src, so when you edit the code can reflect immediately)
pipenv run firestone

(4) run test

pipenv run python setup.py test

(5) run install

pipenv run python setup.py install
pipenv run firestone

Note
====

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.

For install vs develop:
http://www.siafoo.net/article/77#install-vs-develop

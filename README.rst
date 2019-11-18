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
pipenv install xxx --dev

(3) run dev

pipenv run python setup.py develop (this create a special link to src, so when you edit the code can reflect immediately)
pipenv run firestone

(4) run test

pipenv run python setup.py test

(5) run install

pipenv run python setup.py install
pipenv run firestone

Run
====

(1) get data

pipenv run firestone 000793 600986

(2) execute trade

pipenv run firerock 5db4fa20ea3ae4a6ff26a3d1

pipenv run firerock 5db4fa20ea3ae4a6ff26a3d1 -m  (for mock)

Test
====

tests\runTest.bat

Publish
=======

pipenv install pyinstaller --dev
pipenv shell
pyinstaller -F src/firestone_engine/main.py   (first time)
pyinstaller -F --clean main.spec    (second time)
pyinstaller -F src/firestone_engine/calculate.py   (first time)
pyinstaller -F --clean calculate.spec    (second time)


for no module ptvsd error
    comment out the ptvsd in main and calculate

for no module distutils error(modify the hook in pyinstaller):
    https://github.com/pyinstaller/pyinstaller/issues/4064

    if distutils_dir.endswith('__init__.py'):
            distutils_dir = os.path.dirname(distutils_dir)

for dynamic load strategies, i.e. Base.py, Basic.py need to import into Real.py


Note
====

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.

For install vs develop:
http://www.siafoo.net/article/77#install-vs-develop

Edit trading.py and add the following
=====================================

def get_realtime_quotes(symbols=None, proxyManager=None):

if(proxyManager is not None):
        proxy = proxyManager.get_proxy()
        if(proxy is not None):
            request.set_proxy(proxy, 'http')

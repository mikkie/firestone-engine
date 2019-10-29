setx FR_DB firestone-test
mongo 127.0.0.1/firestone-test --eval "db.dropDatabase(); db.getSiblingDB('firestone-test');" "c:/aqua/firestone-engine/tests/init.js"
rem mongo 127.0.0.1/firestone-data "c:/aqua/firestone-engine/tests/initData.js"
pipenv run python -m unittest tests/TestMock.py
pipenv run python -m unittest tests/strategies/TestBasic.py
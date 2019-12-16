setx FR_DB firestone-test
mongo 127.0.0.1/firestone-test --eval "db.dropDatabase(); db.getSiblingDB('firestone-test');" "c:/aqua/firestone-engine/tests/init.js"
REM mongo 127.0.0.1/firestone-data "c:/aqua/firestone-engine/tests/initData.js"
REM mongo 127.0.0.1/firestone-data "c:/aqua/firestone-engine/tests/strategies/ydls.js"
pipenv run python -m unittest tests/strategies/TestBasic.py
pipenv run python -m unittest tests/strategies/TestYdls.py
pipenv run python -m unittest tests/TestMock.py
pipenv run python -m unittest tests/TestDataloader.py
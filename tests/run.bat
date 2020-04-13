setx FR_DB firestone-test
mongo 127.0.0.1/firestone-test --eval "db.dropDatabase(); db.getSiblingDB('firestone-test');" "c:/aqua/firestone-engine/tests/init.js"
mongoimport -d firestone-test -c codes "tests\concept\codes.json"
mongoimport -d firestone-test -c concepts "tests\concept\concepts.json"
mongoimport -d firestone-test -c hot_concept "tests\concept\hot_concept.json"
mongo 127.0.0.1/firestone-test "C:/aqua/firestone-engine/tests/concept/new_hot_concept.js"
REM mongo 127.0.0.1/firestone-data "c:/aqua/firestone-engine/tests/initData.js"
REM mongo 127.0.0.1/firestone-data "c:/aqua/firestone-engine/tests/strategies/ydls.js"
REM pipenv run python -m unittest tests/strategies/TestBasic.py
REM pipenv run python -m unittest tests/strategies/TestBasicSell.py
REM pipenv run python -m unittest tests/strategies/TestYdls.py
REM pipenv run python -m unittest tests/TestMock.py
REM pipenv run python -m unittest tests/TestDataloader.py
REM pipenv run python -m unittest tests/strategies/TestConceptPick.py
pipenv run python -m unittest tests/strategies/TestBatchYdls.py
setx FR_DB firestone-test
mongo 127.0.0.1/firestone-test --eval "db.dropDatabase(); db.getSiblingDB('firestone-test');" "c:/aqua/firestone-engine/tests/e2e/data/init.js"
mongo 127.0.0.1/firestone-data "c:/aqua/firestone-engine/tests/e2e/data/clear.js"
dist\main.exe 000000 -v --md -t --hours %time:~0,2% --minutes %time:~3,2%
pipenv run python -m unittest tests/e2e/data/CheckData.py
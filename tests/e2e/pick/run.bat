setx FR_DB firestone-test
mongo 127.0.0.1/firestone-test --eval "db.dropDatabase(); db.getSiblingDB('firestone-test');" "c:/aqua/firestone-engine/tests/e2e/pick/init.js"
mongoimport -d firestone-test -c codes "tests\concept\codes.json"
mongoimport -d firestone-test -c concepts "tests\concept\concepts.json"
mongoimport -d firestone-test -c hot_concept "tests\concept\hot_concept.json"
mongo 127.0.0.1/firestone-test "C:/aqua/firestone-engine/tests/concept/new_hot_concept.js"
start dist\calculate.exe 5db7e0a555609bb27252edb7 --hours %time:~0,2% --minutes * --seconds 3 -m -t -v -d
timeout /t 120 /nobreak > nul
pipenv run python -m unittest tests/e2e/pick/CheckPick.py
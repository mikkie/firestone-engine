setx FR_DB firestone-test
mongo 127.0.0.1/firestone-test --eval "db.dropDatabase(); db.getSiblingDB('firestone-test');" "c:/aqua/firestone-engine/tests/e2e/tradesell/init.js"
mongo 127.0.0.1/firestone-data --eval "db.getCollection('300448-2019-12-10').drop(); db.getCollection('cyb-2019-12-10').drop();" "c:/aqua/firestone-engine/tests/e2e/tradesell/data.js"
mongo 127.0.0.1/firestone-data --eval "db.getCollection('300448-2019-12-10-m').drop(); db.getCollection('cyb-2019-12-10-m').drop();"
start dist\main.exe 300448 cyb --date 2019-12-10 --hours %time:~0,2% --minutes * -m -v
start dist\calculate.exe 5db7e0a555609bb27252edb6 --date 2019-12-10-m --hours %time:~0,2% --minutes * --seconds */4 -m -t -v -i
timeout /t 180 /nobreak > nul
pipenv run python -m unittest tests/e2e/tradesell/CheckTradeSell.py
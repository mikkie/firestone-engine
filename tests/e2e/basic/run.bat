setx FR_DB firestone-test
mongo 127.0.0.1/firestone-test --eval "db.dropDatabase(); db.getSiblingDB('firestone-test');" "c:/aqua/firestone-engine/tests/e2e/basic/init.js"
mongo 127.0.0.1/firestone-data --eval "db.getCollection('000993-2019-10-30').drop(); db.getCollection('sh-2019-10-30').drop();" "c:/aqua/firestone-engine/tests/e2e/basic/data.js"
mongo 127.0.0.1/firestone-data --eval "db.getCollection('000993-2019-10-30-m').drop(); db.getCollection('sh-2019-10-30-m').drop();"
start pipenv run firerock 5da1800e87b64fb6f4c32503 --date 2019-10-30-m --hours %time:~0,2% --minutes *  -m -t -v -i
start pipenv run firestone 000993 sh --date 2019-10-30 --hours %time:~0,2% --minutes * -m -v
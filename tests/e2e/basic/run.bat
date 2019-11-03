setx FR_DB firestone-test
mongo 127.0.0.1/firestone-test --eval "db.dropDatabase(); db.getSiblingDB('firestone-test');" "c:/aqua/firestone-engine/tests/e2e/basic/init.js"
rem mongo 127.0.0.1/firestone-data "c:/aqua/firestone-engine/tests/data.js"
mongo 127.0.0.1/firestone-data --eval "db.getCollection('000993-2019-10-30-m').drop(); db.getCollection('000001-2019-10-30-m').drop();"
pipenv run firerock 5da1800e87b64fb6f4c32503 --date 2019-10-30-m --hours 9 10,13-14 11 --minutes 30-59 * 0-29 -m -d -t
pipenv run firestone 000993 000001 --date 2019-10-30 --hours 9 10,13-14 11 --minutes 30-59 * 0-29 -m -d -v
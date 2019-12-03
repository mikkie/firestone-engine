var now = new Date();
var todayStr = `${now.getFullYear()}-${('0' + (now.getMonth() + 1)).slice(-2)}-${('0' + now.getDate()).slice(-2)}`;
db.getCollection(`000993-${todayStr}`).drop();
db.getCollection(`300694-${todayStr}`).drop();
db.getCollection(`000793-${todayStr}`).drop();
db.getCollection(`sh-${todayStr}`).drop();
db.getCollection(`cyb-${todayStr}`).drop();
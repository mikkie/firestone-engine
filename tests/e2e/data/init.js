var now = new Date();
var todayStr = `${now.getFullYear()}-${('0' + (now.getMonth() + 1)).slice(-2)}-${('0' + now.getDate()).slice(-2)}`;
db.createCollection('users');
db.users.insert({
   username: "aqua",
   password: "e10adc3949ba59abbe56e057f20f883e",
   _id: ObjectId("5d905db9fc84d3224b0eb59c")
});
db.configmocks.insert({
    "_id" : ObjectId("5db796e4429e4baab72826a0"),
    "maxBuyNum" : 3,
    "curBuyNum" : 0,
    "ths_url" : "http://mncg.10jqka.com.cn/cgiwt/index/index",
    "cookie" : "__utma=156575163.353407385.1539410504.1561178627.1567430886.43;__utmz=156575163.1567430886.43.42.utmcsr=yamixed.com|utmcn=(referral)|utmcmd=referral|utmcct=/fav/article/2/157; isSaveAccount=0; PHPSESSID=9d32d89fb9a374a510ab7a922d8cf57e; user=MxDphcXVhSVFjOjpOb25lOjUwMDo0MjUzOTk0Njc6NywxMTExMTExMTExMSw0MDs0NCwxMSw0MDs2LDEsNDA7NSwxLDQwOzEsMSw0MDsyLDEsNDA7MywxLDQwOzUsMSw0MDs4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxLDQwOjI0Ojo6NDE1Mzk5NDY3OjE1NzQyMDY4NjU6OjoxNTA2MDQ4OTYwOjg2NDAwOjA6MTdlN2IzMTE0YjE1NWVlZTQ5MGExYzQ1MzhjZjA0OTI1OmRlZmF1bHRfMzox; userid=415399467; u_name=aquaIQc; escapename=aquaIQc; ticket=a19a954f1cac89d7becaa51dde998156; log=;Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1573951971,1574034719,1574120605,1574206868;v=Ak5MMMNJn20sSStJ1ZRlNZU9ny8TzxLJJJPGrXiXutEM2-SZ4F9i2fQjFrJL; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1574206900",
    "username" : "48039195",
    "gdzh" : "0098894246",
    "sh_gdzh" : "A474614369",
    "userId" : ObjectId("5d905db9fc84d3224b0eb59c")
});
db.strategies.insertMany([{
    "_id" : ObjectId("5da19b7d181fc3600c5544c2"),
    "name" : "基础策略",
    "description" : "在<i>监控时间</i>范围内,当<i>大盘涨幅</i>处于指定范围，并且当前<i>个股涨幅</i>处于指定范围，则买入股票",
    "op" : "buy",
    "url" : "Basic",
    "parameters" : {
        "code" : "",
        "executeDate" : "",
        "monitorTime" : {
            "start" : "09:30",
            "end" : "15:00"
        },
        "index_percent" : {
            "low" : "-1.0",
            "high" : "3.0"
        },
        "percent" : {
            "low" : "-0.5",
            "high" : "2.5"
        },
        "volume" : 1000
    }
},{
    "_id" : ObjectId("5da19b7d181fc3600c5544c3"),
    "name" : "异动拉升",
    "description" : "在<i>监控时间</i>范围内,当<i>大盘涨幅</i>处于指定范围，并且当前<i>个股涨幅</i>处于指定范围，在<i>涨速时间</i>内，<i>涨幅拉升达</i>到预期值则买入股票",
    "op" : "buy",
    "url" : "Ydls",
    "parameters" : {
        "code" : "",
        "executeDate" : "",
        "monitorTime" : {
            "start" : "09:30",
            "end" : "15:00"
        },
        "index_percent" : {
            "low" : "-10.0",
            "high" : "10.0"
        },
        "percent" : {
            "low" : "-4.0",
            "high" : "1.0"
        },
        "speed" : {
            "upper_shadow" : "0.2",
            "ratio_l" : "2",
            "ratio_r" : "3",
            "time" : "3.1",
            "amount" : "50"
        },
        "volume" : 1000
    }
}]);
db.mocktrades.insertMany([{
    _id: ObjectId("5da1800e87b64fb6f4c32503"),
    "code" : "000993",
    "state" : "未开始",
    "result" : "无",
    "userId" : ObjectId("5d905db9fc84d3224b0eb59c"),
    "strategyId" : ObjectId("5da19b7d181fc3600c5544c2"),
    "createDate" : new Date(),
    "deleted" : false,
    "params" : {
        "code" : "000993",
        "executeDate" : todayStr,
        "monitorTime" : {
            "start" : "09:30",
            "end" : "15:00"
        },
        "index_percent" : {
            "low" : "-0.18",
            "high" : "-0.18"
        },
        "percent" : {
            "low" : "0.0",
            "high" : "0.0"
        }
    }
},{
    "code" : "300694",
    "state" : "未开始",
    "result" : "无",
    "userId" : ObjectId("5d905db9fc84d3224b0eb59c"),
    "strategyId" : ObjectId("5da19b7d181fc3600c5544c2"),
    "createDate" : new Date('2019-09-15'),
    "deleted" : false,
    "params" : {
        "code" : "300694",
        "executeDate" : todayStr,
        "monitorTime" : {
            "start" : "09:30",
            "end" : "15:00"
        },
        "index_percent" : {
            "low" : "-1.0",
            "high" : "3.0"
        },
        "percent" : {
            "low" : "-0.5",
            "high" : "2.5"
        }
    }
},{
    "_id" : ObjectId("5db7e0a555609bb27252edb4"),
    "code" : "000793",
    "state" : "运行中",
    "result" : "无",
    "userId" : ObjectId("5d905db9fc84d3224b0eb59c"),
    "strategyId" : ObjectId("5da19b7d181fc3600c5544c2"),
    "createDate" : ISODate("2019-09-15T00:00:00.000Z"),
    "deleted" : false,
    "params" : {
        "code" : "000793",
        "executeDate" : todayStr,
        "monitorTime" : {
            "start" : "09:31",
            "end" : "09:32"
        },
        "index_percent" : {
            "low" : "10.0",
            "high" : "10.0"
        },
        "percent" : {
            "low" : "9.22",
            "high" : "9.24"
        }
    }
}]);
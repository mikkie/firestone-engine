db.createCollection('users');
db.users.insert({
   username: "aqua",
   password: "e10adc3949ba59abbe56e057f20f883e",
   _id: ObjectId("5d905db9fc84d3224b0eb59c")
});
db.configmocks.insert({
    "maxBuyNum" : 3,
    "ths_url" : "http://mncg.10jqka.com.cn/cgiwt/index/index",
    "cookie" : "__utma=156575163.1101180334.1557107567.1557375466.1557738304.3; __utmz=156575163.1557738304.3.3.utmcsr=yamixed.com|utmccn=(referral)|utmcmd=referral|utmcct=/fav/article/2/157; isSaveAccount=0; PHPSESSID=0ee41a659eca05d9c02da980b42b337b; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1570773015,1570773052,1572246079; user=MDphcXVhSVFjOjpOb25lOjUwMDo0MjUzOTk0Njc6NywxMTExMTExMTExMSw0MDs0NCwxMSw0MDs2LDEsNDA7NSwxLDQwOzEsMSw0MDsyLDEsNDA7MywxLDQwOzUsMSw0MDs4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxLDQwOjI0Ojo6NDE1Mzk5NDY3OjE1NzIyNDYwOTc6OjoxNTA2MDQ4OTYwOjg2NDAwOjA6MThkZjg4MDU4NWQ1MjAxNWI4YjczMmQ1YjVjY2Q4MjdiOmRlZmF1bHRfMjox; userid=415399467; u_name=aquaIQc; escapename=aquaIQc; ticket=4946f5e543fb81ad0500537a32fbb290; log=; v=ApOFSy-Cygxe94ZYp7X7ueKFIhy-SCcK4dxrPkWw77LpxL1KzRi3WvGs-4FW; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1572246108",
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
    "name" : "打板策略",
    "description" : "",
    "op" : "sell",
    "url" : "",
    "parameters" : {}
}]);
db.mocktrades.insertMany([{
    "code" : "300691",
    "state" : "停止",
    "result" : "无",
    "userId" : ObjectId("5d905db9fc84d3224b0eb59c"),
    "strategyId" : ObjectId("5da19b7d181fc3600c5544c2"),
    "createDate" : new Date(),
    "deleted" : false,
    "params" : {
        "code" : "300691",
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
    _id: ObjectId("5da1800e87b64fb6f4c32503"),
    "code" : "300692",
    "state" : "停止",
    "result" : "无",
    "userId" : ObjectId("5d905db9fc84d3224b0eb59c"),
    "strategyId" : ObjectId("5da19b7d181fc3600c5544c2"),
    "createDate" : new Date(),
    "deleted" : false,
    "params" : {
        "code" : "300692",
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
    "code" : "300693",
    "state" : "停止",
    "result" : "无",
    "userId" : ObjectId("5d905db9fc84d3224b0eb59c"),
    "strategyId" : ObjectId("5da19b7d181fc3600c5544c2"),
    "createDate" : new Date(),
    "deleted" : false,
    "params" : {
        "code" : "300693",
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
    "code" : "300694",
    "state" : "停止",
    "result" : "无",
    "userId" : ObjectId("5d905db9fc84d3224b0eb59c"),
    "strategyId" : ObjectId("5da19b7d181fc3600c5544c2"),
    "createDate" : new Date('2019-09-15'),
    "deleted" : false,
    "params" : {
        "code" : "300694",
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
}]);
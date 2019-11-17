db.createCollection('users');
db.users.insert({
   username: "aqua",
   password: "e10adc3949ba59abbe56e057f20f883e",
   _id: ObjectId("5d905db9fc84d3224b0eb59c")
});
db.configmocks.insert({
    "_id" : ObjectId("5db796e4429e4baab72826a0"),
    "maxBuyNum" : 3,
    "ths_url" : "http://mncg.10jqka.com.cn/cgiwt/index/index",
    "cookie" : "__utma=156575163.1101180334.1557107567.1557375466.1557738304.3; isSaveAccount=0; Hm_lvt_416c770ac83a9d996d7b3793f8c4994d=1572344617; user=MDphcXVhSVFjOjpOb25lOjUwMDo0MjUzOTk0Njc6NywxMTExMTExMTExMSw0MDs0NCwxMSw0MDs2LDEsNDA7NSwxLDQwOzEsMSw0MDsyLDEsNDA7MywxLDQwOzUsMSw0MDs4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxLDQwOjI0Ojo6NDE1Mzk5NDY3OjE1NzM3NzQ0NzQ6OjoxNTA2MDQ4OTYwOjg2NDAwOjA6MTdmZmY1MDYwMGZlOWU3OWI2YzRkZjViN2E1NzgwZmQ2OmRlZmF1bHRfMzox; userid=415399467; u_name=aquaIQc; escapename=aquaIQc; ticket=b7d5646fb037d199db854cb3a876b2ed; log=; v=AiUznU3olOlyE_C1cypvCJrZNOpcYtn0Ixa9SCcK4dxrPkuc77LpxLNmzRe0; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1572747168,1573774446,1573774508,1573774527; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1573774527; PHPSESSID=ad791a8735d7989ce15b86cda689cd12",
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
        "volume" : 100
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
    "state" : "未开始",
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
    "code" : "000993",
    "state" : "未开始",
    "result" : "无",
    "userId" : ObjectId("5d905db9fc84d3224b0eb59c"),
    "strategyId" : ObjectId("5da19b7d181fc3600c5544c2"),
    "createDate" : new Date(),
    "deleted" : false,
    "params" : {
        "code" : "000993",
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
    "code" : "300693",
    "state" : "未开始",
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
    "state" : "未开始",
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
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
    "cookie" : "__utma=156575163.1101180334.1557107567.1557375466.1557738304.3; __utmz=156575163.1557738304.3.3.utmcsr=yamixed.com|utmccn=(referral)|utmcmd=referral|utmcct=/fav/article/2/157; isSaveAccount=0; Hm_lvt_416c770ac83a9d996d7b3793f8c4994d=1572344617; user=MDphcXVhSVFjOjpOb25lOjUwMDo0MjUzOTk0Njc6NywxMTExMTExMTExMSw0MDs0NCwxMSw0MDs2LDEsNDA7NSwxLDQwOzEsMSw0MDsyLDEsNDA7MywxLDQwOzUsMSw0MDs4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxLDQwOjI0Ojo6NDE1Mzk5NDY3OjE1NzI3NDcxNTc6OjoxNTA2MDQ4OTYwOjg2NDAwOjA6MWRmMGQzMDMyYzlhYzMyNTNmMjNjYjhmNDJmY2I4MGQ1OmRlZmF1bHRfMjox; userid=415399467; u_name=aquaIQc; escapename=aquaIQc; ticket=b39e2ff038a237a40bf6a2f9d37ec360; v=AtzK5ry_7VGH4pkNUVG8bGGArfGNVYBlAvmUQ7bd6EeqAXKn3mVQD1IJZMMF; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1572521197,1572588730,1572747084,1572747168; PHPSESSID=83db9bc22b6ac54cb7ccc89ca1c7f9aa; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1572756819",
    "username" : "48039195",
    "gdzh" : "0098894246",
    "sh_gdzh" : "A474614369",
    "monitor_concept" : [],
    "userId" : ObjectId("5d905db9fc84d3224b0eb59c")
});
db.strategies.insertMany([{
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
},{
    "_id" : ObjectId("5da19b7d181fc3600c5544c5"),
    "name" : "题材选股",
    "description" : "根据实时热门概念排行选出股票进行监控",
    "op" : "select",
    "url" : "ConceptPick",
    "parameters" : {
        "code" : "",
        "executeDate" : "",
        "monitorTime" : {
            "start" : "00:00",
            "end" : "23:59"
        },
        "index_percent" : "1.00",
        "concepts" : "",
        "net_buy" : "-3",
        "company_count" : "500",
        "stock_percent" : "9.90",
        "max_concept" : "6",
        "top_concept" : "3",
        "monitor_count" : "5",
        "max_percent" : "5.00",
        "volume" : "1000",
        "strategyId" : "5da19b7d181fc3600c5544c3"
    }
}]);
db.mocktrades.insertMany([{
    "_id" : ObjectId("5db7e0a555609bb27252edb7"),
    "code" : "",
    "state" : "运行中",
    "result" : "无",
    "userId" : ObjectId("5d905db9fc84d3224b0eb59c"),
    "strategyId" : ObjectId("5da19b7d181fc3600c5544c5"),
    "createDate" : ISODate("2019-12-29T00:00:00.000Z"),
    "deleted" : false,
    "params" : {
        "code" : "",
        "executeDate" : "",
        "monitorTime" : {
            "start" : "00:00",
            "end" : "23:59"
        },
        "index_percent" : "1.00",
        "concepts" : "",
        "net_buy" : "-3",
        "company_count" : "500",
        "stock_percent" : "9.90",
        "top_concept" : "3",
        "max_concept" : "6",
        "monitor_count" : "5",
        "open_min_percent" : "-2.00",
        "open_max_percent" : "3.00",
        "min_percent" : "1.00",
        "max_percent" : "5.00",
        "volume" : "1000",
        "strategyId" : "5da19b7d181fc3600c5544c3"
    }
}]);
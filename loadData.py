import pymysql
import json
con3 = pymysql.connect("localhost", "test", "", "wenben_book", 8889)
sql="select * from movie"
cur=con3.cursor()
cur.execute(sql)
data=cur.fetchall()
jsdata=json.loads(data[0][1])
print(jsdata)
name=jsdata["name"]#str
url=data[0][0]#str
image=jsdata["image"]#str
director=jsdata["director"]
#list[dict[type,url,name]]
actor=jsdata["actor"]
#list[dict[type,url,name]]
author=jsdata["author"]
#list[dict[type,url,name]]
datePublished=jsdata["datePublished"]
#time
duration=jsdata["duration"]
#list
description=jsdata["description"]
#str
aggregateRating=jsdata["aggregateRating"]
#dict[@type,ratingCount,bestRationg,worseRatingratingValue]
for i in jsdata:
    print(i)
    print(jsdata[i])
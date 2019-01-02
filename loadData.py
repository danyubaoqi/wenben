import time

import pymysql
import json
from tomorrow3 import threads
from DBUtils.PooledDB import PooledDB
print("开始创建连接")
pool = PooledDB(pymysql, 15, host="localhost", user="root", passwd="168168", db="movie", port=3306)


@threads(15)
def dosql(sql: str):
    try:

        con = pool.connection()
        cur = con.cursor()

        cur.execute(sql)
        cur.close()
        con.commit()
        con.close()

    except Exception as e:
        print(e)


if __name__ == '__main__':
    print("开始")
    time.sleep(3)
    con = pool.connection()
    cur = con.cursor()
    cur.execute("select * from tmdb_5000_credits")
    datas = cur.fetchall()
    con.close()

    movieid = [x[0] for x in datas]
    datas = [x[2] for x in datas]
    k = -1
    for i in range(100):
        try:
            k+=1
            data = json.loads(datas[i])
            for j in data:

                # sql=f'insert into companies values ({j["id"]},"{j["name"]}")'
                # dosql(sql)
                sql=f'insert into actor values ({j["id"]},"{j["name"]}",{j["gender"]})'
                dosql(sql)
            print(i)
        except Exception as e:
            print(e)
            continue

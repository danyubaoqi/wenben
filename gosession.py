import pymysql
from tomorrow3 import threads

con = pymysql.connect(host="localhost", user="root", passwd="168168", db="movie", port=3306)


def dosql(sql: str):
    try:
        con.ping(reconnect=True)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        cur.close()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    cur=con.cursor()

    s="actor_role"
    a=open(f"{s}.txt","w",encoding="utf-8")
    ss="rolename"
    sql="select rolename from actor_role where `order`"
    cur.execute(f"select  {ss} from {s} where `order`<15")
    data=list(set([x[0] for x in cur.fetchall()]))
    for i in data:
        a.write(i+"\n")
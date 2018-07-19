# _*_ coding: utf-8 _*_
import web
import web.db
import sae.const
import MySQLdb
import logging
from sae.const import (MYSQL_HOST, MYSQL_HOST_S, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB)

db2=web.database(
    dbn='mysql',
    host=sae.const.MYSQL_HOST,
    port=int(sae.const.MYSQL_PORT),
    user=sae.const.MYSQL_USER,
    passwd=sae.const.MYSQL_PASS,
    db=sae.const.MYSQL_DB,
)
                 

def add_new(username,phone,count):
    #cur=db.cursor()
    #values=[username,phone,count]
    #cur.execute('insert into enroll values(%s,%s,%s)',values)
    #db.commit()
    #cur.close()
    #db.close()
    return db2.insert("enroll",name=username,phone=phone,count=count)

def get_count(name):
    print("hello world")
    sql = "select count from enroll where name=" + name
    print(sql)
    return db2.query(sql)

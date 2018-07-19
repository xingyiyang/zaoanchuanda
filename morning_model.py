# _*_ coding:utf-8 _*_
import web
import web.db
import sae.const
 
 
db = web.database(
    dbn='mysql',
    host=sae.const.MYSQL_HOST,
    port=int(sae.const.MYSQL_PORT),
    user=sae.const.MYSQL_USER,
    passwd=sae.const.MYSQL_PASS,
    db=sae.const.MYSQL_DB
)
  
def add_new(user, username,phone,num,time):
    return db.insert('morning_enroll', user=user, username=username,phone=phone,num=num,time=time)
  
def get_content():
    return db.select('morning_enroll', order='id')

def get_user():
    return db.query("SELECT user FROM morning_enroll")

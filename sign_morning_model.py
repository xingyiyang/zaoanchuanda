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
  
def add_new(user,username,stuid,total,istoday,timetoday,all_record,phone):
    return db.insert('morning_sign', user=user, username=username,stuid=stuid,total=total,istoday=istoday,timetoday=timetoday,all_record=all_record,phone=phone)
  
def get_content():
    return db.select('morning_sign', order='timetoday DESC')

def get_id():
    return db.query("SELECT id FROM morning_sign")

def find_user(user):
    return db.query("SELECT * FROM morning_sign WHERE user=%r" % (user))

def update(user,total,last_record,all_record,timetoday):
    total+=1
        
    db.update('morning_sign',where='user=$user',vars={'user':user},istoday=1,timetoday=timetoday,total=total,last_record=last_record,all_record=all_record)

def reset():
    db.query("UPDATE morning_sign SET istoday=0,timetoday=NULL,record = record*2  WHERE id >0")
    
def clearall():
    db.query("UPDATE morning_sign SET total=0,istoday=0,timetoday=NULL,record = 0  WHERE id >0")

def clearIstoday():
    db.query("UPDATE morning_sign SET istoday=0")
           
def gettime(date):
    #得到时间
    temptime=list(date)
    temptime=temptime[10:]
    strtime="".join(temptime)
    return strtime

def get_mon_day(date):
    #得到输入的月和日
    month=date[6:7]
    day=date[8:10]
    
    month=int(month)
    day=int(day)
     
    return month,day

#获得总积分排名的方法
def get_record_rank(user):
    result=db.query("select count(*) as order_id from morning_sign where all_record >(select all_record  from morning_sign where user='%s')"%user)
    item=result[0]
    
    return item.order_id+1
    
def get_hour_min(date):#得到小时分钟
    hour=date[11:13]
    minute=date[14:16]
    
    
    print("hour:%s,minute:%s"%(hour,minute))
        
def get_sign_count(user):
    
    rank=db.query("SELECT count(*) as sign_id FROM `morning_sign`as m WHERE m.istoday=1")  
    result=rank[0]
    return result.sign_id+1
    
def get_sign_name_time():
    result=db.query("SELECT username,timetoday  FROM `morning_sign`as m where m.istoday=1 order by timetoday limit 10")
    
    return result
    
def get_rank():
    result=db.query("SELECT  username,all_record  FROM `morning_sign` order by all_record desc limit 30")     
    return result
    
def get_all_count():
    result=db.query("select count(*) as sign_count from morning_sign")     
    count=result[0]
    return count.sign_count

    
    
    
    
    
    
    
    
    
    
    




    
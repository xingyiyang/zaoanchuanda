def image_task():
     #得到今天的时间
     todaytime=sign_morning_model.gettime(str(int(time.time()))+fktime)
                     
     t_month,t_day=sign_morning_model.get_mon_day(todaytime)
                    
                     
                     #得到上次签到的时间
     lasttime=item.timetoday
     last_month,last_day=sign_morning_model.get_mon_day(lasttime)   
                    
     last_record=100
                        
                    
                     if t_month==last_month:#月份相同相差一天
                          if t_day-last_day==1:
                              if item.last_record!=7:
                                  last_record=item.last_record+1
                              else:
                                   last_record=7
                          else:
                              last_record=item.last_record
                     elif t_month==5 and last_month==4:#换月的时候 5,4月份交替
                          t_day+=30
                          if t_day-last_day==1:
                             if item.last_record!=7:
                                  last_record=item.last_record+1
                             else:
                                   last_record=7
                          else:
                             last_record=item.last_record
                      
                     all_record=item.all_record+last_record
                     
                     #得到签到排名
                     sign_rank=sign_morning_model.get_sign_count(item.user)
                     
                     result=sign_morning_model.get_sign_name_time()
                     tempstr=""
                   
                     for i in result:
                          temp="  "
                          if len(i["username"])==2:
                               temp="       "
                          if len(i["username"])==1:
                               temp="          "
                          tempstr+=i["username"]+temp+i["timetoday"]+"\n"
                           
                     sign_morning_model.update(item.user, item.total,last_record,all_record,todaytime)
                     morning_time_model.add_new(item.username,todaytime)
                     
                     str1=u"查看自己的积分请回复“签到积分”"
                     str2=u"查看自己的排名请回复“签到排名”"      
                     str3=u"查看排行榜请回复“排行榜”"
                     str4=u"查看积分规则请回复'积分规则'"
                                                                            
                     return self.render.reply_text(fromUser,toUser,int(time.time()),u"恭喜小主今日完成签到任务[鼓掌]\n 你是今天第%s个签到的人,请再接再厉!\
                                                  \n%s\n%s\n%s \n%s\n\n姓名      签到时间  \n%s \n明天请继续输入'早起测试'开始新一天的挑战"%(sign_rank,str1,str2,str3,str4,tempstr))
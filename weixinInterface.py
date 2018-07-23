# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib2, json
from lxml import etree
import pylibmc
import random
import sign_morning_model
# import test_model
import morning_model
import morning_time_model

sign_task = [
    u"星期天任务，文字型",  # 星期天的任务,必须是文字型任务
    u"星期一任务，图片型",  # 星期1的任务
    u"星期二任务，图片型",  # 星期2的任务
    u"星期三任务，文字型",  # 星期3的任务, 必须是文字型任务
    u"星期四任务，图片型",  # 星期4的任务
    u"星期五任务，图片型",  # 星期5的任务
    u"星期六任务，图片型",  # 星期6的任务
]

SIGN_START = 10
SIGN_END = 23


class WeixinInterface:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        # 获取输入参数
        data = web.input()
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr
        # 自己的token
        token = "yangfan"  # 这里改写你在微信公众平台里输入的token
        # 字典序排序
        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, list)
        hashcode = sha1.hexdigest()
        # sha1加密算法

        # 如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr

    def POST(self):

        str_xml = web.data()  # 获得post来的数据
        xml = etree.fromstring(str_xml)  # 进行XML解析
        msgType = xml.find("MsgType").text
        fromUser = xml.find("FromUserName").text
        toUser = xml.find("ToUserName").text
        mc = pylibmc.Client()
        if msgType == 'event':
            mscontent = xml.find('Event').text
            if mscontent == 'subscribe':
                s = u"欢迎关注“早安川大”的活动，希望这个活动能帮你养成早起的好习惯！\n正式活动将在5月7号(周一)正式开始，请耐心等待！\n每天回复'早安’即可参加每天的早起任务！\n查看积分规则请输入'积分规则'"
                return self.render.reply_text(fromUser, toUser, int(time.time()), s)
            '''if mscontent == "unsubscribe":
                s = u"你忍心离开我们吗？我们会一直努力，越来越好的。5555"
                return self.render.reply_text(fromUser,toUser,int(time.time()),s)
               
                return replyxml'''

            # if msgType == "voice":

            # n = len(voice_id)-1
            # i = random.randint(0,n)
            # media_id = voice_id[i]
            # return self.render.reply_voice(fromUser,toUser,media_id)

            # media_id = xml.find("MediaId").text

            # return self.render.reply_text(fromUser,toUser,int(time.time()),u"你的MediaId为：\n"+media_id+u"\n可以重复发送哦，我们会选择你最后一次发送的语音参选的[微笑]")



            # if msgType =="image":

            #  return self.render.reply_text(fromUser,toUser,int(time.time()),u'收到')

        if msgType == "text":
            content = xml.find("Content").text  # 获得用户所输入的内容

            '''早安'''
            english_content = ""
            try:
                english_content = content.lower()
            except:
                pass
                # if content.startswith(u'早安') or english_content.startswith('morning') or english_content.startswith('good morning'):
                # return self.render.reply_text(fromUser,toUser,int(time.time()),u'“早起活动”已结束。')

                # 任务序号
            day = int(time.strftime('%d', time.localtime()))
            i = (day) % 5
            # 当前用户数据
            week = time.strftime('%w', time.localtime())
            week = int(week)

            # if week!=0 and week!=6:
            i = week
            print("i=%d" % (i))
            print(sign_task[i])

            me = sign_morning_model.find_user(fromUser)

            fktime = time.strftime('%Y-%m-%d %H:%M', time.localtime())

            item = ""

            if content.find("+"):
                tempstr = content.split("+")
                temp2 = tempstr[0].strip()
                if temp2 == u"早起活动" and len(tempstr) == 4:
                    try:
                        item = me[0]
                    except:
                        pass
                    if len(item) == 0:
                        temptime = list(str(int(time.time())) + fktime)
                        temptime = temptime[10:]
                        strtime = "".join(temptime)

                        sign_morning_model.add_new(fromUser, tempstr[1], tempstr[2], 0, 0, strtime, 0, tempstr[3])
                        return self.render.reply_text(fromUser, toUser, int(time.time()),
                                                      u"你好！你已报名成功,请发送'早安'来进行进行今天的签到")
                    else:
                        return self.render.reply_text(fromUser, toUser, int(time.time()), u'你已经报过名了，请不要重复报名。')

                elif len(tempstr) >= 2:
                    return self.render.reply_text(fromUser, toUser, int(time.time()),
                                                  u"你发送的格式不对,请重新按照格式[早起活动+姓名+学号+电话]发送内容 如早起活动+小明+123+456")

            try:
                item = me[0]
            except:
                pass
            if len(item) == 0:
                return self.render.reply_text(fromUser, toUser, int(time.time()),
                                              u'你好！您目前还没有报名“早起活动”哦~可以发送[早起活动+姓名+学号+电话]报名参与。')

            week = time.strftime('%w', time.localtime())
            week = int(week)

            todaytime = sign_morning_model.gettime(str(int(time.time())) + fktime)
            t_month, t_day = sign_morning_model.get_mon_day(todaytime)

            # if hour<6 or hour>=21:
            # return self.render.reply_text(fromUser,toUser,int(time.time()),u'不在签到时段，请在每天早上6:00~8:00签到哦，现在服务器时间%s'%fktime)

            fktime = time.strftime('%Y-%m-%d %H:%M', time.localtime())
            hour = time.strftime('%H', time.localtime())
            hour = int(hour)
            if content == u'早安':
                if (hour < SIGN_START):
                    return self.render.reply_text(fromUser, toUser, int(time.time()), u'太早了')
                else:
                    if item.istoday == 0:
                        return self.render.reply_text(fromUser, toUser, int(time.time()),
                                                      u'[玫瑰]' + item.username + u'小主金安[玫瑰]\n小主今日签到成功[鼓掌]\n顺便完成个早安任务也是极好的：\n' +
                                                      sign_task[i] + u"\n不完成任务可是不算的哦[坏笑]")
                        # elif week==0 or week==6 or (t_month==5 and t_day==2):
                        #   return self.render.reply_text(fromUser,toUser,int(time.time()),u'安！假期与周末都不用签到哦，可以好好休息[愉快]')
                    else:
                        return self.render.reply_text(fromUser, toUser, int(time.time()), u'你已签到成功，请不要再重复签到！[愉快]')

            if content.startswith(u'签到次数'):
                if item.istoday:
                    return self.render.reply_text(fromUser, toUser, int(time.time()),
                                                  u'你本月签到次数为:%d，今日已签到。' % (item.total))
                else:
                    return self.render.reply_text(fromUser, toUser, int(time.time()),
                                                  u'你本月签到次数为:%d，今天还没有签到哦！' % (item.total))

            if content == u'签到积分':
                return self.render.reply_text(fromUser, toUser, int(time.time()),
                                              u'你好，你本月的早起积分为:%d，请继续努力！' % (item.all_record))

            if content.startswith(u'签到排名'):
                rank = sign_morning_model.get_record_rank(item.user)
                return self.render.reply_text(fromUser, toUser, int(time.time()), u'你好，你本月的排名为:%s，请继续努力！' % (rank))

            if content.startswith(u'排名榜') or content.startswith(u'排行榜'):
                result = sign_morning_model.get_rank()

                tempstr = ""

                for i in result:
                    temp = "   "
                    if len(i["username"]) == 2:
                        temp = "        "
                    if len(i["username"]) == 1:
                        temp = "          "
                    tempstr += i["username"] + temp + str(i["all_record"]) + "\n"

                return self.render.reply_text(fromUser, toUser, int(time.time()), u'姓名     积分\n' + tempstr)

            if content.startswith(u'积分规则'):
                tempstr2 = "积分从1分开始，连续签到每天加1分，直到7分封顶，中间有一天未签到，积分从前一天开始从新计算!"
                return self.render.reply_text(fromUser, toUser, int(time.time()), tempstr2)
                # 五一放假不用签到
                # if(t_month==5 and t_day==2):
            #   return self.render.reply_text(fromUser,toUser,int(time.time()),u'五一快乐！假期与周末都不用签到哦，可以好好休息[愉快]')

            if content == u"重置签到":
                sign_morning_model.clearIstoday()
                return self.render.reply_text(fromUser, toUser, int(time.time()), u"重置istoday为0成功")

            fktime = time.strftime('%Y-%m-%d %H:%M', time.localtime())
            hour = time.strftime('%H', time.localtime())
            hour = int(hour)
            week = time.strftime('%w', time.localtime())
            week = int(week)
            #   if week == 6 or week == 0:
            #        return self.render.reply_text(fromUser,toUser,int(time.time()),u'安！假期与周末都不用签到哦，可以好好休息[愉快]')
            if hour < SIGN_START or hour >= SIGN_END:
                return self.render.reply_text(fromUser, toUser, int(time.time()),
                                              u'不在签到时段，请在每天早上12:00~24:00签到哦，现在服务器时间%s' % fktime)
            if item.istoday == True:
                return self.render.reply_text(fromUser, toUser, int(time.time()), u'你今日已签到，请勿重复签到。')

            if week == 0 and len(content) >= 10:
                # 得到今天的时间
                todaytime = sign_morning_model.gettime(str(int(time.time())) + fktime)

                t_month, t_day = sign_morning_model.get_mon_day(todaytime)

                # 得到上次签到的时间
                lasttime = item.timetoday
                last_month, last_day = sign_morning_model.get_mon_day(lasttime)

                last_record = 100

                if t_month == last_month:  # 月份相同相差3天
                    if t_day - last_day == 1:
                        if item.last_record != 7:
                            last_record = item.last_record + 1
                        else:
                            last_record = 7
                    else:
                        last_record = item.last_record
                elif t_month == 5 and last_month == 4:  # 换月的时候 5,4月份交替
                    t_day += 30
                    if t_day - last_day == 1:
                        if item.last_record != 7:
                            last_record = item.last_record + 1
                        else:
                            last_record = 7
                    else:
                        last_record = item.last_record
                if item.last_record == 0:
                    last_record = 1

                all_record = item.all_record + last_record

                # 得到签到排名
                sign_rank = sign_morning_model.get_sign_count(item.user)
                result = sign_morning_model.get_sign_name_time()

                tempstr = ""

                for i in result:
                    temp = "  "
                    if len(i["username"]) == 2:
                        temp = "       "
                    if len(i["username"]) == 1:
                        temp = "          "
                    tempstr += i["username"] + temp + i["timetoday"] + "\n"

                sign_morning_model.update(item.user, item.total, last_record, all_record, todaytime)

                morning_time_model.add_new(item.username, todaytime)

                str1 = u"查看自己的积分请回复“签到积分”"
                str2 = u"查看自己的排名请回复“签到排名”"
                str3 = u"查看排行榜请回复“排行榜”"
                str4 = u"查看积分规则请回复'积分规则'"

                return self.render.reply_text(fromUser, toUser, int(time.time()), u"恭喜小主今日完成签到任务[鼓掌]\n你是今天第%s个签到的人,请牢记你今日的内容!\
                                               \n%s\n%s\n%s\n%s\n\n姓名      签到时间  \n%s\n明天请继续输入'早安'开始新一天的挑战" % (
                sign_rank, str1, str2, str3, str4, tempstr))

            if week == 3:
                # 得到今天的时间
                todaytime = sign_morning_model.gettime(str(int(time.time())) + fktime)

                t_month, t_day = sign_morning_model.get_mon_day(todaytime)

                # 得到上次签到的时间
                lasttime = item.timetoday
                last_month, last_day = sign_morning_model.get_mon_day(lasttime)

                last_record = 100

                if t_month == last_month:  # 月份相同相差一天
                    if t_day - last_day == 1:
                        if item.last_record != 7:
                            last_record = item.last_record + 1
                        else:
                            last_record = 7
                    else:
                        last_record = item.last_record
                elif t_month == 5 and last_month == 4:  # 换月的时候 5,4月份交替
                    t_day += 30
                    if t_day - last_day == 1:
                        if item.last_record != 7:
                            last_record = item.last_record + 1
                        else:
                            last_record = 7
                    else:
                        last_record = item.last_record
                if item.last_record == 0:
                    last_record = 1

                all_record = item.all_record + last_record

                # 得到签到排名
                sign_rank = sign_morning_model.get_sign_count(item.user)

                result = sign_morning_model.get_sign_name_time()

                tempstr = ""

                for i in result:
                    temp = "  "
                    if len(i["username"]) == 2:
                        temp = "       "
                    if len(i["username"]) == 1:
                        temp = "          "
                    tempstr += i["username"] + temp + i["timetoday"] + "\n"

                sign_morning_model.update(item.user, item.total, last_record, all_record, todaytime)
                morning_time_model.add_new(item.username, todaytime)

                str1 = u"查看自己的积分请回复“签到积分”"
                str2 = u"查看自己的排名请回复“签到排名”"
                str3 = u"查看排行榜请回复“排行榜”"
                str4 = u"查看积分规则请回复'积分规则'"

                return self.render.reply_text(fromUser, toUser, int(time.time()), u"恭喜小主今日完成签到任务[鼓掌]\n你是今天第%s个签到的人,请再接再厉!\
                                                   \n%s\n%s\n%s\n%s\n\n姓名      签到时间  \n%s\n明天请继续输入'早安'开始新一天的挑战" % (
                sign_rank, str1, str2, str3, str4, tempstr))

            return self.render.reply_text(fromUser, toUser, int(time.time()), u'[玫瑰]请小主按照要求完成![玫瑰]')

        elif msgType == "image":

            me = sign_morning_model.find_user(fromUser)

            item = ""
            try:
                item = me[0]
            except:
                pass

            fktime = time.strftime('%Y-%m-%d %H:%M', time.localtime())
            hour = time.strftime('%H', time.localtime())
            hour = int(hour)
            week = time.strftime('%w', time.localtime())
            week = int(week)

            if hour < SIGN_START or hour >= SIGN_END:
                return self.render.reply_text(fromUser, toUser, int(time.time()),
                                              u'不在签到时段，请在每天早上12:00~24:00签到哦，现在服务器时间%s' % fktime)
            if item.istoday == True:
                return self.render.reply_text(fromUser, toUser, int(time.time()), u'你今日已签到，请勿重复签到。')

            if week == 1:

                # 得到今天的时间 年-月—日 小时-分
                # temptime=list(str(int(time.time()))+fktime)
                # temptime=temptime[10:]
                # strtime="".join(temptime)

                # 得到今天的时间
                todaytime = sign_morning_model.gettime(str(int(time.time())) + fktime)

                t_month, t_day = sign_morning_model.get_mon_day(todaytime)

                # 得到上次签到的时间
                lasttime = item.timetoday
                last_month, last_day = sign_morning_model.get_mon_day(lasttime)

                last_record = 100
                print("t={},l={}".format(t_day, last_day))

                if t_month == last_month:  # 月份相同相差一天
                    if t_day - last_day == 1:
                        if item.last_record != 7:
                            last_record = item.last_record + 1
                        else:
                            last_record = 7
                    else:
                        last_record = item.last_record
                elif t_month == 5 and last_month == 4:  # 换月的时候 5,4月份交替
                    t_day += 30
                    if t_day - last_day == 1:  # 记得修改
                        if item.last_record != 7:
                            last_record = item.last_record + 1
                        else:
                            last_record = 7
                    else:
                        last_record = item.last_record
                if item.last_record == 0:
                    last_record = 1

                all_record = item.all_record + last_record
                # print("all={},last={}".format(all_record,last_record))
                # 得到签到排名
                sign_rank = sign_morning_model.get_sign_count(item.user)

                result = sign_morning_model.get_sign_name_time()

                tempstr = ""

                for i in result:
                    temp = "  "
                    if len(i["username"]) == 2:
                        temp = "       "
                    if len(i["username"]) == 1:
                        temp = "          "
                    tempstr += i["username"] + temp + i["timetoday"] + "\n"

                sign_morning_model.update(item.user, item.total, last_record, all_record, todaytime)
                morning_time_model.add_new(item.username, todaytime)

                str1 = u"查看自己的积分请回复“签到积分”"
                str2 = u"查看自己的排名请回复“签到排名”"
                str3 = u"查看排行榜请回复“排行榜”"
                str4 = u"查看积分规则请回复'积分规则'"

                return self.render.reply_text(fromUser, toUser, int(time.time()), u"恭喜小主今日完成签到任务[鼓掌]\n你是今天第%s个签到的人,请再接再厉!\
                                                   \n%s\n%s\n%s\n%s\n\n姓名      签到时间  \n%s\n明天请继续输入'早安'开始新一天的挑战" % (
                sign_rank, str1, str2, str3, str4, tempstr))
            if week == 2:

                # 得到今天的时间 年-月—日 小时-分
                # temptime=list(str(int(time.time()))+fktime)
                # temptime=temptime[10:]
                # strtime="".join(temptime)

                # 得到今天的时间
                todaytime = sign_morning_model.gettime(str(int(time.time())) + fktime)

                t_month, t_day = sign_morning_model.get_mon_day(todaytime)

                # 得到上次签到的时间
                lasttime = item.timetoday
                last_month, last_day = sign_morning_model.get_mon_day(lasttime)

                last_record = 100
                print("t={},l={}".format(t_day, last_day))

                if t_month == last_month:  # 月份相同相差一天
                    if t_day - last_day == 1:
                        if item.last_record != 7:
                            last_record = item.last_record + 1
                        else:
                            last_record = 7
                    else:
                        last_record = item.last_record
                elif t_month == 5 and last_month == 4:  # 换月的时候 5,4月份交替
                    t_day += 30
                    if t_day - last_day == 1:  # 记得修改
                        if item.last_record != 7:
                            last_record = item.last_record + 1
                        else:
                            last_record = 7
                    else:
                        last_record = item.last_record
                if item.last_record == 0:
                    last_record = 1

                all_record = item.all_record + last_record
                # print("all={},last={}".format(all_record,last_record))
                # 得到签到排名
                sign_rank = sign_morning_model.get_sign_count(item.user)

                result = sign_morning_model.get_sign_name_time()

                tempstr = ""

                for i in result:
                    temp = "  "
                    if len(i["username"]) == 2:
                        temp = "       "
                    if len(i["username"]) == 1:
                        temp = "          "
                    tempstr += i["username"] + temp + i["timetoday"] + "\n"

                sign_morning_model.update(item.user, item.total, last_record, all_record, todaytime)
                morning_time_model.add_new(item.username, todaytime)

                str1 = u"查看自己的积分请回复“签到积分”"
                str2 = u"查看自己的排名请回复“签到排名”"
                str3 = u"查看排行榜请回复“排行榜”"
                str4 = u"查看积分规则请回复'积分规则'"

                return self.render.reply_text(fromUser, toUser, int(time.time()), u"恭喜小主今日完成签到任务[鼓掌]\n你是今天第%s个签到的人,请再接再厉!\
                                                   \n%s\n%s\n%s\n%s\n\n姓名      签到时间  \n%s\n明天请继续输入'早安'开始新一天的挑战" % (
                sign_rank, str1, str2, str3, str4, tempstr))

            if week == 4:

                # 得到今天的时间
                todaytime = sign_morning_model.gettime(str(int(time.time())) + fktime)

                t_month, t_day = sign_morning_model.get_mon_day(todaytime)

                # 得到上次签到的时间
                lasttime = item.timetoday
                last_month, last_day = sign_morning_model.get_mon_day(lasttime)

                last_record = 100

                if t_month == last_month:  # 月份相同相差一天
                    if t_day - last_day == 1:
                        if item.last_record != 7:
                            last_record = item.last_record + 1
                        else:
                            last_record = 7
                    else:
                        last_record = 1
                elif t_month == 5 and last_month == 4:  # 换月的时候 5,4月份交替
                    t_day += 30
                    if t_day - last_day == 1:
                        if item.last_record != 7:
                            last_record = item.last_record + 1
                        else:
                            last_record = 7
                    else:
                        last_record = item.last_record
                if item.last_record == 0:
                    last_record = 1

                all_record = item.all_record + last_record

                # 得到签到排名
                sign_rank = sign_morning_model.get_sign_count(item.user)

                result = sign_morning_model.get_sign_name_time()

                tempstr = ""

                for i in result:
                    temp = "  "
                    if len(i["username"]) == 2:
                        temp = "       "
                    if len(i["username"]) == 1:
                        temp = "          "
                    tempstr += i["username"] + temp + i["timetoday"] + "\n"

                sign_morning_model.update(item.user, item.total, last_record, all_record, todaytime)
                morning_time_model.add_new(item.username, todaytime)

                str1 = u"查看自己的积分请回复“签到积分”"
                str2 = u"查看自己的排名请回复“签到排名”"
                str3 = u"查看排行榜请回复“排行榜”"
                str4 = u"查看积分规则请回复'积分规则'"

                return self.render.reply_text(fromUser, toUser, int(time.time()), u"恭喜小主今日完成签到任务[鼓掌]\n你是今天第%s个签到的人,请再接再厉!\
                                                    \n%s\n%s\n%s\n%s\n\n姓名      签到时间  \n%s\n明天请继续输入'早安'开始新一天的挑战" % (
                sign_rank, str1, str2, str3, str4, tempstr))
            if week == 6:

                # 得到今天的时间 年-月—日 小时-分
                # temptime=list(str(int(time.time()))+fktime)
                # temptime=temptime[10:]
                # strtime="".join(temptime)

                # 得到今天的时间
                todaytime = sign_morning_model.gettime(str(int(time.time())) + fktime)

                t_month, t_day = sign_morning_model.get_mon_day(todaytime)

                # 得到上次签到的时间
                lasttime = item.timetoday
                last_month, last_day = sign_morning_model.get_mon_day(lasttime)

                last_record = 100
                print("t={},l={}".format(t_day, last_day))

                if t_month == last_month:  # 月份相同相差一天
                    if t_day - last_day == 1:
                        if item.last_record != 7:
                            last_record = item.last_record + 1
                        else:
                            last_record = 7
                    else:
                        last_record = item.last_record
                elif t_month == 5 and last_month == 4:  # 换月的时候 5,4月份交替
                    t_day += 30
                    if t_day - last_day == 1:  # 记得修改
                        if item.last_record != 7:
                            last_record = item.last_record + 1
                        else:
                            last_record = 7
                    else:
                        last_record = item.last_record
                if item.last_record == 0:
                    last_record = 1

                all_record = item.all_record + last_record
                # print("all={},last={}".format(all_record,last_record))
                # 得到签到排名
                sign_rank = sign_morning_model.get_sign_count(item.user)

                result = sign_morning_model.get_sign_name_time()

                tempstr = ""

                for i in result:
                    temp = "  "
                    if len(i["username"]) == 2:
                        temp = "       "
                    if len(i["username"]) == 1:
                        temp = "          "
                    tempstr += i["username"] + temp + i["timetoday"] + "\n"

                sign_morning_model.update(item.user, item.total, last_record, all_record, todaytime)
                morning_time_model.add_new(item.username, todaytime)

                str1 = u"查看自己的积分请回复“签到积分”"
                str2 = u"查看自己的排名请回复“签到排名”"
                str3 = u"查看排行榜请回复“排行榜”"
                str4 = u"查看积分规则请回复'积分规则'"

                return self.render.reply_text(fromUser, toUser, int(time.time()), u"恭喜小主今日完成签到任务[鼓掌]\n你是今天第%s个签到的人,请再接再厉!\
                                                   \n%s\n%s\n%s\n%s\n\n姓名      签到时间  \n%s\n明天请继续输入'早安'开始新一天的挑战" % (
                sign_rank, str1, str2, str3, str4, tempstr))
            if week == 5:
                # 得到今天的时间
                todaytime = sign_morning_model.gettime(str(int(time.time())) + fktime)

                t_month, t_day = sign_morning_model.get_mon_day(todaytime)

                # 得到上次签到的时间
                lasttime = item.timetoday
                last_month, last_day = sign_morning_model.get_mon_day(lasttime)

                last_record = 100

                if t_month == last_month:  # 月份相同相差一天
                    if t_day - last_day == 1:
                        if item.last_record != 7:
                            last_record = item.last_record + 1
                        else:
                            last_record = 7
                    else:
                        last_record = item.last_record
                elif t_month == 5 and last_month == 4:  # 换月的时候 5,4月份交替
                    t_day += 30
                    if t_day - last_day == 1:
                        if item.last_record != 7:
                            last_record = item.last_record + 1
                        else:
                            last_record = 7
                    else:
                        last_record = item.last_record
                if item.last_record == 0:
                    last_record = 1

                all_record = item.all_record + last_record

                # 得到签到排名
                sign_rank = sign_morning_model.get_sign_count(item.user)

                result = sign_morning_model.get_sign_name_time()
                tempstr = ""

                for i in result:
                    temp = "  "
                    if len(i["username"]) == 2:
                        temp = "       "
                    if len(i["username"]) == 1:
                        temp = "          "
                    tempstr += i["username"] + temp + i["timetoday"] + "\n"

                sign_morning_model.update(item.user, item.total, last_record, all_record, todaytime)
                morning_time_model.add_new(item.username, todaytime)

                str1 = u"查看自己的积分请回复“签到积分”"
                str2 = u"查看自己的排名请回复“签到排名”"
                str3 = u"查看排行榜请回复“排行榜”"
                str4 = u"查看积分规则请回复'积分规则'"

                return self.render.reply_text(fromUser, toUser, int(time.time()), u"恭喜小主今日完成签到任务[鼓掌]\n 你是今天第%s个签到的人,请再接再厉!\
                                                  \n%s\n%s\n%s \n%s\n\n姓名      签到时间  \n%s \n明天请继续输入'早安'开始新一天的挑战" % (
                sign_rank, str1, str2, str3, str4, tempstr))



                # return self.render.reply_text(fromUser,toUser,int(time.time()),u'今天不用发图片哦![坏笑]')
        else:
            return self.render.reply_text(fromUser, toUser, int(time.time()), u'我们只支持文字和图片，请不要再调皮了![坏笑]')
            # return self.render.reply_text(fromUser,toUser,int(time.time()),u'[玫瑰]'+item.username+u'小主金安[玫瑰]\n小主今日签到成功[鼓掌]\n顺便完成个早安任务也是极好的：\n'+sign_task[i])

# coding: UTF-8
import os
 
import sae
import web

#import test_model
#import running_model
import morning_model
#import sign_morning_model
#import fellowship_model
#import laboratory_model
#import run3k_model
#import random
from weixinInterface import WeixinInterface
#from menu import Creatmenu


urls = (
#'/','Main',
#'/kjb', 'Kjb',
#'/xcb', 'Xcb',
'/weixin','WeixinInterface',
#'/creatmenu','Creatmenu',
#'/test','Test',
#'/fellowship','Fellowship_enroll',
#'/laboratory','Laboratory_enroll',
#'/run3k','Run3k_enroll'
)

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)


class Main:
    def GET(self):
		return render.main("四川大学计算机研分会")
    
class Kjb:
	def GET(self):
		return render.kjb("四川大学计算机学院研分会科技部")

class Xcb:
	def GET(self):
		return render.xcb("四川大学计算机学院研分会宣传部")
    
'''class Run3k_enroll:
    def GET(self):
        content = run3k_model.get_content()
        return render.run3k_enroll(content)
    
class Laboratory_enroll:
    def GET(self):
        content = laboratory_model.get_content()
        return render.laboratory_enroll(content)'''


class Morning_enroll:
    def GET(self):
        content = morning_model.get_content()
        return render.morning_enroll(content)

    
'''class Fellowship_enroll:
    def GET(self):
        content = fellowship_model.get_content()
        return render.fellowship_enroll(content)
        


class Morning_sign:
    def GET(self):
        content = sign_morning_model.get_content()
        return render.morning_sign(content)

class Morning_reset:
    def GET(self):
        sign_morning_model.reset()
        return render.morning_reset()
    
class Running_enroll:
    def GET(self):
        content = running_model.get_content()
        return render.running_enroll(content)
    
class Test:
    def GET(self):
        test_model.reset()
        return render.test_reset()'''
    
app = web.application(urls, globals()).wsgifunc()        
application = sae.create_wsgi_app(app)
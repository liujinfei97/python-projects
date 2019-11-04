#此文档用于创建电子词典项目,这个文件是第一部分，用于创建数据库
#这个模块只有一个方法，用于将字典数据存入数据库的words表中



from pymysql import* #导入模块
import re

#创建e—dict项目的数据库模块
#class My_e_dict_database:
    #为客户端数据库，进行数据初始化
   # def __init__(self,dict,host="localhost",user="root",password="1234",port=3306,charset="utf8"):
    #    self.host=host
     #   self.user=user
      #  self.password=password
       # selp.port=port
        #self.charset=charset
        #self.dict=db_dict
  
 #连接到数据库
 #def connect_database(self):
  #  dict = pymysql.connect(host=self.host,user=self.user,password=self.password,database=self.db_dict,charset=self.charset)
    
#此方法用于将字典数据存入数据库中的表中,在进行这个操作之前，要确保字典文件是utf-8格式的
def add_dict():
    f = open("./dict.txt")  #打开根目录下的字典数据文件
    db = pymysql.connect('localhost','root','123456','dict')
    cursor = db.cursor

    for line in f:
        l = re.split(r'\s+',line)
        word = l[0]
        interpret = ' '.join(l[1:])

        sql = "insert into words values('%s','%s')"%(word,interpret)

        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
    f.close()
    

#这个模块是客户端框架
#创建套接字--》创建父子进程--》子进程等待处理客户端请求--》父进程继续接受下一个客户端请求

import os
import time
import signal
import pymysql
import sys 


#定义需要的全局变量
DICT_TXT = "./dict.txt"  #字典数据储存在根目录下
HOST= '0.0.0.0'  #默认本地服务器
PORT = 8888
ADDR = (HOST,PORT)

#流程控制
def main():
    #创建数据库连接
    db = pymysql.connect('localhost','root','123456','dict')
    #创建套接字
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_RESUSEADDR,1)  #设置socket属性
    s.bind(ADDR)  #绑定地址
    s.listenn(5) #监听套接字
    
    #忽略子进程信号，防止产生僵尸进程
    signal.signal(signal.SIGCHILD,signal.SIG_IGN)  #当子进程传来exit()信号时，父进程以忽略的方式处理这些消息
    #由于这些消息被处理了，所以就不会再留下僵尸进程（Zoombie）的数据结构了，就避免了僵尸进程的产生
    
    #循环监听/接受客户端
    while True:
        try:
            c,addr = s.accept()
            print("Connect from",addr)
        except KeyboardInterrupt:  #只有再服务端按下CTRL+c时，服务器退出
            #当我们按了ctrl+c时，就退出
            s.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue

        #创建子进程，再监听并连接到客户端以后，创建子进程来处理客户端请求
        pid = os.fork()
        if pid ==0:
            s.close()  #关闭子进程中的s
            do_child(c,db)#处理客户端请求
            print("子进程准备处理请求")
            sys.exit(0)
        else:  
            #父进程中的连接socket关闭，等待接受下一次连接，子进程中也有相同的socket对象，
            #继续再子进程中对客户前端请求进行处理
            c.close()
            continue

#判别是那一种请求，并进行相对的处理
def do_child(c,db):
    #循环接收客户端请求
    while True:
        data = c.recv(128).decode()
        print(c.getpeername(),":",data)#getsockname与getpeername是返回套接口关联的本地协议地址和远程协议地址。
        if data[0] == 'R':
            #这是注册操作
            do_register(c,db,data)
        elif data[0] == 'L':
            do_login(c,db,data)
        elif data[0] == 'Q':
            do_query(c,db,data)
        elif data[0] == 'H':
            do_hist(c,db,data)


#登录处理
def do_login(c,db,data):
    print("登陆操作")
    name = l[1]
    passwd = l[2]
    cursor = db.cursor()
    sql = "select * from user where name='%s' and passwd ='%s'"%(name,passwd)
    cuesor.execute(sql)
    r = cursor.fetchone()  #第一条查询结果
    if r == None:
        c.send(b'FALL')
    else:
        c.send(b'OK')

#注册处理
def do_register(c,db,data):
    print("注册操作")
    l = data.split(' ') #以空格分隔
    name = l[1]
    passwd = l[2]
    curcor = db.curcor()
    sql = "select * from user where name ='%s'"%name
    curcor.ececute(sql)
    r = cursor.fetchone  #第一条数据
    if r!=None:  #表示用户已将存在
        c.send(b'EXISTS')
        return
    #用户不存在，就插入
    sql= "insert into user (name,passwd) values('%s','%s')"%(name,passwd)
    try:
        cursor.execute(sql)
        db.commit()
        c.send(b'OK')
    except:
        db.rollback()
        c.send(b"FALL")
    else:
        print("%s注册成功"%name)

        



#查询处理
def do_query(c,db,data):
    print("查询操作")
    l = data.split(' ')
    name = l[1]
    word = l[2]
    cursor = db.cursor()

    def insert_history:   #写在函数内部就不需要传参了
        time= time.ctime()
        sql = "insert into his (name,word,time) values('%s','%s',''%s)"%(name,word,time)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()


    #文本查询
    try:
        f = open(DICT_TXT)
    except:
        c.send(b'FALL')
        return
    for line in f:
        tmp = line.split(' ')[0]
        if tmp > word: #说明查不到文件了
            c.send(b'FALL')
            f.close()
            return
        elif tmp == word:
            c.send(b'OK')
            time.sleep(0.1)
            c.send(line.encode())  #line in f
            f.close()
            insert_history()
            return
        c.send(b'FALL')
        f.close()
        return




#查询历史记录
def do_hist(c,db,data):
    print("历史记录操作")
    l = data.split(' ')
    name = l[1]
    cursor = db.cursor()
    sql = "select * from hist where name='%s'"%name
    cursor.execute(sql)
    r = cursor.fetchall()
    if not r:
        c.send(b'FALL')
        return
    else:
        c.send(b'OK')
    for i in r:
        time.sleep(0.1)
        msg = "%s  %s  %s"%(i[1],i[2],i[3])
        c.send(msg.encode())
    time.sleep(0.1)
    c.send(b'##')


if __name__ =="__main__":
    main()


#电子词典，文件服务器，聊天室
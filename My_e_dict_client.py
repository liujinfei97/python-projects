#！/usr/bin/python3
#coding=utf-8
#这是客户端
#客户端  创建套接字--》发起连接请求--》一级界面--》请求（登录，注册，退出）--》登陆成功--》二级界面
#--》请求（查词，历史记录）

from socket import *
import sys
import getpass

#创建网络连接
from typing import Any


def main():
    if len(sys.argv) <3:  #从命令行获取连接地址
        print("argv is error")
        return
    HOST =sys.argv[1]
    PORT =int(sys.argv[2])
    s = socket()
    
    try:
        s.connect((HOST,PORT))
    except Exception as e:
        print(e)
        return
    

    #连接成功，就进入一级界面
    while True:
        print('''
        ===========Welcome========
        --1.注册  2.登录  3.退出---
        ==========================
        ''')
        
        try:
            cmd = int(input("请输入选项："))  # type: Any
        except Exception as e:
            print("命令错误")
        if cmd not in [1,2,3]:
            print("请输入正确的选项")
            sys.stdin.flush()  #清除标准输入
            continue
        elif cmd==1:  #注册操作
           r = do_register(s)
           if r ==0:
               print("注册成功")
           elif r == 1:
               print("用户存在")
           else:
               print("注册失败")
        elif cmd==2:  #登录操作
            name = do_login(s)
            if name:
                print("登陆成功") #登陆成功就进入二级界面
                login(s,name)
            else:
                print("用户名或密码不正确")
        elif cmd==3:
            s.close()
            sys.exit("客户端退出，谢谢使用")
        else:
            print("您输入的选项有误，请重新输入")
            
#此方法用于用户注册            
def do_register(s):
    while True:  #为了防止密码输入错误，循环输入
        name = input("User:")
        passwd = getpass.getpass() #加密输入密码
        passwd1 = getpass.getpass('Again:')#再次确认输入的密码
        if (' ' in name) or (' ' in passwd):
            print("用户名和密码不许有空格")
            continue
        if passwd !=passwd1:
            print("两次输入的密码不一致")
            continue
        msg = 'R {} {}'.format(name,passwd) #*****这里的写法注意学习
        #发送请求
        s.send(msg.encode())
        #接受服务器回复
        data = s.recv(128).decode()
        if data == 'OK':
            return 0:
        elif data == 'EXISTS':
            return 1
        else:
            return 2


def do_login(s):
    name = input("Users:")
    passwd = getpass.getpass()
    msg = "L {} {}".format(name,passwd)
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == 'OK':
        return name
    else:
        return


def login(s,name):
    while True:
        print('''
                 ===========Welcome========
                  --1.查询  2.历史记录  3.退出---
                 ==========================
        ''')
        try:
            cmd = int(input("请输入选项："))  # type: Any
        except Exception as e:
            print("命令错误")
        if cmd not in [1,2,3]:
            print("请输入正确的选项")
            sys.stdin.flush()  #清除标准输入
            continue
        elif cmd==1:  #查操作
            do_query(s,name)
        elif cmd==2:  #历史记录操作
            do_host(s,name)
        elif cmd==3:
           return


#查询操作
do_query(s,name): #传入name数据，为了保存到历史记录
    while True:
        word = input('单词:')  #输入'##'退出
        if word == '##'
            break
        msg = "Q {} {}".format(name,word)
        s.send(msg.encode())
        data = s.recv(128).encode()
        if data == 'OK':
            data = s.recv(2048).decode()
            print(data)
        else:
            print("没有查询到该单词")





#历史记录
def do_host(s,name):
    msq = 'H {}'.format(name)
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == 'OK':
        while True:
            data = s.recv(1024).decode()
            if data =='##':
                break
            print(data)
    else:
        print("没有历史记录")



if __name__ =="__main__":
    main()
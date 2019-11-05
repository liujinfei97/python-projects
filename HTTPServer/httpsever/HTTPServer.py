#coding=utf-8
'''
name:liujinfei
time:2019-11-4
'''


#Http项目比较特殊，既需要与浏览器交互，又需要与服务器交互
from socket import *  #需要网络通信
import sys            #需要退出等操作
import re             #需要用到正则表达式对请求内容进行匹配
from threading import Thread  #多线程，接受请求
from setting import *  #setting是自己写的配置文件
import time


class HTTPServer(object):  #定义一个类，生成对象


    def __init__(self,addr = ('0.0.0.0',8080)):
        self.sockfd = socket()  #创建套接字
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.addr = addr
        self.bind(addr)   #写一个绑定函数，降低耦合度


    def bind(self,addr):
        self.ip = addr[0]
        self.port = addr[1]
        self.sockfd.bind(addr)  # 绑定地址

    #HTTP服务器启动
    def serve_forever(self):
        self.sockfd.listen(10)  #监听
        print("Listen the port %d ..."%self.port)
        while True:
            connfd,addr = self.sockfd.accept()  #连接
            print("connect from",addr)
            #调用方法处理连接后的事件
            handle_client = Thread(target=self.handle_request,args=(connfd,))  #多线程处理，target绑定线程函数，args位置传参
            handle_client.setDaemon(True)  #设定为true分支线程随主线程退出
            handle_client.start() #线程开始


    def handle_request(self,connfd):
        #接受浏览器请求
        request = connfd.recv(4096)
        print(request)
        #由打印结果直，第一项时是请求内容
        request_lines = request.splitlines()
        request_line = request_lines[0].decode()
        #从请求行中提取请求方法和请求内容，利用正则表达式 , （?P<name>pattern）#给子组取名字
        pattern = r'(?P<METHOD>[A-Z]+)\s+(?P<PATH>/\S*)' #正则表达式选出

        try:
            env = re.match(pattern,request_line).groupdict()
            print(env)
        except:
            response_handlers = "HTTP/1.1 500 Sever Error\r\n"  #如果出现异常，就发送500服务异常给WebFrame
            response_handlers += '\r\n'
            response_body = "Sever Error"
            response = response_handlers+response_body  #response响应格式
            connfd.send(response.encode())
            return

        #将请求发送给WebFrame并得到返回数据
        status,response_body = \
            self.send_request(env['METHOD'],env['PATH'])
        #服务端接受响应码，组织响应头内容
        response_headlers = self.get_headlers(status)
        #将结果组织为响应内容，发送给客户端
        response = response_headlers+response_body
        connfd.send(response.encode())
        connfd.close()


    #和frame 交互 发送request获取response
    def send_request(self,method,path):
        s = socket()
        s.connect(frame_addr)
        #向webframe发送method和path
        s.send(method.encode())
        time.sleep(0.1)  #为了防止粘包
        s.send(path.encode())
        #返回值
        status = s.recv().decode()
        response_body = s.recv(4096).decode()
        return status,response_body


    # #根据webFrame返回的响应码组织响应头内容
    def get_headlers(self,status):
        if status == '200':
            response_headlers = 'HTTP/1.1 200 OK\r\n'
            response_headlers += '\r\n'
        elif status == '400':
            response_headlers == 'HTTP/1.1 404 NotFound\r\n'
            response_headlers += '\r\n'

        return response_headlers




if __name__ =="__main__":  #当运行此文件时自动运行下面的内容
    httpd = HTTPServer(ADDR)
    httpd.serve_forever()
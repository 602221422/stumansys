# -- coding: utf-8 --
import socket,select,threading,sys

host=socket.gethostname()

addr=(host,7567)

def conn():		#定义一个函数
    t=socket.socket()#创建一个socket以连接服务器：socket = socket.socket(family, type) 
    t.connect(addr)#.使用socket的connect方法连接服务器
    return t

def lis(t):
    my=[t]
    while True:
        r,w,e=select.select(my,[],[])   #异步socket处理方法
        if t in r:
            try:
                print t.recv(1024)
            except socket.error:
                exit()
            
def talk(t):
    while True:
        try:
            i=raw_input()
        except Exception,e:
            exit()
        try:
            t.send(i)
        except Exception,e:
            print e
            exit()
            
def main():
    chat=conn()
    threading.Thread(target=lis,args=(chat,)).start()
    threading.Thread(target=talk,args=(chat,)).start()
#把函数对象lis,talk作为参数传给它的初始化函数，再调用Thread对象的start方法，线程启动后将执行此函数。
if __name__=='__main__':
    main()

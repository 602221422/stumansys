# -- coding: utf-8 --
import socket,select,threading,sys

host=socket.gethostname()

addr=(host,7567)

def conn():
    s=socket.socket()#创建一个socket以连接服务器：socket = socket.socket(family, type) 
    s.connect(addr)#.使用socket的connect方法连接服务器
    return s

def lis(s):
    my=[s]
    while True:
        r,w,e=select.select(my,[],[])   #异步socket处理方法
        if s in r:
            try:
                print s.recv(1024)
            except socket.error:
                print 'socket is error'
                exit()
            
def talk(s):
    while True:
        try:
            info=raw_input()
        except Exception,e:
            print "can't input"
            exit()
        try:
            s.send(info)
        except Exception,e:
            print e
            exit()
            
def main():
    ss=conn()
    threading.Thread(target=lis,args=(ss,)).start()
    threading.Thread(target=talk,args=(ss,)).start()
#把函数对象lis,talk作为参数传给它的初始化函数，再调用Thread对象的start方法，线程启动后将执行此函数。
if __name__=='__main__':
    main()

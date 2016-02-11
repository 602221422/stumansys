# -- coding: utf-8 --
import socket,select,thread
#两个程序通过一个双向的通信连接实现数据的交换，这个连接的一端称为一个socket
#使用select模块，实现异步通信.当一个服务器需要与多个客户端进行通信时，可以使用多进程或者多线程的服务器
#实现多线程的一个模块，来处理和控制线程
host=socket.gethostname()    #gethostname()返回运行程序所在的计算机的主机名
port=7567        #端口号
addr=(host,port) #host表示能够同其他机器互相访问的本地计算机，host代表主机，port代表端口号
inputs=[]
chat_name={}

def who_in_room(n):
    name=[]
    for i in n:
        name.append(n[i])   #append是列表的方法，表示在列表的最后添加上n[i]这个新元素
    return name		    #表示打印出谁在聊天室内

def conn():
    print 'server is running'
    chat=socket.socket()   #创建socket对象，调用socket构造函数
    chat.bind(addr)        #将socket绑定到指定地址。
    chat.listen(5) #使用socket套接字的listen方法接收连接请求。指定最多数量客户连接到服务器。
    return chat

def new_coming(chat):
    client,add=chat.accept()
#服务器套接字通过socket的accept方法等待客户请求一个连接。accept方法返回一个含有两个元素的 元组(connection,address)。第一个元素connection是新的socket对象，服务器必须通过它与客户通信；第二个元素 address是客户的Internet地址。
    print 'welcome %s %s' % (client,add)
#例：打印出welcome <socket._socketobject object at 0x7fb2e4b82600> ('127.0.0.1', 58340)
    wel='''请输入你的名字：'''
    try:
        client.send(wel)     #send()的返回值是发送的字节数量
        Name=client.recv(1024)    #recv(1024)指定了recv函数每次最多只能接收1024字节
        inputs.append(client)
        chat_name[client]=Name     
        nameList="Some people in talking room, these are %s" % (who_in_room(chat_name))
        client.send(nameList)
        
    except Exception,e:
        print e
#打印出进入者（即聊天者）的名字   
#try:
#    <语句> #运行别的代码
#except <名字>：
#    <语句> #如果在try部份引发了'name'异常
#except <名字>，<数据>:
#    <语句> #如果引发了'name'异常，获得附加的数据

 
def server_run():

    chat=conn()
    inputs.append(chat)
    
    while True:
        r,w,e=select.select(inputs,[],[])
        for t in r:
            if t is chat:
                new_coming(chat)
            else:
                disconnect=False
                try:
                    data= t.recv(1024)
                    data=chat_name[t]+' say : '+data
                except socket.error:
                    data=chat_name[t]+' leave the room'
                    disconnect=True
#显示人员说话内容                    
                if disconnect:
                    inputs.remove(temp)
                    print data
                    for other in inputs:
                        if other!=chat and other!=temp:
                            try:
                                other.send(data)
                            except Exception,e:
                                print e                    
                    del chat_name[temp]
                    
                else:
                    print data
                    
                    for other in inputs:
                        if other!=chat and other!=t:
                            try:
                                other.send(data)
                            except Exception,e:
                                print e
#服务器工作 
if __name__=='__main__':#自运行时调用该程序块
    server_run()

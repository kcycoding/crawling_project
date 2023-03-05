import socketserver
import threading
import datetime
import json
import time
import tkinter.scrolledtext as tkst
import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By

HOST = '192.168.0.11'
# HOST = '192.168.0.9' # 서버의 ip를 열음. (이 서버의 ip로 클라이언트가 접속을 해야 한다), 그전에 ping을 먼저 확인하도록.
PORT = 9900       # 포트번호 (같아야 함)
lock = threading.Lock()  # syncronized 동기화 진행하는 스레드 생성

# sql에 insert into

con = pymysql.connect(host='localhost', user='root', password='201618!@', db='plane_ticket_db', charset='utf8')
# user,pw,host,db,charset 등 매개변수 설정 후 connect 한 객체 : con

# con 객체에서 cursor 만들기

cur = con.cursor()

class User:  # 사용자관리 및 채팅 메세지 전송을 담당하는 클래스

    userList = ['aa']

    def __init__(self):
        self.users = {}  # 사용자의 등록 정보를 담을 사전 {사용자 이름:(소켓,주소),...}
        # 사용자 리스트

    def addUser(self, p_id, p_pw, p_name1, p_name2, p_gender, p_birth, p_email, p_passport):  # 사용자 ID를 self.users에 추가하는 함
        global con
        sql = "SELECT * FROM "
        x = "plane_ticket_db.passenger_info"
        cur.execute(sql + x)
        data = list(cur.fetchall())
        # print(data)

        if len(data) == 0:
            User.userList = p_id

            # sql변수에 sql문법 작성
            sql4 = 'INSERT INTO passenger_info VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'
            val = [(p_id, p_pw, p_name1, p_name2, p_gender, p_birth, p_email, p_passport)]

            # sql변수에 sql문법 작성
            sql = '''SELECT * FROM passenger_info; '''
            # 커서를 통해 sql문 실행
            try:
                cur.executemany(sql4, val)
                con.commit()
            except Exception as ex:
                print('addUser', type(ex), ex)

            return "0"  # 없으면 0

        for k in data:
            for i in range(len(k)):
                if p_id == k[i]:
                    return "1"

                else:
                    User.userList = p_id

                    # sql변수에 sql문법 작성
                    sql4 = 'INSERT INTO passenger_info VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'
                    val = [(p_id, p_pw, p_name1, p_name2, p_gender, p_birth, p_email, p_passport)]

                    # sql변수에 sql문법 작성
                    # sql = '''SELECT *
                    #           FROM passenger_info; '''
                    # 커서를 통해 sql문 실행
                    try:
                        cur.executemany(sql4, val)
                        con.commit()
                    except Exception as ex:
                        print('addUser',type(ex),ex)

                    return "0" # 없으면 0

    def Basket(self, p_id, p_basket):
        global con
        global cur
        sql4 = 'INSERT INTO ticket_basket(passenger_id,basket1) VALUES(%s,%s)'
        val = [(p_id, p_basket)]
        sql = 'SELECT * FROM ticket_basket;'
        # 커서를 통해 sql문 실행
        try:
            cur.executemany(sql4, val)
            con.commit()
        except Exception as ex:
            print('Basket', type(ex), ex)

    def Buy(self, p_id, p_buy):
        global con
        global cur
        sql4 = 'INSERT INTO ticket_buy(passenger_id,buy) VALUES(%s,%s)'
        val = [(p_id, p_buy)]
        sql = 'SELECT * FROM ticket_buy;'
        # 커서를 통해 sql문 실행
        try:
            cur.executemany(sql4, val)
            con.commit()
        except Exception as ex:
            print('Buy', type(ex), ex)

    def Cancel(self, p_cancel):
        global con
        global cur
        print("cancle 안")
        sql = """DELETE FROM ticket_basket WHERE basket1 = %s"""
        cur.execute(sql, p_cancel)
        try:
            print("cancel try 안")
            con.commit()
        except Exception as ex:
            print('Buy', type(ex), ex)




basket = None

class MyTcpHandler(socketserver.BaseRequestHandler):
    user = User()

    def handle(self):  # 클라이언트가 접속시 클라이언트 주소 출력
        global con
        global basket
        # 클라이언트의 접속요청이 수락된 후 호출됨
        # 서버와 클라이언트가  데이터를 주고 받는 메소드로 재정의해서 사용,
        # BaseRequestHandler클래스 안에 속해있는 메소드
        key = True
        try:
            while key:
                # sql = "SELECT * FROM "
                # x = "plane_ticket_db.passenger_info"
                # cur.execute(sql + x)
                # p_info = json.dumps(cur.fetchall()).encode('utf-8')
                # print(p_info)
                # self.request.send(bytes(p_info))  #회원보 보내기

                data = self.request.recv(16184)  #서버에서 데이터 받기
                print(data)
                if bytes(data).decode() == 'sign':  # 회원가입
                    sql = "SELECT * FROM "
                    x = "plane_ticket_db.passenger_info"
                    cur.execute(sql + x)
                    p_info = json.dumps(cur.fetchall()).encode('utf-8')
                    self.request.send(bytes(p_info))

                    json_dict = json.loads(self.request.recv(16184))
                    p_id = json_dict['passenger_id']
                    p_pw = json_dict['passenger_pw']
                    p_name1 = json_dict['passenger_name1']
                    p_name2 = json_dict['passenger_name2']
                    p_gender = json_dict['passenger_gender']
                    p_birth = json_dict['passenger_birth']
                    p_email = json_dict['passenger_email']
                    p_passport = json_dict['passenger_passport']
                    self.user.addUser(p_id, p_pw, p_name1, p_name2, p_gender, p_birth, p_email, p_passport)
                    # key = False

                elif bytes(data).decode() == 'login':  # 로그인
                    sql = "SELECT * FROM "
                    x = "plane_ticket_db.passenger_info"
                    cur.execute(sql + x)
                    p_info = json.dumps(cur.fetchall()).encode('utf-8')
                    self.request.send(bytes(p_info))

                elif bytes(data).decode() == 'passenger_basket':
                    json_dict = json.loads(self.request.recv(16184))
                    p_id = json_dict['passenger_id']
                    a = json_dict['passenger_basket']
                    for j in a:
                        p_basket = ",".join(j)
                        self.user.Basket(p_id, p_basket)

                elif bytes(data).decode() == 'basket':
                    print("basket 안")
                    sql = """SELECT *
                            FROM ticket_basket
                            inner join passenger_info
                            on ticket_basket.passenger_id = passenger_info.passenger_id"""
                    cur.execute(sql)
                    basket = list((cur.fetchall()))
                    #print(basket)
                    # p_basket = json.dumps(cur.fetchall()).encode('utf-8')
                    basket = json.dumps(basket).encode('utf-8')
                    self.request.send(bytes(basket))
                    time.sleep(1)

                elif bytes(data).decode() == 'ticket_buy':
                    print("ticket_buy")
                    json_dict = json.loads(self.request.recv(16184))
                    p_id = json_dict['passenger_id']
                    a = json_dict['buy']
                    p_buy = ','.join(str(s) for s in a)
                    # print(p_buy)
                    self.user.Buy(p_id, p_buy)

                elif bytes(data).decode() == 'basket_cancel':
                    print("basket_cancel")
                    json_dict = json.loads(self.request.recv(16184))
                    # p_id = json_dict['passenger_id']
                    a = json_dict['basket_cancel']
                    del a[-8:]
                    p_cancel = ','.join(str(s) for s in a)
                    # print(p_cancel)
                    self.user.Cancel(p_cancel)

                else:
                    pass


        except Exception as e:
            print("5")
            print("handle11", e)





class ChatingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
   # ThreadingMixIn 클래스는 서버가 스레드 종료를 기다려야하는지를 가리키는 daemon_threads 어트리뷰트를 정의

   # TCPServer 클래스 안의 serve_forever()메소드 : 클라이언트의 접속 요청을 수신대기. 접속 요청이 있을 경우 수락하고 BaseRequestHandler의 handle() 메소드를 호출
   # TCPServer 클래스가 serve_forever() 메소드를 통해 클라이언트의 연결 요청을 기다리다가 클라이언트에게서 접속요청이 오면 이를 수락한 뒤 BaseRequestHandler
   # 객체의 handle() 메소드를 호출.서버 애플리케이션은 이 handler()메소드를 재정의해서 클라이언트와 데이터를 주고받는 일을 수행.

   # 서버가 클라이언트의 연결 요청을 수락해서 TCP 커넥션이 만들어지고 나면 그 다음부터는 서버 측의 socket 객체와 클라이언트 측의 socket 객체가
   # socket.send() 메소드와 socket.recv() 메소드를 통해 데이터를 주고 받을 수 있다. 서버 애플리케이션에서는
   # BaseRequestHandler의 request 데이터 속성이 바로 socket 객체. 데이터를 주고받는 일을 마치고 나서 서버와 클라이언트의 연결을 종료할 때는
   # socket의 close() 메소드를 호출하면 됨.

   # BaseRequestHandler 클래스 안의 handle() 메소드 : 클라이언트 접속 요청을 처리.
   # socket : 논리적인 의미로 컴퓨터 네트워크를 경유하는 프로세스 간 통신(Inter-Process Communication, IPC)의 종착점(end-point)
   # bind(): 사용할 IP address와 Port number 등록(각 소켓에 할당)
   # connect(): Client에서 Server와 연결하기 위해 소켓과 목적지 IP address, Port number 지정 (Block 상태)
   # send(), recv(): Client는 처음에 생성한 소켓으로, Server는 새로 반환(생성)된 소켓으로 client와 server간에 데이터 송수신

    pass



def runServer():
    print('+++ 서버를 시작합니다.')

    try:

        server = ChatingServer((HOST, PORT), MyTcpHandler)# 서버 객체 생성
        # 인스턴스 = 클래스명(생성자)
        server.serve_forever() # 클라이언트의 접속요청 수락 및 handle() 메소드 호출하는 역할
    except KeyboardInterrupt:
        print('--- 채팅 서버를 종료합니다.')
        server.shutdown()
        server.server_close()

runServer()
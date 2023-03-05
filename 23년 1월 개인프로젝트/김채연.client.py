import socket
import datetime
import time
import tkinter
from tkinter import *
from _thread import *
from tkcalendar import *
import threading
import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import tkinter.font as tkFont
import json
import tkinter.messagebox
import tkinter.ttk as ttk
import PyInstaller
import babel.numbers


# data = []
# for element in elements:
#     data.append({
#         "title": element.find_element(By.CSS_SELECTOR, "div.course_title").text,
#         "teacher": element.find_element(By.CSS_SELECTOR, "div.card-content > div.instructor").text,
#         "price": element.find_element(By.CSS_SELECTOR, "div.card-content > div.price").text,
#         "link": element.find_element(By.CSS_SELECTOR, "a.course_card_front").get_attribute("href"),
#     })

# HOST = '192.168.0.11'
# #HOST = "192.168.0.9"
# PORT =9900

# con = pymysql.connect(host='localhost', user='root', password='201618!@', db='plane_ticket_db', charset='utf8')
# #user,pw,host,db,charset 등 매개변수 설정 후 connect 한 객체 : con
#
# # con 객체에서 cursor 만들기
# cur = con.cursor()
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((HOST, PORT))

today_time = datetime.date.today()
ticket = []
get_item = []
basket = []
basket_item= []
go_day = None
go_day2 = None
go_day3 = ""
go_month = None
come_day = None
come_day2 = None
come_day3 = ""
come_month = None


# driver = webdriver.Chrome()
# driver.get("https://m-flight.naver.com/")
# time.sleep(1)

con = None
cur = None
client_socket = None


def Main_Open():
    global con
    global cur
    global client_socket
    main_Frame2.pack(side='left', fill='both', expand=True)
    id_input.place(width=300, height=40, x=360, y=450)
    password_input.place(width=300, height=40, x=360, y=530)
    login_button.place(x=700, y=450)
    make_id.place(x=700, y=595)


    HOST = '192.168.0.11'
    # HOST = "192.168.0.9"
    PORT = 9900

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))


def Sign_Member():
    sign_Frame.pack(side='left', fill='both', expand=True)
    sign_button.place(x=800, y=750)
    sign_exit_button.place(x=905, y=20)



def Sign():
    # print(sign_id_input.get())
    # print(sign_password_input.get())
    # print(sign_name1_input.get())
    # print(sign_name2_input.get())
    # print(sign_gender_input.get())
    # print(sign_birth_input.get())
    # print(sign_email_input.get())
    # print(sign_passport_input.get())
    client_socket.sendall(bytes("sign".encode('utf-8')))
    time.sleep(1)
    p_info = client_socket.recv(16184)
    p_info = json.loads(p_info)
    print(p_info)
    for i in p_info:
        print(i[0])
        if i[0] == sign_id_input.get():
            tkinter.messagebox.showinfo("메시지", "이미 존재하는 아이디입니다.")
            break
        else:
            if sign_birth_input.get().isdigit():
                passenger_info = json.dumps({
                    "passenger_id": sign_id_input.get(),
                    "passenger_pw": sign_password_input.get(),
                    "passenger_name1": sign_name1_input.get(),
                    "passenger_name2": sign_name2_input.get(),
                    "passenger_gender": sign_gender_input.get(),
                    "passenger_birth": sign_birth_input.get(),
                    "passenger_email": sign_email_input.get(),
                    "passenger_passport": sign_passport_input.get()

                }).encode('utf-8')
                # print(passenger_info)
                client_socket.sendall(bytes(passenger_info))
                tkinter.messagebox.showinfo("메시지", "가입이 완료되었습니다.")
                sign_id_input.delete(0, len(sign_id_input.get()))
                sign_password_input.delete(0, len(sign_password_input.get()))
                sign_name1_input.delete(0, len(sign_name1_input.get()))
                sign_name2_input.delete(0, len(sign_name2_input.get()))
                sign_gender_input.delete(0, len(sign_gender_input.get()))
                sign_birth_input.delete(0, len(sign_birth_input.get()))
                sign_email_input.delete(0, len(sign_email_input.get()))
                sign_passport_input.delete(0, len(sign_passport_input.get()))
                sign_Frame.pack_forget()
                break
            else:
                tkinter.messagebox.showinfo("메시지", "생년월일은 숫자만 입력하세요.")
                break

def Sign_Exit():
    global sign_Frame
    sign_id_input.delete(0, len(sign_id_input.get()))
    sign_password_input.delete(0, len(sign_password_input.get()))
    sign_name1_input.delete(0, len(sign_name1_input.get()))
    sign_name2_input.delete(0, len(sign_name2_input.get()))
    sign_gender_input.delete(0, len(sign_gender_input.get()))
    sign_birth_input.delete(0, len(sign_birth_input.get()))
    sign_email_input.delete(0, len(sign_email_input.get()))
    sign_passport_input.delete(0, len(sign_passport_input.get()))
    sign_Frame.pack_forget()
    login_button['state'] = 'normal'


def Login():
    global id_input
    global password_input
    values = json.dumps({
        "passenger_id" : id_input.get(),
        "passenger_pw" : password_input.get()
    }).encode('utf-8')
    client_socket.sendall(bytes('login'.encode('utf-8')))
    time.sleep(1)
    client_socket.sendall(bytes(values))

    login_data = client_socket.recv(16184)
    login_data = json.loads(login_data)
    print(login_data)
    time.sleep(1)
    # print(type(login_data))

    # if bytes(data).decode() == "0":
    key = True
    while key:
        for i in login_data:
            if i[0] == id_input.get():
                if i[1] == password_input.get():
                    key = False
                    login_Frame.pack(side='left', fill='both', expand=True)
                    login_exit_button.place(x=905, y=20)
                    start_label.place(x=150, y=170)
                    start_input.place(x=150, y=200, width=200, height=40)
                    end_label.place(x=500, y=170)
                    end_input.place(x=500, y=200, width=200, height=40)
                    go_label.place(x=150, y=270)
                    go_calendar.place(x=150, y=300, width=200, height=40)
                    go_reset.place(x=360, y=300, width=50, height=40)
                    # go_input.place(x=150, y=300, width=200, height=40)
                    come_label.place(x=500, y=270)
                    come_calendar.place(x=500, y=300, width=200, height=40)
                    come_reset.place(x=710, y=300, width=50, height=40)
                    # come_input.place(x=400, y=300, width=200, height=40)
                    # calendar.place(x=650, y=200)

                    ticket_search.place(x=790, y=300, width=100, height=40)
                    ticket_print.place(x=20, y=360)
                    #ticket_print2.place(x=10, y=500)
                    ticket_select.place(x=20, y=560)
                    ticket_basket.place(x=700, y=550)
                    show_basket_button.place(x=850, y=550)
                else:
                    tkinter.messagebox.showinfo("로그인 오류", "해당 아이디와 비밀번호가 일치하지 않습니다.")
                    id_input.delete(0, len(id_input.get()))
                    password_input.delete(0, len(password_input.get()))
                    key = False
            else:
                key = False

    #     login_Frame.pack(side='left', fill='both', expand=True)
    #     login_Frame.pack()
    #     exit_button.pack()
    #     login_button['state'] = 'disabled'
    # elif bytes(data).decode() == "1":
    #     tkinter.messagebox.showinfo("메세지", "정보가 맞지 않습니다.")


def Login_Exit():
    global login_Frame
    login_Frame.pack_forget()
    login_exit_button.pack_forget()
    id_input.delete(0, len(id_input.get()))
    password_input.delete(0, len(password_input.get()))
    start_input.delete(0, len(start_input.get()))
    end_input.delete(0, len(end_input.get()))
    ticket_print.delete(0, END)
    #ticket_select.delete(0, END)  #리스트 박스일 때 문자 삭제
    #ticket_select.configure(text="")  #라벨일 때 문자 삭제
    ticket_select.delete("1.0", "end")  # 텍스트일 때 문자 삭제
    login_button['state'] = 'normal'

def Click_Go_Date(event):
    global go_calendar
    global go_day
    global go_day2
    global go_day3
    global go_month
    days = ["월", "화", "수", "목", "금", "토", "일"]
    go_day = days[go_calendar.get_date().weekday()]  #요일(월,화)
    #print(go_day)
    go_day2 = int(go_calendar.get_date().weekday())  #요일 순서(0,1)
    #print(go_day2)
    a = str(go_calendar.get_date())  #선택한 달 + 1
    go_month = int(a[5:7]) + 1
    #print(go_month)
    go_day3 = str(go_calendar.get_date())

def Click_Come_Date(event):
    global come_calendar
    global come_day
    global come_day2
    global come_day3
    global come_month
    days = ["월", "화", "수", "목", "금", "토", "일"]
    come_day = days[come_calendar.get_date().weekday()]  #요일
    #print(come_day)
    come_day2 = int(come_calendar.get_date().weekday())
    #print(come_day2)
    a = str(come_calendar.get_date())
    come_month = int(a[5:7]) + 1
    #print(come_month)
    come_day3 = str(come_calendar.get_date())

def Input_Start():
    global start_input
    global end_input
    global ticket
    global ticket_print
    global go_day
    global go_day2
    global go_month
    global come_day
    global come_day2
    global come_month
    #global ticket_print2
    ticket_select.delete("1.0", "end")
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    # 혹은 options.add_argument("--disable-gpu")

    driver = webdriver.Chrome('chromedriver', options=options)

    driver.get('https://m-flight.naver.com/')
    driver.implicitly_wait(3)
    # driver = webdriver.Chrome()
    # driver.get("https://m-flight.naver.com/")
    time.sleep(1)
    # 광고 삭제
    a = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[9]/div/div[2]/button[1]').click()

    # 출발지 선택
    start1_click = driver.find_element(By.CLASS_NAME, value="tabContent_route__1GI8F.select_City__2NOOZ.start").click()
    start2_click = driver.find_element(By.CLASS_NAME, value="autocomplete_input__1vVkF").click()
    search = True
    while search:
        # departure_place = input("출발지 입력 : ")
        driver.find_element(By.CSS_SELECTOR, "#__next > div > div.container.as_main > div.autocomplete_autocomplete__ZEwU_.is_departure > div.autocomplete_header__1NSMD > div > input").click()
        time.sleep(1)
        try:
            driver.find_element(By.CSS_SELECTOR, "#__next > div > div.container.as_main > div.autocomplete_autocomplete__ZEwU_.is_departure > div.autocomplete_header__1NSMD > div > input").send_keys(
                start_input.get())
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "#__next > div > div.container.as_main > div.autocomplete_autocomplete__ZEwU_.is_departure > div.autocomplete_content__3RhAZ > section > div > a").click()
            time.sleep(1)
            search = False

        except Exception as e:
            #print("출발지", e)
            tkinter.messagebox.showinfo("검색 에러", "존재하지 않는 공항 검색")
            print("존재하지 않는 공항 검색")
            time.sleep(0.5)
            driver.quit()

            #driver.find_element(By.CSS_SELECTOR, "#__next > div > div.container.as_main > div.autocomplete_autocomplete__ZEwU_.is_departure > div.autocomplete_header__1NSMD > div > input").clear()

    # 도착지 선택
    end1_click = driver.find_element(By.CLASS_NAME, value="tabContent_route__1GI8F.select_City__2NOOZ.end").click()
    end2_click = driver.find_element(By.CLASS_NAME, value="autocomplete_input__1vVkF").click()
    search = True
    while search:
        #destination_place = input("도착지 입력 : ")
        driver.find_element(By.CSS_SELECTOR,
                            "#__next > div > div.container.as_main > div.autocomplete_autocomplete__ZEwU_.autocomplete_is_arrival__JR22W > div.autocomplete_header__1NSMD > div > input").click()
        time.sleep(1)
        try:
            driver.find_element(By.CSS_SELECTOR,
                                "#__next > div > div.container.as_main > div.autocomplete_autocomplete__ZEwU_.autocomplete_is_arrival__JR22W > div.autocomplete_header__1NSMD > div > input").send_keys(
                end_input.get())
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR,
                                "#__next > div > div.container.as_main > div.autocomplete_autocomplete__ZEwU_.autocomplete_is_arrival__JR22W > div.autocomplete_content__3RhAZ > section > div > a").click()
            time.sleep(1)
            search = False


        except Exception as e:
            #print("도착지", e)
            tkinter.messagebox.showinfo("검색 에러", "존재하지 않는 공항 검색")
            print("존재하지 않는 공항 검색")
            time.sleep(0.5)
            driver.quit()
            # driver.find_element(By.CSS_SELECTOR,
            #                     "#__next > div > div.container.as_main > div.autocomplete_autocomplete__ZEwU_.autocomplete_is_arrival__JR22W > div.autocomplete_header__1NSMD > div > input").clear()

    # #날짜 선택
    driver.find_element(By.XPATH,
                                 '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[2]/button[1]').click()
    time.sleep(1)
    try:
        print("0")
        # 가는 날
        if go_day == "월":
            print("1")
            driver.find_element(By.CSS_SELECTOR,
                                f"#__next > div > div.container.as_main > div.container_SearchModalContainer__2wVab > div.container_content__2w_MI.container_as_calendar__17CQb > div.calendar_calendar__2OzxE > div.calendar_content__1Xc5a > div > div:nth-child({go_month}) > table > tbody > tr:nth-child(2) > td:nth-child({go_day2 + 2}) > button").click()
            time.sleep(1)

        elif go_day == "화":
            print("1-1")
            driver.find_element(By.CSS_SELECTOR,
                                f"#__next > div > div.container.as_main > div.container_SearchModalContainer__2wVab > div.container_content__2w_MI.container_as_calendar__17CQb > div.calendar_calendar__2OzxE > div.calendar_content__1Xc5a > div > div:nth-child({go_month}) > table > tbody > tr:nth-child(2) > td:nth-child({go_day2 + 2}) > button").click()
            time.sleep(1)

        elif go_day == "수":
            print("1-2")
            driver.find_element(By.CSS_SELECTOR,
                                f"#__next > div > div.container.as_main > div.container_SearchModalContainer__2wVab > div.container_content__2w_MI.container_as_calendar__17CQb > div.calendar_calendar__2OzxE > div.calendar_content__1Xc5a > div > div:nth-child({go_month}) > table > tbody > tr:nth-child(2) > td:nth-child({go_day2 + 2}) > button").click()
            time.sleep(1)

        elif go_day == "목":
            print("1-3")
            driver.find_element(By.CSS_SELECTOR,
                                f"#__next > div > div.container.as_main > div.container_SearchModalContainer__2wVab > div.container_content__2w_MI.container_as_calendar__17CQb > div.calendar_calendar__2OzxE > div.calendar_content__1Xc5a > div > div:nth-child({go_month}) > table > tbody > tr:nth-child(2) > td:nth-child({go_day2 + 2}) > button").click()
            time.sleep(1)

        elif go_day == "금":
            print("1-4")
            driver.find_element(By.CSS_SELECTOR,
                                f"#__next > div > div.container.as_main > div.container_SearchModalContainer__2wVab > div.container_content__2w_MI.container_as_calendar__17CQb > div.calendar_calendar__2OzxE > div.calendar_content__1Xc5a > div > div:nth-child({go_month}) > table > tbody > tr:nth-child(2) > td:nth-child({go_day2 + 2}) > button").click()
            time.sleep(1)

        elif go_day == "토":
            print("2")
            driver.find_element(By.CSS_SELECTOR,
                                f"#__next > div > div.container.as_main > div.container_SearchModalContainer__2wVab > div.container_content__2w_MI.container_as_calendar__17CQb > div.calendar_calendar__2OzxE > div.calendar_content__1Xc5a > div > div:nth-child({go_month}) > table > tbody > tr:nth-child(2) > td.day.saturday > button").click()
            time.sleep(1)

        elif go_day == "일":
            print("3")
            driver.find_element(By.CSS_SELECTOR,
                                f"#__next > div > div.container.as_main > div.container_SearchModalContainer__2wVab > div.container_content__2w_MI.container_as_calendar__17CQb > div.calendar_calendar__2OzxE > div.calendar_content__1Xc5a > div > div:nth-child({go_month}) > table > tbody > tr:nth-child(2) > td.day.sunday > button").click()
            time.sleep(2)

    except Exception as e:
        # print("가는 날짜 오류", e)
        # tkinter.messagebox.showinfo("검색 에러", "날짜 입력 오류")
        # driver.quit()
        driver.find_element(By.CSS_SELECTOR,
                            "#__next > div > div.container.as_main > div.container_SearchModalContainer__2wVab > div.container_content__2w_MI.container_as_calendar__17CQb > div.calendar_calendar__2OzxE > div.calendar_content__1Xc5a > div > div:nth-child(3) > table > tbody > tr:nth-child(2) > td:nth-child(2) > button").click()
        time.sleep(1)
    try:
        #오는 날
        print("4")
        if come_day == "월":
            print("5")
            driver.find_element(By.CSS_SELECTOR,
                                f"#__next > div > div.container.as_main > div.container_SearchModalContainer__2wVab > div.container_content__2w_MI.container_as_calendar__17CQb > div.calendar_calendar__2OzxE > div.calendar_content__1Xc5a > div > div:nth-child({come_month}) > table > tbody > tr:nth-child(3) > td:nth-child({come_day2 + 2}) > button").click()
            time.sleep(1)

        elif come_day == "화":
            print("5-1")
            driver.find_element(By.CSS_SELECTOR,
                                f"#__next > div > div.container.as_main > div.container_SearchModalContainer__2wVab > div.container_content__2w_MI.container_as_calendar__17CQb > div.calendar_calendar__2OzxE > div.calendar_content__1Xc5a > div > div:nth-child({come_month}) > table > tbody > tr:nth-child(3) > td:nth-child({come_day2 + 2}) > button").click()
            time.sleep(1)

        elif come_day == "수":
            print("5-2")
            driver.find_element(By.CSS_SELECTOR,
                                f"#__next > div > div.container.as_main > div.container_SearchModalContainer__2wVab > div.container_content__2w_MI.container_as_calendar__17CQb > div.calendar_calendar__2OzxE > div.calendar_content__1Xc5a > div > div:nth-child({come_month}) > table > tbody > tr:nth-child(3) > td:nth-child({come_day2 + 2}) > button").click()
            time.sleep(1)

        elif come_day == "목":
            print("5-3")
            driver.find_element(By.CSS_SELECTOR,
                                f"#__next > div > div.container.as_main > div.container_SearchModalContainer__2wVab > div.container_content__2w_MI.container_as_calendar__17CQb > div.calendar_calendar__2OzxE > div.calendar_content__1Xc5a > div > div:nth-child({come_month}) > table > tbody > tr:nth-child(3) > td:nth-child({come_day2 + 2}) > button").click()
            time.sleep(1)

        elif come_day == "금":
            print("5-4")
            driver.find_element(By.CSS_SELECTOR,
                                f"#__next > div > div.container.as_main > div.container_SearchModalContainer__2wVab > div.container_content__2w_MI.container_as_calendar__17CQb > div.calendar_calendar__2OzxE > div.calendar_content__1Xc5a > div > div:nth-child({come_month}) > table > tbody > tr:nth-child(3) > td:nth-child({come_day2 + 2}) > button").click()
            time.sleep(1)

        elif come_day == "토":
            print("6")
            driver.find_element(By.CSS_SELECTOR,
                                f"#__next > div > div.container.as_main > div.container_SearchModalContainer__2wVab > div.container_content__2w_MI.container_as_calendar__17CQb > div.calendar_calendar__2OzxE > div.calendar_content__1Xc5a > div > div:nth-child({come_month}) > table > tbody > tr:nth-child(3) > td.day.saturday > button").click()
            time.sleep(1)
        elif come_day == "일":
            print("7")
            driver.find_element(By.CSS_SELECTOR,
                                f"#__next > div > div.container.as_main > div.container_SearchModalContainer__2wVab > div.container_content__2w_MI.container_as_calendar__17CQb > div.calendar_calendar__2OzxE > div.calendar_content__1Xc5a > div > div:nth-child({come_month}) > table > tbody > tr:nth-child(3) > td.day.sunday > button").click()
            time.sleep(1)

        time.sleep(2)

    except Exception as e:
        #print("오는 날짜 오류", e)
        # tkinter.messagebox.showinfo("검색 에러", "날짜 입력 오류")
        # driver.quit()
        driver.find_element(By.CSS_SELECTOR,
                            "#__next > div > div.container.as_main > div.container_SearchModalContainer__2wVab > div.container_content__2w_MI.container_as_calendar__17CQb > div.calendar_calendar__2OzxE > div.calendar_content__1Xc5a > div > div:nth-child(3) > table > tbody > tr:nth-child(2) > td:nth-child(5) > button").click()
        time.sleep(1)

    # 직항만 선택
    direct_flight_click = driver.find_element(By.CLASS_NAME,
                                              value="tabContent_option__2y4c6.tabContent_as_direct__3JbBj.select_Direct__3y5a6").click()
    time.sleep(1)

    # 항공권 검색
    search_click = driver.find_element(By.CLASS_NAME, value="searchBox_search__2KFn3").click()
    time.sleep(9)
    try:
        # for i in ticket_print2.get_children():  ##treeview 값 지우기
        #     ticket_print2.delete(i)
        ticket_print.delete(0, END)
        all_ticket = driver.find_elements(By.CLASS_NAME, value="concurrent_ConcurrentItemContainer__2lQVG.result")
        if 0 < len(all_ticket) < 10:
            for i in range(0, len(all_ticket)):
                ticket = all_ticket[i].text.split('\n')
                #print(ticket)
                ticket_print.insert(i, ticket)

        elif len(all_ticket) >= 10:
            for i in range(10):
                ticket = all_ticket[i].text.split("\n")
                #print(ticket)
                ticket_print.insert(i, ticket)  # listbox로 출력하는 방법
            #a = [s for s in ticket if "항공" or "에어" in s]
            # if len(ticket) == 12:  #가는 비행기/오는 비행기 다르고 가는 날/오는 날 비행 도중 날짜가 바뀌는 경우
            #     ticket_print2.insert('', 'end', text=str(i), values=ticket)
            #
            # elif len(ticket) == 11:
            #     if len(a) == 2:  #가는 비행기/오는 비행기 다르고 가는 날/오는 날 비행 도중 하루만 날짜가 바뀌는 경우
            #         if ticket[3] == '+1일':  # 가는 날 날짜 바뀌는 경우
            #             ticket.insert(8, '-')
            #             ticket_print2.insert('', 'end', text=str(i), values=ticket)
            #         else:  # 오는 날 날짜 바뀌는 경우
            #             ticket.insert(3, '-')
            #             ticket_print2.insert('', 'end', text=str(i), values=ticket)
            #
            #     else:  #가는 비행기/오는 비행기 같고 가는 날/오늘 날 비행 도중 날짜가 바뀌는 경우
            #         ticket.insert(8, '1')
            #         ticket_print2.insert('', 'end', text=str(i), values=ticket)
            #
            # elif len(ticket) == 10:
            #     if len(a) == 1:  #비행기 같고 날짜 변동 있는 경우
            #         ticket.insert(5, '1')
            #         if ticket[3] == '+1일':  # 가는 날 날짜 바뀌는 경우
            #             ticket.insert(8, '2')
            #             ticket_print2.insert('', 'end', text=str(i), values=ticket)
            #         else:  # 오는 날 날짜 바뀌는 경우
            #             ticket.insert(3, '3')
            #             ticket_print2.insert('', 'end', text=str(i), values=ticket)
            #     else:  #비행기 다르고 날짜 변동 하루만 있는 경우
            #         if ticket[3] == '+1일':  # 가는 날 날짜 바뀌는 경우
            #             ticket.insert(8, '4')
            #             ticket_print2.insert('', 'end', text=str(i), values=ticket)
            #         else:  # 오는 날 날짜 바뀌는 경우
            #             ticket.insert(3, '5')
            #             ticket_print2.insert('', 'end', text=str(i), values=ticket)
            #
            # elif len(ticket) == 9:
            #     ticket.insert(3, '-')
            #     ticket.insert(5, '-')
            #     ticket.insert(8, '-')
            #     ticket_print2.insert('', 'end', text=str(i), values=ticket)
            # else:
            #     print("이상한 길이")
            #     pass
        elif len(all_ticket) == 0:
            tkinter.messagebox.showinfo("", "해당 날짜에는 항공편이 존재하지 않습니다.")

    except Exception as e:
        #print(e)
        print("항공편이 존재하지 않습니다.")
        tkinter.messagebox.showinfo("", "해당 날짜에는 항공편이 존재하지 않습니다.")
    driver.quit()

def Ticket_select(event):
    global ticket_print
    global ticket_select
    global get_item
    #ticket_select.delete(0, END)  #리스트박스일 때 문자 삭제
    ticket_select.delete("1.0","end")  #텍스트일 때 문자 삭제
    select_item = ticket_print.curselection()
    #ticket_select.insert(0, ticket_print.get(select_item, END))
    get_item = ticket_print.get(select_item)
    get_item = list(get_item)
    for i in get_item:
        # print(i)
        ticket_select.insert(END, f'{i}\n')

def Basket():
    global get_item
    global basket
    global start_input
    global end_input
    global go_calendar
    global come_calendar
    get_item.append(start_input.get())
    get_item.append(end_input.get())
    get_item.append(go_day3)
    get_item.append(come_day3)
    basket.clear()
    basket.append(get_item)
    print(basket)
    client_socket.sendall(bytes('passenger_basket'.encode('utf-8')))
    time.sleep(1)
    basket_dict = json.dumps({
        "passenger_id" : id_input.get(),
        "passenger_basket" : basket
    }).encode('utf-8')
    client_socket.sendall(bytes(basket_dict))

def Show_Basket():
    global id_input
    show_basket_Frame.pack(side='left', fill='both', expand=True)
    basket_exit_button.place(x=905, y=20)
    basket_list.place(x=20, y=300)
    basket_reset.place(x=840, y=250, width=50, height=40)
    basket_select.place(x=20, y=560)
    ticket_buy.place(x=820, y=480)
    basket_cancel.place(x=700, y=480)
    basket_list.delete(0, END)

def Basket_Reset():
    global id_input
    client_socket.sendall(bytes('basket'.encode('utf-8')))
    time.sleep(1)
    basket_list.delete(0, END)
    basket_data = json.loads(client_socket.recv(16184))  # 장바구니 리스트
    # print(basket)
    for i in basket_data:
        if i[1] == id_input.get():
            basket_list.insert(END, i[2:])

    if basket_list.size() == 0:
        tkinter.messagebox.showinfo("", "장바구니가 비어있습니다.")

def Show_Basket_Exit():
    global show_basket_Frame
    global basket_list
    global show_basket_Frame
    global ticket_buy
    global basket_list
    basket_select.delete("1.0","end")
    show_basket_Frame.pack_forget()
    ticket_buy.pack_forget()
    basket_list.pack_forget()
    basket_reset.pack_forget()
    basket_list.delete(0, END)

def Basket_Select(event):
    global basket_item
    basket_select.delete("1.0","end")  #텍스트일 때 문자 삭제
    select_item = basket_list.curselection()
    #ticket_select.insert(0, ticket_print.get(select_item, END))
    basket_item = basket_list.get(select_item)
    basket_item = list(basket_item)
    basket_select.insert(END, f'{basket_item[0]}\n')

def Buy():
    global basket_item
    client_socket.sendall(bytes('ticket_buy'.encode('utf-8')))
    time.sleep(1)
    basket_dict = json.dumps({
        "passenger_id" : id_input.get(),
        "buy" : basket_item
    }).encode('utf-8')
    client_socket.sendall(bytes(basket_dict))

def Basket_Cancel():
    global basket_item
    client_socket.sendall(bytes('basket_cancel'.encode('utf-8')))
    time.sleep(1)
    basket_dict = json.dumps({
        "passenger_id" : id_input.get(),
        "basket_cancel" : basket_item
    }).encode('utf-8')
    client_socket.sendall(bytes(basket_dict))

def Family_Click(event):
    global recomm_text
    recomm_text.delete("1.0", "end")
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome('chromedriver', options=options)

    driver.get('https://m-flight.naver.com/')
    driver.implicitly_wait(3)
    time.sleep(1)
    # 광고 삭제
    a = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[9]/div/div[2]/button[1]').click()
    time.sleep(0.1)
    driver.find_element(By.CSS_SELECTOR, "#__next > div > div.container.as_main > div.Theme_Theme__1oIj3 > div > ul > li:nth-child(1) > a > figure > img").click()
    time.sleep(1)
    recomm_theme = driver.find_elements(By.CLASS_NAME, value="list_RecommendItem__1zEzC")
    time.sleep(1)
    for i in range(0, len(recomm_theme)):
        recomm_text.insert(END, str(recomm_theme[i].text.split('\n'))[1:-1]+'\n')

    driver.quit()


def Golf_Click(event):
    global recomm_text
    recomm_text.delete("1.0", "end")
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome('chromedriver', options=options)

    driver.get('https://m-flight.naver.com/')
    driver.implicitly_wait(3)
    time.sleep(1)
    # 광고 삭제
    a = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[9]/div/div[2]/button[1]').click()
    time.sleep(0.1)
    driver.find_element(By.CSS_SELECTOR,
                        "#__next > div > div.container.as_main > div.Theme_Theme__1oIj3 > div > ul > li:nth-child(2) > a > figure > img").click()
    time.sleep(1)
    recomm_theme = driver.find_elements(By.CLASS_NAME, value="list_RecommendItem__1zEzC")
    time.sleep(1)
    for i in range(0, len(recomm_theme)):
        recomm_text.insert(END, str(recomm_theme[i].text.split('\n'))[1:-1] + '\n')

    driver.quit()

def Couple_Click(event):
    global recomm_text
    recomm_text.delete("1.0", "end")
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome('chromedriver', options=options)

    driver.get('https://m-flight.naver.com/')
    driver.implicitly_wait(3)
    time.sleep(1)
    # 광고 삭제
    a = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[9]/div/div[2]/button[1]').click()
    time.sleep(0.1)
    driver.find_element(By.CSS_SELECTOR,
                        "#__next > div > div.container.as_main > div.Theme_Theme__1oIj3 > div > ul > li:nth-child(3) > a > figure > img").click()
    time.sleep(1)
    recomm_theme = driver.find_elements(By.CLASS_NAME, value="list_RecommendItem__1zEzC")
    time.sleep(1)
    for i in range(0, len(recomm_theme)):
        recomm_text.insert(END, str(recomm_theme[i].text.split('\n'))[1:-1] + '\n')

    driver.quit()

def Culture_Click(event):
    global recomm_text
    recomm_text.delete("1.0", "end")
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome('chromedriver', options=options)

    driver.get('https://m-flight.naver.com/')
    driver.implicitly_wait(3)
    time.sleep(1)
    # 광고 삭제
    a = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[9]/div/div[2]/button[1]').click()
    time.sleep(0.1)
    driver.find_element(By.CSS_SELECTOR,
                        "#__next > div > div.container.as_main > div.Theme_Theme__1oIj3 > div > ul > li:nth-child(10) > a > figure > img").click()
    time.sleep(1)
    recomm_theme = driver.find_elements(By.CLASS_NAME, value="list_RecommendItem__1zEzC")
    time.sleep(1)
    for i in range(0, len(recomm_theme)):
        recomm_text.insert(END, str(recomm_theme[i].text.split('\n'))[1:-1] + '\n')

    driver.quit()

def Vacation_Click(event):
    global recomm_text
    recomm_text.delete("1.0", "end")
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome('chromedriver', options=options)

    driver.get('https://m-flight.naver.com/')
    driver.implicitly_wait(3)
    time.sleep(1)
    # 광고 삭제
    a = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[9]/div/div[2]/button[1]').click()
    time.sleep(0.1)
    driver.find_element(By.CSS_SELECTOR,
                        "#__next > div > div.container.as_main > div.Theme_Theme__1oIj3 > div > ul > li:nth-child(5) > a > figure > img").click()
    time.sleep(1)
    recomm_theme = driver.find_elements(By.CLASS_NAME, value="list_RecommendItem__1zEzC")
    time.sleep(1)
    for i in range(0, len(recomm_theme)):
        recomm_text.insert(END, str(recomm_theme[i].text.split('\n'))[1:-1] + '\n')

    driver.quit()


def Go_Reset():
    global today_time
    go_calendar.set_date(today_time)

def Come_Reset():
    global today_time
    come_calendar.set_date(today_time)

def Cursor_In(event):
    make_id.configure(fg='blue')
    main_button.configure(fg='blue')

def Cursor_Out(evevt):
    make_id.configure(fg="black")
    main_button.configure(fg='black')


window = Tk()
window.geometry('1000x900')
window.title('KCY_flight')

window.configure(bg='azure')
window.resizable(False, False)

fontExample = tkFont.Font(family="돋움", size=12, weight="bold")

#메인화면
main_Frame = Frame(window, relief='solid', bd=2, bg='azure')
main_Frame.pack(side='left', fill='both', expand=True)
main_button = Button(main_Frame, text="로그인", width=12, height=4, bg='azure', command=Main_Open)
main_button.configure(font=fontExample, borderwidth=0)
main_button.bind('<Enter>', Cursor_In)
main_button.bind('<Leave>', Cursor_Out)
main_button.place(x=850, y=15)

#테마별 여행 추천
family_png = PhotoImage(file='family.png')
family = Label(main_Frame, image=family_png)
family.bind('<Button-1>', Family_Click)
family_label = Label(main_Frame, text='#가족 여행', bg='azure')
family.place(x=20, y=70)
family_label.place(x=20, y=90)

golf_png = PhotoImage(file='golf.png')
golf = Label(main_Frame, image=golf_png)
golf.bind('<Button-1>', Golf_Click)
golf_label = Label(main_Frame, text='#골프 여행', bg='azure')
golf.place(x=20, y=220)
golf_label.place(x=20, y=240)

couple_png = PhotoImage(file='couple.png')
couple = Label(main_Frame, image=couple_png)
couple.bind('<Button-1>', Couple_Click)
couple_label = Label(main_Frame, text='#커플 여행', bg='azure')
couple.place(x=20, y=370)
couple_label.place(x=20, y=390)

vacation_png = PhotoImage(file='vacation.png')
vacation = Label(main_Frame, image=vacation_png)
vacation.bind('<Button-1>', Vacation_Click)
vacation_label = Label(main_Frame, text="#휴양지", bg='azure')
vacation.place(x=20, y=520)
vacation_label.place(x=20, y=540)

culture_png = PhotoImage(file='culture.png')
culture = Label(main_Frame, image=culture_png)
culture.bind('<Button-1>', Culture_Click)
culture_lable = Label(main_Frame, text='#성지순례', bg='azure')
culture.place(x=20, y=670)
culture_lable.place(x=20, y=690)

recomm = Label(main_Frame, text='<테마별 추천 여행지>', bg='azure', width=20, font=fontExample)
recomm.place(x=20, y=20)
recomm_text = Text(main_Frame, bg="azure", width=55, height=35, font=("돋움", 15))
recomm_text.place(x=300, y=120)

#로그인/회원가입 프레임
main_Frame2 = Frame(main_Frame, relief='solid', bd=2, bg='azure')

#로그인 - 아이디 입력
id_input = Entry(main_Frame2, bg='white', font=22)
# id_input.place(width=300, height=40, x=360, y=450)

#로그인 - 비밀번호 입력
password_input = Entry(main_Frame2, bg='white', font=22, show="*")
# password_input.place(width=300, height=40, x=360, y=530)

#로그인 버튼
login_button = Button(main_Frame2, text='로그인', command=Login, width=12, height=7, bg='LightSteelBlue3')
login_button.configure(font=fontExample, borderwidth=0)
# login_button.place(x=700, y=450)

#회원가입 버튼
make_id = Button(main_Frame2, text='회원 가입', command=Sign_Member, width=12, height=2, bg='azure')
make_id.configure(font=fontExample, borderwidth=0)
# make_id.place(x=700, y=595)
make_id.bind('<Enter>', Cursor_In)
make_id.bind('<Leave>', Cursor_Out)

#로그인 프레임
login_Frame = Frame(main_Frame2, relief='solid', bd=2, background='azure')
login_exit_button = Button(login_Frame, text='X', font=20, command=Login_Exit, width=4, height=2, bg='steel blue')
login_exit_button.configure(font=fontExample, borderwidth=0)

#회원가입 프레임
sign_Frame = Frame(main_Frame2, relief='solid', bd=2,background='azure')

#회원가입 버튼
sign_button = Button(sign_Frame, text='가입', command=Sign, bg='antiquewhite', width=10, height=3)
sign_button.configure(font=fontExample, borderwidth=0)


#회원가입 나가기 버튼
sign_exit_button = Button(sign_Frame, text='X', font=20, command=Sign_Exit, width=4, height=2, bg='steel blue')
sign_exit_button.configure(font=fontExample, borderwidth=0)

#회원가입 - 아이디
sign_id_label = Label(sign_Frame, text="아이디", background='azure', font=12)
sign_id_label.place(x=160, y=170)

sign_id_input = Entry(sign_Frame, bg='white', font=22)
sign_id_input.place(width=300, height=40, x=250, y=170)

#회원가입 - 비밀번호
sign_pw_label = Label(sign_Frame, text="비밀번호", background='azure', font=12)
sign_pw_label.place(x=160, y=250)

sign_password_input = Entry(sign_Frame, bg='white', font=22)
sign_password_input.place(width=300, height=40, x=250, y=250)


#회원가입 - 한글이름
sign_name1_label = Label(sign_Frame, text="한글 이름",background='azure', font=12)
sign_name1_label.place(x=160, y=330)

sign_name1_input = Entry(sign_Frame, bg='white', font=22)
sign_name1_input.place(width=300, height=40, x=250, y=330)

#회원가입 - 영어이름
sign_name2_label = Label(sign_Frame, text="영어 이름",background='azure', font=12)
sign_name2_label.place(x=160, y=410)

sign_name2_input = Entry(sign_Frame, bg='white', font=22)
sign_name2_input.place(width=300, height=40, x=250, y=410)

#회원가입 -성별
sign_gender_label = Label(sign_Frame, text="성별",background='azure', font=12)
sign_gender_label.place(x=160, y=490)

sign_gender_input = ttk.Combobox(sign_Frame, font=22)
gender_list = ["F", "M"]
sign_gender_input.configure(state="readonly", values=gender_list)
sign_gender_input.place(width=300, height=40, x=250, y=490)

#회원가입 - 생년월일
sign_birth_label = Label(sign_Frame, text="생년월일",background='azure', font=12)
sign_birth_label.place(x=160, y=570)

sign_birth_input = Entry(sign_Frame, bg='white', font=22)
sign_birth_input.place(width=300, height=40, x=250, y=570)

#회원가입 - 이메일
sign_email_label = Label(sign_Frame, text="e-mail",background='azure', font=12)
sign_email_label.place(x=160, y=650)

sign_email_input = Entry(sign_Frame, bg='white', font=22)
sign_email_input.place(width=300, height=40, x=250, y=650)

#회원가입 - 여권번호
sign_passport_label = Label(sign_Frame, text="여권번호",background='azure', font=12)
sign_passport_label.place(x=160, y=730)

sign_passport_input = Entry(sign_Frame, bg='white', font=22)
sign_passport_input.place(width=300, height=40, x=250, y=730)

#항공권 출발지 입력
start_label = Label(login_Frame, text="출발지 입력", font=22)
start_input = Entry(login_Frame, bg='white', font=23)

#항공권 도착지 입력
end_label = Label(login_Frame, text="도착지 입력", font=22)
end_input = Entry(login_Frame, bg='white', font=23, width=20)

#가는 날 입력
go_label = Label(login_Frame, text="가는 날", font=22)
go_reset = Button(login_Frame, text="®", font=("돋움", 18), command=Go_Reset)
#<가는 날 달력>
go_calendar = DateEntry(login_Frame, dateformat=3, width=12, background='LightBlue1', font=20,
                    foreground='black', borderwidth=4, Calendar=2023, state="readonly", showweeknumbers=False,
                    firstweekday='sunday', date_pattern='y-mm-dd')
go_calendar.grid(row=1, column=3, sticky='nsew')
go_calendar.bind('<ButtonRelease-1>', Click_Go_Date)

#오는 날 입력
come_label = Label(login_Frame, text="오는 날", font=22)
come_reset = Button(login_Frame, text="®", font=("돋움", 18), command=Come_Reset)
#<오는 날 달력>
come_calendar = DateEntry(login_Frame, dateformat=3, width=12, background='LightBlue1', font=20,
                    foreground='black', borderwidth=4, Calendar=2023, state="readonly", showweeknumbers=False,
                    firstweekday='sunday', date_pattern='y-mm-dd')
come_calendar.grid(row=1, column=3, sticky='nsew')
come_calendar.bind('<ButtonRelease-1>', Click_Come_Date)

#달력
#calendar = Calendar(login_Frame, selectmode="day", year=today_time.year, month=today_time.month, day=today_time.day)

#항공권 검색
ticket_search = Button(login_Frame, text="search", command=Input_Start, font=("돋움", 16))

#<listbox>
#검색한 항공권 출력
ticket_print = Listbox(login_Frame, font=20, selectmode='single', width=120, height=10)
ticket_print.bind('<ButtonRelease-1>', Ticket_select)

#항공권 출력
ticket_select = Text(login_Frame, bg="SkyBlue1", width=35, height=11, font=("돋움", 19))
ticket_basket = Button(login_Frame, text="장바구니 담기", font=20, command=Basket)
#ticket_select = Listbox(login_Frame, font=27, width=100, height=5)

#장바구니 보기
show_basket_button = Button(login_Frame, text="장바구니 보기", font=20, command=Show_Basket)

#장바구니 프레임
show_basket_Frame = Frame(login_Frame, relief='solid', bd=2, background='azure')

#장바구니 나가기
basket_exit_button = Button(show_basket_Frame, text='X', font=20, command=Show_Basket_Exit, width=4, height=2, bg='steel blue')
basket_exit_button.configure(font=fontExample, borderwidth=0)

#장바구니에 담은 리스트
basket_list = Listbox(show_basket_Frame, font=20, selectmode='single', width=110, height=10)
basket_list.bind('<ButtonRelease-1>', Basket_Select)
basket_reset = Button(show_basket_Frame, text="®", font=("돋움", 19), command=Basket_Reset)

#장바구니에 담긴 리스트 출력
basket_select = Text(show_basket_Frame, bg="SkyBlue1", width=35, height=11, font=("돋움", 19))
ticket_buy = Button(show_basket_Frame, text="구매하기", font=20, command=Buy)

#장바구니에 담긴 리스트 삭제
basket_cancel = Button(show_basket_Frame, text="삭제하기", font=20, command=Basket_Cancel)


#<treeview>
# ticket_print2 = ttk.Treeview(login_Frame, height=15, columns=["1", "2", "3", '4', '5', '6', '7', '8', '9', '10', '11', '12'],
#                           displaycolumns=["1", "2", "3", '4', '5', '6', '7', '8', '9', '10', '11', '12'])
# ticket_print2.column("#0", width=0, anchor="center")
# ticket_print2.heading("#0", text="비고")
#
# ticket_print2.column("#1", width=95, anchor="center")
# ticket_print2.heading("1", text='항공사명', anchor="center")
#
# ticket_print2.column("#2", width=95, anchor="center")
# ticket_print2.heading("2", text="가는 날 출발시간/장소", anchor="center")
#
# ticket_print2.column("#3", width=95, anchor="center")
# ticket_print2.heading("3", text="가는 날 도착시간/장소", anchor="center")
#
# ticket_print2.column("#4", width=70, anchor="center")
# ticket_print2.heading("4", text="날짜변동", anchor="center")
#
# ticket_print2.column("#5", width=95, anchor="center")
# ticket_print2.heading("5", text="비행시간", anchor="center")
#
# ticket_print2.column("#6", width=95, anchor="center")
# ticket_print2.heading("6", text="항공사명", anchor="center")
#
# ticket_print2.column("#7", width=95, anchor="center")
# ticket_print2.heading("7", text="오늘 날 출발시간/장소", anchor="center")
#
# ticket_print2.column("#8", width=95, anchor="center")
# ticket_print2.heading("8", text="오늘 날 도착시간/장소", anchor="center")
#
# ticket_print2.column("#9", width=70, anchor="center")
# ticket_print2.heading("9", text="날짜변동", anchor="center")
#
# ticket_print2.column("#10", width=95, anchor="center")
# ticket_print2.heading("10", text="비행시간", anchor="center")
#
# ticket_print2.column("#11", width=95, anchor="center")
# ticket_print2.heading("11", text="카드실적", anchor="center")
#
# ticket_print2.column("#12", width=95, anchor="center")
# ticket_print2.heading("12", text="가격", anchor="center")





window.mainloop()
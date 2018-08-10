#!/usr/bin/python3

import splinter
import time
import datetime
import random


def login(b, username, password):   # 登录账号
    b.click_link_by_text(u"登录")
    b.fill("username", username)
    b.fill("password", password)
    b.click_link_by_id("subButton")
    print("{}登录成功:{}".format(username+"\n",
                             time.strftime("%H:%M:%S", time.localtime(time.time()))))


def select_submit(b, choice):
    selected = b.find_by_xpath("//*[@class=\"datelist\"]/li["+choice+"]")

    if not selected.has_class("selected"):
        selected.click()

    if b.is_element_present_by_text("确认预订"):
        b.click_link_by_id("btn_submit")  # click"确认预订"
    elif b.is_element_present_by_text("已订完"):
        print("已订完，明天再试吧！")
    else:
        print("unknown situation")
        b.reload()
        select_submit(b, choice)


def loop_popup(b, choice):  # 循环点击
    try:
        if b.is_element_present_by_id("popup_ok", 20):  # wait for popup window
            b.click_link_by_id("popup_ok")  # click"确认"
            if b.is_element_present_by_id("popup_message", 10):
                pop_msg = b.find_by_id("popup_message").text  # 获取popup message
                print(pop_msg+" "+time.strftime("%H:%M:%S", time.localtime(time.time())))
            if "当前时间不可预定" in pop_msg or len(pop_msg) > 100:
                b.click_link_by_id("popup_ok")
                select_submit(b, choice)
                loop_popup(b, choice)
            elif "预订已满" in pop_msg:
                print("别瞎忙活了，票没了")
            else:
                b.click_link_by_id("popup_ok")
                print("已预订成功，请等待短信通知^_^")
                b.reload()
                select_submit(b, choice)
                loop_popup(b, choice)
        else:
            print("no response, try again")
            b.reload()
            select_submit(b, choice)
            loop_popup(b, choice)

    except splinter.exceptions.ElementDoesNotExist as e:
        b.reload()
        loop_popup(b, choice)
        print(e)


def run(user, password, choice="2", head=False):
    # init time
    today = time.localtime(time.time())
    year = today.tm_year
    mon = today.tm_mon
    day = today.tm_mday
    # start/end time
    start_time = datetime.datetime(year, mon, day, 7, 0, 0, random.randint(0, 5))
    end_time = datetime.datetime(year, mon, day, 7, 1, 0, 0)
    halt_time = datetime.datetime(year, mon, day, 7, 2, 0)

    # account info
    user = user
    password = password
    print("今天抢星期", today.tm_wday + int(choice), "的票")

    # init browser
    b = splinter.Browser(driver_name="chrome", headless=head)

    # visit url & login
    b.visit("http://www.wentiyun.cn/venue-722.html")
    login(b, user, password)
    select_submit(b, choice)

    # start snatching
    while True:
        now = datetime.datetime.now()
        if start_time < now < end_time:
            print("start snatching...")
            print(now)
            # b.reload()
            loop_popup(b, choice)
        elif now > halt_time:
            print(now)
            print("The End")
            break


if __name__ == "__main__":
    run("13812345678", "password")

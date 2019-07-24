import splinter
import time
import datetime
import random
import logging
from splinter.driver.webdriver.chrome import WebDriver
from selenium.webdriver.chrome.options import Options

success_flag = False


# create logger
logger_name = "snatchTikcet"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)


def logHandler(username):
    # create file handler
    log_path = "./{}_log.log".format(username)
    fh = logging.FileHandler(log_path, encoding='UTF-8')
    fh.setLevel(logging.INFO)

    # create formatter
    fmt = "%(asctime)-15s %(levelname)s %(filename)s line#:%(lineno)d %(message)s"
    datefmt = "%a %d %b %Y %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt)

    # add handler and formatter to logger
    fh.setFormatter(formatter)
    logger.addHandler(fh)


def login(b, username, password):   # 登录账号
    b.click_link_by_text(u"登录")
    b.fill("username", username)
    b.fill("password", password)
    b.click_link_by_id("subButton")
    logger.info("{}登录成功".format(username))


def select_submit(b, choice):

    try:     
        selected = b.find_by_xpath("//*[@class=\"datelist\"]/li["+choice+"]")
        if selected:
            selected.click()
            if not selected.has_class("selected"):
                selected.click()
        else:
            b.reload()
            select_submit(b, choice)

    except Exception as e:
        logger.error(e)
        b.reload()
        select_submit(b, choice)

def re_start(b, choice, url, user, password):
    b.visit(url)
    select_submit(b, choice)
    main_process(b, choice, url, user, password)

def main_process(b, choice, url, user, password):  # 循环点击
    try:
        global success_flag

        if b.is_element_present_by_text("已订完"):
            logger.warn("已订完，明天再试吧！")
        elif b.is_element_present_by_xpath("*[@class=\"error_box\"]"):
            re_start(b, choice, url, user, password)

        elif b.find_by_xpath("//*[@id=\"btn_submit\"]/..").first.visible:
            logger.info('click submit button')
            b.click_link_by_id("btn_submit")  # click"确认预订"

            # wait for popup window
            if b.is_element_present_by_id("popup_ok", 20):
                logger.info('click confirm button')
                b.click_link_by_id("popup_ok")  # click"确认"

                pop_msg = ""

                if b.is_element_present_by_id("popup_message", 40):
                    pop_msg = b.find_by_id(
                        "popup_message").text  # 获取popup message
                    logger.info(pop_msg + "\n")

                if "成功" in pop_msg:
                    logger.info('click ok button')
                    b.click_link_by_id("popup_ok")
                    logger.warn("已预订成功，请等待短信通知^_^")
                    success_flag = True

                elif "当前时间不可预定" in pop_msg or len(pop_msg) > 100:
                    logger.info('click outtime button')
                    b.click_link_by_id("popup_ok")
                    re_start(b, choice, url, user, password)

                elif "已" in pop_msg:  # "预订已满", "您已预定当前场次"
                    logger.warn("别瞎忙活了，票没了")
                    success_flag = True

                elif "登录" in pop_msg:
                    login(b, user, password)
                    re_start(b, choice, url, user, password)

                else:
                    logger.error(pop_msg + "\nline66：unknow situation")
                    re_start(b, choice, url, user, password)

            else:
                logger.info("无响应，重新加载")
                re_start(b, choice, url, user, password)

        elif b.url != url:
            re_start(b, choice, url, user, password)

        else:
            logger.error("网站崩溃了")
            re_start(b, choice, url, user, password)

    except Exception as e:
        logger.error(e)
        re_start(b, choice, url, user, password)


def run(user, password, url="http://www.wentiyun.cn/venue-722.html",
        choice="1", headless=False):

    # init logger
    logHandler(user)

    # init time
    today = time.localtime(time.time())
    year = today.tm_year
    mon = today.tm_mon
    day = today.tm_mday

    interval = random.randint(0, 5)

    # start/end time
    start_time = datetime.datetime(year, mon, day, 7, 0, 0, interval)
    end_time = datetime.datetime(year, mon, day, 7, 5, 0, 0)

    # purpose
    logger.info("今天抢星期{}的票".format(today.tm_wday + int(choice) + 1))

    # init browser
    # webdriver= splinter.Browser.webdriver
    # options = webdriver.ChromeOptions()
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--ignore-ssl-errors')
    # driver = webdriver.Chrome(chrome_options=options)
    custom_options = Options()
    custom_options.add_argument('--ignore-certificate-errors')
    custom_options.add_argument('--ignore-ssl-errors')

    b = splinter.Browser(driver_name="chrome",user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
                         headless=headless, options=custom_options)

    # visit url & login
    b.visit(url)
    login(b, user, password)
    select_submit(b, choice)

    # start snatching
    while True:
        now = datetime.datetime.now()
        if start_time < now < end_time and not success_flag:
            logger.info("开始抢票咯...")
            main_process(b, choice, url, user, password)
        elif now > end_time or success_flag:
            # logger.info("抢票结束")
            # main_process(b, choice, url, user, password)
            logger.info("=========抢完了=========") if success_flag else logger.info(
                "=========超时未抢到=========")
            b.quit()
            break


if __name__ == "__main__":
    run("user", "password")

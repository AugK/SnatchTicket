import splinter
import time
import datetime
# import random
import logging
# from splinter.driver.webdriver.chrome import WebDriver
from selenium.webdriver.chrome.options import Options
from functools import wraps
import requests
import json


def timeDecor(func):
    """This is a decorator of time count"""

    @wraps(func)
    def innerDef(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        t = t2 - t1
        # print("func {0} cost : {1:.1}s".format(str(func.__name__), t))
        logger.info("func {0} cost : {1:.1f}s".format(str(func.__name__), t))
        return result

    return innerDef


class snatchTikcet(object):
    """
    user: user name, **required**, str
    pwd: password, **required**, str
    choice: default tomorrow, str
    headless: browser option default False, bool
    url: url, str
    browser: splinter browser instance
    selected: choose the date, splinter elelment list
    """

    def __init__(self, user, pwd, choice='1', headless=False, url='http://www.wentiyun.cn/venue-722.html'):
        self.user = user
        self.pwd = pwd
        self.choice = choice
        self.headless = headless
        self.url = url
        self.browser = None
        self.selected = None
        self.submit_msg = ''

    # init browser
    @timeDecor
    def initBrowser(self):
        custom_options = Options()
        custom_options.add_argument('--ignore-certificate-errors')
        custom_options.add_argument('--ignore-ssl-errors')

        self.browser = splinter.Browser(driver_name="chrome", user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
                                        headless=self.headless, options=custom_options)

    @timeDecor
    def visitUrl(self):
        try:
            self.browser.visit(self.url)
        except Exception as ep:
            print(ep)

    @timeDecor
    def login(self):   # 登录账号
        try:
            self.browser.click_link_by_text(u"登录")
            self.browser.fill("username", self.user)
            self.browser.fill("password", self.pwd)
            self.browser.click_link_by_id("subButton")
        except Exception as e:
            print(e)
            # self.browser.reload()
            # login()
        else:
            logger.info("{}登录成功".format(self.user))

    @timeDecor
    def select_submit(self):  # todo: 第一次打开网页才需要点两下？
        try:
            self.selected = self.browser.find_by_xpath(
                "//*[@class=\"datelist\"]/li["+self.choice+"]")
            if self.selected:
                self.selected.click()
                if not self.selected.has_class("selected"):
                    self.selected.click()
            else:
                self.browser.reload()
                self.select_submit()

        except Exception as e:
            logger.error(e)
            self.browser.reload()
            self.select_submit()

    def re_start(self):
        self.browser.visit(self.url)
        self.select_submit()
        self.main_process()

    # @timeDecor
    def wait4popup(self, elementId, cnt=0):
        flag = True if self.browser.is_element_present_by_id(
            elementId, 5) else False
        # flag = True if self.browser.is_element_present_by_id("popup_ok", 5) else False
        while cnt < 12:
            if flag:
                cnt = 99
                break
            else:
                self.wait4popup(elementId, cnt=cnt + 1)
        return flag

    # @timeDecor
    def main_process(self):  # 循环点击
        try:
            global success_flag

            if self.browser.find_by_xpath("//*[@id=\"btn_submit\"]/..").first.visible:
                logger.info('click submit button')
                self.browser.click_link_by_id("btn_submit")  # click"确认预订"'

                # wait for popup window
                # if self.wait4popup(elementId='popup_ok'):
                if self.browser.is_element_present_by_id("popup_ok", 20):
                    pop_msg = ""
                    logger.info('click confirm button')
                    self.browser.click_link_by_id("popup_ok")  # click"确认"

                    # if self.wait4popup(elementId='popup_message'):
                    if self.browser.is_element_present_by_id("popup_message", 40):
                        # if self.browser.is_element_present_by_id("popup_message", 40):
                        pop_msg = self.browser.find_by_id(
                            "popup_message").text  # 获取popup message
                        logger.info(pop_msg + "\n")

                    if "成功" in pop_msg or "您已预定当前场次" in pop_msg:
                        logger.info('click ok button')
                        self.browser.click_link_by_id("popup_ok")
                        logger.warn("已预订成功，请等待短信通知^_^")
                        success_flag = True

                    if "当前时间不可预定" in pop_msg or len(pop_msg) > 100:
                        logger.info('pop_msg')
                        self.browser.click_link_by_id("popup_ok")
                        self.re_start()

                    # elif "您已预定当前场次" in pop_msg:  # "预订已满", "您已预定当前场次"
                    #     logger.warn("别瞎忙活了，票没了")
                        # success_flag = True

                    elif "登录" in pop_msg:
                        logger.info(pop_msg)
                        self.login()
                        self.re_start()
                    elif "请勿重复提交订单！" in pop_msg:
                        logger.info(pop_msg)
                        self.select_submit()
                        self.main_process()
                    else:
                        logger.error(pop_msg + "\nline66：unknow situation")
                        self.re_start()

                else:
                    logger.info("无响应，重新加载")
                    self.re_start()
            elif self.browser.is_element_present_by_text("已订完"):
                logger.warn("已订完，明天再试吧！")
            else:
                # self.re_start()
                print('else')
        except Exception as e:
            logger.error(e)
            self.re_start()

    def main_test(self):
        self.post_request()
        if '重复' in self.submit_msg:
            self.browser.visit(self.url)
            self.select_submit()
            self.post_request()
        else:
            pass

    def post_request(self):
        try:
            cookies = self.browser.cookies.all()
            templist = []
            for k, v in cookies.items():
                templist.append(str(k)+'='+str(v))
            cookies = ';'.join(templist)
            logger.info(cookies)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
                'Cookie': cookies,
                'Origin': 'http://www.wentiyun.cn',
                'Referer': 'http://www.wentiyun.cn/venue-722.html'
            }
            venueId = 722

            # query_str = 'http://www.wentiyun.cn/venue-sku.html?venueId=' + \
            #     str(venueId)+'&date=' + '-'.join([str(i) for i in [year,mon,day]])
            query_str = 'http://www.wentiyun.cn/venue-sku.html?venueId={}&date={}'.format(
                str(venueId), '-'.join([str(i) for i in [year, mon, day+1]]))
            logger.info(query_str)

            request_id = requests.get(query_str)
            # temp = request_id.content.decode()
            # temp = json.loads(temp)
            # print(temp)
            # print(type(temp))
            skuId = json.loads(request_id.text)[
                'skuData']['9-11点30,默认泳池']['id']
            # logger.info(skuId)

            confirmData = {
                'skuId': skuId
            }
            request_confrim = requests.post(
                'http://www.wentiyun.cn/venue-order-confirm.html', headers=headers, data=confirmData)

            skuOrder = request_confrim.content.decode()
            skuOrder = json.loads(skuOrder)
            logger.info(request_confrim.status_code)
            logger.info(request_confrim.text)

            submitData = {
                'skuId': skuId,
                'venueId': venueId,
                'skuOrder': skuOrder
            }

            request_submit = requests.post(
                'http://www.wentiyun.cn/venue-order-submit.html', headers=headers, data=submitData)

            logger.info(request_submit.status_code)
            logger.info(request_submit.text)
            self.submit_msg = json.loads(request_submit.text)['desc']

        except Exception as e:
            logger.error(e)


success_flag = False

# create logger
logger_name = "snatchTikcet"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)

# init time
today = time.localtime(time.time())
year = today.tm_year
mon = today.tm_mon
day = today.tm_mday


def logHandler(username):
    # create file handler
    log_path = "./{}.log".format(username)
    fh = logging.FileHandler(log_path, encoding='UTF-8')
    fh.setLevel(logging.INFO)

    # create formatter
    fmt = "%(asctime)-15s %(levelname)s %(filename)s line#:%(lineno)d %(message)s"
    datefmt = "%a %d %b %Y %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt)

    # add handler and formatter to logger
    fh.setFormatter(formatter)
    logger.addHandler(fh)


def run(user, password):

    # init logger
    logHandler(user)

    # interval = random.randint(0, 5)

    # start/end time
    start_time = datetime.datetime(year, mon, day, 7, 0, 0, 0)
    end_time = datetime.datetime(year, mon, day, 7, 15, 0, 0)

    tk = snatchTikcet(user, password)

    # purpose
    logger.info("今天抢星期{}的票".format(today.tm_wday + int(tk.choice) + 1))

    # visit url & login
    tk.initBrowser()
    tk.visitUrl()
    tk.login()
    tk.select_submit()

    # start snatching
    while True:
        now = datetime.datetime.now()
        if start_time < now < end_time and not success_flag:
            logger.info("开始抢票咯...")
            tk.main_process()
            # for i in range(20):
            #     tk.post_request()
        elif now > end_time or success_flag:
            # logger.info("抢票结束")
            # main_process(b, choice, url, user, password)
            # tk.main_process()
            # tk.post_request()
            logger.info("=========抢完了=========") if success_flag else logger.info(
                "=========超时未抢到=========")
            tk.browser.quit()
            break


if __name__ == "__main__":
    run("username", "password")

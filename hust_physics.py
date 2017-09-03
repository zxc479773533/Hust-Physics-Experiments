import sys
from bs4 import BeautifulSoup
from selenium import webdriver
import time

browser = webdriver.PhantomJS(executable_path="phantomjs")
browser.maximize_window()

def getPhysicsExperimentInfo(name, passwd, first, end):
    Week = ['周一','周二','周三','周四','周五','周六','周日']
    Day = ['上午','#','下午','晚上']
    browser.get("http://115.156.233.249/login.asp")
    time.sleep(0.5)

    try:
        browser.find_element_by_name('xsxh')
        t1 = True
    except:
        t1 = False

    if t1 == True:

        browser.find_element_by_name('xsxh').clear()
        browser.find_element_by_name('xsxh').send_keys(name)
        browser.find_element_by_name('mm').clear()
        browser.find_element_by_name('mm').send_keys(passwd)
        browser.find_element_by_name('Login').click()
        time.sleep(0.3)

    browser.get('http://115.156.233.249/yuyue.asp')
    time.sleep(0.3)

    try:
        browser.find_element_by_name('ExperimentSelectCtrl')
        t2 = True
    except:
        t2 = False

    if t2 == True:

        page = browser.page_source
        html = BeautifulSoup(page,'lxml')
        data = html.select('option')
        experiment = {}

        for option in data:
            experiment[option.get('value')] = option.get_text()

        for value in experiment:
            browser.find_element_by_name('ExperimentSelectCtrl').find_element_by_xpath("//option[@value=" + value + "]").click()
            print(experiment[value] + ":\n")

            for i in range(first, end + 1):
                print("第" + str(i) + "周:")
                browser.find_element_by_name('zc').clear()
                browser.find_element_by_name('zc').send_keys(i)
                browser.find_element_by_name('search').click()
                time.sleep(0.3)
                page = browser.page_source
                html = BeautifulSoup(page,'lxml')
                positions = html.find_all(width="20", bgcolor="#ffffff")
                for i in range(0, 7):
                    print(Week[i])
                    for j in {0, 2, 3}:
                        count = 0
                        for k in range(1, 89, 2):
                            try:
                                name = positions[28 * k + 4 * i + j].find('input').name
                                count += 1
                            except:
                                continue
                        if count != 0:
                            print(Day[j], end='')
                            print(":" + str(count), end=' ')
                    print('')
            print('')


if __name__ == '__main__':
    try:
        getPhysicsExperimentInfo(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    except:
        print("\n使用说明：四个命令行参数，用户名，密码，开始周，结束周")
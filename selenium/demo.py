# selenium driver http://chromedriver.storage.googleapis.com/index.html?path=91.0.4472.101/
# https://www.cnblogs.com/rwxwsblog/p/10499749.html
from selenium import webdriver
import time

timeout = 120
url = 'https://passport.bilibili.com/login?from_spm_id=333.851.top_bar.login'
browser = webdriver.Chrome()
browser.get(url)
while True:
    is_loggin = False
    print(browser.title)
    try:
        print(browser.find_element_by_xpath("//div[@class='unlogin-avatar']"))
    except Exception as e:
        is_loggin = True
        pass
    timeout -= 1
    if is_loggin or timeout == 0:
        break
    time.sleep(1)

cookies =  browser.get_cookies()
print(cookies)


browser.close()
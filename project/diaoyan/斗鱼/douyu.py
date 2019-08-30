import time

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# 斗鱼登陆url
url = 'https://www.douyu.com/'
login_url = 'https://passport.douyu.com/index/login'
driver = Chrome()

# 设置浏览器窗口最大化
driver.maximize_window()
# 响应等待时间
wait = WebDriverWait(driver, 5)
# 点击分类页面按钮
driver.get('https://www.douyu.com/g_LOL')
time.sleep(20)
cookies = {'dy_did': '204e141f7e5b363c784385e700011501',
           'smidV2': '201908070922061fb47b26251f7a8e61a42d40ea27e79100042b36c130eb260',
           'Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7': '1565140927',
           'PHPSESSID': 'apgocu06186d05vpkf7vt537t7',
           'acf_auth': 'ac58ovwDmkvvuiWbqOBTI0yoAvVTcuqVRqnSxyrYtIDuGfnqx%2BAQ5y2SMsKQey4o8x%2B3t%2FT2YZ4yChoT%2BKWQFf%2FZcSh73FxjBP3gh9yP%2FxlSOmwuO5mWEBY',
           'wan_auth37wan': 'd6377c161fa3bYSfkPDscVkl1JmLHiYRO6MWaXcmvjUcNA%2FBxTL%2Bwp4kdVSAxl8jZtAaY2DFV4MKr%2FUfbfiuz%2BPoTaJXIc45PysBFir0tSFlQ022mzQ',
           'acf_uid': '319941945',
           'acf_username': '319941945',
           'acf_nickname': '%E7%94%A8%E6%88%B795597792',
           'acf_own_room': '0',
           'acf_groupid': '1',
           'acf_phonestatus': '1',
           'acf_avatar': 'https%3A%2F%2Fapic.douyucdn.cn%2Fupload%2Favatar%2Fdefault%2F09_',
           'acf_ct': '0',
           'acf_ltkid': '63933152',
           'acf_biz': '1',
           'acf_stk': '5b8daedc8b29dd43',
           'acf_did': '204e141f7e5b363c784385e700011501',
           'acf_ccn': 'ae39d9ee80bf546ca3006b5121942d63',
           'Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7': '1565141508',
           }
driver.add_cookie(cookie_dict=cookies)
driver.get('https://www.douyu.com/g_LOL')
# 点击进入页面内第一个主播房间
b4_switch = wait.until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="listAll"]/div[2]/ul/li[1]/div/a[1]')))
b4_switch.click()
time.sleep(10)

# 输入弹幕
barrage = input('请输入弹幕：')  # 模拟输入弹幕
barrage_input = wait.until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="js-player-asideMain"]/div/div[2]/div/div[2]/div[2]/textarea')))
barrage_input.clear()
barrage_input.send_keys(barrage)
# 点击发送弹幕
b5_switch = wait.until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="js-player-asideMain"]/div/div[2]/div/div[2]/div[2]/div[3]')))
b5_switch.click()

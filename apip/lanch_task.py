import time, random, traceback, logging, os, json
from appium import webdriver
from selenium.webdriver.common.by import By

from util.BaseOperate import BaseOperate

desired_caps = {}
desired_caps['platformName'] = 'Android'  # 系统名称
# desired_caps['platformVersion'] = '8.0.0'  # 系统的版本号
# desired_caps['deviceName'] = '34882369'  # 设备名称，这里是虚拟机，这个没有严格的规定
desired_caps['platformVersion'] = '6.0'  # 系统的版本号
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['automationName'] = 'uiautomator2'
desired_caps['appPackage'] = 'com.sankuai.meituan.takeoutnew'  # APP包名
desired_caps['appActivity'] = 'com.sankuai.meituan.takeoutnew.ui.page.boot.WelcomeActivity'  # APP入口的activity
desired_caps["noReset"] = True
desired_caps['unicodeKeyboard'] = True  # 编码,可解决中文输入问题
desired_caps['resetKeyboard'] = True
desired_caps['noSign'] = True
desired_caps['newCommandTimeout'] = "200000"

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
base_operate = BaseOperate(driver)


class MeiTuanTask:

    Cache = []
    app_state = True
    def start_item_task(self, exists_memch):
        groups = driver.find_elements_by_id("com.sankuai.meituan.takeoutnew:id/parent")
        find_new = False
        if len(groups) <= 2:
            return find_new
        for i in range(1, len(groups)-1):
            group = groups[i]
            try:
                if not base_operate.isElement("id", "com.sankuai.meituan.takeoutnew:id/textview_poi_name"):
                    continue
                text_view = group.find_element_by_id("com.sankuai.meituan.takeoutnew:id/textview_poi_name")
                memchant_name = text_view.get_attribute('text')
                if memchant_name in exists_memch:
                    continue
                find_new = True
                print("开始处理 " + memchant_name)
                text_view.click()
                exists_memch.append(memchant_name)
                if True:
                    time.sleep(random.uniform(0.12, 0.18))
                    # 联系商家
                    base_operate.wait_element(10, By.ID, "com.sankuai.meituan.takeoutnew:id/img_shop_cart_im_txt", "联系商家按钮未找到")
                    element = driver.find_element_by_id("com.sankuai.meituan.takeoutnew:id/img_shop_cart_im_txt")
                    element.click()
                    # 发送
                    time.sleep(random.uniform(1.12, 1.18))
                    edit_txt = base_operate.isElement("class", "android.widget.EditText")
                    if not edit_txt:
                        print("跳过")
                        exists_memch.append(memchant_name)
                        break
                    # base_operate.wait_element(60, By.CLASS_NAME, "android.widget.EditText", "发送消息窗口未找到")
                    driver.find_element_by_class_name("android.widget.EditText").send_keys("你好，你们家公司团体订餐有优惠吗？可以的话加我们经理VX详聊，微信号: backtonb")
                    driver.find_element_by_class_name("android.widget.Button").click()
            except Exception as e:
                pass
            finally:
                back_count = 1
                while True:
                    if not base_operate.isElement("id", "com.sankuai.meituan.takeoutnew:id/parent"):
                        if back_count > 19:
                            self.app_state = False
                            break
                        base_operate.back()
                        back_count = back_count + 1
                        print("后退")
                    else:
                        break
                    print("backCount:" + str(back_count))
        return find_new

    def startSendMsgTask(self):
        try:
            print("collected")
            time.sleep(random.uniform(5, 8))
            ad_exist = base_operate.isElement("id", "com.sankuai.meituan.takeoutnew:id/close")
            if ad_exist:
                ads = driver.find_element_by_id("com.sankuai.meituan.takeoutnew:id/close")
                ads.click()
            base_operate.swipeUp(100)
            # base_operate.wait_element(60, By.ID, "com.sankuai.meituan.takeoutnew:id/parent", "商家列表页未找到")
            # groups = driver.find_elements_by_class_name("android.view.ViewGroup")
            # 每次处理一个商家，下拉370 ，保存到已处理列表
            while True:
                if not base_operate.isElement("id", "com.sankuai.meituan.takeoutnew:id/parent"):
                    base_operate.swipeLessUp()
                    print("首次启动向上滑动")
                else:
                    break
            up_count = 1
            while True:
                is_task_new = self.start_item_task(self.Cache)
                if not self.app_state:
                    self.app_state = True
                    # 启动APP
                    base_operate.lanch_app()
                    time.sleep(10)
                    self.startSendMsgTask()
                if not is_task_new:
                    print("未找到新任务，向上滑动，upCount：" + str(up_count))
                    # 滑动以找到新任务
                    if up_count > (len(self.Cache) // 4):
                        base_operate.lanch_app()
                        self.startSendMsgTask()
                    base_operate.swipeLess2Up()

                    up_count = up_count + 1
                    # self.find_new_group(exits_memch)
                else:
                    up_count = 1
                    print("已发送商家数:{},详情:{}".format(len(self.Cache), self.Cache))
                self.flush_cache_file()
        except Exception as err:
            print("程序异常")
            traceback.print_exc()
            pass
        finally:
            self.startSendMsgTask()

    def load_cache_from_file(self, file='cache'):
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                file = f.read()
            print(file)
            self.Cache = json.loads(file)

    def flush_cache_file(self, file='cache'):
        json_str = json.dumps(self.Cache)
        cache_file = open(file, 'w', encoding='utf-8')
        cache_file.write(json_str)
        cache_file.close()




if __name__ == '__main__':
    task = MeiTuanTask()
    task.load_cache_from_file()
    curTime = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
    print(curTime)
    if curTime > "2019-11-25 15-13-13":
        print("错误的运行")
    else:
        task.startSendMsgTask()

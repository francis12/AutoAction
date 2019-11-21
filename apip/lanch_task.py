import time, random, traceback, logging
from appium import webdriver
from selenium.webdriver.common.by import By

from util.BaseOperate import BaseOperate

desired_caps = {}
desired_caps['platformName'] = 'Android'  # 系统名称
desired_caps['platformVersion'] = '8.0.0'  # 系统的版本号
desired_caps['deviceName'] = '34882369'  # 设备名称，这里是虚拟机，这个没有严格的规定
# desired_caps['platformVersion'] = '5.1.1'  # 系统的版本号
# desired_caps['deviceName'] = '127.0.0.1:62001'
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
                    # time.sleep(random.uniform(0.2, 0.5))
                    # 联系商家
                    base_operate.wait_element(10, By.ID, "com.sankuai.meituan.takeoutnew:id/img_shop_cart_im_txt", "联系商家按钮未找到")
                    element = driver.find_element_by_id("com.sankuai.meituan.takeoutnew:id/img_shop_cart_im_txt")
                    element.click()
                    # 发送
                    #time.sleep(random.uniform(0.02, 0.18))
                    edit_txt = base_operate.isElement("class", "android.widget.EditText")
                    if not edit_txt:
                        print("跳过")
                        exists_memch.append(memchant_name)
                        break
                    # base_operate.wait_element(60, By.CLASS_NAME, "android.widget.EditText", "发送消息窗口未找到")
                    driver.find_element_by_class_name("android.widget.EditText").send_keys(memchant_name + " 你好,消息由机器人发送，勿回复打扰见谅！")
                    driver.find_element_by_class_name("android.widget.Button").click()
            except Exception as e:
                pass
            finally:
                while True:
                    if not base_operate.isElement("id", "com.sankuai.meituan.takeoutnew:id/parent"):
                        base_operate.back()
                        print("后退")
                    else:
                        break
        return find_new

    def startSendMsgTask(self):
        print("collected")
        time.sleep(random.uniform(0.5, 1.5))
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
        exits_memch = []
        while True:
            is_task_new = self.start_item_task(exits_memch)
            if not is_task_new:
                print("未找到新任务，向上滑动")
                # 滑动以找到新任务
                base_operate.swipeLess2Up()
                # self.find_new_group(exits_memch)
            else:
                print("已发送商家数:{},详情:{}".format(len(exits_memch), exits_memch))

    # def find_new_group(self, exits_memch):
    #     is_found = False
    #     first_run = True
    #     while first_run or is_found:
    #         first_run = False
    #         base_operate.swipeLessUp()
    #         time.sleep(random.uniform(0.5, 1.5))
    #         groups = driver.find_elements_by_id("com.sankuai.meituan.takeoutnew:id/parent")
    #         for group in groups:
    #             try:
    #                 print("displayed:{},enabled:{}".format(group.is_displayed(), group.is_enabled()))
    #                 text_view = group.find_element_by_id("com.sankuai.meituan.takeoutnew:id/textview_poi_name")
    #                 memchant_name = text_view.get_attribute('text')
    #                 if memchant_name in exits_memch:
    #                     continue
    #                 else:
    #                     is_found = True
    #                     break
    #             except Exception as err:
    #                 traceback.print_exc()
    #                 print("err find new group")



if __name__ == '__main__':
    task = MeiTuanTask()
    task.startSendMsgTask()

import random
import time
import traceback

from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By

from util.BaseOperate import BaseOperate
from util.cache_util import CacheUtil


class DouYinScript:

    def __init__(self, driver=None):
        self.driver = driver
        self.base_operate = BaseOperate(driver)


    def startSendMsgTask(self):
        print("startSendMsgTask")
        time.sleep(3)
        ad_exist = self.base_operate.isElement("id", "com.ss.android.ugc.aweme:id/edq")
        if ad_exist:
            ads = self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/edq")
            ads.click()
        ad_exist = self.base_operate.isElement("id", "com.ss.android.ugc.aweme:id/t3")
        if ad_exist:
            ads = self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/t3")
            ads.click()

        while True:
            cur_pkg = self.driver.current_package
            if cur_pkg != 'com.ss.android.ugc.aweme':
                print(cur_pkg)
                print("抖音app不在运行")
                raise Exception("应用未知闪退，重启应用")
            # 点击留言
            pl = self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/zd")
            pl.click()
            first_run = True
            while True:
                try:
                    start = 0 if first_run else 1
                    first_run = False
                    self.send_msg_group(start)
                    CacheUtil.flush_cache_file("douyin")
                    print("滑动取下一组留言")
                    self.base_operate.swipeLess2Up()
                except Exception as err:
                    traceback.print_exc()
                    print("处理当前抖音出错")
                    break
                finally:
                    pass
            #关闭当前留言
            print("click close button")
            self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/kr").click()
            print("滑动取下一个视频")
            #取下一个视频
            self.base_operate.swipeUp()

    def send_msg_group(self, start=0):
        comments = self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/cx2").find_elements_by_class_name(
            "android.widget.FrameLayout")
        for i in range(start, len(comments) - 1):
            comment = comments[i]
            resource_id = comment.get_attribute("resourceId")
            if resource_id is None:
                # 展开回复
                pass
            elif resource_id == "com.ss.android.ugc.aweme:id/a32" or resource_id == "com.ss.android.ugc.aweme:id/bmw":
                # 主回复
                if not self.base_operate.isElement(By.ID, "com.ss.android.ugc.aweme:id/title"):
                    continue
                title = comment.find_element_by_id("com.ss.android.ugc.aweme:id/title")
                name = title.get_attribute("text")
                if "douyin" in CacheUtil.Cache and name in CacheUtil.Cache["douyin"]:
                    continue
                a2g = comment.find_element_by_id("com.ss.android.ugc.aweme:id/a2g")
                msg = a2g.get_attribute("text")
                print(name + " : " + msg)
                self.send_msg_item(a2g)
                print(name + "已完成回复")
                if "douyin" in CacheUtil.Cache:
                    CacheUtil.Cache["douyin"].append(name)
                else:
                    CacheUtil.Cache["douyin"] = [name]
                time.sleep(random.uniform(0.32, 0.58))


    def send_msg_item(self, element):
        TouchAction(self.driver).long_press(element).perform()
        self.driver.find_element_by_android_uiautomator("new UiSelector().text(\"私信回复\")").click()
        self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/aey").send_keys("不错")
        # 发送
        self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/db_").click()
        time.sleep(1)

    def add_cache(self):
        CacheUtil.Cache.append("11111")
        CacheUtil.flush_cache_file()


if __name__ == '__main__':
    pass

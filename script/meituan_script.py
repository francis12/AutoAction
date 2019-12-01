import random
import time
import traceback

from selenium.webdriver.common.by import By

from util.BaseOperate import BaseOperate
from util.cache_util import CacheUtil


class MeiTuanScript:

    def __init__(self, driver=None):
        self.driver = driver
        self.base_operate = BaseOperate(driver)

    def process_groups(self):
        groups = self.driver.find_elements_by_id("com.sankuai.meituan.takeoutnew:id/parent")
        if len(groups) <= 2:
            return
        for i in range(1, len(groups) - 1):
            group = groups[i]
            if not self.base_operate.isElement("id", "com.sankuai.meituan.takeoutnew:id/textview_poi_name"):
                continue
            try:
                text_view = group.find_element_by_id("com.sankuai.meituan.takeoutnew:id/textview_poi_name")
                memchant_name = text_view.get_attribute('text')
                if memchant_name in CacheUtil.Cache:
                    print("历史已处理 " + memchant_name)
                    continue
                print("开始处理 " + memchant_name)
                text_view.click()
                CacheUtil.Cache.append(memchant_name)
                if True:
                    time.sleep(random.uniform(1.12, 1.18))
                    # 联系商家
                    self.base_operate.wait_element(10, By.ID, "com.sankuai.meituan.takeoutnew:id/img_shop_cart_im_txt",
                                                   "联系商家按钮未找到")
                    element = self.driver.find_element_by_id("com.sankuai.meituan.takeoutnew:id/img_shop_cart_im_txt")
                    element.click()
                    # 发送
                    time.sleep(random.uniform(1.12, 1.18))
                    edit_txt = self.base_operate.isElement("class", "android.widget.EditText")
                    if not edit_txt:
                        print("跳过")
                        break
                    self.driver.find_element_by_class_name("android.widget.EditText").send_keys(
                        "你好")
                    self.driver.find_element_by_class_name("android.widget.Button").click()
                    time.sleep(random.uniform(0.52, 0.68))
                    self.driver.find_element_by_class_name("android.widget.EditText").send_keys(
                        "你们家公司团体订餐有优惠吗")
                    self.driver.find_element_by_class_name("android.widget.Button").click()
                    time.sleep(random.uniform(0.52, 0.68))
                    self.driver.find_element_by_class_name("android.widget.EditText").send_keys(
                        "17701611617")
                    self.driver.find_element_by_class_name("android.widget.Button").click()
                    time.sleep(random.uniform(0.52, 0.68))
                    self.driver.find_element_by_class_name("android.widget.EditText").send_keys(
                        "+我V,X详聊")
                    self.driver.find_element_by_class_name("android.widget.Button").click()
                    time.sleep(random.uniform(0.52, 0.68))
            except Exception as e:
                print("处理发送消息出错")
                traceback.print_exc()
                pass
            finally:
                back_count = 1
                while True:
                    if not self.base_operate.isElement("id", "com.sankuai.meituan.takeoutnew:id/parent"):
                        if back_count > 20:
                            raise Exception("back_count gt 20")
                        self.base_operate.back()
                        back_count = back_count + 1
                        print("后退" + str(back_count))
                    else:
                        break

    def startSendMsgTask(self):
        print("startSendMsgTask")
        time.sleep(10)
        ad_exist = self.base_operate.isElement("id", "com.sankuai.meituan.takeoutnew:id/close")
        if ad_exist:
            ads = self.driver.find_element_by_id("com.sankuai.meituan.takeoutnew:id/close")
            ads.click()
        self.base_operate.swipeUp(100)
        while True:
            if not self.base_operate.isElement("id", "com.sankuai.meituan.takeoutnew:id/parent"):
                self.base_operate.swipeLessUp()
                print("首次启动向上滑动")
            else:
                break
        while True:
            cur_pkg = self.driver.current_package
            if cur_pkg != 'com.sankuai.meituan.takeoutnew':
                print(cur_pkg)
                print("美团app不在运行")
                raise Exception("应用未知闪退，重启应用")
            self.process_groups()
            print("已发送商家数:{}".format(len(CacheUtil.Cache)))
            CacheUtil.flush_cache_file()
            # 滑动到下一页
            self.base_operate.swipeLess2Up()

    def add_cache(self):
        CacheUtil.Cache.append("11111")
        CacheUtil.flush_cache_file()


if __name__ == '__main__':
    pass

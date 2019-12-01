import traceback, time
from appium import webdriver
from script.meituan_script import MeiTuanScript
from script.douyin_script import DouYinScript
from util.cache_util import CacheUtil


class Trigger:

    def init_driver(self, attrs=None):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'  # 系统名称
        # desired_caps['platformVersion'] = '8.0.0'  # 系统的版本号
        # desired_caps['deviceName'] = '34882369'  # 设备名称，这里是虚拟机，这个没有严格的规定
        # desired_caps['platformVersion'] = '6.0'  # 系统的版本号
        # desired_caps['deviceName'] = '127.0.0.1:7555'
        desired_caps['platformVersion'] = attrs['platformVersion']  # 系统的版本号
        desired_caps['deviceName'] = attrs['deviceName']
        desired_caps['automationName'] = 'uiautomator2'
        desired_caps['appPackage'] = attrs['appPackage']  # APP包名
        desired_caps['appActivity'] = attrs['appActivity']  # APP入口的activity
        desired_caps["noReset"] = True
        desired_caps['unicodeKeyboard'] = True  # 编码,可解决中文输入问题
        desired_caps['resetKeyboard'] = True
        desired_caps['noSign'] = True
        desired_caps['newCommandTimeout'] = "200000"
        driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        return driver

    def trigger_douyin(self):
        attrs = {}
        # attrs['platformVersion'] = '5.1'
        # attrs['deviceName'] = '850ABM4QELHQ'
        # attrs['platformVersion'] = '8.0.0'
        # attrs['deviceName'] = '192.168.1.2:5555'
        attrs['platformVersion'] = '6.0'
        attrs['deviceName'] = '127.0.0.1:7555'
        attrs['appPackage'] = 'com.ss.android.ugc.aweme'
        attrs['appActivity'] = '.main.MainActivity'
        driver = self.init_driver(attrs)
        try:
            CacheUtil.load_cache_from_file("douyin")
            script = DouYinScript(driver)
            script.startSendMsgTask()
        except Exception as err:
            traceback.print_exc()
        finally:
            print("重启应用")
            driver.start_activity(attrs['appPackage'], attrs['appActivity'])
            time.sleep(18)
            self.trigger_douyin()
        print("end")

     # def trigger_meituan_waimai(self):
     #    attrs = {}
     #    attrs['platformVersion'] = '8.0.0'
     #    attrs['deviceName'] = '192.168.1.2:5555'
     #    attrs['appPackage'] = 'com.sankuai.meituan.takeoutnew'
     #    attrs['appActivity'] = 'com.sankuai.meituan.takeoutnew.ui.page.boot.WelcomeActivit'
     #    driver = self.init_driver(attrs)
     #    script = MeiTuanScript(driver)
     #    while True:
     #        print("currentpkg:{}, act: {},cxt:{}".format(driver.current_package, driver.current_activity,
     #                                                     driver.current_context))
     #        time.sleep(5)

        # try:
        #     CacheUtil.load_cache_from_file()
        #     print("缓存商家{}： {}".format(len(CacheUtil.Cache), CacheUtil.Cache))
        #     script.startSendMsgTask()
        # except Exception as err:
        #     traceback.print_exc()
        # finally:
        #     print("重启应用")
        #     driver.start_activity('com.sankuai.meituan.takeoutnew', 'com.sankuai.meituan.takeoutnew.ui.page.boot.WelcomeActivity')
        #     time.sleep(18)
        #     self.trigger_meituan_waimai()


if __name__ == '__main__':
    trigger = Trigger()
    trigger.trigger_douyin()

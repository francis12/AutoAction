import time
if __name__ == '__main__':
    # task = MeiTuanTask()
    # task.startSendMsgTask()
    # sss = ["1","2"]
    # for i in range(0, len(sss)-1):
    #     print(sss[i])
    curTime = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
    print(curTime)
    if curTime > "2019-11-21 22-24-38":
        print("已过期")

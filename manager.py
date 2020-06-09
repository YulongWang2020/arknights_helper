import win32con
import win32gui
import win32api
import aircv
import time
import random
import numpy as np
from PIL import Image, ImageGrab
import sys

class manager():
    def __init__(self, name):
        self.win_name = name
        self.count_limit = 30
        self.time_limit = 60
        self.threshold = 0.8
        self.ratio = 1.5     # Win 10 text sizing ration (can be fund in Win10 setting)    win10 文本缩放倍率
        self.start_time = 0
        self.win = win32gui.FindWindow(None,self.win_name)
        self.if_battle_fail_continue = False
        self.default_resolution = [1600, 988]
        self.if_recharge = [True,50]
        self.status_message = "十连把把六星！"
        self.time_message = "Made by 鵺鸟"
        self.start_small = "images/start_small.png"
        self.start_big = "images/start_big.png"
        self.end = "images/battle_end.png"
        self.battle_normal = "images/battle_normal.png"
        self.battle_failed = "images/battle_fail.png"
        self.main_page = "images/main_page.png"
        self.recharge = "images/recharge.png"
        self.level_up = "images/level_up.png"

        self.quit = False



    def setfore(self):
        try:
            self.my_sleep(0.1)
            win32gui.SetForegroundWindow(self.win)
        except Exception as e:
            print('置顶窗口失败')
            self.status_message = '置顶窗口失败'
            # raise

    def get_crop_size(self):
        self.setfore()
        left, top, right, bottom = win32gui.GetWindowRect(self.win)
        rect = (left * self.ratio, top * self.ratio, right * self.ratio, bottom * self.ratio)
        return rect

    def get_win_size(self):
        size = self.get_crop_size()
        w = int((size[2] - size[0]))
        h = int((size[3] - size[1]))
        # print("win size:",[w,h])
        return [w,h]


    def get_screen_shoot(self):
        self.setfore()
        img = ImageGrab.grab(self.get_crop_size())
        return img

    def pos(self,x,y):
        #鼠标位置整合，32位整数型
        return y<<16|x

    def mouse_click(self,xy):
        try:
            #模拟鼠标点击，
            self.setfore()
            w = int(xy[1][0]/3)
            h = int(xy[1][1]/3)
            randw = random.randint(-w,w)
            randh = random.randint(-h,h)
            # print(w,h)
            # print(int(xy[0][0]/ratio),int(xy[0][1]/ratio))
            x = int((xy[0][0] + randw)/self.ratio)
            y = int((xy[0][1] + randh)/self.ratio)
            print(x,y)
            # print("rand",randw,randh)
            # win32api.SetCursorPos(self.pos(x,y))
            win32gui.SendMessage(self.win,win32con.WM_LBUTTONDOWN,win32con.MK_LBUTTON, self.pos(x,y))
            self.my_sleep(0.1)
            win32gui.SendMessage(self.win, win32con.WM_LBUTTONUP,0, self.pos(x,y))
        except Exception as e:
            self.status_message = '点击出错'
            print('点击出错')
            # raise

    def find_position(self,target,src = 0,confidence = False,if_status = False):
        #return [x,y] coordinate of click position
        print("looking for ", target)
        if not if_status:
            img = self.get_screen_shoot()
            src = np.asarray(img)
        try:
            target_img = Image.open(target,'r')
        except Exception as e:
            self.status_message = "读取图片失败"
            print("读取图片失败")

        win_size = self.get_win_size()
        width = int(win_size[0] / self.default_resolution[0] * target_img.size[0])
        height = int(win_size[1] / self.default_resolution[1] * target_img.size[1])
        img_size = [width,height]
        print("original img size:",target_img.size[0],target_img.size[1])
        print("Changed img size: ",width,height)
        print("ratio changed:",width/target_img.size[0],height/target_img.size[1])
        print("original win size: ",self.default_resolution )
        print("now win size:",win_size)
        print("ratio changed: ",win_size[0] / self.default_resolution[0],win_size[1] / self.default_resolution[1])
        target_img = np.array(target_img.resize((width, height), Image.ANTIALIAS))
        position = aircv.find_template(src, target_img)
        print(position)
        if not position:
            return 0
        if position["confidence"] < self.threshold:
            return 0
        if confidence:
            return position["confidence"]
        result = list(position['result'])
        return result,img_size

    def get_status(self):
        img = self.get_screen_shoot()
        src = np.asarray(img)
        confidences = {}
        confidences["end"] = self.find_position(self.end,src,True,True)
        confidences["start_small"] = self.find_position(self.start_small,src, True,True)
        confidences["start_big"] = self.find_position(self.start_big,src,True,True)
        confidences["battle_normal"] = self.find_position(self.battle_normal,src,True,True)
        confidences["main_page"] = self.find_position( self.main_page,src, True,True)
        confidences["recharge"] = self.find_position( self.recharge,src, True,True)
        confidences["battle_failed"] = self.find_position(self.battle_failed,src, True,True)
        confidences["level_up"] = self.find_position(self.level_up,src, True,True)
        status = max(confidences,key=confidences.get)
        if confidences[status] > self.threshold:
            return status
        return "UnKnown"

    def end_game(self):
        try:
            sys.exit(0)
        except Exception as e:
            print('运行结束')

    def my_sleep(self,sec):
        time_limits = sec
        start_times = time.time()
        while (time.time() - start_times) < time_limits:
            self.quit_game()
        return

    def quit_game(self):
        time_passed = (time.time() - self.start_time) / 60
        if (not self.quit) & (time_passed < int(self.time_limit)) & (self.count < int(self.count_limit)):
            return
        self.status_message = "运行结束"
        print("运行结束")
        self.end_game()

    def start_game(self):
        self.win = win32gui.FindWindow(None, self.win_name)
        print(self.win_name)
        self.quit = False
        self.start_time = time.time()
        self.count = 0
        while (1):
            time_passed = (time.time() - self.start_time) / 60
            print("已运行 ", "%.2f" % time_passed, " / ", self.time_limit, "分钟  ", "战斗：", self.count, " / ",
                  self.count_limit, " 次")
            self.time_message = "已运行 "+ "%.2f" % time_passed+" / "+ str(self.time_limit)+ "分钟  \n"+ "战斗："+ str(self.count)+ " / "+ str(self.count_limit)+ " 次"

            self.quit_game()
            status = self.get_status()
            if status == "UnKnown":
                self.my_sleep(1)
                self.status_message = "未知界面，识别失败"
                print("未知界面，识别失败")
                continue

            if status == "start_small":
                self.mouse_click(self.find_position(self.start_small,False,False))
                self.status_message = "开始战斗"
                print("开始战斗")
                self.my_sleep(1)
                continue
            if status == "recharge":
                if (self.if_recharge[0]) & (self.if_recharge[1]>0):
                    self.mouse_click(self.find_position(self.recharge, False,False))
                    self.status_message ="体力不足，恢复体力"
                    print("体力不足，恢复体力")
                    self.my_sleep(1)
                    self.if_recharge[1]-=1
                    print("剩余恢复次数： ",self.if_recharge[1])
                    continue
                print("体力耗尽，终止程序")
                break
            if status == "level_up":
                self.mouse_click(self.find_position(self.level_up, False,False))
                print("升级啦")
                self.status_message = "升级啦"
                self.my_sleep(1)
                continue

            if status == "start_big":
                self.mouse_click(self.find_position(self.start_big, False,False))
                print("编队完成，开始战斗")
                self.status_message = "编队完成，开始战斗"
                self.my_sleep(1)
                continue

            if status == "battle_normal":
                print("战斗中")
                self.status_message = "战斗中"
                self.my_sleep(20)
                continue

            if status == "battle_failed":
                print("战斗失败")
                self.status_message = "战斗失败"
                self.my_sleep(2)
                if if_battle_fail_continue:
                    self.mouse_click(self.find_position(self.battle_failed, False,False))
                    print("继续战斗")
                    self.status_message = "继续战斗"
                    continue
                self.status_message = "退出程序"
                print("退出程序")
                break

            if status == "end":
                self.mouse_click(self.find_position(self.end, False,False))
                self.count += 1
                self.status_message = "战斗完成"
                print("战斗完成")
                self.my_sleep(2)
                continue

# if __name__ == "__main__":
#     win = manager("明日方舟 - MuMu模拟器")
#
#     self.my_sleep(1)
#     # print(get_win_size(ratio,win))
#     # get_screen_shoot(ratio,win).show()
#     # win32gui.SetWindowPos(win, win32con.HWND_TOPMOST, 0,0,int(1600/ratio),int(988/ratio), win32con.SWP_SHOWWINDOW)
#     # win32api.MessageBox(0, "请勿改变窗口大小，窗口将会锁定在最顶层", "提醒",win32con.MB_ICONWARNING)
#     win.start_game()







import tkinter as tk
from manager import manager
import threading


def trans_cor(win,x,y):
    return win.winfo_width*x,win.winfo_height*y


def start_helper():
    print(count_limit.get())
    auto.count_limit = count_limit.get()
    auto.time_limit = time_limit.get()
    if ratio.get() != '请输入系统缩放倍率(默认1.5)':
        auto.ratio = float(ratio.get())
    auto.if_recharge[1] = int(recharge_num.get())
    if win_name.get() != "请输入模拟器窗口名（默认MuMu）":
        auto.win_name = win_name.get()
    thread_it(auto.start_game)

def end_helper(auto):
    auto.quit = True


def thread_it(func, *args):
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func, args=args)
    # 守护
    t.setDaemon(True)
    # 启动
    t.start()

def change():
    status_message.set(auto.status_message)
    time_message.set(auto.time_message)
    window.after(250, change)

window = tk.Tk()
window.title('明日方舟—脚本')
window.geometry('400x350')
count_limit = tk.StringVar()
count_limit.set('请输入运行次数')

time_limit = tk.StringVar()
time_limit.set('请输入运行时间（分钟）')

win_name = tk.StringVar()
win_name.set('请输入模拟器窗口名（默认MuMu）')

recharge_num = tk.StringVar()
recharge_num.set('请输入碎石数量')

ratio = tk.StringVar()
ratio.set('请输入系统缩放倍率(默认1.5)')
w = 400
h = 300
auto = manager("明日方舟 - MuMu模拟器")
status_message = tk.StringVar()
status_message.set(auto.status_message)
time_message = tk.StringVar()
time_message.set(auto.time_message)

entry_win_name = tk.Entry(window, textvariable=win_name,width = 35, font=("微软雅黑", 14))
entry_win_name.pack(anchor='center')
entry_ratio = tk.Entry(window, textvariable=ratio, width = 35, font=("微软雅黑", 14))
entry_ratio.pack(anchor='center')

entry_recharge_num = tk.Entry(window, textvariable=recharge_num, width = 35, font=("微软雅黑", 14))
entry_recharge_num.pack(anchor='center')

entry_count_limit = tk.Entry(window, textvariable=count_limit, width = 35, font=("微软雅黑", 14))
entry_count_limit.pack(anchor='center')

entry_time_limit = tk.Entry(window, textvariable=time_limit, width = 35, font=("微软雅黑", 14))
entry_time_limit.pack(anchor='center')



auto = manager("明日方舟 - MuMu模拟器")
status = tk.Label(window, textvariable=status_message, bg='pink', font=("微软雅黑", 12), width=25, height=2)
progress = tk.Label(window, textvariable=time_message, bg='pink', font=("微软雅黑", 12), width=25, height=3)
status.pack(anchor='center')
progress.pack(anchor='center')
print(auto.status_message)

start = tk.Button(window, text='开始', font=("微软雅黑", 12), width=10, height=1, command=lambda: thread_it(start_helper))
start.pack(anchor='center')

end = tk.Button(window, text='停止', font=("微软雅黑", 12), width=10, height=1, command=lambda: end_helper(auto))
end.pack(anchor='center')

window.after(250,change)
window.mainloop()

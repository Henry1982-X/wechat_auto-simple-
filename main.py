from pywinauto.application import Application
from pywinauto.keyboard import SendKeys
import keyboard
import psutil
import time

def find_control_retry(window, title, control_type, retry_interval=1, max_retries=5):
    """在指定窗口中查找控件，带有重试机制"""
    retries = 0
    while retries < max_retries:
        try:
            control = window.child_window(title=title, control_type=control_type)
            return control
        except ElementNotFoundError:
            retries += 1
            time.sleep(retry_interval)
    raise ElementNotFoundError(f"Failed to find control after {max_retries} retries.")


def check_wechat_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'WeChat.exe':
            return True
    return False

def open_wechat(we_path):
    if not check_wechat_running():
        # 打开微信
        app = Application(backend="uia").start(we_path)
    else:
        app = Application(backend="uia").start(we_path)
        app = Application(backend="uia").connect(path=we_path)
    # 获取微信窗口
    we_win = app.window(title='微信')
    try:
        # 微信窗口中，找到“进入微信”按钮
        loginButton = we_win.child_window(title="进入微信", control_type="Button")
        # 点击按钮
        loginButton.click_input()
    except:
        print("微信已打开")

def find_wechat_pid():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'WeChat.exe':
            return proc.info['pid']
    return None

def main(path):
    # 初始化
    name = input("输入聊天列表中发送对象的微信名称:")
    inputthings = input("输入想要发送的内容:\n")
    open_wechat(path)

    # 获取WeChat的进程号PID
    we_pid = find_wechat_pid()

    time.sleep(2)
    # 连接到wx
    wx_app = Application(backend='uia').connect(process=we_pid)
    wx_window = wx_app.window(title="微信")
    wx_chat_win = find_control_retry(wx_window, name, "ListItem")
    wx_chat_win.click_input()

    # 输入发送信息
    keyboard.write(inputthings)
    # 模拟按下键盘enter键
    keyboard.send('enter')

if __name__ == "__main__":
    we_chat_path = "C:\\Program Files (x86)\\Tencent\\WeChat\\WeChat.exe"
    main(we_chat_path)

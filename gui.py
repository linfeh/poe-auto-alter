import tkinter as tk
from tkinter import messagebox
import pyautogui
import keyboard
import threading
from core import run_auto_alter  # 导入核心功能

# 全局变量
currency_pos = None
item_pos = None
automation_running = False
auto_alter_thread = None
stop_event = threading.Event()
status_label = None
console_text = None
hotkey_id = None  # 用于存储快捷键的全局变量


def update_hotkey(hotkey_entry, mod_entry, threshold_entry, alert_file):
    """
    更新用户设置的快捷键
    """
    global hotkey_id
    hotkey = hotkey_entry.get()
    if hotkey_id:
        keyboard.unhook(hotkey_id)  # 如果已经设置了快捷键，取消之前的快捷键绑定

    # 设置新的快捷键
    hotkey_id = keyboard.add_hotkey(hotkey, start_or_stop_automation, args=(mod_entry, threshold_entry, alert_file))
    messagebox.showinfo("成功", f"已设置快捷键为 {hotkey}")


def set_position():
    """
    设置改造石和装备位置
    通过模拟鼠标点击来设置这些位置。
    """
    global currency_pos, item_pos

    # 获取改造石位置
    currency_pos = pyautogui.position()
    currency_label.config(text=f"改造石位置: {currency_pos}")

    # 获取装备位置
    item_pos = pyautogui.position()
    item_label.config(text=f"装备位置: {item_pos}")

    messagebox.showinfo("设置完成", "位置已设置成功！")


def start_or_stop_automation(mod_entry, threshold_entry, alert_file):
    """
    启动或停止自动改造
    """
    global automation_running, auto_alter_thread, stop_event

    if automation_running:
        stop_event.set()  # 停止当前的改造过程
        status_label.config(text="自动改造状态: 已停止")
        automation_running = False
    else:
        stop_event.clear()  # 清除停止标志
        automation_running = True
        status_label.config(text="自动改造状态: 正在进行")

        # 获取用户输入的词缀、阈值等信息
        target_mods = mod_entry.get("1.0", tk.END).strip().split("\n")
        mod_threshold = int(threshold_entry.get())

        # 启动自动改造线程
        auto_alter_thread = threading.Thread(target=run_auto_alter, args=(
            currency_pos, item_pos, target_mods, mod_threshold, alert_file, stop_event, update_console
        ))
        auto_alter_thread.start()


def update_console(item_info, is_satisfied):
    """
    更新控制台输出
    """
    console_text.after(0, lambda: console_text.insert(tk.END,
                                                      f"{item_info}\n满足条件: {'是' if is_satisfied else '否'}\n"))
    console_text.after(0, lambda: console_text.see(tk.END))


def start_gui():
    """
    启动 Tkinter 图形界面
    """
    alert_file = "resources/alert.mp3"  # 提示音文件路径
    root = tk.Tk()
    root.title("poe自动改造")  # 修改窗口标题

    global status_label, console_text, currency_label, item_label

    # 使用 grid 布局
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=5)
    root.grid_rowconfigure(4, weight=2)

    # 目标词缀区域
    tk.Label(root, text="目标词缀:\n同行内为同时满足，\n不同行之间按条数匹配").grid(row=0, column=0, padx=10, pady=5, sticky='w')

    mod_entry = tk.Text(root, height=15, width=40)
    mod_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')
    mod_entry.insert(tk.END, "生命,抗性,法术伤害\n元素伤害,攻击速度")

    # 词缀阈值
    tk.Label(root, text="满足多少条词缀停止:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
    threshold_entry = tk.Entry(root, width=40)
    threshold_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')
    threshold_entry.insert(0, "2")

    # 快捷键
    tk.Label(root, text="自动改造快捷键:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
    hotkey_entry = tk.Entry(root, width=40)
    hotkey_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')
    hotkey_entry.insert(0, "F5")

    tk.Button(root, text="设置快捷键",
              command=lambda: update_hotkey(hotkey_entry, mod_entry, threshold_entry, alert_file)).grid(row=2, column=2,
                                                                                                        padx=10, pady=5)

    # 位置设置区域
    currency_label = tk.Label(root, text="改造石位置: 未设置")
    currency_label.grid(row=3, column=0, padx=10, pady=5, sticky='w')
    tk.Button(root, text="设置位置 (F2)", command=set_position).grid(row=3, column=1, padx=10, pady=5)

    item_label = tk.Label(root, text="装备位置: 未设置")
    item_label.grid(row=4, column=0, padx=10, pady=5, sticky='w')
    tk.Button(root, text="设置位置 (F2)", command=set_position).grid(row=4, column=1, padx=10, pady=5)

    # 状态标签
    status_label = tk.Label(root, text="自动改造状态: 未开始")
    status_label.grid(row=5, column=0, columnspan=3, padx=10, pady=5)

    # 控制台文本区域
    console_label = tk.Label(root, text="控制台输出:")
    console_label.grid(row=0, column=2, padx=10, pady=5, sticky='w')

    console_text = tk.Text(root, height=20, width=40)
    console_text.grid(row=1, column=2, rowspan=4, padx=10, pady=5, sticky='nsew')

    # **左下角作者信息**
    footer_label = tk.Label(root, text="by Linfeh ver. 1.0", fg="gray")
    footer_label.grid(row=6, column=0, columnspan=3, pady=10, sticky='w')  # 置于左下角

    # 启动 GUI 循环
    root.mainloop()


if __name__ == "__main__":
    start_gui()

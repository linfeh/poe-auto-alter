import pyautogui
import time
import random


def run_auto_alter(currency_pos, item_pos, target_mods, mod_threshold, alert_file, stop_event, update_console_callback):
    """
    自动改造逻辑，判断每一行的词缀是否满足要求，并进行改造
    """
    while not stop_event.is_set():
        # 获取装备的词条信息
        item_info = pyautogui.hotkey('ctrl', 'alt', 'c')  # 获取复制的装备信息
        item_info = item_info.strip()

        # 判断每一行是否满足条件
        lines = item_info.split("\n")
        satisfied_lines = 0

        for line in lines:
            match_count = 0
            for mod in target_mods:
                if mod in line:
                    match_count += 1

            if match_count >= mod_threshold:
                satisfied_lines += 1

        # 更新控制台信息
        update_console_callback(item_info, satisfied_lines >= mod_threshold)

        # 如果满足条件的行数达到了阈值，停止改造
        if satisfied_lines >= mod_threshold:
            pyautogui.click(item_pos)
            time.sleep(random.uniform(0.5, 1.5))  # 模拟点击改造石
            pyautogui.click(currency_pos)  # 模拟点击改造石
            time.sleep(1)

            # 播放提示音
            # play_sound(alert_file)

            stop_event.set()
            break
        time.sleep(1)

import time
import pyautogui

# 等待3秒
print(1)
time.sleep(1)
print(2)
time.sleep(1)
print(3)
time.sleep(1)

# 設定滑鼠要移動到的座標
x, y = 1138, 936  # 這裡可以改成你想要的座標

# 移動滑鼠到指定座標
pyautogui.moveTo(x, y)

# 在指定座標點擊滑鼠左鍵
pyautogui.click()



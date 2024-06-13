import json
import paho.mqtt.client as mqtt
import pyautogui

"""
    此為成功國小的 AGV 派車系統 MQTT 之補丁2(執行Reset)
    version: python 3.11.0/paho.mqtt 2.0.0
    因 paho.mqtt 2.0.0 版本的 client = mqtt.Client() 疑似棄用
    這邊使用 client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2) 解決問題
    編譯為 exe 使用 auto-py-to-exe (僅在windows上才能執行)
    最後編輯 2024.6.13
"""

# MQTT 代理資訊
MQTT_BROKER_HOST = "127.0.0.1"  # MQTT 代理地址
MQTT_BROKER_PORT = 1883  # MQTT 代理端口
MQTT_TOPIC = "RT_DATA/1"  # 要訂閱的主題

RESET_LAST_RFID = "A0054"
RESET_NOW_RFID_1 = "A0053"

LAST_RFID = ""
# 當收到消息時的回調函數
def on_message(client, userdata, msg):
    global LAST_RFID

    receivedMessage = msg.payload.decode('utf-8')  # 將收到的消息解碼為 UTF-8 格式
    data = json.loads(receivedMessage)
    NOW_RFID = data["LastRFID"]
    print("Received LastRFID: " + NOW_RFID)  # 輸出收到的消息到控制台

    # 如果收到特定消息，則轉發消息
    if LAST_RFID == RESET_LAST_RFID:
        if NOW_RFID == RESET_NOW_RFID_1:
            # 設定滑鼠要移動到的座標
            x, y = 1138, 936
            # 移動滑鼠到指定座標
            pyautogui.moveTo(x, y)
            # 在指定座標點擊滑鼠左鍵
            pyautogui.click()

    LAST_RFID = NOW_RFID


# 創建 MQTT 客戶端並指定回調 API 版本
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# 設置收到消息的回調函數
client.on_message = on_message

# 連接到 MQTT 代理
client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)

# 訂閱指定主題
client.subscribe(MQTT_TOPIC)

# 保持連接並持續監聽消息
client.loop_forever()
import paho.mqtt.client as mqtt

"""
    此為成功國小的 AGV 派車系統 MQTT 之補丁
    version: python 3.11.0/paho.mqtt 2.0.0
    因 paho.mqtt 2.0.0 版本的 client = mqtt.Client() 疑似棄用
    這邊使用 client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2) 解決問題
    最後編輯 2024.3.8
"""

# MQTT 代理資訊
MQTT_BROKER_HOST = "127.0.0.1"  # MQTT 代理地址
MQTT_BROKER_PORT = 1883  # MQTT 代理端口
MQTT_TOPIC = "SFS2AGV/1"  # 要訂閱的主題

# 轉發配置
FORWARD_TOPIC = "SFS2AGV/1"  # 轉發的主題
FORWARD_MESSAGE = "CMD=GBTN"  # 要轉發的消息內容


# 當收到消息時的回調函數
def on_message(client, userdata, msg):
    receivedMessage = msg.payload.decode('utf-8')  # 將收到的消息解碼為 UTF-8 格式
    print("Received message: " + receivedMessage)  # 輸出收到的消息到控制台

    # 如果收到特定消息，則轉發消息
    if receivedMessage == "ADDCMD=AGVLEAVE" or receivedMessage == "ADDCMD=AGVENTER":
        client.publish(FORWARD_TOPIC, FORWARD_MESSAGE)  # 發布轉發消息到指定主題
        print("Send message: " + FORWARD_MESSAGE)  # 輸出發送的消息到控制台


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

# 註解：這個程式碼段用於連接到 MQTT 代理、訂閱特定主題、並且在收到特定消息時進行處理和轉發。
# client.disconnect()

import json
import random
import time
import paho.mqtt.client as mqtt

# 1. Cấu hình MQTT Broker công cộng dùng để thử nghiệm
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC_TEMPLATE = "iot/lab/{device_id}/data"
INTERVAL = 3  # Chu kỳ gửi dữ liệu (giây)

# 2. Danh sách các cảm biến mô phỏng (mở rộng: nhiều thiết bị)
DEVICES = ["sensor01", "sensor02"]


# Hàm callback khi client kết nối thành công tới broker
def on_connect(client, userdata, flags, rc):
  if rc == 0:
    print("Kết nối thành công tới MQTT Broker!")
  else:
    print(f"Kết nối thất bại, mã lỗi: {rc}")


# Sinh dữ liệu cảm biến ngẫu nhiên trong khoảng hợp lý
def read_sensor(device_id):
  return {
    "device_id": device_id,
    "temperature": round(random.uniform(25.0, 40.0), 1),
    "humidity": round(random.uniform(30.0, 80.0), 1),
  }


# Khởi tạo MQTT Client
client = mqtt.Client()
client.on_connect = on_connect

# Kết nối tới Broker
print(f"Đang kết nối tới broker {BROKER}...")
client.connect(BROKER, PORT, 60)

# Bắt đầu vòng lặp mạng của client chạy ở luồng nền
client.loop_start()

try:
  while True:
    for device_id in DEVICES:
      # Đóng gói dữ liệu cảm biến thành chuỗi JSON
      payload = json.dumps(read_sensor(device_id))
      topic = TOPIC_TEMPLATE.format(device_id=device_id)

      # Gửi dữ liệu lên topic của từng thiết bị
      client.publish(topic, payload)
      print(f"Đã gửi lên topic '{topic}': {payload}")

    # Đợi 3 giây trước khi gửi dữ liệu tiếp theo
    time.sleep(INTERVAL)

except KeyboardInterrupt:
  # Xử lý khi nhấn Ctrl + C để dừng chương trình
  print("\nĐang ngắt kết nối...")
  client.loop_stop()
  client.disconnect()
  print("Đã dừng chương trình Sensor Publisher.")

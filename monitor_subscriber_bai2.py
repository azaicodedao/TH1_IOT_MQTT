import json
from datetime import datetime
import paho.mqtt.client as mqtt

# 1. Cấu hình MQTT Broker (phải khớp với cấu hình của Sensor Publisher)
BROKER = "broker.hivemq.com"
PORT = 1883
# Đăng ký các topic dữ liệu của từng cảm biến
TOPICS = ["iot/lab/sensor01/data", "iot/lab/sensor02/data"]

# 2. Ngưỡng cảnh báo
TEMP_MAX = 35.0
HUMIDITY_MIN = 40.0


# 3. Hàm callback được gọi khi client kết nối thành công với broker
def on_connect(client, userdata, flags, rc):
  if rc == 0:
    print("Kết nối thành công tới MQTT Broker!")
    for topic in TOPICS:
      client.subscribe(topic)
      print(f"Đã đăng ký lắng nghe topic: {topic}")
  else:
    print(f"Kết nối thất bại, mã lỗi: {rc}")


# 4. Hàm callback được gọi khi có dữ liệu cảm biến mới
def on_message(client, userdata, msg):
  current_time = datetime.now().strftime("%H:%M:%S")

  # Phân tích chuỗi JSON nhận được
  try:
    data = json.loads(msg.payload.decode("utf-8"))
    device_id = data["device_id"]
    temperature = float(data["temperature"])
    humidity = float(data["humidity"])
  except (ValueError, KeyError, TypeError) as e:
    print(f"\nPayload không hợp lệ trên topic {msg.topic}: {e}")
    return

  # In dữ liệu ra màn hình theo từng dòng
  print(f"\n[{current_time}] Topic: {msg.topic}")
  print(f"Device: {device_id}")
  print(f"Temperature: {temperature} C")
  print(f"Humidity: {humidity} %")

  # Kiểm tra ngưỡng và in cảnh báo
  if temperature > TEMP_MAX:
    print("CANH BAO: Nhiet do cao")
  if humidity < HUMIDITY_MIN:
    print("CANH BAO: Do am thap")
  print("-" * 40)


# 5. Khởi tạo MQTT Client và gắn các hàm callback
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# 6. Kết nối tới Broker
print(f"Đang kết nối tới broker {BROKER}...")
client.connect(BROKER, PORT, 60)

# 7. Lắng nghe liên tục cho đến khi người dùng nhấn Ctrl + C
try:
  print("Đang chờ nhận dữ liệu cảm biến... Nhấn Ctrl+C để thoát.")
  client.loop_forever()
except KeyboardInterrupt:
  print("\nĐã dừng chương trình Monitoring Subscriber.")

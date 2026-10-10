import json
import paho.mqtt.client as mqtt

# 1. Cấu hình MQTT Broker công cộng dùng để thử nghiệm
BROKER = "broker.hivemq.com"
PORT = 1883
CMD_TOPIC = "iot/lab/{device_id}/cmd"
STATUS_TOPIC = "iot/lab/{device_id}/status"

# 2. Danh sách thiết bị mô phỏng và trạng thái ban đầu (mở rộng: nhiều thiết bị)
devices = {
  "light01": "OFF",
  "fan01": "OFF",
  "pump01": "OFF",
}
VALID_COMMANDS = ("ON", "OFF")


# Gửi trạng thái hiện tại của thiết bị lên topic status
def publish_status(client, device_id):
  payload = json.dumps({"device_id": device_id, "status": devices[device_id]})
  topic = STATUS_TOPIC.format(device_id=device_id)
  client.publish(topic, payload)
  print(f"Đã gửi trạng thái lên topic '{topic}': {payload}")


# 3. Hàm callback khi kết nối thành công: subscribe topic lệnh của từng thiết bị
def on_connect(client, userdata, flags, rc):
  if rc == 0:
    print("Kết nối thành công tới MQTT Broker!")
    for device_id in devices:
      topic = CMD_TOPIC.format(device_id=device_id)
      client.subscribe(topic)
      print(f"Đã đăng ký lắng nghe topic: {topic}")
  else:
    print(f"Kết nối thất bại, mã lỗi: {rc}")


# 4. Hàm callback khi nhận được lệnh điều khiển
def on_message(client, userdata, msg):
  # Topic có dạng iot/lab/<device_id>/cmd
  device_id = msg.topic.split("/")[2]
  command = msg.payload.decode("utf-8", errors="replace").strip().upper()
  print(f"\n[{device_id}] Nhận lệnh: {command}")

  if command not in VALID_COMMANDS:
    print(f"Lệnh không hợp lệ: {command} (chỉ chấp nhận ON/OFF)")
    return

  # Cập nhật trạng thái và phản hồi trạng thái mới
  devices[device_id] = command
  print(f"[{device_id}] Trạng thái hiện tại: {'BẬT' if command == 'ON' else 'TẮT'}")
  publish_status(client, device_id)


# 5. Khởi tạo MQTT Client và gắn các hàm callback
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# 6. Kết nối tới Broker
print(f"Đang kết nối tới broker {BROKER}...")
client.connect(BROKER, PORT, 60)

# 7. Chạy liên tục chờ lệnh cho đến khi người dùng nhấn Ctrl + C
try:
  print("Thiết bị đang chờ lệnh... Nhấn Ctrl+C để thoát.")
  client.loop_forever()
except KeyboardInterrupt:
  print("\nĐã dừng chương trình Smart Device.")

import time
import paho.mqtt.client as mqtt

# 1. Cấu hình MQTT Broker (phải khớp với cấu hình của Device)
BROKER = "broker.hivemq.com"
PORT = 1883
CMD_TOPIC = "iot/lab/{device_id}/cmd"
STATUS_TOPIC = "iot/lab/{device_id}/status"

DEVICES = ["light01", "fan01", "pump01"]
DEFAULT_DEVICE = "light01"
VALID_COMMANDS = ("ON", "OFF")


# 2. Hàm callback khi kết nối thành công: subscribe topic trạng thái của các thiết bị
def on_connect(client, userdata, flags, rc):
  if rc == 0:
    print("Kết nối thành công tới MQTT Broker!")
    userdata["connected"] = True
    for device_id in DEVICES:
      topic = STATUS_TOPIC.format(device_id=device_id)
      client.subscribe(topic)
      print(f"Đã đăng ký lắng nghe topic: {topic}")
  else:
    print(f"Kết nối thất bại, mã lỗi: {rc}")


# 3. Hàm callback khi nhận được phản hồi trạng thái từ thiết bị
def on_message(client, userdata, msg):
  payload = msg.payload.decode("utf-8", errors="replace")
  print("\nTrang thai nhan duoc:")
  print(payload)


# 4. Khởi tạo MQTT Client và gắn các hàm callback
client = mqtt.Client(userdata={"connected": False})
client.on_connect = on_connect
client.on_message = on_message

# 5. Kết nối tới Broker, chạy vòng lặp mạng ở luồng nền để nhận phản hồi
print(f"Đang kết nối tới broker {BROKER}...")
client.connect(BROKER, PORT, 60)
client.loop_start()

# Chờ kết nối thành công rồi mới cho nhập lệnh (tránh lệnh bị mất khi chưa kết nối)
for _ in range(100):
  if client.user_data_get()["connected"]:
    break
  time.sleep(0.1)
else:
  print("Không kết nối được tới broker, vui lòng thử lại.")

print("\nCú pháp: ON | OFF | <thiết bị> ON | <thiết bị> OFF | EXIT")
print(f"Thiết bị: {', '.join(DEVICES)} (mặc định: {DEFAULT_DEVICE})")

# 6. Vòng lặp nhập lệnh từ bàn phím
try:
  while True:
    parts = input("\nNhap lenh: ").strip().split()
    if not parts:
      continue

    # Lệnh EXIT để kết thúc chương trình
    if len(parts) == 1 and parts[0].upper() == "EXIT":
      break

    # Hỗ trợ "ON" (mặc định light01) hoặc "fan01 ON"
    if len(parts) == 1:
      device_id, command = DEFAULT_DEVICE, parts[0].upper()
    elif len(parts) == 2:
      device_id, command = parts[0].lower(), parts[1].upper()
    else:
      print("Loi: Sai cu phap lenh")
      continue

    if device_id not in DEVICES:
      print(f"Loi: Thiet bi '{device_id}' khong ton tai")
      continue
    if command not in VALID_COMMANDS:
      print("Loi: Lenh khong hop le, chi chap nhan ON hoac OFF")
      continue

    # Gửi lệnh lên topic điều khiển của thiết bị
    client.publish(CMD_TOPIC.format(device_id=device_id), command)
    print(f"Da gui lenh {command} toi {device_id}")
    # Chờ một chút để nhận phản hồi trạng thái trước khi nhập lệnh tiếp
    time.sleep(1)

except (KeyboardInterrupt, EOFError):
  pass

print("\nĐang ngắt kết nối...")
client.loop_stop()
client.disconnect()
print("Đã dừng chương trình Controller.")

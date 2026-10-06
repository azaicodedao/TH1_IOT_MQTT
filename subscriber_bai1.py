from datetime import datetime
import paho.mqtt.client as mqtt

# 1. Cấu hình MQTT Broker (phải khớp với cấu hình của Publisher)
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "iot/lab/message"


# 2. Hàm callback được gọi khi client kết nối thành công với broker
def on_connect(client, userdata, flags, rc):
  if rc == 0:
    print("Kết nối thành công tới MQTT Broker!")
    # Đăng ký (subscribe) lắng nghe topic ngay sau khi kết nối thành công
    client.subscribe(TOPIC)
    print(f"Đã đăng ký lắng nghe topic: {TOPIC}")
  else:
    print(f"Kết nối thất bại, mã lỗi: {rc}")


# 3. Hàm callback được gọi khi có thông điệp mới gửi đến topic đã đăng ký
def on_message(client, userdata, msg):
  # Lấy thời điểm hiện tại nhận được thông điệp
  current_time = datetime.now().strftime("%H:%M:%S")
  # Giải mã nội dung thông điệp từ dạng bytes sang chuỗi (utf-8)
  payload = msg.payload.decode("utf-8")

  # In ra màn hình theo đúng định dạng yêu cầu
  print("\nNhan duoc message:")
  print(f"Topic: {msg.topic}")
  print(f"Payload: {payload}")
  print(f"Time: {current_time}")
  print("-" * 40)


# 4. Khởi tạo MQTT Client
client = mqtt.Client()

# Gắn các hàm callback vào client
client.on_connect = on_connect
client.on_message = on_message

# 5. Kết nối tới Broker
print(f"Đang kết nối tới broker {BROKER}...")
client.connect(BROKER, PORT, 60)

# 6. Bắt đầu vòng lặp lắng nghe liên tục cho đến khi người dùng nhấn Ctrl + C
try:
  print("Đang chờ nhận thông điệp... Nhấn Ctrl+C để thoát.")
  client.loop_forever()
except KeyboardInterrupt:
  print("\nĐã dừng chương trình Subscriber.")
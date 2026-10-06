import time
import paho.mqtt.client as mqtt

# 1. Cấu hình MQTT Broker công cộng dùng để thử nghiệm
BROKER = "broker.hivemq.com" 
PORT = 1883
TOPIC = "iot/lab/message"

# 2. Thông tin sinh viên 
HO_TEN = "Nguyen Van Tien"
MSSV = "B23DCCN821"
NOI_DUNG = "Xin chao tu client Python MQTT"


# Hàm callback khi client kết nối thành công tới broker
def on_connect(client, userdata, flags, rc):
  if rc == 0:
    print("Kết nối thành công tới MQTT Broker!")
  else:
    print(f"Kết nối thất bại, mã lỗi: {rc}")


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
    # Đóng gói nội dung thông điệp
    message = f"Họ tên: {HO_TEN} | MSSV: {MSSV} | Nội dung: {NOI_DUNG}"

    # Gửi thông điệp lên topic
    client.publish(TOPIC, message)
    print(f"Đã gửi lên topic '{TOPIC}': {message}")

    # Đợi 5 giây trước khi gửi thông điệp tiếp theo
    time.sleep(5)

except KeyboardInterrupt:
  # Xử lý khi bạn nhấn tổ hợp phím Ctrl + C để dừng chương trình
  print("\nĐang ngắt kết nối...")
  client.loop_stop()
  client.disconnect()
  print("Đã dừng chương trình Publisher.")
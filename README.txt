BÀI 1: ỨNG DỤNG GỬI VÀ NHẬN THÔNG ĐIỆP MQTT CƠ BẢN

1. MỤC TIÊU
- Làm quen với cơ chế Publisher/Subscriber trong giao thức MQTT.
- Hiểu cách khởi tạo kết nối, gửi (publish) và nhận (subscribe) thông điệp thông qua MQTT Broker sử dụng thư viện paho-mqtt trên Python.

2. MÔ TẢ
- Broker sử dụng: broker.hivemq.com (Port: 1883)
- Topic sử dụng: iot/lab/message
- Các file chương trình:
  + publisher_bai1.py: Đoạn mã đóng vai trò Publisher, thực hiện gửi thông điệp chứa Họ tên, MSSV và nội dung lên Broker định kỳ 5 giây một lần.
  + subscriber_bai1.py: Đoạn mã đóng vai trò Subscriber, thực hiện đăng ký lắng nghe topic và in ra thông điệp nhận được kèm mốc thời gian thực.

3. CÁCH CHẠY TỪNG CHƯƠNG TRÌNH
Bước 1: Cài đặt thư viện paho-mqtt (nếu chưa cài đặt)
    pip install paho-mqtt

Bước 2: Chạy Subscriber để chờ nhận dữ liệu
    python subscriber_bai1.py

Bước 3: Mở một terminal/command prompt mới và chạy Publisher để bắt đầu gửi dữ liệu
    python publisher_bai1.py

4. KẾT QUẢ ĐẠT ĐƯỢC
- Publisher:
  + Kết nối thành công tới MQTT Broker "broker.hivemq.com".
  + Gửi thành công chuỗi thông điệp (Ví dụ: "Họ tên: Nguyen Van Tien | MSSV: B23DCCN821 | Nội dung: Xin chao tu client Python MQTT") lên topic "iot/lab/message" định kỳ mỗi 5 giây.
- Subscriber:
  + Kết nối thành công tới Broker và subscribe topic "iot/lab/message".
  + Nhận và hiển thị đầy đủ các thông điệp được gửi từ Publisher theo thời gian thực với định dạng chi tiết (Topic, Payload, Time).
    * Topic: iot/lab/message
    * Payload: Họ tên: Nguyen Van Tien | MSSV: B23DCCN821 | Nội dung: Xin chao tu client Python MQTT
    * Time: 22:32:03


==========================================================================================

BÀI 2: MÔ PHỎNG CẢM BIẾN NHIỆT ĐỘ VÀ ĐỘ ẨM BẰNG MQTT

1. MỤC TIÊU
- Mô phỏng thiết bị IoT gửi dữ liệu cảm biến định kỳ qua MQTT.
- Tổ chức dữ liệu theo mô hình thiết bị - topic - payload (JSON).

2. MÔ TẢ
- Broker sử dụng: broker.hivemq.com (Port: 1883)
- Topic sử dụng: iot/lab/sensor01/data, iot/lab/sensor02/data
- Định dạng payload (JSON):
    {"device_id": "sensor01", "temperature": 28.5, "humidity": 65.2}
- Các file chương trình:
  + sensor_publisher_bai2.py: Mô phỏng 2 cảm biến (sensor01, sensor02), sinh ngẫu nhiên nhiệt độ (25 - 40 °C) và độ ẩm (30 - 80 %), gửi dữ liệu dạng JSON lên topic iot/lab/<device_id>/data mỗi 3 giây.
  + monitor_subscriber_bai2.py: Subscribe topic dữ liệu của các cảm biến, phân tích JSON, in dữ liệu theo từng dòng và kiểm tra ngưỡng:
      * Nhiệt độ > 35 °C  -> in "CANH BAO: Nhiet do cao"
      * Độ ẩm < 40 %      -> in "CANH BAO: Do am thap"

3. CÁCH CHẠY TỪNG CHƯƠNG TRÌNH
Bước 1: Chạy Monitoring Subscriber để chờ nhận dữ liệu
    python monitor_subscriber_bai2.py

Bước 2: Mở một terminal mới và chạy Sensor Publisher
    python sensor_publisher_bai2.py

Bước 3: Nhấn Ctrl+C ở mỗi terminal để dừng chương trình.

4. KẾT QUẢ ĐẠT ĐƯỢC
- Sensor Publisher gửi tuần hoàn mỗi 3 giây payload đúng định dạng JSON cho sensor01 và sensor02.
- Monitoring Subscriber nhận, phân tích dữ liệu và cảnh báo đúng điều kiện. Ví dụ:
    [10:15:20] Topic: iot/lab/sensor01/data
    Device: sensor01
    Temperature: 36.1 C
    Humidity: 38.7 %
    CANH BAO: Nhiet do cao
    CANH BAO: Do am thap


==========================================================================================

BÀI 3: MÔ PHỎNG HỆ THỐNG ĐIỀU KHIỂN ĐÈN THÔNG MINH QUA MQTT

1. MỤC TIÊU
- Xây dựng mô hình IoT hai chiều: giám sát + điều khiển thiết bị qua MQTT.

2. MÔ TẢ
- Broker sử dụng: broker.hivemq.com (Port: 1883)
- Tổ chức topic theo dạng iot/lab/<device_id>/<loại>:
  + Topic điều khiển: iot/lab/light01/cmd    (tương tự fan01, pump01)
  + Topic trạng thái: iot/lab/light01/status (tương tự fan01, pump01)
- Payload trạng thái (JSON):
    {"device_id": "light01", "status": "ON"}
- Các file chương trình:
  + device_bai3.py: Mô phỏng các thiết bị thông minh light01, fan01, pump01. Subscribe topic cmd của từng thiết bị, nhận lệnh "ON"/"OFF" để bật/tắt; sau mỗi lệnh hợp lệ sẽ publish trạng thái mới lên topic status. Lệnh không hợp lệ sẽ bị bỏ qua và in thông báo lỗi.
  + controller_bai3.py: Cho người dùng nhập lệnh từ bàn phím, publish lệnh lên topic cmd và subscribe topic status để hiển thị trạng thái phản hồi từ thiết bị.
- Cú pháp lệnh trong Controller:
  + ON / OFF            : điều khiển thiết bị mặc định light01
  + <thiết bị> ON/OFF   : điều khiển thiết bị khác, ví dụ: fan01 ON, pump01 OFF
  + EXIT                : kết thúc chương trình
  + Lệnh khác ON/OFF hoặc thiết bị không tồn tại -> báo lỗi

3. CÁCH CHẠY TỪNG CHƯƠNG TRÌNH
Bước 1: Chạy chương trình thiết bị để chờ lệnh
    python device_bai3.py

Bước 2: Mở một terminal mới và chạy Controller
    python controller_bai3.py

Bước 3: Nhập lệnh trong cửa sổ Controller (ON, OFF, fan01 ON, ...). Nhập EXIT để thoát Controller, nhấn Ctrl+C để dừng Device.

4. KẾT QUẢ ĐẠT ĐƯỢC
- Điều khiển được thiết bị qua MQTT, thiết bị phản hồi đúng trạng thái, giao tiếp hai chiều. Ví dụ:
    Nhap lenh: ON
    Da gui lenh ON toi light01

    Trang thai nhan duoc:
    {"device_id": "light01", "status": "ON"}

    Nhap lenh: abc
    Loi: Lenh khong hop le, chi chap nhan ON hoac OFF


==========================================================================================

CẤU HÌNH MQTT BROKER
- Mặc định tất cả chương trình dùng broker công cộng broker.hivemq.com, cổng 1883, không cần tài khoản.
- Để đổi broker (ví dụ test.mosquitto.org hoặc Mosquitto cài trên máy), sửa 2 biến ở đầu mỗi file:
    BROKER = "broker.hivemq.com"
    PORT = 1883
  Lưu ý: Publisher và Subscriber phải dùng cùng một broker.
- Cài Mosquitto trên máy (tùy chọn): tải tại https://mosquitto.org/download/, chạy "mosquitto -v", rồi đặt BROKER = "localhost".

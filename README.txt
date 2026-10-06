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

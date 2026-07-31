# Phản hồi Cá nhân (Reflection) - Hoàng Hương Giang (2A202601470)

## 1. Vai trò và Công việc đã làm
Trong dự án **TA Co-pilot**, tôi đảm nhận vai trò **Tích hợp Discord API & Vận hành Bot**. Các nhiệm vụ chính tôi đã hoàn thành bao gồm:
*   Đăng ký ứng dụng Bot trên Discord Developer Portal, cấu hình các quyền hạn cần thiết (đặc biệt là Message Content Intent và Manage Messages).
*   Xây dựng hàm kéo dữ liệu lịch sử chat tại `codebase/services/discord_service.py` và `codebase/discord_fetcher.py` kể từ mốc 00:00 GMT+7 cùng ngày, đồng thời lọc bỏ tin nhắn rác (tin nhắn của Bot khác hoặc tin chat tự do của TA).
*   Lập trình cơ chế Caching tại `codebase/services/cache_service.py` để lưu trữ kết quả phân tích LLM trong vòng 10 phút, giúp giảm số lượng token gọi lên API và đảm bảo bot phản hồi ngay lập tức cho các TA khác cùng truy cập.

## 2. Cách AI hỗ trợ trong quá trình làm việc
AI đã hỗ trợ tôi giải quyết các vấn đề kỹ thuật sau:
*   **Viết code bất đồng bộ (Async/Await):** AI giúp tôi viết các hàm async kéo tin nhắn từ Discord một cách hiệu quả mà không làm nghẽn tiến trình chạy chính của Bot.
*   **Xử lý múi giờ phức tạp:** Hỗ trợ tính toán mốc 00:00 giờ Việt Nam (GMT+7) từ thời gian hệ thống UTC để bot quét đúng các tin nhắn gửi trong ngày.
*   **Xử lý ngoại lệ (Error Handling):** Đề xuất cấu trúc try-except bắt các lỗi thường gặp của Discord API như lỗi Timeout hoặc lỗi mất kết nối Gateway.

## 3. Bài học kinh nghiệm từ trường hợp thất bại của nhóm
Bài học lớn nhất của tôi liên quan đến **sự không đồng bộ trong logic kiểm tra phản hồi (is_replied)** giữa hai cấu phần trong hệ thống:
*   **Vấn đề:** Trong lệnh kiểm tra `/test_fetch`, tôi viết code quét phản hồi của TA ở cả hai luồng: Reply trực tiếp và thảo luận trong Thread phụ. Tuy nhiên, trong logic chính `/checkmiss` (chạy qua `discord_service.py`), code chỉ kiểm tra trường `reference` (chỉ chấp nhận Reply trực tiếp). Điều này dẫn đến sự chênh lệch số liệu: `/test_fetch` báo đã trả lời, nhưng `/checkmiss` vẫn lôi câu hỏi đó ra hiển thị cho TA.
*   **Bài học:** Khi thiết kế các hệ thống AI kết hợp nhiều dịch vụ, việc đồng bộ hóa định nghĩa logic nghiệp vụ (business logic consistency) giữa các hàm phụ trợ là vô cùng quan trọng. Một thay đổi nhỏ ở cơ sở dữ liệu hoặc cách lọc thô ở backend sẽ gây ảnh hưởng lớn đến kết quả hiển thị trên UI. Nhóm tôi đã xử lý bằng cách chuẩn hóa cơ chế kiểm tra phản hồi chỉ tính Reply trực tiếp và bổ sung cảnh báo hướng dẫn sử dụng rõ ràng trong thông tin chào mừng của Bot để TA nắm rõ quy trình vận hành.

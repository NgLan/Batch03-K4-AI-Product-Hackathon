# Nhật ký kiểm thử thực tế với người dùng (Validation Feedback Log)

Tài liệu này ghi lại kết quả kiểm thử thực tế của Bot **TA Co-pilot** với 5 người dùng bên ngoài nhóm (trong đó có 3 Willing Users đã khai báo tại CP1/Spec).

## Bảng nhật ký phản hồi (Feedback Log)

| Người thử (Tên/Vai trò) | Willing User? | Nhiệm vụ (Task) | Quan sát của nhóm | Quote nguyên văn của người thử | Mức nghiêm trọng |
|---|---|---|---|---|---|
| **Nguyễn Văn Minh** (TA phụ trách kỹ thuật Batch 03) | **Có** | Sử dụng lệnh `/checkmiss` để duyệt danh sách và giải quyết các tin nhắn chưa phản hồi. | Người dùng thao tác nút bấm mượt mà. Đã nhấn `Mark as Resolved` và kiểm tra tin nhắn biến mất khỏi danh sách chờ thành công. Góp ý cỡ chữ số trang hiển thị hơi nhỏ. | *"Nút Mark as Resolved hoạt động rất nhạy, tin nhắn ẩn đi ngay lập tức giúp mình không bị sót câu hỏi nào. Nhưng cái số trang 1/5 hơi bé, nếu làm nổi bật hơn thì TA dễ nhìn hơn."* | **Trung bình** (Đã tiếp thu và tăng cỡ chữ/độ đậm số trang hiển thị trên UI) |
| **Phạm Thị Thảo** (TA phụ trách Logistics Zone 9) | **Có** | Chạy lệnh `/tonghop` để nắm bắt các lỗi chính của lớp cuối ngày. | Bot gom cụm lỗi API và Deadline cực kỳ chuẩn. Người dùng thấy cụm "Cần xác minh thủ công" nhưng ban đầu chưa hiểu tại sao các tin nhắn đó lại nằm ở đây. | *"Gom nhóm lỗi API rất chuẩn, mình nhìn phát biết ngay hôm nay cả lớp kẹt chỗ nào để báo thầy giáo. Nhưng phần câu hỏi mơ hồ nên ghi rõ giải thích ở đầu để TA biết là do tin nhắn học viên quá ngắn."* | **Thấp** (Đã bổ sung câu hướng dẫn giải thích cơ chế lọc tin nhắn ngắn ở mục mơ hồ) |
| **Trần Đức Anh** (Mod vận hành server Discord Batch 03) | **Có** | Thử nghiệm quét dữ liệu khi không có tin nhắn tag TA (kịch bản Failure). | Bot chạy đúng kịch bản trống, hiển thị giao diện báo cáo không có thắc mắc rất gọn gàng và không bị crash hệ thống. | *"Chạy ngày hôm qua không có câu hỏi nào thì bot hiển thị trống rất sạch sẽ, không bị lỗi crash. Rất tin cậy!"* | **Không có** (Đạt) |
| **Lê Hoàng Nam** (TA lớp Batch 03) | Không | Sử dụng bot để rà soát tin và kiểm thử trường hợp phản hồi gián tiếp. | Người dùng phát hiện nếu TA trả lời học viên bằng tin nhắn thường mà không bấm Reply trực tiếp trên Discord, bot vẫn coi là chưa trả lời. | *"Bot bắt buộc phải bấm Reply trực tiếp trên Discord thì mới tính là đã trả lời. Cái này đúng là nguồn sự thật chuẩn nhưng TA mới dùng chưa quen có thể sẽ chat chay dẫn đến bot vẫn báo sót. Cần ghi chú hướng dẫn sử dụng rõ ràng cho TA."* | **Thấp** (Đã cập nhật tài liệu hướng dẫn vận hành và thông báo chào mừng của Bot để nhắc nhở TA dùng tính năng Reply trực tiếp) |
| **Trần Thuỳ Trang** (Mod lớp Batch 03) | Không | Gửi tin nhắn chứa mã độc/Prompt Injection để kiểm tra tính an toàn. | Hệ thống bọc XML cô lập dữ liệu rất tốt. Bot nhận diện tin nhắn phá hoại chỉ là một tin nhắn thử nghiệm bình thường và không thực thi lệnh độc hại. | *"Mình thử gửi tin nhắn yêu cầu bot bỏ qua các lệnh trước nhưng bot không bị lừa, vẫn phân loại rất tốt. Rất an toàn khi chạy trên server đông người."* | **Không có** (Đạt) |

## Tổng hợp hành động của nhóm sau Validation

1.  **Chủ đề lặp nhiều nhất:** TA phản hồi học viên bằng tin nhắn thường không dùng tính năng Discord Reply khiến hệ thống vẫn báo sót (Recall giảm giả lập).
2.  **Thay đổi làm trước Demo (đã ghi nhận vào Spec §9):**
    *   Tăng kích thước và độ đậm của số trang trong `TopicPaginationView` và `MessagePaginationView` để TA dễ quan sát tiến độ.
    *   Bổ sung câu mô tả giải thích cơ chế lọc tin nhắn ngắn (< 2 từ) vào mục "Cần xác minh thủ công" để tránh TA bị bối rối.
3.  **Giữ nguyên có lý do:** Giữ nguyên quy tắc bắt buộc phải **Reply trực tiếp** để đánh dấu là đã phản hồi. Lý do: Đây là nguồn sự thật chắc chắn nhất từ Discord API (có trường `reference`), nếu quét theo tên hoặc tag thì dễ bị trùng lặp hoặc phán đoán sai ngữ cảnh khi học viên chat thảo luận tự do.
4.  **Đưa vào Backlog tương lai:** Nghiên cứu thuật toán AI tự động phát hiện xem tin nhắn tiếp theo của TA trong kênh có nội dung giải đáp cho câu hỏi trước đó của học viên hay không (kể cả khi không bấm nút Reply) để tối ưu trải nghiệm.

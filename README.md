# KyMonTCX

Ứng dụng lập trận Kỳ Môn Độn Giáp với giao diện Streamlit và API JSON.

## Chạy Streamlit

```bash
streamlit run app.py
```

## Chạy API

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

Ví dụ gọi API:

```text
http://localhost:8000/qimen?y=2026&m=6&d=17&h=8&mi=1
```

## Field chính trong output

- `TuTru`: tứ trụ năm, tháng, ngày, giờ đã dùng để lập trận.
- `Data9Cung`: dữ liệu 9 cung gồm Địa bàn, Thiên bàn, sao, cửa, thần và phân tích bổ sung.
- `Maps`: bản đồ nhanh các can/cửa quan trọng sang cung, có xử lý giờ Giáp ẩn nghi.
- `HiddenStems`: bảng Giáp ẩn nghi và tuần thủ hiện tại.
- `Flags`: các cờ luận nhanh, ví dụ Nhật can, Thời can, Khai môn, Sinh môn có rơi vào cung chứa địa chi Tuần Không ngày/giờ hay không.

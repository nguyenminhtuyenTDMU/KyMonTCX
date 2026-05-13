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

## Cache lịch/tiết khí

Repo có thể đọc sẵn `data/tiet_khi_cache.json` để tránh tính tiết khí bằng Skyfield trong mỗi request.

Tạo lại cache tiết khí 1900-2100:

```bash
python generate_calendar_cache.py --start-year 1900 --end-year 2100
```

Nếu muốn precompute thêm âm lịch theo ngày, có thể thêm `--with-lunar`, nhưng thao tác này chậm hơn nhiều.

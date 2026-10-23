# KyMonTCX

Ứng dụng lập trận Kỳ Môn Độn Giáp với giao diện Streamlit và API JSON.

## Chạy Streamlit

```bash
streamlit run app.py
```

## App Desktop & Mobile (offline)

`main.py` là app [Flet](https://flet.dev) chạy hoàn toàn offline trên Windows, macOS, Linux, Android và iOS.
App dùng chung engine với Streamlit (qua `kymon_view.py`), có đủ 5 loại cục (Thời Gia, Thời Gia Chuyển Bàn,
Nhật/Nguyệt/Niên Gia), badge Tuần Không/Mã/Hình/Mộ/Bách, Tỏa Cung, lưu/copy JSON.
App không cần Skyfield hay `de440s.bsp`: tiết khí đọc từ `data/tiet_khi_cache.json` (1900–2100),
âm lịch tính bằng thuật toán Hồ Ngọc Đức (`am_lich_offline.py`).

Chạy thử trên máy:

```bash
pip install "flet[all]==1.0.3"
flet run main.py            # cửa sổ desktop
flet run --android main.py  # chạy thử trên điện thoại qua app "Flet" (cùng mạng Wi-Fi)
```

Build file cài đặt (lần đầu Flet tự tải Flutter SDK / Android SDK):

```bash
flet build apk       # Android  -> build/apk
flet build windows   # Windows  -> build/windows (cần Visual Studio + "Desktop development with C++")
flet build macos     # macOS    -> build/macos (chạy trên máy Mac)
flet build ipa       # iOS      (chạy trên máy Mac, cần tài khoản Apple Developer)
```

Hoặc build trên GitHub: tab **Actions** → **Build apps** → **Run workflow**, tải file ở mục *Artifacts*
(cũng tự chạy khi push tag `v*`).

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

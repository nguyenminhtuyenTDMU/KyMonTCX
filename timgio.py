import datetime
from kymon_logic import KyMonLapTran

# =========================================================
# 1. CẤU HÌNH QUY TẮC PHONG THỦY (DỄ DÀNG CHỈNH SỬA)
# =========================================================

# Danh sách cung bạn muốn quét (Ví dụ: [3] cho Chấn, hoặc [2, 3, 4, 8] cho các cung cát)
DANH_SACH_CUNG_CAN_TIM = [3,4,6,7]

# Mapping Cung -> Địa chi (Để check Không Vong Thời)
CUNG_CHI = {
    1: ["Tý"], 2: ["Mùi", "Thân"], 3: ["Mão"], 4: ["Thìn", "Tỵ"],
    6: ["Tuất", "Hợi"], 7: ["Dậu"], 8: ["Sửu", "Dần"], 9: ["Ngọ"]
}

# Mapping Cung -> Thiên Can bị Kích Hình
CUNG_KICH_HINH = {
    2: ["Kỷ"], 3: ["Mậu"], 4: ["Nhâm", "Quý"],
    8: ["Canh"], 9: ["Bính"], 1: ["Quý"]  # Cung 1 kỵ Quý (Giáp Dần hình Tý)
}

MAP_TEN_CUNG = {
    1: "Khảm 1", 2: "Khôn 2", 3: "Chấn 3", 4: "Tốn 4",
    6: "Càn 6", 7: "Đoài 7", 8: "Cấn 8", 9: "Ly 9"
}


# =========================================================
# 2. HÀM TÍNH ĐIỂM CÁT (SCORE ENGINE)
# =========================================================gksdugojksdhjflkgjl
def tinh_diem_cat(thien, dia, sao, than, cua):
    diem = 0
    # Tam Kỳ (Ất, Bính, Đinh)
    if any(k in thien for k in ["Ất", "Bính", "Đinh"]): diem += 1
    if any(k in dia for k in ["Ất", "Bính", "Đinh"]): diem += 1

    # Cát Tinh (Nhậm, Phụ, Tâm)
    if any(s in sao for s in ["Nhậm", "Phụ", "Tâm"]): diem += 2

    # Cát Thần (Trực Phù, Lục Hợp, Cửu Thiên, Thái Âm)
    if any(t in than for t in ["Trực Phù", "Lục Hợp", "Cửu Thiên", "Thái Âm"]): diem += 2

    # Cát Môn (Hưu, Sinh, Khai)
    if any(m in cua for m in ["Hưu", "Sinh", "Khai"]): diem += 4

    return diem


# =========================================================
# 3. BỘ LỌC ĐIỀU KIỆN (FILTER ENGINE)
# =========================================================
def kiem_tra_cung_dat_chuan(kq, cung_id):
    cung_data = kq['Data9Cung'].get(cung_id)
    if not cung_data: return False

    cua = cung_data.get('Cua', '')
    than = cung_data.get('Than', '')
    sao = cung_data.get('Sao', '')
    thien = cung_data.get('Thien', '')
    dia = cung_data.get('Dia', '')

    # --- ĐIỀU KIỆN CỨNG (HARD CRITERIA) ---

    # 1. Bắt buộc: Cảnh Môn + Trực Phù (Có thể đổi tùy mục đích)
    if cua != 'Hưu':
        return False

    # 2. Loại trừ Hung Thần/Hung Tinh
    if 'Canh' in thien or 'Canh' in dia: return False
    if 'Bạch Hổ' in than: return False
    if 'Nhu' in sao or 'Bồng' in sao: return False

    # 3. Check Không Vong (Thời)
    tk_thoi = kq['InfoTuanKhong'].get('Thoi', [])
    for chi in CUNG_CHI.get(cung_id, []):
        if chi in tk_thoi: return False

    # 4. Check Kích Hình (Cả Thiên và Địa bàn)
    can_thien_chinh = thien.split("/")[0].strip()
    can_dia_chinh = dia.split("/")[0].strip()
    list_kich = CUNG_KICH_HINH.get(cung_id, [])
    if can_thien_chinh in list_kich or can_dia_chinh in list_kich:
        return False

    # --- ĐIỀU KIỆN ĐIỂM (SOFT CRITERIA) ---
    # Bật dòng dưới nếu muốn lọc quẻ có điểm cát cao (ví dụ >= 6)
    if tinh_diem_cat(thien, dia, sao, than, cua) < 6: return False

    return True


# =========================================================
# 4. CHƯƠNG TRÌNH QUÉT THỜI GIAN
# =========================================================
def tim_tran_phu_hop():
    print("--- KHỞI TẠO MÁY QUÉT KỲ MÔN ---")
    km = KyMonLapTran()

    now = datetime.datetime.now()
    # Căn chỉnh giờ lẻ (canh giờ)
    hour_aligned = now.hour if now.hour % 2 != 0 else now.hour - 1
    if hour_aligned < 0:
        hour_aligned = 23
        now -= datetime.timedelta(days=1)

    current_time = now.replace(hour=hour_aligned, minute=30, second=0, microsecond=0)
    end_time = current_time + datetime.timedelta(days=365)  # Quét 1 năm

    print(f"Bắt đầu quét từ: {current_time.strftime('%d/%m/%Y %H:%M')}")
    print(f"Mục tiêu: Cung {DANH_SACH_CUNG_CAN_TIM}\n")

    while current_time < end_time:
        try:
            kq = km.lap_que(current_time.year, current_time.month, current_time.day, current_time.hour,
                            current_time.minute)
        except:
            current_time += datetime.timedelta(hours=2)
            continue

        for cung_id in DANH_SACH_CUNG_CAN_TIM:
            if kiem_tra_cung_dat_chuan(kq, cung_id):
                c_data = kq['Data9Cung'][cung_id]
                diem = tinh_diem_cat(c_data['Thien'], c_data['Dia'], c_data['Sao'], c_data['Than'], c_data['Cua'])

                print(f"⭐ TÌM THẤY TRẬN ĐỒ ƯNG Ý!")
                print("-" * 55)
                print(f"⏰ Thời gian: {current_time.strftime('%H:%M - %d/%m/%Y')}")
                print(f"🎯 Cung: {MAP_TEN_CUNG[cung_id].upper()} | Điểm Cát: {diem}")
                print(
                    f"📜 Tứ Trụ: {kq['TuTru']['Nam']} - {kq['TuTru']['Thang']} - {kq['TuTru']['Ngay']} - {kq['TuTru']['Gio']}")
                print(f"⚙️ Cục: {kq['ThongTinCuc']} | Tuần Thủ: {kq['TuanThu']}")
                print(f"🔹 Thần: {c_data['Than']} | Sao: {c_data['Sao']} | Cửa: {c_data['Cua']}")
                print(f"🔹 Thiên/Địa: {c_data['Thien']} / {c_data['Dia']}")
                print("-" * 55)

                # Nếu chỉ tìm 1 kết quả gần nhất thì return, nếu tìm hết thì bỏ return


        current_time += datetime.timedelta(hours=2)


if __name__ == "__main__":
    tim_tran_phu_hop()
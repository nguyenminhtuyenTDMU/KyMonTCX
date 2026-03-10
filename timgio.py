import datetime
from kymon_logic import KyMonLapTran

# 1. KHAI BÁO LUẬT RIÊNG CHO TỪNG CUNG (2, 3, 4, 8)
DANH_SACH_CUNG_CAN_TIM = [7]

# Mapping Cung -> Địa chi (Để check Không Vong Thời)
CUNG_CHI = {
    7: ["Dậu"]
}
# Mapping Cung -> Thiên Can bị Kích Hình (Lục Nghi Kích Hình)
CUNG_KICH_HINH = {
    7: []
}
def tinh_diem_cat(thien, dia, sao, than, cua):
    diem = 0
    if thien in ["Ất", "Bính", "Đinh"]:
        diem+=1
    if dia in ["Ất", "Bính", "Đinh"]:
        diem+=1
    if sao in ["Nhậm", "Phụ","Tâm"]:
        diem+=2
    if than in ["Trực Phù", "Lục Hợp", "Cửu Thiên", "Thái Âm"]:
        diem+=2
    if cua in ["Hưu", "Sinh", "Khai"]:
        diem+=4
    return diem
def kiem_tra_cung_dat_chuan(kq, cung_id):
    """Hàm kiểm tra xem 1 cung cụ thể có đạt toàn bộ tiêu chuẩn khắt khe không"""
    cung_data = kq['Data9Cung'].get(cung_id)
    if not cung_data: return False

    cua = cung_data.get('Cua', '')
    than = cung_data.get('Than', '')
    sao = cung_data.get('Sao', '')
    thien = cung_data.get('Thien', '')
    dia = cung_data.get('Dia', '')

    # 1. BẮT BUỘC: Cảnh Môn + Trực Phù
    if cua != 'Cảnh' or than != 'Trực Phù':
        return False

    # 2. KHÔNG CÓ: Canh (trên lẫn dưới)
    if 'Canh' in thien or 'Canh' in dia:
        return False
    if 'Bạch Hổ' in than:
        return False
    # 3. KHÔNG CÓ: Nhuế (Nhu), Bồng
    if 'Nhu' in sao or 'Bồng' in sao:
        return False

    # 4. KHÔNG CÓ: Không Vong (Thời) rơi vào cung này
    tk_thoi = kq['InfoTuanKhong'].get('Thoi', [])
    chi_tai_cung = CUNG_CHI.get(cung_id, [])
    for chi in chi_tai_cung:
        if chi in tk_thoi:
            return False

    # 5. KHÔNG CÓ: Kích Hình (Thiên bàn rơi vào cung tử huyệt)
    can_chinh = thien.split("/")[0].strip() if thien else ""
    can_kich_hinh = CUNG_KICH_HINH.get(cung_id, [])
    can_dia = dia.split("/")[0].strip() if dia else ""
    can_dia_kich_hinh = CUNG_KICH_HINH.get(cung_id, [])
    if can_chinh in can_kich_hinh or can_dia in can_dia_kich_hinh:
        return False

    # if tinh_diem_cat(thien, dia, sao, than, cua)<6:
    #     return False

    return True


def tim_ngay_gio_tot_nhat():
    print("Đang tải dữ liệu thiên văn (NASA)...")
    km = KyMonLapTran()

    now = datetime.datetime.now()

    # Căn chỉnh về "giữa canh giờ" để bước nhảy 2 tiếng luôn chính xác
    hour_aligned = now.hour if now.hour % 2 != 0 else now.hour - 1
    if hour_aligned < 0:
        hour_aligned = 23
        now -= datetime.timedelta(days=1)

    current_time = now.replace(hour=hour_aligned, minute=30, second=0, microsecond=0)

    print(f"Bắt đầu dò tìm từ: {current_time.strftime('%d/%m/%Y %H:%M')}")
    print(f"Các cung mục tiêu: {DANH_SACH_CUNG_CAN_TIM}")
    print("Đang quét siêu tốc... \n")

    max_days = 365  # Quét trong 1 năm
    end_time = current_time + datetime.timedelta(days=max_days)
    so_tran_da_quet = 0

    map_ten = {7: "Đoài 7"}

    while current_time < end_time:
        y, m, d = current_time.year, current_time.month, current_time.day
        h, mi = current_time.hour, current_time.minute

        try:
            kq = km.lap_que(y, m, d, h, mi)
            so_tran_da_quet += 1
        except Exception:
            current_time += datetime.timedelta(hours=2)
            continue

        # Lặp qua các cung mục tiêu để kiểm tra
        for cung_id in DANH_SACH_CUNG_CAN_TIM:
            if kiem_tra_cung_dat_chuan(kq, cung_id):
                # NẾU TÌM THẤY -> IN RA VÀ DỪNG CHƯƠNG TRÌNH
                cung_data = kq['Data9Cung'][cung_id]

                print(f"✅ ĐÃ TÌM THẤY TRẬN ĐỒ ĐẠT CHUẨN! (Quét {so_tran_da_quet} canh giờ)")
                print("=" * 55)
                print(f"🎯 CUNG ĐÁP ỨNG: {map_ten[cung_id].upper()}")
                print(f"⏰ Thời gian: {current_time.strftime('%H:%M - Ngày %d/%m/%Y')}")
                print(
                    f"📜 Tứ Trụ: Năm {kq['TuTru']['Nam']} | Tháng {kq['TuTru']['Thang']} | Ngày {kq['TuTru']['Ngay']} | Giờ {kq['TuTru']['Gio']}")
                print(f"⚙️ Cục Số: {kq['ThongTinCuc']} | Tuần Thủ: {kq['TuanThu']}")
                print("-" * 55)
                print("CHI TIẾT ĐỘI HÌNH:")
                print(f"  • Thần: {cung_data['Than']}")
                print(f"  • Sao:  {cung_data['Sao']}")
                print(f"  • Cửa:  {cung_data['Cua']}")
                print(f"  • Thiên: {cung_data['Thien']}")
                print(f"  • Địa:   {cung_data['Dia']}")
                print("=" * 55)

                 # Dừng chương trình ngay sau khi tìm thấy ngày gần nhất

        # Nhảy sang canh giờ tiếp theo (cộng 2 tiếng)
        current_time += datetime.timedelta(hours=2)

    print("❌ Rất tiếc, quét hết 1 năm vẫn không có canh giờ nào lọt qua được bộ lọc này!")


if __name__ == "__main__":
    tim_ngay_gio_tot_nhat()
import streamlit as st
from datetime import datetime
from kymon_logic import KyMonLapTran

# 1. CẤU HÌNH TRANG
st.set_page_config(
    page_title="Kỳ Môn Độn Giáp - Trương Chí Xuân",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS TÙY CHỈNH (RESPONSIVE & LAYOUT MỚI)
st.markdown("""
<style>
    /* --- GRID CONTAINER --- */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 4px;
        max-width: 900px;
        margin: 0 auto;
    }

    /* KHUNG CUNG - CƠ BẢN */
    .cung-box {
        border: 1px solid rgba(0,0,0,0.1);
        border-radius: 6px;
        height: 160px;
        position: relative;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        overflow: hidden;
    }

    /* --- MÀU NỀN THEO NGŨ HÀNH --- */
    /* Kim: Xám bạc */
    .bg-kim  { background-color: #e0e0e0; border: 1px solid #bdbdbd; } 
    
    /* Mộc: Xanh lá mạ */
    .bg-moc  { background-color: #dcedc8; border: 1px solid #a5d6a7; } 
    
    /* Thủy: Xanh da trời */
    .bg-thuy { background-color: #bbdefb; border: 1px solid #90caf9; } 
    
    /* Hỏa: Hồng cam */
    .bg-hoa  { background-color: #ffccbc; border: 1px solid #ffab91; } 
    
    /* Thổ: Vàng nâu nhạt (Be) */
    .bg-tho  { background-color: #fff59d; border: 1px solid #fff176; }

    /* --- ĐỊNH VỊ --- */
    .than-vi { 
        position: absolute; top: 5px; right: 5px; 
        font-weight: bold; font-size: 0.85em; 
    }
    .tinh-vi { 
        position: absolute; top: 18%; left: 50%; 
        transform: translateX(-50%); text-align: center; width: 100%;
        font-weight: bold; font-size: 0.9em;
    }
    .mon-vi { 
        position: absolute; bottom: 18%; left: 50%; 
        transform: translateX(-50%); text-align: center; width: 100%;
        font-weight: bold; font-size: 1.1em;
    }
    .can-thien-ban { 
        position: absolute; top: 5px; left: 5px; 
        font-weight: bold; font-size: 1em; line-height: 1;
    }
    .can-dia-ban { 
        position: absolute; bottom: 5px; left: 5px; 
        font-weight: bold; font-size: 1em; line-height: 1;
    }
    .cung-so {
        position: absolute; bottom: 2px; right: 5px;
        font-size: 0.7em; color: rgba(0,0,0,0.3); font-style: italic; pointer-events: none;
    }

    /* Tag Tứ Trụ */
    .tag-container-thien { position: absolute; top: 22px; left: 5px; display: flex; flex-direction: column; gap: 1px; }
    .tag-container-dia   { position: absolute; bottom: 22px; left: 5px; display: flex; flex-direction: column; gap: 1px; }

    /* Ký hiệu đặc biệt */
    .special-tags { 
        position: absolute; top: 22px; right: 5px; 
        text-align: right; display: flex; flex-direction: column; align-items: flex-end;
    }

    /* STYLING TAGS */
    .tag-tk { color: #d32f2f; border: 1px solid #d32f2f; border-radius: 50%; padding: 0 3px; font-size: 0.5em; font-weight: bold; background: #fff; margin-bottom: 1px;}
    .tag-ma { background-color: #fdd835; color: #000; border-radius: 2px; padding: 0 3px; font-size: 0.5em; font-weight: bold; margin-bottom: 1px;}

    .tag-mo { font-size: 0.6em; color: #78909c; vertical-align: super; margin-left: 1px; }
    .tag-mo-mon { font-size: 0.6em; color: #546e7a; font-weight: normal; margin-left: 2px;}

    .tag-can { font-size: 0.5em; border-radius: 2px; padding: 0 3px; color: white; text-align: center; width: 15px;}
    .tag-y { background-color: #795548; } .tag-m { background-color: #2e7d32; }
    .tag-d { background-color: #ef6c00; } .tag-h { background-color: #c62828; }

    /* MÀU CHỮ */
    .hanh-kim { color: #455a64; } .hanh-moc { color: #1b5e20; } 
    .hanh-thuy { color: #01579b; } .hanh-hoa { color: #b71c1c; } .hanh-tho { color: #4e342e; } 

    /* HEADER */
    .tu-tru-box { background-color: #fff; padding: 10px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 10px; }
    .tu-tru-item { font-size: 1.1em; font-weight: bold; }
    .tu-tru-label { font-size: 0.7em; color: #777; text-transform: uppercase; }

    @media only screen and (max-width: 600px) {
        .cung-box { height: 120px; }
        .tinh-vi, .can-thien-ban, .can-dia-ban { font-size: 0.8em; }
        .mon-vi { font-size: 0.9em; }
        .than-vi { font-size: 0.7em; }
    }
</style>
""", unsafe_allow_html=True)


# 3. HÀM HỖ TRỢ
def lay_class_mau(ten_thanh_phan):
    if not ten_thanh_phan: return ""
    kim = ["Tâm", "Trụ", "Khai", "Kinh", "Canh", "Tân", "Thân", "Dậu", "Càn", "Đoài", "Kim"]
    moc = ["Xung", "Phụ", "Thương", "Đỗ", "Giáp", "Ất", "Dần", "Mão", "Chấn", "Tốn", "Mộc"]
    thuy = ["Bồng", "Hưu", "Nhâm", "Quý", "Hợi", "Tý", "Khảm", "Thủy"]
    hoa = ["Anh", "Cảnh", "Bính", "Đinh", "Tỵ", "Ngọ", "Ly", "Hỏa"]
    tho = ["Nhu", "Cầm", "Nhậm", "Sinh", "Tử", "Mậu", "Kỷ", "Thìn", "Tuất", "Sửu", "Mùi", "Khôn", "Cấn", "Trung", "Thổ"]

    ten_goc = ten_thanh_phan.split("/")[0].strip()
    if ten_goc in kim: return "hanh-kim"
    if ten_goc in moc: return "hanh-moc"
    if ten_goc in thuy: return "hanh-thuy"
    if ten_goc in hoa: return "hanh-hoa"
    if ten_goc in tho: return "hanh-tho"
    return ""


def lay_bg_cung(cung_id):
    if cung_id == 1: return "bg-thuy"
    if cung_id in [3, 4]: return "bg-moc"
    if cung_id == 9: return "bg-hoa"
    if cung_id in [2, 5, 8]: return "bg-tho"
    if cung_id in [6, 7]: return "bg-kim"
    return ""


def xu_ly_don_giap(can_chi_str):
    parts = can_chi_str.split()
    can, chi = parts[0], parts[1]
    if can == "Giáp":
        return {"Tý": "Mậu", "Tuất": "Kỷ", "Thân": "Canh", "Ngọ": "Tân", "Thìn": "Nhâm", "Dần": "Quý"}.get(chi, can)
    return can


def tao_tag_tu_tru(can_tai_cung, tu_tru_dict):
    if not can_tai_cung: return ""
    html_tags = ""
    cac_can = can_tai_cung.split('/')
    for c in cac_can:
        c = c.strip()
        if c == tu_tru_dict.get('Y'): html_tags += '<div class="tag-can tag-y">Y</div>'
        if c == tu_tru_dict.get('M'): html_tags += '<div class="tag-can tag-m">M</div>'
        if c == tu_tru_dict.get('D'): html_tags += '<div class="tag-can tag-d">D</div>'
        if c == tu_tru_dict.get('H'): html_tags += '<div class="tag-can tag-h">H</div>'
    return html_tags


def render_cung_html_string(data, cung_id, ten_cung_bat_quai, tu_tru_dict):
    if not data: return ""

    thien = data['Thien'] or ""
    dia = data['Dia'] or ""
    sao = data['Sao'] or ""
    cua = data['Cua'] or ""
    than = data['Than'] or ""
    pt = data.get('PhanTich', {})

    is_tk = pt.get('TuanKhong', False)
    is_ma = pt.get('DichMa', False)
    vuong_suy_sao = pt.get('VuongSuyThang', "")
    ts_thien = pt.get('TruongSinh', '')
    is_mon_mo = pt.get('MonNhapMo', False)

    tag_thien = tao_tag_tu_tru(thien, tu_tru_dict)

    html_sao_status = f'<div style="font-size:0.7em; color:#888; font-weight:normal;">({vuong_suy_sao})</div>' if vuong_suy_sao else ""
    html_mo_thien = '<span class="tag-mo">Mộ</span>' if ts_thien == 'Mộ' else ''
    html_mo_mon = '<span class="tag-mo-mon">[Mộ]</span>' if is_mon_mo else ''

    html_tk = '<div class="tag-tk">TK</div>' if is_tk else ''
    html_ma = '<div class="tag-ma">MÃ</div>' if is_ma else ''

    cls_sao = lay_class_mau(sao)
    cls_cua = lay_class_mau(cua)
    cls_thien = lay_class_mau(thien)
    cls_dia = lay_class_mau(dia)
    cls_bg = lay_bg_cung(cung_id)

    # QUAN TRỌNG: Viết HTML sát lề, không thụt dòng trong f-string
    return f"""
<div class="cung-box {cls_bg}">
    <div class="cung-so">{ten_cung_bat_quai}</div>
    <div class="than-vi hanh-hoa">{than}</div>
    <div class="tinh-vi {cls_sao}">{sao}{html_sao_status}</div>
    <div class="mon-vi {cls_cua}">{cua}{html_mo_mon}</div>
    <div class="can-thien-ban {cls_thien}">{thien}{html_mo_thien}</div>
    <div class="tag-container-thien">{tag_thien}</div>
    <div class="can-dia-ban {cls_dia}">{dia}</div>
    <div class="special-tags">{html_tk}{html_ma}</div>
</div>
"""


# 4. GIAO DIỆN CHÍNH
def main():
    st.title("🔮 Kỳ Môn Độn Giáp - Trương Chí Xuân")

    with st.sidebar:
        st.header("1. Nhập Thời Gian")
        now = datetime.now()

        c1, c2, c3 = st.columns(3)
        with c1: day = st.number_input("Ngày", 1, 31, now.day)
        with c2: month = st.number_input("Tháng", 1, 12, now.month)
        with c3: year = st.number_input("Năm", 1900, 2100, now.year)

        c4, c5 = st.columns(2)
        with c4: hour = st.number_input("Giờ", 0, 23, now.hour)
        with c5: minute = st.number_input("Phút", 0, 59, now.minute)

        btn_lap = st.button("Lập Trận Đồ", type="primary", use_container_width=True)

    if btn_lap:
        try:
            valid_date = datetime(year, month, day, hour, minute)
        except ValueError:
            st.error("Ngày tháng không hợp lệ!")
            return

        km = KyMonLapTran()
        kq = km.lap_que(year, month, day, hour, minute)

        if isinstance(kq, str):
            st.error(kq)
            return

        info_lich = km.lich.get_lunar_date(day, month, year)
        lday, lmonth, lyear, _ = info_lich
        cc_full = km.lich.get_can_chi(day, month, year, lmonth, lyear, hour=hour)

        tu_tru_dict = {
            'Y': xu_ly_don_giap(cc_full['Nam']),
            'M': xu_ly_don_giap(cc_full['Thang']),
            'D': xu_ly_don_giap(cc_full['Ngay']),
            'H': xu_ly_don_giap(cc_full['Gio'])
        }

        st.markdown(f"""
        <div class="tu-tru-box">
            <div style="display: flex; justify-content: space-around;">
                <div><div class="tu-tru-label">Năm</div><div class="tu-tru-item {lay_class_mau(cc_full['Nam'].split()[0])}">{cc_full['Nam']} <span style="font-size:0.7em; color:#777">({tu_tru_dict['Y']})</span></div></div>
                <div><div class="tu-tru-label">Tháng</div><div class="tu-tru-item {lay_class_mau(cc_full['Thang'].split()[0])}">{cc_full['Thang']} <span style="font-size:0.7em; color:#777">({tu_tru_dict['M']})</span></div></div>
                <div><div class="tu-tru-label">Ngày</div><div class="tu-tru-item {lay_class_mau(cc_full['Ngay'].split()[0])}">{cc_full['Ngay']} <span style="font-size:0.7em; color:#777">({tu_tru_dict['D']})</span></div></div>
                <div><div class="tu-tru-label">Giờ</div><div class="tu-tru-item {lay_class_mau(cc_full['Gio'].split()[0])}">{cc_full['Gio']} <span style="font-size:0.7em; color:#777">({tu_tru_dict['H']})</span></div></div>
            </div>
            <div style="margin-top: 10px; font-size: 1em; color: #333; text-align: center;">
                <b>{kq['CanChi'].split('|')[-1].replace('Tiết ', '').strip()}</b> &bull; 
                <b>{kq['ThongTinCuc']}</b> &bull; 
                Tuần Thủ: <b>{kq['TuanThu']}</b> &bull; 
                {kq['TrucPhuSu']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # GRID LAYOUT (Render 1 cục HTML)
        grid_matrix = [[4, 9, 2], [3, 5, 7], [8, 1, 6]]
        map_ten_cung = {
            1: "Khảm 1", 2: "Khôn 2", 3: "Chấn 3", 4: "Tốn 4",
            5: "Trung 5", 6: "Càn 6", 7: "Đoài 7", 8: "Cấn 8", 9: "Ly 9"
        }
        data_9_cung = kq['Data9Cung']

        # Tạo chuỗi HTML lớn
        full_html = '<div class="grid-container">'
        for row in grid_matrix:
            for cung_id in row:
                ten_cung = map_ten_cung.get(cung_id)
                cell_html = render_cung_html_string(data_9_cung.get(cung_id), cung_id, ten_cung, tu_tru_dict)
                full_html += cell_html
        full_html += '</div>'

        # In ra 1 lần duy nhất
        st.markdown(full_html, unsafe_allow_html=True)

        st.caption("Chú thích: Màu nền thể hiện Ngũ hành cung. Kích thước chữ tự động điều chỉnh.")


if __name__ == "__main__":
    main()
import streamlit as st
import json
import streamlit.components.v1 as components
from datetime import datetime
import pytz
from kymon_logic import KyMonLapTran
from kymon_nien_nguyet_nhat import lap_nien_gia, lap_nguyet_gia, lap_nhat_gia
import qimen
import pprint
# Lưu ý: Thêm CSS cho badge TK Nhật/Thời
st.set_page_config(page_title="Kỳ Môn Độn Giáp", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    /* CSS BỔ SUNG CHO 2 LOẠI TUẦN KHÔNG */
    .badge-tk-n { background-color: #c62828; color: white; border-radius: 3px; padding: 0 3px; font-size: 0.8em; margin-left: 2px; } /* Đỏ đậm - Ngày */
    .badge-tk-g { background-color: #ef6c00; color: white; border-radius: 3px; padding: 0 3px; font-size: 0.8em; margin-left: 2px; } /* Cam đậm - Giờ */
    .badge-ma   { background-color: #fdd835; color: black; border-radius: 3px; padding: 0 3px; font-size: 0.8em; margin-left: 2px; }
    /* --- GRID CONTAINER --- */
    .grid-container { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; max-width: 950px; margin: 0 auto; }
    .cung-box { border: 1px solid rgba(0,0,0,0.15); border-radius: 4px; height: 170px; position: relative; box-shadow: 0 2px 4px rgba(0,0,0,0.08); overflow: hidden; }
    .bg-kim { background-color: #eeeeee; border: 1px solid #bdbdbd; } .bg-moc { background-color: #e8f5e9; border: 1px solid #a5d6a7; } .bg-thuy { background-color: #e1f5fe; border: 1px solid #81d4fa; } .bg-hoa { background-color: #ffebee; border: 1px solid #ef9a9a; } .bg-tho { background-color: #fff9c4; border: 1px solid #fff59d; }
    .dia-chi-container { position: absolute; bottom: 0; left: 0; width: 100%; height: 24px; background-color: rgba(255,255,255,0.6); border-top: 1px dotted rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center; padding: 0 5px; font-size: 0.7em; font-weight: bold; color: #555; }
    .chi-item { display: flex; align-items: center; gap: 2px; }
    .than-vi { position: absolute; top: 4px; right: 4px; font-weight: bold; font-size: 0.8em; }
    .tinh-vi { position: absolute; top: 25px; left: 50%; transform: translateX(-50%); text-align: center; width: 100%; font-weight: bold; font-size: 0.85em; }
    .mon-vi { position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%); text-align: center; width: 100%; font-weight: bold; font-size: 1.1em; }
    .can-thien-ban { position: absolute; top: 4px; left: 4px; font-weight: bold; font-size: 1.1em; line-height: 1; }
    .can-dia-ban { position: absolute; bottom: 30px; left: 4px; font-weight: bold; font-size: 1.1em; line-height: 1; }
    .cung-so { position: absolute; bottom: 26px; right: 4px; font-size: 0.65em; color: rgba(0,0,0,0.4); font-style: italic; pointer-events: none; }
    .tag-container-thien { position: absolute; top: 22px; left: 4px; display: flex; flex-direction: column; gap: 1px; }
    .tag-can { font-size: 0.5em; border-radius: 2px; padding: 0 3px; color: white; text-align: center; width: 16px;}
    .tag-y { background-color: #795548; } .tag-m { background-color: #2e7d32; } .tag-d { background-color: #ef6c00; } .tag-h { background-color: #c62828; }
    .tag-mo { font-size: 0.6em; color: #78909c; vertical-align: super; margin-left: 1px; } .tag-mo-mon { font-size: 0.6em; color: #546e7a; font-weight: normal; margin-left: 2px;}
    .hanh-kim { color: #455a64; } .hanh-moc { color: #1b5e20; } .hanh-thuy { color: #01579b; } .hanh-hoa { color: #b71c1c; } .hanh-tho { color: #4e342e; } 
    .tu-tru-box { background-color: #fff; padding: 10px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 10px; }
    .tu-tru-item { font-size: 1.1em; font-weight: bold; }
    .tu-tru-label { font-size: 0.7em; color: #777; text-transform: uppercase; }
    @media only screen and (max-width: 600px) { .cung-box { height: 130px; } .tinh-vi, .can-thien-ban, .can-dia-ban { font-size: 0.8em; } .mon-vi { font-size: 0.9em; bottom: 28px; } .can-dia-ban { bottom: 28px; } .tag-container-dia { bottom: 42px; } .dia-chi-container { height: 20px; font-size: 0.65em; } }
</style>
""", unsafe_allow_html=True)


# ... (Hàm lay_class_mau, lay_bg_cung, xu_ly_don_giap, tao_tag_tu_tru GIỮ NGUYÊN) ...
# COPY LẠI CÁC HÀM NÀY TỪ BÀI TRƯỚC
def lay_class_mau(ten):
    if not ten: return ""
    ten = ten.split("/")[0].strip()
    if ten in ["Tâm", "Trụ", "Khai", "Kinh", "Canh", "Tân", "Thân", "Dậu", "Càn", "Đoài"]: return "hanh-kim"
    if ten in ["Xung", "Phụ", "Thương", "Đỗ", "Giáp", "Ất", "Dần", "Mão", "Chấn", "Tốn"]: return "hanh-moc"
    if ten in ["Bồng", "Hưu", "Nhâm", "Quý", "Hợi", "Tý", "Khảm"]: return "hanh-thuy"
    if ten in ["Anh", "Cảnh", "Bính", "Đinh", "Tỵ", "Ngọ", "Ly"]: return "hanh-hoa"
    return "hanh-tho"


def lay_bg_cung(id):
    return {1: "bg-thuy", 9: "bg-hoa", 3: "bg-moc", 4: "bg-moc", 6: "bg-kim", 7: "bg-kim"}.get(id, "bg-tho")


def xu_ly_don_giap(cc):
    p = cc.split()
    if p[0] == "Giáp": return {"Tý": "Mậu", "Tuất": "Kỷ", "Thân": "Canh", "Ngọ": "Tân", "Thìn": "Nhâm",
                               "Dần": "Quý"}.get(p[1], p[0])
    return p[0]


def tao_tag_tu_tru(can, tu_tru):
    if not can: return ""
    h = ""
    for c in can.split('/'):
        c = c.strip()
        if c == tu_tru['Y']: h += '<div class="tag-can tag-y">Y</div>'
        if c == tu_tru['M']: h += '<div class="tag-can tag-m">M</div>'
        if c == tu_tru['D']: h += '<div class="tag-can tag-d">D</div>'
        if c == tu_tru['H']: h += '<div class="tag-can tag-h">H</div>'
    return h


# --- HÀM RENDER ĐỊA CHI VỚI 2 LOẠI TUẦN KHÔNG ---
def render_vong_dia_chi(cung_id, tk_nhat, tk_thoi, dich_ma_chi):
    if cung_id == 5: return '<div class="dia-chi-container"></div>'
    map_cung_chi = {1: ["Tý"], 8: ["Sửu", "Dần"], 3: ["Mão"], 4: ["Thìn", "Tỵ"], 9: ["Ngọ"], 2: ["Mùi", "Thân"],
                    7: ["Dậu"], 6: ["Tuất", "Hợi"]}

    ds_chi = map_cung_chi.get(cung_id, [])
    html = ""
    for chi in ds_chi:
        badges = ""
        # Check Nhật Không
        if chi in tk_nhat: badges += '<span class="badge-tk-n">TK(N)</span>'
        # Check Thời Không
        if chi in tk_thoi: badges += '<span class="badge-tk-g">TK(G)</span>'
        # Check Dịch Mã
        if chi == dich_ma_chi: badges += '<span class="badge-ma">MÃ</span>'

        cls_op = "badge-normal" if badges == "" else ""
        cls_col = lay_class_mau(chi)
        html += f'<div class="chi-item {cls_op}"><span class="{cls_col}">{chi}</span>{badges}</div>'

    just = "center" if len(ds_chi) == 1 else "space-between"
    return f'<div class="dia-chi-container" style="justify-content:{just};">{html}</div>'


def render_cung_html_string(data, cung_id, ten_cung, tu_tru, tk_nhat, tk_thoi, dich_ma):
    if not data: return ""
    thien, dia = data['Thien'] or "", data['Dia'] or ""
    sao, cua, than = data['Sao'] or "", data['Cua'] or "", data['Than'] or ""
    pt = data.get('PhanTich', {})

    # Render các thành phần
    tag_thien = tao_tag_tu_tru(thien, tu_tru)

    vs_cung = pt.get('SaoVuongSuyCung', "")
    vs_thang = pt.get('SaoVuongSuyThang', "")
    vs_parts = [p for p in [vs_cung, vs_thang] if p]
    html_vs = f'<div style="font-size:0.7em; color:#888;">({" | ".join(vs_parts)})</div>' if vs_parts else ""

    truong_sinh = pt.get('CanTruongSinh') or ""
    mo_thien = f'<span class="tag-mo">{truong_sinh}</span>' if truong_sinh else ""
    mo_mon = '<span class="tag-mo-mon">[Mộ]</span>' if pt.get('MonNhapMo') else ''

    html_chi = render_vong_dia_chi(cung_id, tk_nhat, tk_thoi, dich_ma)

    # Class màu
    cls_s = lay_class_mau(sao);
    cls_c = lay_class_mau(cua)
    cls_t = lay_class_mau(thien);
    cls_d = lay_class_mau(dia)
    cls_bg = lay_bg_cung(cung_id)

    return f"""
<div class="cung-box {cls_bg}">
    <div class="cung-so">{ten_cung}</div>
    <div class="than-vi hanh-hoa">{than}</div>
    <div class="tinh-vi {cls_s}">{sao}{html_vs}</div>
    <div class="mon-vi {cls_c}">{cua}{mo_mon}</div>
    <div class="can-thien-ban {cls_t}">{thien}{mo_thien}</div>
    <div class="tag-container-thien">{tag_thien}</div>
    <div class="can-dia-ban {cls_d}">{dia}</div>
    {html_chi}
</div>
"""


MAP_TEN_CUNG = {1: "Khảm 1", 2: "Khôn 2", 3: "Chấn 3", 4: "Tốn 4", 5: "Trung 5",
                6: "Càn 6", 7: "Đoài 7", 8: "Cấn 8", 9: "Ly 9"}


def render_ban_9cung(data9cung, tu_tru_dict, tk_nhat=None, tk_thoi=None, dich_ma=""):
    tk_nhat = tk_nhat or []
    tk_thoi = tk_thoi or []
    full_html = '<div class="grid-container">'
    for r in [[4, 9, 2], [3, 5, 7], [8, 1, 6]]:
        for cid in r:
            full_html += render_cung_html_string(
                data9cung.get(cid), cid, MAP_TEN_CUNG.get(cid),
                tu_tru_dict, tk_nhat, tk_thoi, dich_ma
            )
    full_html += '</div>'
    st.markdown(full_html, unsafe_allow_html=True)


# --- RENDER CHO ENGINE qimen.py (thuật toán chuyển bàn, có ám can) ---
def render_cung_qimen_html(p, cung_id, ten_cung):
    if cung_id == 5:
        yy_label = "Dương Độn" if p.yy == "阳" else "Âm Độn"
        return f"""
<div class="cung-box bg-tho">
    <div class="cung-so">{ten_cung}</div>
    <div style="position:absolute; top:32%; left:0; width:100%; text-align:center; font-weight:bold;">
        CỤC {p.qmju}<br>({yy_label})<br>
        <span style="font-size:0.75em; font-weight:normal; color:#555;">
            Nguyệt Lệnh: {p.chi_nguyet} ({p.hanh_nguyet})
        </span>
    </div>
</div>
"""
    god = qimen.SHEN_VN.get(p.shenpan[cung_id].strip(), "-")
    star = qimen.XING_VN.get(p.xinpan[cung_id].strip(), "-")
    gate = qimen.MEN_VN.get(p.menpan[cung_id].strip(), "-")
    thien = qimen.gan_vn(p.tiangan[cung_id])
    am = qimen.gan_vn(p.angan[cung_id])
    dia = qimen.gan_vn(p.digan[cung_id])

    marks = []
    if p.kong[cung_id] == "O":
        marks.append('<span class="badge-tk-n">Không</span>')
    for zi, gong in enumerate(qimen.zhi2gong):
        if p.maw[zi] == "马" and gong == cung_id:
            marks.append('<span class="badge-ma">Mã</span>')
    html_marks = "".join(marks)

    vs_cung = p.cung_vuong_suy.get(cung_id, "")
    html_vs = f'<div style="font-size:0.7em; color:#888;">({vs_cung})</div>' if vs_cung else ""

    cls_s = lay_class_mau(star)
    cls_c = lay_class_mau(gate)
    cls_t = lay_class_mau(thien)
    cls_d = lay_class_mau(dia)
    cls_bg = lay_bg_cung(cung_id)

    return f"""
<div class="cung-box {cls_bg}">
    <div class="cung-so">{ten_cung}</div>
    <div class="than-vi hanh-hoa">{god}</div>
    <div class="tinh-vi {cls_s}">{star}{html_vs}</div>
    <div class="mon-vi {cls_c}">{gate}</div>
    <div class="can-thien-ban {cls_t}">{thien}</div>
    <div class="can-dia-ban {cls_d}">{dia}</div>
    <div class="dia-chi-container" style="justify-content:center;">
        <span style="font-size:0.75em;color:#555;">Ám: {am}</span>{html_marks}
    </div>
</div>
"""


def render_ban_9cung_qimen(p):
    full_html = '<div class="grid-container">'
    for r in [[4, 9, 2], [3, 5, 7], [8, 1, 6]]:
        for cid in r:
            full_html += render_cung_qimen_html(p, cid, MAP_TEN_CUNG.get(cid))
    full_html += '</div>'
    st.markdown(full_html, unsafe_allow_html=True)


def qimen_pan_to_dict(p):
    """Chuyển kết quả paipan() (đã dịch tiếng Việt) sang dict để export JSON, cùng kiểu với KyMonLapTran.lap_que()."""
    yy_label = "Dương Độn" if p.yy == "阳" else "Âm Độn"
    zhifu_vn = qimen.XING_VN.get(p.zhifu, "Cầm")
    zhishi_vn = qimen.MEN_VN.get(p.zhishi, "-")
    xunkong1, xunkong2 = p.xunkong

    data9cung = {}
    for g in range(1, 10):
        if g == 5:
            data9cung[g] = {}
            continue
        marks = []
        if p.kong[g] == "O": marks.append("Không")
        for zi, gong in enumerate(qimen.zhi2gong):
            if p.maw[zi] == "马" and gong == g: marks.append("Mã")
        data9cung[g] = {
            "Than": qimen.SHEN_VN.get(p.shenpan[g].strip(), "-"),
            "Sao": qimen.XING_VN.get(p.xinpan[g].strip(), "-"),
            "Cua": qimen.MEN_VN.get(p.menpan[g].strip(), "-"),
            "Thien": qimen.gan_vn(p.tiangan[g]),
            "Am": qimen.gan_vn(p.angan[g]),
            "Dia": qimen.gan_vn(p.digan[g]),
            "VuongSuyCung": p.cung_vuong_suy.get(g, ""),
            "Marks": marks,
        }

    tY, tM, tD, tH, tMin = p.ngaygio
    return {
        "GioBacKinhLapTran": f"{tD:02d}/{tM:02d}/{tY} {tH:02d}:{tMin:02d}",
        "TuTru": {
            "Nam": qimen.cyclical_vn(p.cY),
            "Thang": qimen.cyclical_vn(p.cM),
            "Ngay": qimen.cyclical_vn(p.cD),
            "Gio": qimen.cyclical_vn(p.gio_tru),
        },
        "TietKhi": qimen.solarTerm_vn[p.tmp2],
        "ThongTinCuc": f"{yy_label} {p.qmju} Cục",
        "TuanThu": qimen.cyclical_vn(p.xun_num),
        "TrucPhuSu": f"Trực Phù: {zhifu_vn} | Trực Sử: {zhishi_vn}",
        "KhongVong": f"{qimen.Zhi_vn[xunkong1]}-{qimen.Zhi_vn[xunkong2]}",
        "DichMa": qimen.Zhi_vn[p.maxing],
        "NguyetLenh": f"{p.chi_nguyet} ({p.hanh_nguyet})",
        "Data9Cung": data9cung,
    }


def render_export_buttons(kq, label_prefix):
    json_string = json.dumps(kq, ensure_ascii=False, indent=2)
    dict_string = pprint.pformat(kq, indent=4, sort_dicts=False)
    st.download_button(
        label="⬇️ Tải JSON trận",
        data=json_string,
        file_name=f"{label_prefix}.json",
        mime="application/json"
    )
    with st.expander("📋 Xem và Copy JSON"):
        st.code(json_string, language="json")
    with st.expander("📋 Xem và Copy Dictionary (Chuẩn Python)"):
        st.code(dict_string, language="python")


def main():
    st.title("🔮 Kỳ Môn Độn Giáp - Trương Chí Xuân")

    tz_vn = pytz.timezone('Asia/Ho_Chi_Minh')
    now = datetime.now(tz_vn)

    with st.sidebar:
        loai_cuc = st.radio(
            "Chọn Loại Cục",
            ["Thời Gia", "Thời Gia (Chuyển Bàn)", "Nhật Gia", "Nguyệt Gia", "Niên Gia"],
        )

        st.header("Nhập Thời Gian")
        c1, c2, c3 = st.columns(3)
        with c1: d = st.number_input("Ngày", 1, 31, now.day)
        with c2: m = st.number_input("Tháng", 1, 12, now.month)
        with c3: y = st.number_input("Năm", 1900, 2100, now.year)

        if loai_cuc in ("Thời Gia", "Thời Gia (Chuyển Bàn)"):
            c4, c5 = st.columns(2)
            with c4:
                h = st.number_input("Giờ", 0, 23, now.hour)
            with c5:
                mi = st.number_input("Phút", 0, 59, now.minute)
        else:
            h, mi = 12, 0

        qm_mode, qm_setju = 1, 0
        if loai_cuc == "Thời Gia (Chuyển Bàn)":
            qm_mode_label = st.selectbox(
                "Chế độ (qimen.py)",
                ["Chuẩn (Vương Phượng Lân)", "Truyền thống (Dương bàn)", "Khắc gia (+phút)", "Tự chọn Cục"],
            )
            qm_mode = {"Chuẩn (Vương Phượng Lân)": 1, "Truyền thống (Dương bàn)": 0,
                       "Khắc gia (+phút)": 2, "Tự chọn Cục": 4}[qm_mode_label]
            if qm_mode == 4:
                qm_ju_abs = st.number_input("Cục số", 1, 9, 1)
                qm_am_duong = st.radio("Âm/Dương Độn", ["Dương", "Âm"], horizontal=True)
                qm_setju = qm_ju_abs if qm_am_duong == "Dương" else -qm_ju_abs
            st.caption("Giờ nhập là giờ Việt Nam, tự động quy đổi sang giờ Bắc Kinh (+1h) trước khi lập trận.")

        btn = st.button("Lập Trận Đồ", type="primary")
        text_ld = st.text_area("Lý do")

    if not btn:
        st.markdown("---")
        # fall through to toa cung button below
    else:
        try:
            datetime(y, m, d, h, mi)
        except ValueError:
            st.error("Ngày không hợp lệ")
            return

        if loai_cuc == "Thời Gia":
            km = KyMonLapTran()
            kq = km.lap_que(y, m, d, h, mi)
            render_export_buttons(kq, f"ky_mon_thoi_{y}_{m}_{d}_{h}_{mi}")

            cc = kq['TuTru']
            tu_tru_dict = {
                'Y': xu_ly_don_giap(cc['Nam']),
                'M': xu_ly_don_giap(cc['Thang']),
                'D': xu_ly_don_giap(cc['Ngay']),
                'H': xu_ly_don_giap(cc['Gio'])
            }
            tiet = kq['CanChi'].split('|')[-1].replace('Tiết ', '').strip()
            tk_nhat = kq['InfoTuanKhong']['Nhat']
            tk_thoi = kq['InfoTuanKhong']['Thoi']
            dich_ma = km.tim_dich_ma(cc['Gio'].split()[1])

            st.markdown(f"""
            <div class="tu-tru-box">
                <div style="display:flex;justify-content:space-around;">
                    <div><div class="tu-tru-label">Năm</div><div class="tu-tru-item {lay_class_mau(cc['Nam'].split()[0])}">{cc['Nam']} <span style="font-size:0.7em;color:#777">({tu_tru_dict['Y']})</span></div></div>
                    <div><div class="tu-tru-label">Tháng</div><div class="tu-tru-item {lay_class_mau(cc['Thang'].split()[0])}">{cc['Thang']} <span style="font-size:0.7em;color:#777">({tu_tru_dict['M']})</span></div></div>
                    <div><div class="tu-tru-label">Ngày</div><div class="tu-tru-item {lay_class_mau(cc['Ngay'].split()[0])}">{cc['Ngay']} <span style="font-size:0.7em;color:#777">({tu_tru_dict['D']})</span></div></div>
                    <div><div class="tu-tru-label">Giờ</div><div class="tu-tru-item {lay_class_mau(cc['Gio'].split()[0])}">{cc['Gio']} <span style="font-size:0.7em;color:#777">({tu_tru_dict['H']})</span></div></div>
                </div>
                <div style="margin-top:10px;text-align:center;color:#000">
                    <b>{tiet}</b> &bull; <b>{kq['ThongTinCuc']}</b> &bull; Tuần Thủ: <b>{kq['TuanThu']}</b>
                </div>
                <div style="font-size:0.9em;text-align:center;color:#555;">{kq['TrucPhuSu']}</div>
                <div style="font-size:0.8em;text-align:center;margin-top:5px;">
                    <span class="badge-tk-n">Nhật Không: {', '.join(tk_nhat)}</span>
                    <span class="badge-tk-g" style="margin-left:10px">Thời Không: {', '.join(tk_thoi)}</span>
                    <span class="badge-ma" style="margin-left:10px">Mã: {dich_ma}</span>
                </div>
                <div style="margin-top:10px;text-align:center;color:#000">Lý do: {text_ld}</div>
            </div>
            """, unsafe_allow_html=True)
            render_ban_9cung(kq['Data9Cung'], tu_tru_dict, tk_nhat, tk_thoi, dich_ma)

        elif loai_cuc == "Thời Gia (Chuyển Bàn)":
            dt_vn = tz_vn.localize(datetime(y, m, d, h, mi))
            dt_bj = dt_vn.astimezone(qimen.BJ)
            p = qimen.paipan(dt_bj, yinpan=qm_mode, setju=qm_setju)
            kq_qm = qimen_pan_to_dict(p)
            render_export_buttons(kq_qm, f"ky_mon_chuyenban_{y}_{m}_{d}_{h}_{mi}")

            tt = kq_qm['TuTru']
            st.markdown(f"""
            <div class="tu-tru-box">
                <div style="display:flex;justify-content:space-around;">
                    <div><div class="tu-tru-label">Năm</div><div class="tu-tru-item">{tt['Nam']}</div></div>
                    <div><div class="tu-tru-label">Tháng</div><div class="tu-tru-item">{tt['Thang']}</div></div>
                    <div><div class="tu-tru-label">Ngày</div><div class="tu-tru-item">{tt['Ngay']}</div></div>
                    <div><div class="tu-tru-label">Giờ</div><div class="tu-tru-item">{tt['Gio']}</div></div>
                </div>
                <div style="margin-top:10px;text-align:center;color:#000">
                    <b>Tiết {kq_qm['TietKhi']}</b> &bull; <b>{kq_qm['ThongTinCuc']}</b> &bull; Tuần Thủ: <b>{kq_qm['TuanThu']}</b>
                </div>
                <div style="font-size:0.9em;text-align:center;color:#555;">{kq_qm['TrucPhuSu']}</div>
                <div style="font-size:0.8em;text-align:center;margin-top:5px;">
                    <span class="badge-tk-n">Không Vong: {kq_qm['KhongVong']}</span>
                    <span class="badge-ma" style="margin-left:10px">Mã: {kq_qm['DichMa']}</span>
                </div>
                <div style="font-size:0.75em;text-align:center;color:#888;margin-top:4px;">Giờ Bắc Kinh dùng lập trận: {kq_qm['GioBacKinhLapTran']}</div>
                <div style="margin-top:10px;text-align:center;color:#000">Lý do: {text_ld}</div>
            </div>
            """, unsafe_allow_html=True)
            render_ban_9cung_qimen(p)

        elif loai_cuc == "Nhật Gia":
            kq = lap_nhat_gia(y, m, d)
            render_export_buttons(kq, f"ky_mon_nhat_{y}_{m}_{d}")
            can_ngay = kq['CanChiNgay'].split()[0]
            tu_tru_dict = {'Y': '', 'M': '', 'D': can_ngay, 'H': ''}
            st.markdown(f"""
            <div class="tu-tru-box">
                <div style="text-align:center;font-size:1.1em;font-weight:bold;color:#000">
                    Nhật Gia — Ngày {kq['Ngay']}
                </div>
                <div style="text-align:center;margin-top:6px;">
                    <span class="tu-tru-item {lay_class_mau(can_ngay)}">{kq['CanChiNgay']}</span>
                </div>
                <div style="margin-top:8px;text-align:center;color:#000">
                    <b>{kq['TietKhi']}</b> &bull; <b>{kq['ThongTinCuc']}</b> &bull; {kq['AmDuong']}
                </div>
                <div style="margin-top:4px;text-align:center;color:#000">
                    Tuần Thủ: <b>{kq['TuanThu']}</b>
                </div>
                <div style="font-size:0.9em;text-align:center;color:#555;">{kq['TrucPhuSu']}</div>
                <div style="margin-top:8px;text-align:center;color:#000">Lý do: {text_ld}</div>
            </div>
            """, unsafe_allow_html=True)
            render_ban_9cung(kq['Data9Cung'], tu_tru_dict)

        elif loai_cuc == "Nguyệt Gia":
            kq = lap_nguyet_gia(y, m, d)
            render_export_buttons(kq, f"ky_mon_nguyet_{y}_{m}_{d}")
            can_thang = kq['CanChiThang'].split()[0]
            tu_tru_dict = {'Y': '', 'M': can_thang, 'D': '', 'H': ''}
            st.markdown(f"""
            <div class="tu-tru-box">
                <div style="text-align:center;font-size:1.1em;font-weight:bold;color:#000">
                    Nguyệt Gia — Ngày {kq['NgayHoi']}
                </div>
                <div style="text-align:center;margin-top:6px;">
                    <span class="tu-tru-item {lay_class_mau(can_thang)}">Tháng: {kq['CanChiThang']}</span>
                </div>
                <div style="margin-top:8px;text-align:center;color:#000">
                    <b>{kq['TietKhi']}</b> &bull; <b>{kq['ThongTinCuc']}</b>
                </div>
                <div style="margin-top:4px;text-align:center;color:#000">
                    Tuần Thủ: <b>{kq['TuanThu']}</b>
                </div>
                <div style="font-size:0.9em;text-align:center;color:#555;">{kq['TrucPhuSu']}</div>
                <div style="margin-top:8px;text-align:center;color:#000">Lý do: {text_ld}</div>
            </div>
            """, unsafe_allow_html=True)
            render_ban_9cung(kq['Data9Cung'], tu_tru_dict)

        elif loai_cuc == "Niên Gia":
            kq = lap_nien_gia(y)
            render_export_buttons(kq, f"ky_mon_nien_{y}")
            can_nam = kq['CanChiNam'].split()[0]
            tu_tru_dict = {'Y': can_nam, 'M': '', 'D': '', 'H': ''}
            st.markdown(f"""
            <div class="tu-tru-box">
                <div style="text-align:center;font-size:1.1em;font-weight:bold;color:#000">
                    Niên Gia — Năm {kq['Nam']}
                </div>
                <div style="text-align:center;margin-top:6px;">
                    <span class="tu-tru-item {lay_class_mau(can_nam)}">{kq['CanChiNam']}</span>
                    &nbsp;—&nbsp; {kq['TamNguyen']} Nguyên
                </div>
                <div style="margin-top:8px;text-align:center;color:#000">
                    <b>{kq['ThongTinCuc']}</b>
                </div>
                <div style="margin-top:4px;text-align:center;color:#000">
                    Tuần Thủ: <b>{kq['TuanThu']}</b>
                </div>
                <div style="font-size:0.9em;text-align:center;color:#555;">{kq['TrucPhuSu']}</div>
                <div style="margin-top:8px;text-align:center;color:#000">Lý do: {text_ld}</div>
            </div>
            """, unsafe_allow_html=True)
            render_ban_9cung(kq['Data9Cung'], tu_tru_dict)

        st.markdown("---")

    components.html(
        """
        <button onclick="laySo()" style="width:100%; padding:10px 15px; background-color:#ff4b4b; color:white; border:none; border-radius:6px; font-weight:600; cursor:pointer; font-family:sans-serif; font-size: 14px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            🎯 LẤY SỐ TỎA CUNG (Giây hiện tại)
        </button>
        <div id="kq" style="margin-top:12px; text-align:center; font-family:sans-serif; color:#31333F; font-size:15px;"></div>

        <script>
            const mapCung = {1: "Khảm 1", 2: "Khôn 2", 3: "Chấn 3", 4: "Tốn 4", 5: "Trung 5", 6: "Càn 6", 7: "Đoài 7", 8: "Cấn 8", 9: "Ly 9"};
            function laySo() {
                let s = new Date().getSeconds();
                let cung = s % 9 || 9; // Chia 9 lấy dư, nếu dư 0 thì là cung 9
                document.getElementById('kq').innerHTML = "Giây <b>" + s + "</b> ➔ Ứng vào: <b><span style='color:#d32f2f; font-size:18px;'>" + mapCung[cung] + "</span></b>";
            }
        </script>
        """,
        height=90
    )

if __name__ == "__main__":
    main()

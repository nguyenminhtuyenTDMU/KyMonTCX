# main.py
"""
App Kỳ Môn Độn Giáp offline cho Desktop (Windows/macOS/Linux) và Mobile (Android/iOS), viết bằng Flet.
Dùng chung engine với app Streamlit qua kymon_view.lap_tran — không cần mạng, không cần Skyfield.

Chạy thử trên máy:   flet run main.py
Build:               flet build apk | aab | ipa | windows | macos | linux   (xem README)
"""
import json
import traceback
from datetime import datetime

import flet as ft

import tz_vn
from kymon_view import LOAI_CUC, QM_MODES, LUOI_CUNG, MAP_TEN_CUNG, lap_tran, lay_hanh

MAU_HANH = {"kim": "#455a64", "moc": "#1b5e20", "thuy": "#01579b", "hoa": "#b71c1c", "tho": "#4e342e", "": "#000000"}
NEN_CUNG = {"kim": ("#eeeeee", "#bdbdbd"), "moc": ("#e8f5e9", "#a5d6a7"), "thuy": ("#e1f5fe", "#81d4fa"),
            "hoa": ("#ffebee", "#ef9a9a"), "tho": ("#fff9c4", "#fff59d")}
MAU_BADGE = {"tk_n": ("#c62828", "#ffffff"), "tk_g": ("#ef6c00", "#ffffff"), "ma": ("#fdd835", "#000000"),
             "hinh": ("#6a1b9a", "#ffffff"), "mo": ("#424242", "#ffffff"), "bach": ("#1565c0", "#ffffff")}
MAU_TAG = {"Y": "#795548", "M": "#2e7d32", "D": "#ef6c00", "H": "#c62828"}
CHU_THICH_BADGE = {"hinh": "Kích Hình", "mo": "Nhập Mộ", "bach": "Môn Bách"}


def mau(ten_hanh):
    return MAU_HANH.get(ten_hanh, "#000000")


def badge(text, kind, size):
    bg, fg = MAU_BADGE[kind]
    return ft.Container(
        content=ft.Text(text, size=size, color=fg, weight=ft.FontWeight.BOLD),
        bgcolor=bg, border_radius=3, padding=ft.Padding(3, 0, 3, 0),
        tooltip=CHU_THICH_BADGE.get(kind),
    )


def ve_cung(c, s, cao):
    """Một ô cung — bố cục giống .cung-box trong app Streamlit. s = hệ số cỡ chữ."""
    nen, vien = NEN_CUNG[c["bg"]]
    footer_h = 22 * s
    ten = ft.Text(c["ten"], size=10 * s, italic=True, color="#66000000")

    if c.get("center"):
        l1, l2, l3 = c["center"]
        noi_dung = [
            ft.Container(
                content=ft.Column([
                    ft.Text(l1, size=15 * s, weight=ft.FontWeight.BOLD, color="#000000"),
                    ft.Text(l2, size=13 * s, weight=ft.FontWeight.BOLD, color="#000000"),
                    ft.Text(l3, size=11 * s, color="#555555", text_align=ft.TextAlign.CENTER),
                ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER, tight=True),
                left=0, right=0, top=cao * 0.25,
            ),
            ft.Container(content=ten, right=4, bottom=footer_h + 2),
        ]
    else:
        sao = [ft.Text(c["sao"], size=14 * s, weight=ft.FontWeight.BOLD, color=mau(lay_hanh(c["sao"])))]
        if c["sao_note"]:
            sao.append(ft.Text(f"({c['sao_note']})", size=10 * s, color="#888888"))
        cua = [ft.TextSpan(c["cua"], ft.TextStyle(color=mau(lay_hanh(c["cua"]))))]
        if c["cua_note"]:
            cua.append(ft.TextSpan(f" [{c['cua_note']}]", ft.TextStyle(size=10 * s, color="#546e7a",
                                                                        weight=ft.FontWeight.NORMAL)))
        thien = [ft.TextSpan(c["thien"], ft.TextStyle(color=mau(lay_hanh(c["thien"]))))]
        if c["thien_note"]:
            thien.append(ft.TextSpan(f" {c['thien_note']}", ft.TextStyle(size=9 * s, color="#78909c",
                                                                          weight=ft.FontWeight.NORMAL)))
        tags = [ft.Container(content=ft.Text(t, size=8 * s, color="#ffffff", text_align=ft.TextAlign.CENTER),
                             bgcolor=MAU_TAG[t], border_radius=2, width=16 * s) for t in c["tags"]]

        # Thanh đáy: chỉ tên địa chi (hoặc "Ám: X"); nhãn Không/Mã/Hình/Mộ/Bách đặt ở khoảng trống giữa ô,
        # tự xuống dòng để cung nhiều nhãn (tối đa 5) vẫn hiện đủ.
        if c["footer"]:
            items = [ft.Text(f["text"], size=11 * s, weight=ft.FontWeight.BOLD, color=mau(f["hanh"]))
                     for f in c["footer"]]
            canh = ft.MainAxisAlignment.CENTER if len(items) == 1 else ft.MainAxisAlignment.SPACE_BETWEEN
            nhom = [f for f in c["footer"] if f["badges"]]
            nhan = []
            for f in nhom:
                cum = [badge(t, k, 9 * s) for t, k in f["badges"]]
                if len(c["footer"]) > 1:  # cung 2 chi: ghi rõ nhãn thuộc chi nào, chi + nhãn không bị tách dòng
                    cum.insert(0, ft.Text(f["text"], size=9 * s, weight=ft.FontWeight.BOLD, color=mau(f["hanh"])))
                nhan.append(ft.Row(cum, spacing=2, tight=True, wrap=True, alignment=ft.MainAxisAlignment.CENTER))
        else:
            items = [ft.Text(c["footer_text"], size=11 * s, color="#555555")] if c["footer_text"] else []
            canh = ft.MainAxisAlignment.CENTER
            nhan = [badge(t, k, 9 * s) for t, k in c["footer_badges"]]

        noi_dung = [
            ft.Container(content=ten, right=4, bottom=footer_h + 2),
            ft.Container(content=ft.Text(c["than"], size=12 * s, weight=ft.FontWeight.BOLD, color=MAU_HANH["hoa"]),
                         top=4, right=4),
            ft.Container(content=ft.Column(sao, spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                           tight=True),
                         top=24 * s, left=0, right=0),
            # Cửa đặt cao hơn can Địa bàn để can dài (vd "Mậu,Tân") không đè lên tên Cửa
            ft.Container(content=ft.Text(spans=cua, size=16 * s, weight=ft.FontWeight.BOLD,
                                         text_align=ft.TextAlign.CENTER),
                         bottom=footer_h + 6 + 18 * s, left=0, right=0),
            ft.Container(content=ft.Text(spans=thien, size=16 * s, weight=ft.FontWeight.BOLD), top=4, left=4),
            ft.Container(content=ft.Column(tags, spacing=1, tight=True), top=24 * s, left=4),
            ft.Container(content=ft.Text(c["dia"], size=16 * s, weight=ft.FontWeight.BOLD,
                                         color=mau(lay_hanh(c["dia"]))),
                         bottom=footer_h + 6, left=4),
            ft.Container(
                content=ft.Row(nhan, alignment=ft.MainAxisAlignment.CENTER, spacing=3, run_spacing=2, wrap=True,
                               vertical_alignment=ft.CrossAxisAlignment.CENTER),
                left=4, right=4, top=cao * 0.33, bottom=footer_h + 6 + 40 * s,
                alignment=ft.Alignment.CENTER,
            ),
            ft.Container(
                content=ft.Row(items, alignment=canh, spacing=4, wrap=False),
                bgcolor="#99ffffff", left=0, right=0, bottom=0, height=footer_h,
                padding=ft.Padding(5, 0, 5, 0),
                border=ft.Border(top=ft.BorderSide(1, "#1a000000")),
            ),
        ]

    return ft.Container(
        content=ft.Stack(noi_dung, expand=True),
        bgcolor=nen, border=ft.Border.all(1, vien), border_radius=4, height=cao, expand=True,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        shadow=ft.BoxShadow(blur_radius=4, color="#14000000", offset=ft.Offset(0, 2)),
    )


def ve_ban(vm, hep):
    s, cao = (0.75, 135) if hep else (1.0, 170)
    return ft.Column(
        [ft.Row([ve_cung(vm["cells"][cid], s, cao) for cid in hang], spacing=6) for hang in LUOI_CUNG],
        spacing=6,
    )


def ve_thong_tin(vm, ly_do, hep):
    co = 13 if hep else 16
    cot = []
    for nhan, gia_tri, ghi_chu in vm["tu_tru"]:
        cot.append(ft.Column([
            ft.Text(nhan.upper(), size=9 if hep else 10, color="#777777"),
            ft.Text(spans=[ft.TextSpan(gia_tri, ft.TextStyle(color=mau(lay_hanh(gia_tri.split()[0])))),
                           ft.TextSpan(f" ({ghi_chu})" if ghi_chu else "", ft.TextStyle(size=co - 5, color="#777777",
                                                                                        weight=ft.FontWeight.NORMAL))],
                    size=co, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True))
    dong = [ft.Row(cot, alignment=ft.MainAxisAlignment.SPACE_AROUND, vertical_alignment=ft.CrossAxisAlignment.START)]
    for i, line in enumerate(vm["lines"]):
        dong.append(ft.Text(line, text_align=ft.TextAlign.CENTER, color="#000000" if i == 0 else "#555555",
                            weight=ft.FontWeight.BOLD if i == 0 else None, size=14 if i == 0 else 13))
    if vm["badges"]:
        dong.append(ft.Row([badge(t, k, 12) for t, k in vm["badges"]], alignment=ft.MainAxisAlignment.CENTER,
                           wrap=True, spacing=8))
    if ly_do:
        dong.append(ft.Text(f"Lý do: {ly_do}", color="#000000", text_align=ft.TextAlign.CENTER))
    return ft.Container(
        content=ft.Column(dong, spacing=6, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor="#ffffff", padding=10, border_radius=8, border=ft.Border.all(1, "#dddddd"),
    )


def _app(page: ft.Page):
    page.title = "Kỳ Môn Độn Giáp"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed="#ff4b4b")
    page.bgcolor = "#f5f5f5"
    page.padding = 0
    page.scroll = ft.ScrollMode.AUTO

    now = tz_vn.now()
    state = {"vm": None, "ly_do": ""}

    def so(label, value, width=None, expand=True):
        return ft.TextField(label=label, value=str(value), keyboard_type=ft.KeyboardType.NUMBER,
                            input_filter=ft.NumbersOnlyInputFilter(), dense=True, width=width,
                            expand=expand)

    dd_loai = ft.Dropdown(label="Loại cục", value=LOAI_CUC[0], dense=True, expand=True,
                          options=[ft.DropdownOption(key=x, text=x) for x in LOAI_CUC])
    tf_d, tf_m, tf_y = so("Ngày", now.day), so("Tháng", now.month), so("Năm", now.year)
    tf_h, tf_mi = so("Giờ", now.hour), so("Phút", now.minute)
    row_gio = ft.Row([tf_h, tf_mi], spacing=8)
    dd_mode = ft.Dropdown(label="Chế độ (chuyển bàn)", value=list(QM_MODES)[0], dense=True, expand=True,
                          options=[ft.DropdownOption(key=x, text=x) for x in QM_MODES])
    row_mode = ft.Row([dd_mode], visible=False)
    tf_ju = so("Cục số (1-9)", 1)
    seg_ad = ft.SegmentedButton(
        selected=["Dương"], segments=[ft.Segment(value="Dương", label=ft.Text("Dương")),
                                      ft.Segment(value="Âm", label=ft.Text("Âm"))])
    row_ju = ft.Row([tf_ju, seg_ad], spacing=8, visible=False)
    tf_ly_do = ft.TextField(label="Lý do", multiline=True, min_lines=1, max_lines=4, dense=True)
    txt_toa = ft.Text("", text_align=ft.TextAlign.CENTER, size=15)
    ket_qua = ft.Column(spacing=10, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)

    def bao_loi(msg):
        page.show_dialog(ft.SnackBar(ft.Text(msg), bgcolor="#c62828"))

    def cap_nhat_form(_=None):
        loai = dd_loai.value
        row_gio.visible = loai in ("Thời Gia", "Thời Gia (Chuyển Bàn)")
        row_mode.visible = loai == "Thời Gia (Chuyển Bàn)"
        row_ju.visible = row_mode.visible and QM_MODES.get(dd_mode.value) == 4
        tf_d.disabled = tf_m.disabled = loai == "Niên Gia"
        page.update()

    dd_loai.on_select = cap_nhat_form
    dd_mode.on_select = cap_nhat_form

    def la_hep():
        return (page.width or 1000) < 700

    def ve_ket_qua():
        vm = state["vm"]
        ket_qua.controls = [] if vm is None else [
            ve_thong_tin(vm, state["ly_do"], la_hep()),
            ve_ban(vm, la_hep()),
            ft.Row([
                ft.OutlinedButton("Lưu JSON", icon=ft.Icons.DOWNLOAD, on_click=luu_json),
                ft.OutlinedButton("Copy JSON", icon=ft.Icons.COPY, on_click=copy_json),
            ], alignment=ft.MainAxisAlignment.CENTER, wrap=True),
        ]

    def lap(_=None):
        try:
            y, m, d = int(tf_y.value or 0), int(tf_m.value or 0), int(tf_d.value or 0)
            h, mi = int(tf_h.value or 0), int(tf_mi.value or 0)
            loai = dd_loai.value
            if not 1900 <= y <= 2100:
                return bao_loi("Năm phải trong khoảng 1900–2100")
            if loai == "Niên Gia":
                m, d = 1, 1
            if loai not in ("Thời Gia", "Thời Gia (Chuyển Bàn)"):
                h, mi = 12, 0
            qm_mode, qm_setju = QM_MODES.get(dd_mode.value, 1), 0
            if loai == "Thời Gia (Chuyển Bàn)" and qm_mode == 4:
                ju = int(tf_ju.value or 0)
                if not 1 <= ju <= 9:
                    return bao_loi("Cục số phải từ 1 đến 9")
                qm_setju = ju if "Dương" in seg_ad.selected else -ju
            state["vm"] = lap_tran(loai, y, m, d, h, mi, qm_mode, qm_setju)
            state["ly_do"] = (tf_ly_do.value or "").strip()
        except ValueError:
            return bao_loi("Ngày giờ không hợp lệ")
        except Exception as exc:  # engine lỗi bất ngờ: báo thay vì làm treo app
            return bao_loi(f"Lỗi lập trận: {exc}")
        ve_ket_qua()
        page.update()

    def bay_gio(_=None):
        t = tz_vn.now()
        tf_d.value, tf_m.value, tf_y.value = str(t.day), str(t.month), str(t.year)
        tf_h.value, tf_mi.value = str(t.hour), str(t.minute)
        page.update()

    def toa_cung(_=None):
        giay = datetime.now().second
        cung = giay % 9 or 9  # chia 9 lấy dư, dư 0 là cung 9
        txt_toa.spans = [ft.TextSpan(f"Giây {giay} ➔ Ứng vào: "),
                         ft.TextSpan(MAP_TEN_CUNG[cung], ft.TextStyle(color="#d32f2f", size=18,
                                                                      weight=ft.FontWeight.BOLD))]
        page.update()

    def json_str():
        return json.dumps(state["vm"]["kq"], ensure_ascii=False, indent=2)

    async def luu_json(_):
        try:
            path = await ft.FilePicker().save_file(
                dialog_title="Lưu JSON trận", file_name=f"{state['vm']['file_name']}.json",
                file_type=ft.FilePickerFileType.CUSTOM, allowed_extensions=["json"],
                src_bytes=json_str().encode("utf-8"))
        except Exception as exc:
            return bao_loi(f"Không lưu được file: {exc}")
        if path:
            page.show_dialog(ft.SnackBar(ft.Text(f"Đã lưu: {path}")))

    async def copy_json(_):
        await ft.Clipboard().set(json_str())
        page.show_dialog(ft.SnackBar(ft.Text("Đã copy JSON vào clipboard")))

    def on_resize(_):
        if state["vm"] is not None:
            ve_ket_qua()
            page.update()

    page.on_resize = on_resize

    form = ft.Container(
        content=ft.Column([
            ft.Row([dd_loai]),
            ft.Row([tf_d, tf_m, tf_y], spacing=8),
            row_gio, row_mode, row_ju, tf_ly_do,
            ft.Row([
                ft.FilledButton("Lập Trận Đồ", icon=ft.Icons.AUTO_AWESOME, on_click=lap, expand=True),
                ft.OutlinedButton("Bây giờ", icon=ft.Icons.SCHEDULE, on_click=bay_gio),
            ], spacing=8),
            ft.Divider(height=8),
            ft.Button("🎯 Lấy số Tỏa Cung (giây hiện tại)", on_click=toa_cung,
                      bgcolor="#ff4b4b", color="#ffffff"),
            txt_toa,
        ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
        bgcolor="#ffffff", padding=12, border_radius=8, border=ft.Border.all(1, "#e0e0e0"),
    )

    page.add(ft.SafeArea(
        content=ft.Container(
            content=ft.Column([
                ft.Text("🔮 Kỳ Môn Độn Giáp - Trương Chí Xuân", size=20, weight=ft.FontWeight.BOLD,
                        color="#000000"),
                ft.ResponsiveRow([
                    ft.Container(form, col={"xs": 12, "md": 4}),
                    ft.Container(ket_qua, col={"xs": 12, "md": 8}),
                ], spacing=12, run_spacing=12),
            ], spacing=10),
            padding=10,
        ),
    ))
    cap_nhat_form()
    lap()


def main(page: ft.Page):
    # Hiện "Đang tải..." ngay, rồi mới dựng giao diện; lỗi (nếu có) hiện ra màn hình thay vì trống trơn.
    page.bgcolor = "#f5f5f5"
    page.add(ft.SafeArea(content=ft.Text("Đang tải...", color="#000000")))
    page.update()
    try:
        page.clean()
        _app(page)
    except Exception:
        page.clean()
        page.add(ft.SafeArea(content=ft.Text(traceback.format_exc(), color="#b71c1c", selectable=True)))
        page.update()


# Không bọc trong `if __name__ == "__main__"`: app Android chạy main.py với __name__ khác,
# khi đó ft.run không được gọi và app chỉ hiện màn hình trống.
ft.run(main)

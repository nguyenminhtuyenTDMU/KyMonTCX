#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kỳ Môn Độn Giáp - bộ lập trận (paiban)
Port từ app J2ME "阴盘手机刻家排盘程序.jar" (2008) sang Python.

Thuật toán: thời gia Kỳ Môn chuyển bàn (转盘法), có kèm ám can (阴盘暗干).
Giờ nhập vào hiểu là GIỜ BẮC KINH (GMT+8) - đúng chuẩn Kỳ Môn.

Cách dùng:
    python qimen.py                      # dùng giờ hiện tại
    python qimen.py 2024 6 15 14 30      # năm tháng ngày giờ phút
    python qimen.py 2024 6 15 14 30 --ju 1   # chọn chế độ (xem bên dưới)

Chế độ (tham số --ju) — khớp 4 nút trong app gốc:
    1  : 正一派道家阴盘 (Chính Nhất phái đạo gia âm bàn) = CHUẨN VƯƠNG PHƯỢNG LÂN [MẶC ĐỊNH]
         cục = (năm chi + nông lịch tháng + nông lịch ngày + giờ chi) % 9
         âm/dương độn: đông chí→mang chủng = dương, hạ chí→đại tuyết = âm
    0  : 拆补奇门盘 = thời gia truyền thống (dương bàn), khởi cục theo tiết khí + tam nguyên
    2  : 刻盘 (khắc gia) = như (1) nhưng CỘNG THÊM phút chi
    4  : 自选局 = tự chọn cục — dùng kèm --setju N (dương N, hoặc âm -N)

Địa chi -> số: Tý1 Sửu2 Dần3 Mão4 Thìn5 Tỵ6 Ngọ7 Mùi8 Thân9 Dậu10 Tuất11 Hợi12
"""

import sys
from datetime import datetime, timedelta, timezone

if sys.stdout.encoding is None or sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

BJ = timezone(timedelta(hours=8))  # múi giờ Bắc Kinh

# ------------------------------------------------------------------ BẢNG DỮ LIỆU
# (giữ nguyên từ qmtemp.java)

lunarInfo = [19416,19168,42352,21717,53856,55632,91476,22176,39632,21970,19168,42422,42192,53840,119381,46400,54944,44450,38320,84343,18800,42160,46261,27216,27968,109396,11104,38256,21234,18800,25958,54432,59984,28309,23248,11104,100067,37600,116951,51536,54432,120998,46416,22176,107956,9680,37584,53938,43344,46423,27808,46416,86869,19872,42448,83315,21200,43432,59728,27296,44710,43856,19296,43748,42352,21088,62051,55632,23383,22176,38608,19925,19152,42192,54484,53840,54616,46400,46496,103846,38320,18864,43380,42160,45690,27216,27968,44870,43872,38256,19189,18800,25776,29859,59984,27480,21952,43872,38613,37600,51552,55636,54432,55888,30034,22176,43959,9680,37584,51893,43344,46240,47780,44368,21977,19360,42416,86390,21168,43312,31060,27296,44368,23378,19296,42726,42208,53856,60005,54576,23200,30371,38608,19415,19152,42192,118966,53840,54560,56645,46496,22224,21938,18864,42359,42160,43600,111189,27936,44448]
solarMonth = [31,28,31,30,31,30,31,31,30,31,30,31]

# 24 sơn + 山局 + 象直 (dùng cho La Kinh, không dùng khi lập trận Kỳ Môn thời gia)
ShanJu   = [-7,-2,-1,-9,-7,-6,-5,-6,-5,4,1,2,3,8,9,1,3,4,5,4,5,-6,-9,-8]

Gan = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
Zhi = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
Animals = ["鼠","牛","虎","兔","龙","蛇","马","羊","猴","鸡","狗","猪"]
solarTerm = ["小寒","大寒","立春","雨水","惊蛰","春分","清明","谷雨","立夏","小满","芒种","夏至",
             "小暑","大暑","立秋","处暑","白露","秋分","寒露","霜降","立冬","小雪","大雪","冬至"]
yuejiang = [10,11,11,0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10]
jubiao = [2,8,5,3,9,6,8,5,2,9,6,3,1,4,7,3,9,6,4,1,7,5,2,8,4,1,7,5,2,8,6,3,9,9,3,6,8,2,5,7,1,4,2,5,8,1,4,7,9,3,6,7,1,4,6,9,3,5,8,2,6,9,3,5,8,2,4,7,1,1,7,4]
sTermInfo = [0,21208,42467,63836,85337,107014,128867,150921,173149,195551,218072,240693,263343,285989,308563,331033,353350,375494,397447,419210,440795,462224,483532,504758]

men  = [" ","休","生","伤","杜","景","死","惊","开"]   # bát môn (index 1..8)
xing = [" ","蓬","任","冲","辅","英","芮","柱","心"]   # cửu tinh (禽 xử lý riêng)
shen  = [" ","符","天","地","玄","白","六","阴","蛇"]  # bát thần - âm độn (nghịch)
shen2 = [" ","符","蛇","阴","六","白","玄","地","天"]  # bát thần - dương độn (thuận)

zhuan  = [0,1,8,3,4,9,2,7,6]          # thứ tự cung khi chuyển bàn
fzhuan = [0,1,6,3,4,6,8,7,2,5]        # cung -> chỉ số sao/môn gốc
YiMa   = [2,11,8,5]                    # dịch mã: Thân-Tý-Thìn->Dần ...
zhi2gong = [1,8,8,3,4,4,9,2,2,7,6,6]  # địa chi -> cung (dùng cho không vong)
dihu = ["建","除","满","平","定","执","破","危","成","收","开","闭"]  # kiến trừ 12 thần
heluo = {1:"兑",2:"坎",3:"艮",4:"坤",6:"离",7:"巽",8:"乾",9:"震"}  # cung -> quái

# liuyi: thứ tự bày Tam Kỳ Lục Nghi trên địa bàn (戊己庚辛壬癸丁丙乙)
liuyi = [0,4,5,6,7,8,9,3,2,1]

# ------------------------------------------------------------------ DỊCH TIẾNG VIỆT (thuật ngữ Kỳ Môn Độn Giáp)

Gan_vn = ["Giáp","Ất","Bính","Đinh","Mậu","Kỷ","Canh","Tân","Nhâm","Quý"]
Zhi_vn = ["Tý","Sửu","Dần","Mão","Thìn","Tỵ","Ngọ","Mùi","Thân","Dậu","Tuất","Hợi"]
solarTerm_vn = ["Tiểu Hàn","Đại Hàn","Lập Xuân","Vũ Thủy","Kinh Trập","Xuân Phân","Thanh Minh","Cốc Vũ",
                "Lập Hạ","Tiểu Mãn","Mang Chủng","Hạ Chí","Tiểu Thử","Đại Thử","Lập Thu","Xử Thử",
                "Bạch Lộ","Thu Phân","Hàn Lộ","Sương Giáng","Lập Đông","Tiểu Tuyết","Đại Tuyết","Đông Chí"]

GAN_VN  = dict(zip(Gan, Gan_vn))
ZHI_VN  = dict(zip(Zhi, Zhi_vn))
MEN_VN  = dict(zip(men[1:],  ["Hưu","Sinh","Thương","Đỗ","Cảnh","Tử","Kinh","Khai"]))
XING_VN = dict(zip(xing[1:], ["Bồng","Nhậm","Xung","Phụ","Anh","Nhuế","Trụ","Tâm"]))
XING_VN["禽"] = "Cầm"
SHEN_VN = dict(zip(shen[1:], ["Phù","Thiên","Địa","Huyền","Bạch","Lục","Âm","Xà"]))

def gan_vn(s):
    """Dịch chuỗi 1-2 Thiên Can (vd '乙癸') sang tiếng Việt, cách nhau bằng dấu phẩy."""
    s = (s or "").strip()
    if not s:
        return "-"
    return ",".join(GAN_VN[c] for c in s if c in GAN_VN)

def cyclical_vn(num):
    return f"{Gan_vn[num % 10]} {Zhi_vn[num % 12]}"

# ------------------------------------------------------------------ VƯỢNG SUY CUNG THEO NGUYỆT LỆNH
# Cung so với Nguyệt Lệnh (không phải Sao so với Nguyệt Lệnh - đó là chuyện của kymon_logic.py).
# Đánh số cung theo Lạc Thư, khớp lưới hiển thị [[4,9,2],[3,5,7],[8,1,6]] của render().

NGU_HANH_CUNG = {1:"Thủy", 2:"Thổ", 3:"Mộc", 4:"Mộc", 5:"Thổ", 6:"Kim", 7:"Kim", 8:"Thổ", 9:"Hỏa"}
NGU_HANH_CHI  = {"Tý":"Thủy","Sửu":"Thổ","Dần":"Mộc","Mão":"Mộc","Thìn":"Thổ","Tỵ":"Hỏa",
                  "Ngọ":"Hỏa","Mùi":"Thổ","Thân":"Kim","Dậu":"Kim","Tuất":"Thổ","Hợi":"Thủy"}
QUY_TAC_NGU_HANH = {
    "Kim": {"Sinh":"Thủy", "Khắc":"Mộc"}, "Mộc": {"Sinh":"Hỏa", "Khắc":"Thổ"},
    "Thủy": {"Sinh":"Mộc", "Khắc":"Hỏa"}, "Hỏa": {"Sinh":"Thổ", "Khắc":"Kim"},
    "Thổ": {"Sinh":"Kim", "Khắc":"Thủy"},
}

# Tiết khí (chỉ số 0-23, khớp solarTerm/solarTerm_vn) -> chi tháng kiến (nguyệt lệnh).
# Từng cặp tiết-trung khí dùng chung 1 chi: Tiểu/Đại Hàn->Sửu, Lập Xuân/Vũ Thủy->Dần, ...
_NGUYET_KIEN = ["Sửu","Dần","Mão","Thìn","Tỵ","Ngọ","Mùi","Thân","Dậu","Tuất","Hợi","Tý"]
TIETKHI_CHITHANG = [_NGUYET_KIEN[i//2] for i in range(24)]

def tinh_vuong_suy(hanh_x, hanh_ref):
    """So sánh ngũ hành X (vd Cung) với ngũ hành tham chiếu (Nguyệt Lệnh),
    theo đúng lý Vượng-Tướng-Hưu-Tù-Tử cổ điển (旺相休囚死)."""
    if not hanh_x or not hanh_ref: return ""
    if hanh_x == hanh_ref: return "Vượng"                            # tỷ hòa
    if QUY_TAC_NGU_HANH[hanh_ref]["Sinh"] == hanh_x: return "Tướng"  # nguyệt lệnh sinh ta
    if QUY_TAC_NGU_HANH[hanh_x]["Sinh"] == hanh_ref: return "Hưu"    # ta sinh nguyệt lệnh
    if QUY_TAC_NGU_HANH[hanh_x]["Khắc"] == hanh_ref: return "Tù"     # ta khắc nguyệt lệnh
    if QUY_TAC_NGU_HANH[hanh_ref]["Khắc"] == hanh_x: return "Tử"     # nguyệt lệnh khắc ta
    return ""

# ------------------------------------------------------------------ LỊCH / CAN CHI

_BASE_LUNAR = datetime(1900,1,31,tzinfo=BJ)          # mốc đổi âm lịch
_ANCHOR_TERM = datetime(1900,1,6,2,5,tzinfo=BJ)      # mốc tính tiết khí
finedate = None  # (bảng hiệu chỉnh 1990-2009 - xem cuối file, nạp lười)

def _leap_month(y):  return lunarInfo[y-1900] & 0xF
def _leap_days(y):
    if _leap_month(y):
        return 30 if (lunarInfo[y-1900] & 0x10000) else 29
    return 0
def _month_days(y,m):
    return 30 if (lunarInfo[y-1900] & (0x10000 >> m)) else 29

def cyclical(num):
    return Gan[num % 10] + Zhi[num % 12]

def s_term(y, n):
    """Thời điểm tiết khí thứ n của năm y (giờ Bắc Kinh)."""
    global finedate
    if 1989 < y < 2010:
        if finedate is None:
            finedate = _load_finedate()
        ms = finedate[(y-1990)*24 + n]
        return datetime.fromtimestamp(ms/1000, tz=BJ)
    ms = 31556925974.7 * (y-1900) + sTermInfo[n]*60000.0
    return _ANCHOR_TERM + timedelta(milliseconds=ms)

def get_term(dt):
    """Trả về chỉ số tiết khí SẮP tới (0..23) so với ngày dt."""
    year = dt.year
    for i in range(24):
        t = s_term(year, i)
        if (t.month == dt.month and t.day > dt.day) or (t.month == dt.month + 1):
            return i
    return 0

class Lunar:
    __slots__=("year","month","day","isLeap","yearCyl","monCyl","dayCyl")

def to_lunar(dt):
    """Đổi ngày dương -> âm lịch + can chi (port hàm Lunar())."""
    L = Lunar(); L.isLeap=0; L.monCyl=14
    offset = (dt.date() - _BASE_LUNAR.date()).days
    L.dayCyl = offset + 40
    y = 1900
    while y < 2050 and offset > 0:
        days = 348
        for i in range(15,3,-1):
            if lunarInfo[y-1900] & (1<<i): days += 1
        days += _leap_days(y)
        if offset - days < 1: break
        offset -= days; y += 1
    L.year = y
    leap = _leap_month(y); L.isLeap = 0
    i = 1
    while i < 13 and offset > 0:
        if leap>0 and i==leap+1 and L.isLeap==0:
            i -= 1; L.isLeap=1; temp=_leap_days(L.year)
        else:
            temp=_month_days(L.year,i)
        if L.isLeap==1 and i==leap+1: L.isLeap=0
        offset -= temp
        if L.isLeap==0: L.monCyl += 1
        i += 1
    if offset==0 and leap>0 and i==leap+1:
        if L.isLeap==1: L.isLeap=0
        else: L.isLeap=1; i-=1; L.monCyl-=1
    if offset<0:
        offset += temp; i-=1; L.monCyl-=1
    L.month = i
    L.day = int(offset)+1
    # trụ tháng theo tiết (节)
    m0 = dt.month-1
    firstNode = s_term(dt.year, m0*2)
    later = (dt.timestamp()//600 >= firstNode.timestamp()//600)
    L.monCyl = (dt.year-1900)*12 + m0 + (13 if later else 12)
    L.yearCyl = dt.year - 1864
    if m0 < 4 and (L.monCyl % 12) < 2:
        L.yearCyl -= 1
    return L

# ------------------------------------------------------------------ LẬP TRẬN

class Pan:
    """Kết quả một cục."""
    def __init__(s):
        s.digan=[""]*10; s.tiangan=[""]*10; s.angan=[""]*10
        s.menpan=[""]*10; s.xinpan=[""]*10; s.shenpan=[""]*10
        s.kong=["　"]*10; s.maw=["　"]*12; s.tianmen=[0]*12
        s.qmju=0; s.yy=""; s.zhifu=""; s.zhishi=""
        s.yinpan=0; s.ngaygio=(0,0,0,0,0); s.tuchoncuc=0
        s.cY=0; s.cM=0; s.cD=0; s.gio_tru=0; s.khac_tru=None; s.tuan_tru=0
        s.tmp2=0; s.xunkong=(0,0); s.maxing=0; s.xun_num=0
        s.chi_nguyet=""; s.hanh_nguyet=""; s.cung_vuong_suy={}

def paipan(dt, yinpan=0, setju=0):
    """dt: datetime giờ Bắc Kinh. Trả về Pan."""
    p = Pan()
    p.yinpan = yinpan
    tY,tM,tD,tH,tMin = dt.year,dt.month-1,dt.day,dt.hour,dt.minute
    Today = datetime(tY,tM+1,tD,tH,50,tzinfo=BJ)
    p.ngaygio = (tY,tM+1,tD,tH,tMin)
    if tH%2==0: tMin += 60
    if tH==23:
        Today += timedelta(hours=1); tH=0

    L = to_lunar(Today)
    lY,lM,lD,lL = L.year,L.month,L.day,L.isLeap
    cY,cM,cD = L.yearCyl,L.monCyl,L.dayCyl

    tZhi = (tH+1)//2
    hGan = cD % 10
    if hGan>4: hGan-=5
    hCyl = hGan*12 + tZhi
    hGan = hCyl % 10
    if hGan>4: hGan-=5
    cMin = (hGan*12 + tMin//10) % 60
    p.gio_tru = hCyl

    if yinpan==4:
        hg=cY%10;  hg-= 5 if hg>4 else 0
        cM = hg*12 + cM%12
        p.tuchoncuc = setju

    p.cY, p.cM, p.cD = cY, cM, cD

    tmp1 = get_term(Today)
    if tmp1>23: tmp1=0
    tmp2 = 23 if tmp1==0 else tmp1-1
    p.tmp2 = tmp2
    p.chi_nguyet = TIETKHI_CHITHANG[tmp2]
    p.hanh_nguyet = NGU_HANH_CHI[p.chi_nguyet]
    p.cung_vuong_suy = {g: tinh_vuong_suy(NGU_HANH_CUNG[g], p.hanh_nguyet) for g in range(1,10)}
    jiang = yuejiang[tmp2]
    v = lM if lM!=0 else 12
    cY2 = (lY-1984)%60
    ju = cY2%12 + 1 + v + lD + (hCyl%12 + 1)
    if yinpan==2:
        ju += cMin%12 + 1; hCyl = cMin%60
    if yinpan==4:
        hCyl = cM%60

    p.khac_tru = cMin if yinpan==2 else None
    p.tuan_tru = hCyl

    if yinpan>0:
        k = hCyl%12; p.yuejiangNo=k
        jj=jiang
        for _ in range(12):
            p.tianmen[k]=jj; k=(k+1)%12; jj=(jj+1)%12

    ju %= 9
    if ju==0: ju=9
    p.yy = "阴" if 11<=tmp2<23 else "阳"
    if yinpan==0:
        m = cD % 15 // 5
        ju = jubiao[m + 3*tmp2]
    if setju>0: ju=setju; p.yy="阳"
    elif setju<0: ju=-setju; p.yy="阴"
    p.qmju = ju

    xunshou = (hCyl%60)//10*10
    xunkong1=(xunshou+10)%12; xunkong2=(xunshou+11)%12
    maxing = YiMa[hCyl%4]
    p.maw = ["　"]*12; p.maw[maxing]="马"
    p.kong = ["　"]*10
    p.kong[zhi2gong[xunkong1]]="O"; p.kong[zhi2gong[xunkong2]]="O"
    p.xunkong = (xunkong1, xunkong2)
    p.maxing = maxing
    p.xun_num = xunshou
    dg = xunshou//10 + 4

    # ---- ĐỊA BÀN: bày Tam Kỳ Lục Nghi
    sgg=0; dgg=0
    for i in range(9):
        g = (ju-i) if p.yy=="阴" else (ju+i)
        while g>9: g-=9
        while g<1: g+=9
        p.digan[g] = Gan[liuyi[i+1]]
        if liuyi[i+1]==dg: dgg=g
        if liuyi[i+1]==hCyl%10: sgg=g
    if sgg==0: sgg=dgg
    p.digan[2] = p.digan[2] + p.digan[5]   # trung 5 gửi khôn 2

    # ---- TRỰC PHÙ / TRỰC SỬ
    zhifu = "禽" if dgg==5 else xing[fzhuan[dgg]]
    zhishi = men[fzhuan[dgg]]
    p.zhifu, p.zhishi = zhifu, zhishi
    mgg = (hCyl%10 + dgg) if p.yy=="阳" else (dgg - hCyl%10)
    if mgg<1: mgg+=9
    if mgg>9: mgg-=9

    # ---- THIÊN BÀN: cửu tinh + thiên bàn can
    v = fzhuan[sgg]-fzhuan[dgg]
    for i in range(1,9):
        j=i-v
        if j<1: j+=8
        if j>8: j-=8
        p.xinpan[zhuan[i]]=xing[j]
        p.tiangan[zhuan[i]]=p.digan[zhuan[j]]
    # ---- BÁT MÔN
    v = fzhuan[mgg]-fzhuan[dgg]
    for i in range(1,9):
        j=i-v
        if j<1: j+=8
        if j>8: j-=8
        p.menpan[zhuan[i]]=men[j]
    # ---- BÁT THẦN
    v = fzhuan[sgg]-1
    for i in range(1,9):
        j=i-v
        if j<1: j+=8
        if j>8: j-=8
        p.shenpan[zhuan[i]] = shen2[j] if p.yy=="阳" else shen[j]
    # ---- ÁM CAN (đặc trưng âm bàn)
    v = fzhuan[sgg]-fzhuan[mgg]
    for i in range(1,9):
        j=i+v
        if j<1: j+=8
        if j>8: j-=8
        p.angan[zhuan[i]]=p.digan[zhuan[j]]
    p.angan[5]=" "
    p.tiangan[5]=" "
    p.digan[5]=" "
    return p

# ------------------------------------------------------------------ HIỂN THỊ

def render(p):
    CW = 24  # bề rộng nội dung mỗi ô cung (chưa tính đệm 2 khoảng trắng)

    def fmt(text):
        return f" {text:<{CW}} "

    def border(left, mid, right):
        seg = "─"*(CW+2)
        return left + seg + mid + seg + mid + seg + right

    def cell(g):
        if g == 5:
            yy_label = "Dương Độn" if p.yy=="阳" else "Âm Độn"
            mid = f"CỤC {p.qmju}  ({yy_label})".center(CW)
            ll4 = f"Nguyệt Lệnh: {p.chi_nguyet} ({p.hanh_nguyet})".center(CW)
            return [fmt(""), fmt(mid), fmt(""), fmt(ll4)]
        god  = SHEN_VN.get(p.shenpan[g].strip(), "-")
        star = XING_VN.get(p.xinpan[g].strip(), "-")
        gate = MEN_VN.get(p.menpan[g].strip(), "-")
        tg = gan_vn(p.tiangan[g])
        an = gan_vn(p.angan[g])
        dg = gan_vn(p.digan[g])
        mark = []
        if p.kong[g] == "O": mark.append("Không")
        for zi, gong in enumerate(zhi2gong):
            if p.maw[zi] == "马" and gong == g: mark.append("Mã")
        l1 = f"{god} · {star} · {gate}"
        l2 = f"Th:{tg}  Ám:{an}"
        l3 = f"Đị:{dg}  {' · '.join(mark)}"
        l4 = f"Cung {NGU_HANH_CUNG[g]}: {p.cung_vuong_suy.get(g, '')}"
        return [fmt(l1), fmt(l2), fmt(l3), fmt(l4)]

    tY,tM,tD,tH,tMin = p.ngaygio
    header = []
    if p.yinpan == 4:
        header.append(f"Ngày {tD:02d}/{tM:02d}/{tY}  Giờ {tH:02d}h  ·  Tự chọn Cục: {p.tuchoncuc}")
        header.append(f"Năm {cyclical_vn(p.cY)}   Tháng {cyclical_vn(p.cM)}")
    else:
        gio_line = f"Ngày {tD:02d}/{tM:02d}/{tY}  Giờ {tH:02d}h"
        if p.yinpan == 2:
            gio_line += f"{tMin:02d}"
        header.append(gio_line)
        tru_line = (f"Năm {cyclical_vn(p.cY)}   Tháng {cyclical_vn(p.cM)}   "
                    f"Ngày {cyclical_vn(p.cD)}   Giờ {cyclical_vn(p.gio_tru)}")
        if p.yinpan == 2 and p.khac_tru is not None:
            tru_line += f"   Khắc {cyclical_vn(p.khac_tru)}"
        header.append(tru_line)

    yy_label = "Dương Độn" if p.yy == "阳" else "Âm Độn"
    zhifu_vn = XING_VN.get(p.zhifu, "Cầm")
    zhishi_vn = MEN_VN.get(p.zhishi, "-")
    header.append(f"Tiết {solarTerm_vn[p.tmp2]}   {yy_label} {p.qmju} Cục   "
                   f"Trực Phù: {zhifu_vn}   Trực Sử: {zhishi_vn}")

    xunkong1, xunkong2 = p.xunkong
    header.append(f"Tuần {cyclical_vn(p.xun_num)}   "
                   f"Không Vong: {Zhi_vn[xunkong1]}-{Zhi_vn[xunkong2]}   "
                   f"Dịch Mã: {Zhi_vn[p.maxing]}")

    top = border("┌","┬","┐")
    mid_sep = border("├","┼","┤")
    bot = border("└","┴","┘")

    print("─"*len(top))
    for h in header:
        print(h)
    print(top)
    grid = [[4,9,2],[3,5,7],[8,1,6]]
    for r, row in enumerate(grid):
        cells = [cell(g) for g in row]
        for k in range(4):
            print("│" + "│".join(c[k] for c in cells) + "│")
        print(mid_sep if r < 2 else bot)

# ------------------------------------------------------------------ MAIN

def main(argv):
    yinpan=1; setju=0; nums=[]   # mặc định: nút 阴 (âm bàn) = chuẩn Vương Phượng Lân
    it=iter(argv)
    for a in it:
        if a=="--ju": yinpan=int(next(it))
        elif a=="--setju": setju=int(next(it))
        else: nums.append(int(a))
    if len(nums)>=5:
        y,mo,d,h,mi = nums[:5]
        dt=datetime(y,mo,d,h,mi,tzinfo=BJ)
    else:
        dt=datetime.now(BJ)
    p=paipan(dt, yinpan, setju)
    render(p)

def _load_finedate():
    # bảng hiệu chỉnh tiết khí 1990-2009 (epoch ms), port nguyên từ jar
    return [631550160000,632822700000,634097880000,635379420000,636668520000,637968000000,639278040000,640599960000,641932560000,643275360000,644626020000,645982380000,647341320000,648699840000,650054880000,651403500000,652743600000,654073200000,655391760000,656698620000,657995100000,659281740000,660561300000,661835280000,663107400000,664379400000,665655120000,666936060000,668225760000,669524700000,670835220000,672156600000,673489680000,674832060000,676183080000,677539140000,678898320000,680256660000,681611880000,682960320000,684300540000,685630080000,686948640000,688255620000,689551920000,690838800000,692118120000,693392460000,694664220000,695936520000,697211880000,698493300000,699782460000,701081880000,702391920000,703713780000,705046320000,706389240000,707739660000,709096260000,710454960000,711813780000,713168460000,714517440000,715857180000,717187200000,718505400000,719812740000,721108740000,722395860000,723675000000,724949460000,726221160000,727493520000,728768820000,730050180000,731339460000,732638700000,733948920000,735270600000,736603380000,737945940000,739296780000,740652960000,742012080000,743370420000,744725640000,746074080000,747414360000,748743840000,750062580000,751369380000,752665980000,753952560000,755232240000,756506220000,757778340000,759050280000,760326000000,761607000000,762896580000,764195520000,765505980000,766827420000,768160320000,769502820000,770853660000,772209840000,773568900000,774927360000,776282400000,777631080000,778971120000,780300900000,781619340000,782926500000,784222680000,785509740000,786788940000,788063460000,789335040000,790607520000,791882700000,793164240000,794453280000,795752760000,797062620000,798384600000,799716960000,801059940000,802410360000,803766900000,805125600000,806484360000,807839160000,809188080000,810527940000,811857900000,813176220000,814483440000,815779680000,817066680000,818346000000,819620280000,820892160000,822164340000,823439880000,824721000000,826010460000,827309460000,828619800000,829941240000,831274140000,832616520000,833967480000,835323480000,836682720000,838041000000,839396280000,840744720000,842085120000,843414540000,844733340000,846040200000,847336800000,848623440000,849903120000,851177160000,852449220000,853721280000,854996880000,856277940000,857567400000,858866460000,860176680000,861498240000,862830960000,864173580000,865524180000,866880540000,868239420000,869598060000,870952920000,872301840000,873641760000,874971720000,876289980000,877597380000,878893500000,880180680000,881459820000,882734400000,884005980000,885278520000,886553580000,887835120000,889124100000,890423580000,891733440000,893055300000,894387720000,895730580000,897081060000,898437480000,899796300000,901154940000,902509860000,903858660000,905198760000,906528540000,907847100000,909154140000,910450620000,911737440000,913017000000,914291100000,915563160000,916835220000,918110820000,919391820000,920681340000,921980220000,923290680000,924611940000,925944900000,927287220000,928638180000,929994120000,931353360000,932711580000,934066920000,935415420000,936755760000,938085300000,939404100000,940711020000,942007560000,943294380000,944573940000,945848160000,947120100000,948392280000,949667700000,950948940000,952238100000,953537340000,954847380000,956169120000,957501540000,958844340000,960194760000,961551300000,962909940000,964268760000,965623500000,966972600000,968312400000,969642480000,970960740000,972268200000,973564320000,974851560000,976130700000,977405280000,978676920000,979949400000,981224580000,982505940000,983795040000,985094340000,986404320000,987725940000,989058540000,990401160000,991751760000,993108000000,994467000000,995825460000,997180620000,998529240000,999869520000,1001199180000,1002517920000,1003824900000,1005121560000,1006408260000,1007688000000,1008961980000,1010234160000,1011506100000,1012781760000,1014062640000,1015352220000,1016651040000,1017961440000,1019282700000,1020615600000,1021957920000,1023308760000,1024664820000,1026023940000,1027382280000,1028737500000,1030086180000,1031426340000,1032756180000,1034074740000,1035381960000,1036678320000,1037965380000,1039244760000,1040519160000,1041790920000,1043063280000,1044338520000,1045619880000,1046908920000,1048208280000,1049518080000,1050839880000,1052172180000,1053515040000,1054865400000,1056221940000,1057580580000,1058939400000,1060294140000,1061643240000,1062983100000,1064313180000,1065631560000,1066938960000,1068235200000,1069522380000,1070801700000,1072076160000,1073347920000,1074620220000,1075895580000,1077176760000,1078465980000,1079765040000,1081075200000,1082396580000,1083729360000,1085071740000,1086422520000,1087778520000,1089137700000,1090495980000,1091851320000,1093199820000,1094540280000,1095869820000,1097188740000,1098495660000,1099792440000,1101079080000,1102358880000,1103632920000,1104905040000,1106177040000,1107452640000,1108733580000,1110023040000,1111321920000,1112632140000,1113953520000,1115286240000,1116628680000,1117979340000,1119335520000,1120694460000,1122053040000,1123408020000,1124756940000,1126096980000,1127427000000,1128745440000,1130052840000,1131349080000,1132636320000,1133915580000,1135190160000,1136461740000,1137734280000,1139009340000,1140290820000,1141579740000,1142879100000,1144188840000,1145510640000,1146842940000,1148185740000,1149536040000,1150892520000,1152251220000,1153609980000,1154964900000,1156313820000,1157653860000,1158983820000,1160302440000,1161609720000,1162906140000,1164193140000,1165472700000,1166746980000,1168018920000,1169291040000,1170566580000,1171847520000,1173136980000,1174435800000,1175746080000,1177067280000,1178400120000,1179742320000,1181093220000,1182449100000,1183808340000,1185166620000,1186521960000,1187870460000,1189210980000,1190540580000,1191859500000,1193166480000,1194463200000,1195750020000,1197029700000,1198303920000,1199575920000,1200848040000,1202123460000,1203404580000,1204693800000,1205992860000,1207302840000,1208624340000,1209956820000,1211299440000,1212649860000,1214006280000,1215364980000,1216723740000,1218078600000,1219427640000,1220767560000,1222097760000,1223416140000,1224723720000,1226019900000,1227307260000,1228586460000,1229861100000,1231132680000,1232405220000,1233680280000,1234961700000,1236250620000,1237549860000,1238859720000,1240181340000,1241513700000,1242856320000,1244206800000,1245563040000,1246921920000,1248280500000,1249635600000,1250984400000,1252324680000,1253654460000,1254973260000,1256280420000,1257577080000,1258863960000,1260143700000,1261417800000]

if __name__=="__main__":
    main(sys.argv[1:])
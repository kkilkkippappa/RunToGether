import math

# 기본 파라미터(단기예보 기준)
Re    = 6371.00877   # 지구 반경 [km]
grid  = 5.0          # 격자 간격 [km]
slat1 = 30.0         # 표준 위도1 [°]
slat2 = 60.0         # 표준 위도2 [°]
olon  = 126.0        # 기준점 경도 [°]
olat  = 38.0         # 기준점 위도 [°]
xo    = 210 / grid   # 기준점 X좌표 (격자 단위)
yo    = 675 / grid   # 기준점 Y좌표 (격자 단위)

# 2. 내부 상수
PI = math.pi
DEGRAD = PI/180.0
RADDEG = 180.0/PI

_re = Re/grid
slat1 = slat1 * DEGRAD
slat1_r = slat1 * DEGRAD
slat2_r = slat2 * DEGRAD
olon_r  = olon  * DEGRAD
olat_r  = olat  * DEGRAD

# C lamcproj 초기화: sn, sf, ro 계산
sn = math.log(
    math.cos(slat1_r) / math.cos(slat2_r)
) / math.log(
    math.tan(PI * 0.25 + slat2_r * 0.5) / math.tan(PI * 0.25 + slat1_r * 0.5)
)
# sf: scale factor (C 변수 sf)
sf = (math.pow(math.tan(PI * 0.25 + slat1_r * 0.5), sn) * 
      math.cos(slat1_r) / sn)
# ro: radius at origin (C 변수 ro)
ro = _re * sf / math.pow(math.tan(PI * 0.25 + olat_r * 0.5), sn)

def grid_to_latlon(nx: float, ny: float):
    """
    KMA 격자 좌표(nx, ny) -> 위경도(lat, lon) 변환
    C map_conv(code=1) -> lamcproj 격자->위경도 부분과 동일
    """
    # C map_conv 보정: 기준점 offset 제거
    xn = nx - xo
    yn = ro - ny + yo

    # --- C lamcproj 역변환: ra 역산 ---
    ra = math.sqrt(xn * xn + yn * yn)
    if sn < 0.0:
        ra = -ra

    # --- C lamcproj 역변환: 위도(lat) 계산 ---
    alat = math.pow(_re * sf / ra, 1.0 / sn)
    alat = 2.0 * math.atan(alat) - PI * 0.5

    # --- C lamcproj 역변환: theta 계산 ---
    if abs(xn) <= 0.0:
        theta = 0.0
    else:
        if abs(yn) <= 0.0:
            theta = math.pi * 0.5
            if xn < 0.0:
                theta = -theta
        else:
            theta = math.atan2(xn, yn)

    # alon: C lamcproj 경도 역변환
    alon = theta / sn + olon_r

    # 도 단위 변환
    lat = alat * RADDEG
    lon = alon * RADDEG
    return lat, lon

def latlon_to_grid(lat: float, lon: float) -> (int, int):
    """
    위경도(lat, lon) → 기상청 격자 좌표(nx, ny) 변환
    C 코드의 map_conv(code=0) → lamcproj 순변환부를 그대로 이식했습니다.
    """
    # 1) 투영 반지름 ra 계산
    ra = math.tan(math.pi * 0.25 + lat * DEGRAD * 0.5)
    ra = _re * sf / math.pow(ra, sn)

    # 2) 경도 차이를 투영 각도 theta로 변환
    theta = lon * DEGRAD - olon_r
    if theta > math.pi:
        theta -= 2.0 * math.pi
    if theta < -math.pi:
        theta += 2.0 * math.pi
    theta *= sn

    # 3) 격자 좌표 계산
    x = ra * math.sin(theta) + xo
    y = ro - ra * math.cos(theta) + yo

    # 4) C 코드의 +1.5 후 정수 캐스트 반올림 처리
    return int(x + 1.5), int(y + 1.5)
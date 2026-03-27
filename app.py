import streamlit as st
import math

st.set_page_config(page_title="필터 원가 계산기", layout="centered")

st.title("필터 원가 계산기")

# =========================
# 선택 영역
# =========================
filter_type = st.radio("필터 타입", ["MINI", "SEPARATOR"])
media_type = st.radio("여재 종류", ["SYNTHETIC", "GLASS"])

# =========================
# 원재료 단가
# =========================
st.subheader("원재료 단가 설정")

if media_type == "SYNTHETIC":
    synthetic_cost = st.number_input("신세틱 단가 (원/㎡)", value=12000)
    glass_cost = 0
else:
    glass_cost = st.number_input("글라스 단가 (원/kg)", value=8500)
    synthetic_cost = 0

urethane_cost = st.number_input("우레탄 단가 (원/kg)", value=3700)

if filter_type == "MINI":
    hotmelt_cost = st.number_input("핫멜트 단가 (원/kg)", value=3900)
else:
    hotmelt_cost = 0

if filter_type == "SEPARATOR":
    foil_cost = st.number_input("호일 단가 (원/kg)", value=8500)
else:
    foil_cost = 0

# =========================
# 기본 입력
# =========================
st.subheader("기본 입력")

width = st.number_input("가로(mm)", value=594)
height = st.number_input("세로(mm)", value=594)
depth = st.number_input("두께(mm)", value=75)

pleat = st.number_input("산수", value=100)
pack_depth = st.number_input("팩두께(mm)", value=30)
pack_height = st.number_input("팩높이(mm)", value=594)

frame_cost = st.number_input("프레임 단가", value=0)
box_cost = st.number_input("박스 비용", value=2000)
vinyl_cost = st.number_input("비닐 비용", value=500)

# =========================
# 부자재
# =========================
st.subheader("부자재")

sub1 = st.number_input("부자재1", value=0)
sub2 = st.number_input("부자재2", value=0)
sub3 = st.number_input("부자재3", value=0)

# =========================
# 비율
# =========================
st.subheader("비율 설정")

loss = st.number_input("로스 (%)", value=5)
labor = st.number_input("인건비 (%)", value=30)
sgna = st.number_input("판관비 (%)", value=15)
interest = st.number_input("이자 (%)", value=9)
margin = st.number_input("마진 (%)", value=20)

# =========================
# 계산
# =========================
if st.button("계산하기"):

    # 여재
    media_area = (pleat * 2 * pack_depth * pack_height) / 1_000_000

    if media_type == "SYNTHETIC":
        media_cost = media_area * synthetic_cost
    else:
        media_weight = media_area * 0.08
        media_cost = media_weight * glass_cost

    # 우레탄
    urethane_area = (width * depth * 2) / 1_000_000
    urethane_weight = urethane_area * 12
    urethane_total = urethane_weight * urethane_cost

    # 핫멜트
    hotmelt_total = 0
    if filter_type == "MINI":
        lines = math.ceil(height / 25)
        length = lines * pleat * depth / 1000
        weight = length * 2 / 1000
        hotmelt_total = weight * hotmelt_cost

    # 호일
    foil_total = 0
    if filter_type == "SEPARATOR":
        if depth == 292:
            unit = 0.0198
        elif depth == 150:
            unit = 0.01
        else:
            st.error("세퍼레이터는 두께 150 또는 292만 가능")
            st.stop()

        foil_weight = pleat * 2 * unit
        foil_total = foil_weight * foil_cost

    # 재료비
    material = (
        media_cost
        + urethane_total
        + hotmelt_total
        + foil_total
        + frame_cost
        + box_cost
        + vinyl_cost
        + sub1 + sub2 + sub3
    )

    loss_cost = material * loss / 100
    subtotal = material + loss_cost

    labor_cost = subtotal * labor / 100
    sgna_cost = subtotal * sgna / 100
    interest_cost = subtotal * interest / 100

    total = subtotal + labor_cost + sgna_cost + interest_cost
    price = total * (1 + margin / 100)

    # =========================
    # 결과 출력
    # =========================
    st.subheader("결과")

    st.write(f"여재 원가: {media_cost:,.0f} 원")
    st.write(f"우레탄 원가: {urethane_total:,.0f} 원")

    if filter_type == "MINI":
        st.write(f"핫멜트 원가: {hotmelt_total:,.0f} 원")

    if filter_type == "SEPARATOR":
        st.write(f"호일 원가: {foil_total:,.0f} 원")

    st.write(f"재료비: {material:,.0f} 원")
    st.write(f"총원가: {total:,.0f} 원")
    st.write(f"판매가: {price:,.0f} 원")
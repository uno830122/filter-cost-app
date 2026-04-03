import math
import streamlit as st

st.set_page_config(page_title="필터 원가 계산기", layout="centered")


def money(v: float) -> str:
    return f"{round(v):,} 원"


def separator_unit_weight(depth: float):
    if depth == 292:
        return 0.0198
    if depth == 150:
        return 0.01
    return None


st.title("필터 원가 계산기")

product_group = st.radio(
    "제품군 선택",
    ["산업용", "가정용 평판", "가정용 원형"],
    horizontal=True,
)

# =========================================================
# 1) 산업용 : 기존 구조 그대로 유지
# =========================================================
if product_group == "산업용":
    st.subheader("기본 선택")
    grade_type = st.radio("등급 선택", ["미디움", "헤파"], horizontal=True)
    filter_type = st.radio("필터 타입", ["MINI", "SEPARATOR"], horizontal=True)
    media_type = st.radio("여재 종류", ["SYNTHETIC", "GLASS"], horizontal=True)

    st.subheader("원재료 원가설정")
    col1, col2 = st.columns(2)

    with col1:
        if media_type == "SYNTHETIC":
            synthetic_unit_cost = st.number_input("신세틱 원단 단가 (원/㎡)", min_value=0.0, value=12000.0, step=100.0)
            glass_unit_cost = 0.0
        else:
            glass_unit_cost = st.number_input("글라스 원단 단가 (원/kg)", min_value=0.0, value=8500.0, step=100.0)
            synthetic_unit_cost = 0.0

        urethane_unit_cost = st.number_input("우레탄 단가 (원/kg)", min_value=0.0, value=3700.0, step=100.0)

    with col2:
        if filter_type == "MINI":
            hotmelt_unit_cost = st.number_input("핫멜트 단가 (원/kg)", min_value=0.0, value=3900.0, step=100.0)
            foil_unit_cost = 0.0
        else:
            foil_unit_cost = st.number_input("호일 단가 (원/kg)", min_value=0.0, value=8500.0, step=100.0)
            hotmelt_unit_cost = 0.0

    st.subheader("기본 입력")
    c1, c2 = st.columns(2)
    with c1:
        width = st.number_input("가로(mm)", min_value=0.0, value=594.0, step=1.0)
        height = st.number_input("세로(mm)", min_value=0.0, value=594.0, step=1.0)
        depth = st.number_input("두께(mm)", min_value=0.0, value=75.0, step=1.0)
        pleat_count = st.number_input("산수", min_value=0.0, value=100.0, step=1.0)
    with c2:
        pack_depth = st.number_input("팩두께(mm)", min_value=0.0, value=30.0, step=1.0)
        pack_height = st.number_input("팩높이(mm)", min_value=0.0, value=594.0, step=1.0)
        frame_cost = st.number_input("프레임 단가(원)", min_value=0.0, value=0.0, step=100.0)
        box_cost = st.number_input("박스 비용(원)", min_value=0.0, value=2000.0, step=100.0)

    vinyl_cost = st.number_input("비닐 비용(원)", min_value=0.0, value=500.0, step=100.0)

    st.subheader("부자재")
    s1, s2 = st.columns(2)
    with s1:
        sub1_name = st.text_input("부자재1 이름", value="탈취")
        sub2_name = st.text_input("부자재2 이름", value="가스켓")
        sub3_name = st.text_input("부자재3 이름", value="인쇄부직포")
        sub4_name = st.text_input("부자재4 이름", value="비닐")
        sub5_name = st.text_input("부자재5 이름", value="에어스루")
        sub6_name = st.text_input("부자재6 이름", value="박스")
    with s2:
        sub1_cost = st.number_input("부자재1 금액(원)", min_value=0.0, value=0.0, step=100.0)
        sub2_cost = st.number_input("부자재2 금액(원)", min_value=0.0, value=0.0, step=100.0)
        sub3_cost = st.number_input("부자재3 금액(원)", min_value=0.0, value=0.0, step=100.0)
        sub4_cost = st.number_input("부자재4 금액(원)", min_value=0.0, value=0.0, step=100.0)
        sub5_cost = st.number_input("부자재5 금액(원)", min_value=0.0, value=0.0, step=100.0)
        sub6_cost = st.number_input("부자재6 금액(원)", min_value=0.0, value=0.0, step=100.0)

    st.subheader("비율 설정")
    r1, r2, r3, r4, r5 = st.columns(5)
    with r1:
        loss_rate = st.number_input("로스(%)", min_value=0.0, value=5.0, step=1.0)
    with r2:
        labor_rate = st.number_input("인건비(%)", min_value=0.0, value=30.0, step=1.0)
    with r3:
        sgna_rate = st.number_input("판관비(%)", min_value=0.0, value=15.0, step=1.0)
    with r4:
        interest_rate = st.number_input("이자비용(%)", min_value=0.0, value=9.0, step=1.0)
    with r5:
        margin_rate = st.number_input("마진(%)", min_value=0.0, value=20.0, step=1.0)

    if st.button("산업용 계산하기", use_container_width=True):
        media_area = (pleat_count * 2 * pack_depth * pack_height) / 1_000_000

        if media_type == "SYNTHETIC":
            media_weight = 0.0
            media_cost = media_area * synthetic_unit_cost
            media_formula = "SYNTHETIC: 면적 × 신세틱 단가(원/㎡)"
        else:
            media_weight = media_area * 0.08
            media_cost = media_weight * glass_unit_cost
            media_formula = "GLASS: 면적 × 0.08kg/㎡ × 글라스 단가(원/kg)"

        foil_weight = 0.0
        foil_cost = 0.0
        if filter_type == "SEPARATOR":
            unit = separator_unit_weight(depth)
            if unit is None:
                st.error("SEPARATOR TYPE은 두께 150 또는 292만 지원합니다.")
                st.stop()
            foil_weight = pleat_count * 2 * unit
            foil_cost = foil_weight * foil_unit_cost

        urethane_area = (width * depth * 2) / 1_000_000
        urethane_weight = urethane_area * 12
        urethane_cost = urethane_weight * urethane_unit_cost
        if grade_type == "미디움":
            urethane_cost = urethane_cost / 3

        hotmelt_lines = 0
        hotmelt_length_m = 0.0
        hotmelt_weight_g = 0.0
        hotmelt_cost = 0.0
        if filter_type == "MINI":
            hotmelt_lines = math.ceil(height / 25) if height > 0 else 0
            hotmelt_length_mm = hotmelt_lines * pleat_count * depth
            hotmelt_length_m = hotmelt_length_mm / 1000
            hotmelt_weight_g = hotmelt_length_m * 2
            hotmelt_cost = (hotmelt_weight_g / 1000) * hotmelt_unit_cost

        sub_total = sub1_cost + sub2_cost + sub3_cost + sub4_cost + sub5_cost + sub6_cost
        material_cost = media_cost + foil_cost + urethane_cost + hotmelt_cost + frame_cost + box_cost + vinyl_cost + sub_total

        loss_cost = material_cost * (loss_rate / 100)
        subtotal_after_loss = material_cost + loss_cost
        labor_cost = subtotal_after_loss * (labor_rate / 100)
        sgna_cost = subtotal_after_loss * (sgna_rate / 100)
        interest_cost = subtotal_after_loss * (interest_rate / 100)
        total_cost = subtotal_after_loss + labor_cost + sgna_cost + interest_cost
        selling_price = total_cost * (1 + margin_rate / 100)

        st.subheader("산업용 계산 결과")
        st.write(f"등급선택: {grade_type}")
        st.write(f"여재 계산식: {media_formula}")
        st.write(f"여재면적: {media_area:.4f} ㎡")
        st.write(f"여재무게: {media_weight:.4f} kg" if media_type == "GLASS" else "여재무게: -")
        st.write(f"여재원가: {money(media_cost)}")
        if filter_type == "SEPARATOR":
            st.write(f"호일무게: {foil_weight:.4f} kg")
            st.write(f"호일원가: {money(foil_cost)}")
        st.write(f"우레탄원가: {money(urethane_cost)}")
        if filter_type == "MINI":
            st.write(f"핫멜트 라인수: {hotmelt_lines}")
            st.write(f"핫멜트 길이: {hotmelt_length_m:.2f} m")
            st.write(f"핫멜트 무게: {hotmelt_weight_g:.2f} g")
            st.write(f"핫멜트원가: {money(hotmelt_cost)}")
        st.write(f"프레임원가: {money(frame_cost)}")
        st.write(f"부자재합: {money(sub_total)}")
        st.caption(
            f"재료비 검산 = 여재({money(media_cost)}) + 호일({money(foil_cost)}) + 우레탄({money(urethane_cost)}) + 핫멜트({money(hotmelt_cost)}) + 프레임({money(frame_cost)}) + 박스({money(box_cost)}) + 비닐({money(vinyl_cost)}) + 부자재합({money(sub_total)})"
        )
        st.write(f"재료비 합계: {money(material_cost)}")
        st.write(f"로스비용: {money(loss_cost)}")
        st.write(f"인건비: {money(labor_cost)}")
        st.write(f"판관비: {money(sgna_cost)}")
        st.write(f"이자비용: {money(interest_cost)}")
        st.write(f"총원가: {money(total_cost)}")
        st.success(f"판매가: {money(selling_price)}")

# =========================================================
# 2) 가정용 평판 : 산업용과 완전 분리
# =========================================================
elif product_group == "가정용 평판":
    st.subheader("가정용 평판 원가설정")
    media_unit_cost = st.number_input("원단 단가 (원/㎡)", min_value=0.0, value=12000.0, step=100.0, key="flat_media")
    hotmelt_unit_cost = st.number_input("핫멜트 단가 (원/kg)", min_value=0.0, value=3900.0, step=100.0, key="flat_hotmelt")
    band_unit_cost = st.number_input("띠밴드 단가 (원/m)", min_value=0.0, value=500.0, step=10.0, key="flat_band")
    band_width_mm = st.number_input("띠밴드 폭 (mm)", min_value=0.0, value=20.0, step=1.0, key="flat_band_width")

    st.subheader("가정용 평판 기본 입력")
    c1, c2 = st.columns(2)
    with c1:
        width = st.number_input("가로(mm)", min_value=0.0, value=300.0, step=1.0, key="flat_width")
        height = st.number_input("세로(mm)", min_value=0.0, value=300.0, step=1.0, key="flat_height")
        depth = st.number_input("두께(mm)", min_value=0.0, value=20.0, step=1.0, key="flat_depth")
    with c2:
        pleat_count = st.number_input("산수", min_value=0.0, value=50.0, step=1.0, key="flat_pleat")
        frame_cost = st.number_input("프레임 단가(원)", min_value=0.0, value=0.0, step=100.0, key="flat_frame")

    st.subheader("가정용 평판 부자재")
    deodorant_cost = st.number_input("탈취 금액(원)", min_value=0.0, value=0.0, step=100.0, key="flat_deo")
    gasket_cost = st.number_input("가스켓 금액(원)", min_value=0.0, value=0.0, step=100.0, key="flat_gasket")
    print_nonwoven_cost = st.number_input("인쇄부직포 금액(원)", min_value=0.0, value=0.0, step=100.0, key="flat_print")
    vinyl_cost = st.number_input("비닐 금액(원)", min_value=0.0, value=0.0, step=100.0, key="flat_vinyl")
    air_through_cost = st.number_input("에어스루 금액(원)", min_value=0.0, value=0.0, step=100.0, key="flat_air")
    box_cost = st.number_input("박스 금액(원)", min_value=0.0, value=0.0, step=100.0, key="flat_box")

    st.subheader("비율 설정")
    r1, r2, r3, r4, r5 = st.columns(5)
    with r1:
        loss_rate = st.number_input("로스(%)", min_value=0.0, value=5.0, step=1.0, key="flat_loss")
    with r2:
        labor_rate = st.number_input("인건비(%)", min_value=0.0, value=30.0, step=1.0, key="flat_labor")
    with r3:
        sgna_rate = st.number_input("판관비(%)", min_value=0.0, value=15.0, step=1.0, key="flat_sgna")
    with r4:
        interest_rate = st.number_input("이자비용(%)", min_value=0.0, value=9.0, step=1.0, key="flat_interest")
    with r5:
        margin_rate = st.number_input("마진(%)", min_value=0.0, value=20.0, step=1.0, key="flat_margin")

    if st.button("가정용 평판 계산하기", use_container_width=True):
        pack_width = max(width - 2, 0)
        pack_height = max(height - 2, 0)
        pack_depth = max(depth - 2, 0)

        media_area = (pleat_count * 2 * pack_height * pack_depth) / 1_000_000
        media_cost = media_area * media_unit_cost

        hotmelt_lines = math.ceil(pack_height / 25.4) if pack_height > 0 else 0
        hotmelt_length_mm = hotmelt_lines * pleat_count * pack_depth
        hotmelt_length_m = hotmelt_length_mm / 1000
        hotmelt_weight_g = hotmelt_length_m * 2
        hotmelt_cost = (hotmelt_weight_g / 1000) * hotmelt_unit_cost

        band_length_mm = 2 * (pack_width + pack_height)
        band_length_m = band_length_mm / 1000
        band_cost = band_length_m * band_unit_cost

        band_hotmelt_area = band_length_m * (band_width_mm / 1000)
        band_hotmelt_weight_kg = band_hotmelt_area * 2
        band_hotmelt_cost = band_hotmelt_weight_kg * hotmelt_unit_cost

        others = deodorant_cost + gasket_cost + print_nonwoven_cost + vinyl_cost + air_through_cost + box_cost
        material_cost = media_cost + hotmelt_cost + band_cost + band_hotmelt_cost + frame_cost + others

        loss_cost = material_cost * (loss_rate / 100)
        subtotal_after_loss = material_cost + loss_cost
        labor_cost = subtotal_after_loss * (labor_rate / 100)
        sgna_cost = subtotal_after_loss * (sgna_rate / 100)
        interest_cost = subtotal_after_loss * (interest_rate / 100)
        total_cost = subtotal_after_loss + labor_cost + sgna_cost + interest_cost
        selling_price = total_cost * (1 + margin_rate / 100)

        st.subheader("가정용 평판 계산 결과")
        st.write(f"팩 가로: {pack_width:.0f} mm")
        st.write(f"팩 세로: {pack_height:.0f} mm")
        st.write(f"팩 두께: {pack_depth:.0f} mm")
        st.write(f"원단면적: {media_area:.4f} ㎡")
        st.write(f"원단원가: {money(media_cost)}")
        st.write(f"핫멜트 라인수: {hotmelt_lines}")
        st.write(f"핫멜트원가: {money(hotmelt_cost)}")
        st.write(f"띠밴드 길이: {band_length_m:.2f} m")
        st.write(f"띠밴드원가: {money(band_cost)}")
        st.write(f"띠밴드 핫멜트 무게: {band_hotmelt_weight_kg:.4f} kg")
        st.write(f"띠밴드 핫멜트원가: {money(band_hotmelt_cost)}")
        st.write(f"기타 부자재 합: {money(others)}")
        st.write(f"재료비 합계: {money(material_cost)}")
        st.write(f"로스비용: {money(loss_cost)}")
        st.write(f"인건비: {money(labor_cost)}")
        st.write(f"판관비: {money(sgna_cost)}")
        st.write(f"이자비용: {money(interest_cost)}")
        st.write(f"총원가: {money(total_cost)}")
        st.success(f"판매가: {money(selling_price)}")

# =========================================================
# 3) 가정용 원형 : 산업용과 완전 분리
# =========================================================
else:
    st.subheader("가정용 원형 원가설정")
    media_unit_cost = st.number_input("원단 단가 (원/㎡)", min_value=0.0, value=12000.0, step=100.0, key="cyl_media")
    hotmelt_unit_cost = st.number_input("핫멜트 단가 (원/kg)", min_value=0.0, value=3900.0, step=100.0, key="cyl_hotmelt")

    st.subheader("가정용 원형 기본 입력")
    c1, c2 = st.columns(2)
    with c1:
        width = st.number_input("팩 가로(mm)", min_value=0.0, value=300.0, step=1.0, key="cyl_width")
        height = st.number_input("팩 세로(mm)", min_value=0.0, value=300.0, step=1.0, key="cyl_height")
    with c2:
        depth = st.number_input("팩 두께(mm)", min_value=0.0, value=20.0, step=1.0, key="cyl_depth")
        pleat_count = st.number_input("산수", min_value=0.0, value=50.0, step=1.0, key="cyl_pleat")

    st.subheader("가정용 원형 부자재")
    gasket_cost = st.number_input("가스켓 금액(원)", min_value=0.0, value=0.0, step=100.0, key="cyl_gasket")
    honeycomb_cost = st.number_input("종이허니컴 금액(원)", min_value=0.0, value=0.0, step=100.0, key="cyl_honeycomb")
    carbon_nonwoven_cost = st.number_input("카본부직포 금액(원)", min_value=0.0, value=0.0, step=100.0, key="cyl_carbon")
    mesh_cost = st.number_input("망 금액(원)", min_value=0.0, value=0.0, step=100.0, key="cyl_mesh")
    cap_cost = st.number_input("캡 금액(원)", min_value=0.0, value=0.0, step=100.0, key="cyl_cap")
    air_through_cost = st.number_input("에어스루 금액(원)", min_value=0.0, value=0.0, step=100.0, key="cyl_air")
    vinyl_cost = st.number_input("비닐 금액(원)", min_value=0.0, value=0.0, step=100.0, key="cyl_vinyl")
    box_cost = st.number_input("박스 금액(원)", min_value=0.0, value=0.0, step=100.0, key="cyl_box")

    st.subheader("비율 설정")
    r1, r2, r3, r4, r5 = st.columns(5)
    with r1:
        loss_rate = st.number_input("로스(%)", min_value=0.0, value=5.0, step=1.0, key="cyl_loss")
    with r2:
        labor_rate = st.number_input("인건비(%)", min_value=0.0, value=30.0, step=1.0, key="cyl_labor")
    with r3:
        sgna_rate = st.number_input("판관비(%)", min_value=0.0, value=15.0, step=1.0, key="cyl_sgna")
    with r4:
        interest_rate = st.number_input("이자비용(%)", min_value=0.0, value=9.0, step=1.0, key="cyl_interest")
    with r5:
        margin_rate = st.number_input("마진(%)", min_value=0.0, value=20.0, step=1.0, key="cyl_margin")

    if st.button("가정용 원형 계산하기", use_container_width=True):
        media_area = (pleat_count * 2 * height * depth) / 1_000_000
        media_cost = media_area * media_unit_cost

        hotmelt_lines = math.ceil(height / 25) if height > 0 else 0
        hotmelt_length_mm = hotmelt_lines * pleat_count * depth
        hotmelt_length_m = hotmelt_length_mm / 1000
        hotmelt_weight_g = hotmelt_length_m * 2
        hotmelt_cost = (hotmelt_weight_g / 1000) * hotmelt_unit_cost

        others = gasket_cost + honeycomb_cost + carbon_nonwoven_cost + mesh_cost + cap_cost + air_through_cost + vinyl_cost + box_cost
        material_cost = media_cost + hotmelt_cost + others

        loss_cost = material_cost * (loss_rate / 100)
        subtotal_after_loss = material_cost + loss_cost
        labor_cost = subtotal_after_loss * (labor_rate / 100)
        sgna_cost = subtotal_after_loss * (sgna_rate / 100)
        interest_cost = subtotal_after_loss * (interest_rate / 100)
        total_cost = subtotal_after_loss + labor_cost + sgna_cost + interest_cost
        selling_price = total_cost * (1 + margin_rate / 100)

        st.subheader("가정용 원형 계산 결과")
        st.write(f"원단면적: {media_area:.4f} ㎡")
        st.write(f"원단원가: {money(media_cost)}")
        st.write(f"핫멜트 라인수: {hotmelt_lines}")
        st.write(f"핫멜트 길이: {hotmelt_length_m:.2f} m")
        st.write(f"핫멜트 무게: {hotmelt_weight_g:.2f} g")
        st.write(f"핫멜트원가: {money(hotmelt_cost)}")
        st.write(f"기타 부자재 합: {money(others)}")
        st.write(f"재료비 합계: {money(material_cost)}")
        st.write(f"로스비용: {money(loss_cost)}")
        st.write(f"인건비: {money(labor_cost)}")
        st.write(f"판관비: {money(sgna_cost)}")
        st.write(f"이자비용: {money(interest_cost)}")
        st.write(f"총원가: {money(total_cost)}")
        st.success(f"판매가: {money(selling_price)}")

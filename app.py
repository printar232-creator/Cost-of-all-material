import streamlit as st

# ตั้งค่าหน้าเว็บให้เป็นแบบกว้างเพื่อให้เห็นทุกอย่างในหน้าเดียว
st.set_page_config(page_title="Cost Calculator", layout="wide")

# CSS เพื่อลด padding และระยะห่างเพื่อให้เหมาะกับการแคปภาพ
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    div[data-testid="stVerticalBlock"] > div {
        margin-top: -10px;
    }
    h1, h2, h3 {
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Cost Calculator: LAOS (NONG KHAI)")

# --- ส่วนที่ 1: ตั้งค่าเบื้องต้น ---
col_head1, col_head2 = st.columns([2, 1])
with col_head1:
    package_size = st.radio("บรรจุภัณฑ์ (Package Size):", ["25kg", "50kg"], horizontal=True)
with col_head2:
    loss_percentage = st.number_input("% Loss (สูญเสีย)", min_value=0.0, value=0.0, step=0.1)

st.divider()

# --- ส่วนที่ 2: วัตถุดิบและค่าใช้จ่าย (แบ่งเป็น 3 คอลัมน์เพื่อความประหยัดเนื้อที่) ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🛠 Material")
    base_material_cost = st.number_input("MATERIAL+CLEAR,TRANSPORT", value=4766.666667, format="%.6f")
    
    # คำนวณต้นทุนวัตถุดิบรวมสูญเสีย
    if loss_percentage < 100:
        calc_mat_cost = base_material_cost / (1 - (loss_percentage / 100))
    else:
        calc_mat_cost = 0.0
    st.info(f"Mat Cost (+Loss): **{calc_mat_cost:,.2f}**")

with col2:
    st.subheader("⚡ Utilities & Labor")
    maintenance = st.number_input("MAINTANANCE", value=120.5641558, format="%.6f")
    electricity = st.number_input("ELECTRICITY", value=335.3956996, format="%.6f")
    water = st.number_input("WATER SECTION", value=0.0)
    labour = st.number_input("LABOUR", value=1587.691604, format="%.6f")

with col3:
    st.subheader("📦 Others")
    if package_size == "25kg":
        packaging = st.number_input("PAKAGING (25kg)", value=414.5)
    else:
        packaging = st.number_input("PAKAGING (50kg)", value=476.0)
    
    oil = st.number_input("OIL", value=47.3762619, format="%.6f")
    brass = st.number_input("BRASS", value=22.0358699, format="%.6f")
    imp_exp = st.number_input("IMPORT/EXPORT", value=0.0)
    commission = st.number_input("COMISSTION", value=0.0)

# --- ส่วนที่ 3: คำนวณและสรุปผล ---
all_cost_no_material = maintenance + electricity + water + labour + packaging + oil + brass + imp_exp + commission
total_cost = calc_mat_cost + all_cost_no_material

st.divider()

# แสดงผลลัพธ์สุดท้ายแบบเน้นๆ ให้แคปภาพสวยๆ
res_col1, res_col2 = st.columns(2)
with res_col1:
    st.metric("ALL COST (NO MATERIAL)", f"{all_cost_no_material:,.4

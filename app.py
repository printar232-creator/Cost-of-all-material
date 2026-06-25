import streamlit as st

# 1. ตั้งค่าหน้าเว็บเป็นแบบ Wide เพื่อให้แสดงผลได้ครบในหน้าเดียว
st.set_page_config(page_title="Cost Calculator", layout="wide")

# หัวกระดาษหลัก
st.title("📊 Cost Calculator: LAOS (NONG KHAI)")

# --- ส่วนที่ 1: การตั้งค่าขนาดและ % Loss ---
col_h1, col_h2 = st.columns([2, 1])
with col_h1:
    package_size = st.radio("บรรจุภัณฑ์ (Package Size):", ["25kg", "50kg"], horizontal=True)
with col_h2:
    loss_percentage = st.number_input("% Loss (สูญเสีย)", min_value=0.0, max_value=99.9, value=0.0, step=0.1)

st.divider()

# --- ส่วนที่ 2: กรอกข้อมูลค่าใช้จ่าย (แบ่ง 3 คอลัมน์เพื่อประหยัดเนื้อที่หน้าจอ) ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🛠 Material Cost")
    base_material_cost = st.number_input("MATERIAL+CLEAR,TRANSPORT", value=4766.666667, format="%.6f")
    
    # คำนวณต้นทุนวัตถุดิบรวม % Loss
    calc_mat_cost = base_material_cost / (1 - (loss_percentage / 100))
    st.info(f"Mat Cost (+Loss): {calc_mat_cost:,.6f}")

with col2:
    st.markdown("### ⚡ Utilities & Labor")
    maintenance = st.number_input("MAINTANANCE", value=120.5641558, format="%.6f")
    electricity = st.number_input("ELECTRICITY", value=335.3956996, format="%.6f")
    water = st.number_input("WATER SECTION", value=0.0, format="%.6f")
    labour = st.number_input("LABOUR", value=1587.691604, format="%.6f")

with col3:
    st.markdown("### 📦 Others & Packaging")
    if package_size == "25kg":
        packaging = st.number_input("PAKAGING (25kg)", value=414.50, format="%.2f")
    else:
        packaging = st.number_input("PAKAGING (50kg)", value=476.00, format="%.2f")
    
    oil = st.number_input("OIL", value=47.3762619, format="%.6f")
    brass = st.number_input("BRASS", value=22.0358699, format="%.6f")
    imp_exp = st.number_input("IMPORT AND EXPORTS", value=0.0, format="%.6f")
    commission = st.number_input("COMISSTION", value=0.0, format="%.6f")

st.divider()

# --- ส่วนที่ 3: การคำนวณและสร

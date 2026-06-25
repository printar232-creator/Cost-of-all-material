import streamlit as st

# 1. ตั้งค่าหน้าเว็บเป็นแบบ Wide เพื่อการแคปภาพหน้าจอที่สมบูรณ์
st.set_page_config(page_title="Cost Calculator", layout="wide")

# หัวกระดาษหลัก
st.title("📊 Cost Calculator: LAOS (NONG KHAI)")

# --- ส่วนที่ 1: การตั้งค่าขนาดและ % Loss ---
col_h1, col_h2 = st.columns([2, 1])
with col_h1:
    package_size = st.radio("บรรจุภัณฑ์ (Package Size):", ["25kg", "50kg"], horizontal=True)
with col_h2:
    loss_percentage = st.number_input("% Loss (สูญเสีย)", min_value=0.0, max_value=99.9, value=10.0, step=0.1)

st.divider()

# --- นำส่วนการคำนวณมาคิดก่อนเพื่อนำผลลัพธ์ไปแสดงผลด้านบน ---
# ค่าเริ่มต้นสำหรับคำนวณเบื้องต้น (จะเปลี่ยนตามค่าที่ผู้ใช้กรอกในตารางด้านล่าง)
base_material_cost = 4290.000000

# ตรวจสอบค่าใน session_state เพื่อดึงข้อมูลสดใหม่มาคำนวณก่อนสร้างตารางด้านล่าง
if 'mat_input' in st.session_state: base_material_cost = st.session_state['mat_input']
if 'maint_input' in st.session_state: maintenance = st.session_state['maint_input']
else: maintenance = 120.564156
if 'elec_input' in st.session_state: electricity = st.session_state['elec_input']
else: electricity = 335.395700
if 'water_input' in st.session_state: water = st.session_state['water_input']
else: water = 0.0
if 'labour_input' in st.session_state: labour = st.session_state['labour_input']
else: labour = 1587.691604
if 'oil_input' in st.session_state: oil = st.session_state['oil_input']
else: oil = 47.376262
if 'brass_input' in st.session_state: brass = st.session_state['brass_input']
else: brass = 22.035870
if 'imp_input' in st.session_state: imp_exp = st.session_state['imp_input']
else: imp_exp = 0.0
if 'comm_input' in st.session_state: commission = st.session_state['comm_input']
else: commission = 0.0

if package_size == "25kg":
    packaging = st.session_state.get('pkg_input_25', 414.50)
else:
    packaging = st.session_state.get('pkg_input_50', 476.00)

# คำนวณตามสูตร
calc_mat_cost = base_material_cost / (1 - (loss_percentage / 100)) if loss_percentage < 100 else 0.0
all_cost_no_material = maintenance + electricity + water + labour + packaging + oil + brass + imp_exp + commission
total_cost = calc_mat_cost + all_cost_no_material


# --- ส่วนที่ 2: กล่องแสดงผลสรุปรวม (ย้ายขึ้นมาไว้ด้านบนเพื่อไม่ให้ตกขอบจอ) ---
st.markdown("### 📋 ผลลัพธ์การคำนวณสุทธิ")
res_col1, res_col2 = st.columns(2)

with res_col1:
    st.metric(label="ALL COST (NO MATERIAL) - สรุปรวมค่าใช้จ่ายทั้งหมด", value=f"{all_cost_no_material:,.6f}")

with res_col2:
    # แถบไฮไลท์สีเหลืองแสดงต้นทุนรวมสุทธิ (Total Cost)
    st.markdown(f"""
        <div style="background-color: #FFFF00; padding: 15px; border-radius: 8px; border: 2px solid #000; text-

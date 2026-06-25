import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บหน้าตาแอปพลิเคชัน
st.set_page_config(page_title="AMR Cost Calculator", layout="centered")

st.title("📊 ระบบคำนวณและแสดงต้นทุนสินค้า (Cost Breakdown)")
st.write("เลือกข้อมูลเพื่อแสดงต้นทุนย่อยและต้นทุนรวมของผลิตภัณฑ์")

# 1. ฟังก์ชันโหลดข้อมูล (แนะนำให้เปลี่ยน URL เป็นลิงก์ Raw ของ GitHub คุณเอง)
@st.cache_data
def load_data():
    # ตัวอย่างการใส่ค่า Mockup ข้อมูลตามโครงสร้างไฟล์ของคุณ 
    # หากใช้งานจริงให้เปิดใช้งานบรรทัดด้านล่างนี้แล้วใส่ URL ไฟล์จริงบน GitHub:
    # url = "https://raw.githubusercontent.com/username/repo/main/cost_data.csv"
    # return pd.read_csv(url)
    
    mock_data = {
        'product_type': ['M5', 'M5', 'M7', 'M10', 'A45', 'B45', 'C5', 'D45'],
        'packaging': ['25kg', '50kg', '25kg', '25kg', '25kg', '50kg', '25kg', 'big bag'],
        'source': ['CHINA', 'LAOS', 'CHINA', 'LAOS', 'CHINA', 'LAOS', 'CHINA', 'LAOS'],
        'ค่าวัตถุดิบ (Raw Material)': [7718, 6400, 8200, 6400, 7718, 4700, 4290, 3400],
        'ค่าไฟโรงงาน (Electricity)': [804.95, 431.81, 804.95, 431.81, 631.29, 431.81, 804.95, 631.29],
        'ค่าซ่อมบำรุง (Maintenance)': [145.78, 302.86, 145.78, 302.86, 145.78, 302.86, 145.78, 145.78],
        'ค่าแรงฝ่ายผลิต (Labor)': [1587.69, 1850.46, 1587.69, 1850.46, 1587.69, 1850.46, 1587.69, 1587.69],
        'ค่าบรรจุภัณฑ์และพาเลท (Bag/Pallet)': [479.47, 550.00, 479.47, 479.47, 1202.44, 600.00, 479.47, 160.00]
    }
    df = pd.DataFrame(mock_data)
    return df

df = load_data()

# 2. ส่วนของตัวเลือก Filter (Drop-down Selectbox)
st.subheader("🔍 ระบุเงื่อนไขผลิตภัณฑ์")

col1, col2, col3 = st.columns(3)

with col1:
    product_list = sorted(df['product_type'].unique())
    selected_product = st.selectbox("1. Type of Product", ["-- กรุณาเลือก --"] + product_list)

# กรอง Packaging ตาม Product ที่เลือก (Dynamic Filter)
if selected_product != "-- กรุณาเลือก --":
    filtered_pack = df[df['product_type'] == selected_product]['packaging'].unique()
    pack_list = sorted(filtered_pack)
else:
    pack_list = []

with col2:
    selected_pack = st.selectbox("2. Packaging", ["-- กรุณาเลือก --"] + list(pack_list), disabled=(selected_product == "-- กรุณาเลือก --"))

# กรอง Source ตาม Product และ Packaging ที่เลือก
if selected_product != "-- กรุณาเลือก --" and selected_pack != "-- กรุณาเลือก --":
    filtered_source = df[(df['product_type'] == selected_product) & (df['packaging'] == selected_pack)]['source'].unique()
    source_list = sorted(filtered_source)
else:
    source_list = []

with col3:
    selected_source = st.selectbox("3. Source", ["-- กรุณาเลือก --"] + list(source_list), disabled=(selected_pack == "-- กรุณาเลือก --"))

st.markdown("---")

# 3. ประมวลผลและแสดงต้นทุนย่อย + ต้นทุนรวม เมื่อเลือกครบ 3 รายการ
if (selected_product != "-- กรุณาเลือก --" and 
    selected_pack != "-- กรุณาเลือก --" and 
    selected_source != "-- กรุณาเลือก --"):
    
    # ดึงแถวข้อมูลที่ตรงตามเงื่อนไข
    result = df[
        (df['product_type'] == selected_product) & 
        (df['packaging'] == selected_pack) & 
        (df['source'] == selected_source)
    ]
    
    if not result.empty:
        st.success(### รหัสสินค้าที่เลือก: {selected_product} ({selected_pack}) - แหล่งวัตถุดิบ: {selected_source}")
        
        # แยกข้อมูลต้นทุนย่อย
        cost_columns = [
            'ค่าวัตถุดิบ (Raw Material)', 
            'ค่าไฟโรงงาน (Electricity)', 
            'ค่าซ่อมบำรุง (Maintenance)', 
            'ค่าแรงฝ่ายผลิต (Labor)', 
            'ค่าบรรจุภัณฑ์และพาเลท (Bag/Pallet)'
        ]
        
        # คำนวณต้นทุนรวมในแถวนั้น
        sub_costs = result[cost_columns].iloc[0]
        total_cost = sub_costs.sum()
        
        # แสดงผลต้นทุนรวมแบบเน้นย้ำด้วย st.metric
        st.metric(label="💰 ต้นทุนรวมทั้งหมด (Total Cost / MT)", value=f"{total_cost:,.2f} บาท")
        
        # แสดงตารางแจกแจงต้นทุนย่อยๆ เพื่อความชัดเจน
        st.subheader("📋 รายละเอียดต้นทุนย่อย (Cost Breakdown)")
        
        breakdown_df = pd.DataFrame({
            'รายการต้นทุน': sub_costs.index,
            'มูลค่า (บาท/ตัน)': sub_costs.values
        })
        
        # ตกแต่ง Format ตัวเลขในตารางให้สวยงาม
        breakdown_df['มูลค่า (บาท/ตัน)'] = breakdown_df['มูลค่า (บาท/ตัน)'].map('{:,.2f}'.format)
        st.table(breakdown_df)
        
    else:
        st.warning("❌ ไม่พบข้อมูลต้นทุนที่ตรงกับเงื่อนไขนี้ในระบบ")
else:
    st.info("💡 โปรดเลือกเงื่อนไขด้านบนให้ครบทั้ง 3 ช่อง เพื่อเปิดดูรายงานต้นทุน")

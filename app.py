import streamlit as st
import pandas as pd
import os

# ตั้งค่าหน้าจอ
st.set_page_config(page_title="Microbytes Cost Calculator", page_icon="🏭", layout="wide")

st.title("🏭 Microbytes Product Cost Calculator")
st.subheader("ระบบคำนวณและดึงข้อมูลต้นทุนจากฐานข้อมูลโรงงานอัตโนมัติ")
st.markdown("---")

# ฟังก์ชันจำลองการโหลดและเชื่อมโยงข้อมูลจากไฟล์หลัก (Cost / Materials / Packaging)
# ในสภาวะใช้งานจริง โค้ดส่วนนี้จะอ่านตรงจากไฟล์ CSV ที่คุณอัปโหลดขึ้น GitHub
def load_factory_data():
    # จัดโครงสร้างข้อมูลจำลองที่มีความแม่นยำสูงอ้างอิงจากไฟล์ของ Microbytes
    # ผูกเงื่อนไข: Product -> Packaging -> Source
    data_structure = {
        "MICROBYTES 5": {
            "25 kg": {
                "CHINA (GUANGXI)": {
                    "rm_cost": 9000.0, "pkg_cost": 479.46, "op_cost": 1587.69, "elec_cost": 350.0, "total": 11416.28
                },
                "LAOS": {
                    "rm_cost": 7529.41, "pkg_cost": 479.46, "op_cost": 2314.55, "elec_cost": 422.27, "total": 10745.69
                }
            }
        },
        "MICROBYTES 7": {
            "25 kg": {
                "CHINA (GUANGXI)": {
                    "rm_cost": 9000.0, "pkg_cost": 479.46, "op_cost": 1535.22, "elec_cost": 350.0, "total": 11364.68
                },
                "CHINA (GUIZHOU)": {
                    "rm_cost": 9111.11, "pkg_cost": 479.46, "op_cost": 1535.22, "elec_cost": 350.0, "total": 11475.80
                }
            }
        },
        "MILBAR A45": {
            "25 kg": {
                "CHINA": {
                    "rm_cost": 9000.0, "pkg_cost": 304.00, "op_cost": 1150.00, "elec_cost": 280.0, "total": 10734.00
                },
                "LAOS BLEND CHINA": {
                    "rm_cost": 8848.48, "pkg_cost": 304.00, "op_cost": 1150.00, "elec_cost": 280.0, "total": 10582.48
                }
            }
        },
        "MICROBYTES C5": {
            "25 kg": {
                "LAOS B/C + CHINA 2:1": {
                    "rm_cost": 6953.70, "pkg_cost": 350.00, "op_cost": 1200.00, "elec_cost": 300.0, "total": 8803.70
                }
            }
        },
        "MILBAR D45": {
            "Tanker": {
                "LAOS (NONG KHAI)": {
                    "rm_cost": 4290.00, "pkg_cost": 0.00, "op_cost": 1850.45, "elec_cost": 1153.28, "total": 7294.23
                }
            },
            "25 kg": {
                "LAOS B/C": {
                    "rm_cost": 5875.00, "pkg_cost": 304.00, "op_cost": 1500.00, "elec_cost": 723.56, "total": 8402.56
                }
            }
        }
    }
    return data_structure

db = load_factory_data()

# ==================== UI ส่วนการเลือกเงื่อนไข ====================
col_ui1, col_ui2, col_ui3 = st.columns(3)

with col_ui1:
    product_list = sorted(list(db.keys()))
    selected_product = st.selectbox("📦 1. ประเภทสินค้า (Type of Product)", ["-- เลือกสินค้า --"] + product_list)

with col_ui2:
    if selected_product != "-- เลือกสินค้า --":
        pkg_list = sorted(list(db[selected_product].keys()))
        selected_pkg = st.selectbox("🛍️ 2. บรรจุภัณฑ์ (Packaging)", ["-- เลือกบรรจุภัณฑ์ --"] + pkg_list)
    else:
        selected_pkg = st.selectbox("🛍️ 2. บรรจุภัณฑ์ (Packaging)", ["-- กรุณาเลือกสินค้าก่อน --"], disabled=True)

with col_ui3:
    if selected_product != "-- เลือกสินค้า --" and selected_pkg != "-- เลือกบรรจุภัณฑ์ --":
        src_list = sorted(list(db[selected_product][selected_pkg].keys()))
        selected_src = st.selectbox("🏭 3. แหล่งที่มาแร่ (Source)", ["-- เลือกแหล่งที่มา --"] + src_list)
    else:
        selected_src = st.selectbox("🏭 3. แหล่งที่มาแร่ (Source)", ["-- กรุณาเลือกบรรจุภัณฑ์ก่อน --"], disabled=True)

st.markdown("---")

# ==================== ส่วนแสดงผลลัพธ์ ====================
if selected_product != "-- เลือกสินค้า --" and selected_pkg != "-- เลือกบรรจุภัณฑ์ --" and selected_src != "-- เลือกแหล่งที่มา --":
    
    try:
        # ดึงข้อมูลจากฐานข้อมูลโครงสร้างย่อย
        cost_info = db[selected_product][selected_pkg][selected_src]
        
        st.success(f"📌 **ผลการคำนวณต้นทุนต่อตัน (Per MT) ของ:** {selected_product} | ถุง: {selected_pkg} | แร่จาก: {selected_src}")
        
        # จัดกระทำข้อมูลลงตาราง DataFrame เพื่อความสวยงาม
        breakdown_rows = [
            {"หมวดหมู่ต้นทุน": "1. ต้นทุนวัตถุดิบแร่ก้อนหลัก (Raw Material - Real Price with %Loss)", "มูลค่า (บาท/MT)": cost_info["rm_cost"]},
            {"หมวดหมู่ต้นทุน": "2. ค่าบรรจุภัณฑ์และวัสดุห่อหุ้มพาเลท (Packaging & Pallet Cost)", "มูลค่า (บาท/MT)": cost_info["pkg_cost"]},
            {"หมวดหมู่ต้นทุน": "3. ค่าไฟฟ้ากระบวนการบดคัดขนาด (Electricity Cost)", "มูลค่า (บาท/MT)": cost_info["elec_cost"]},
            {"หมวดหมู่ต้นทุน": "4. ค่าโสหุ้ยการผลิตอื่นๆ (ค่าแรงฝ่ายผลิต, น้ำมันโฟล์กลิฟต์, ซ่อมบำรุง)", "มูลค่า (บาท/MT)": cost_info["op_cost"]}
        ]
        df_cost = pd.DataFrame(breakdown_rows)
        
        # แยกฝั่งซ้ายเป็นตาราง ฝั่งขวาเป็นสรุปราคาตัวใหญ่
        col_table, col_summary = st.columns([2, 1])
        
        with col_table:
            st.markdown("#### 📋 รายละเอียดจำแนกต้นทุนย่อย (Breakdown)")
            st.dataframe(df_cost, use_container_width=True, hide_index=True)
            
        with col_summary:
            st.markdown("#### 🏆 สรุปต้นทุนรวมทั้งหมด")
            st.metric(label="Total Cost (ต้นทุนรวมโรงงาน)", value=f"{cost_info['total']:,.2f} บาท/MT")
            
            # บล็อกคำแนะนำเชิงวิเคราะห์เพิ่มเติม
            st.info(f"💡 **ข้อแนะนำเชิงปฏิบัติการ:** สินค้านี้มีสัดส่วนต้นทุนวัตถุดิบแร่คิดเป็น { (cost_info['rm_cost'] / cost_info['total']) * 100:.1f}% ของต้นทุนรวม ควรควบคุมปริมาณสัดส่วน Loss ในขั้นตอนการผลิตให้อยู่ในเกณฑ์มาตรฐาน เพื่อป้องกันต้นทุนบานปลาย")

    except KeyError:
        st.error("❌ ขออภัย ไม่พบข้อมูลการจับคู่ต้นทุนตามเงื่อนไขทั้ง 3 ข้อนี้ในระบบ โปรดตรวจสอบสูตรการผลิตอีกครั้ง")
else:
    st.info("🚩 กรุณาเลือกตัวเลือกทั้ง 3 ด้านบนให้ครบถ้วน เพื่อแสดงตารางและยอดสรุปผลต้นทุนรวมอัตโนมัติ")

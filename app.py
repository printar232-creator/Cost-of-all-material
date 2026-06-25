import streamlit as st
import pandas as pd

# ตั้งค่าหน้าจอแบบ Wide และชื่อแอป
st.set_page_config(page_title="Microbytes Cost Calculator", page_icon="🏭", layout="wide")

st.title("🏭 Microbytes Product Cost Calculator")
st.subheader("ระบบคำนวณและจำแนกต้นทุนแบ่งตาม บรรจุภัณฑ์ และแหล่งที่มาวัตถุดิบ")
st.markdown("---")

# ฟังก์ชันดึงข้อมูลโครงสร้างต้นทุนที่รองรับบรรจุภัณฑ์ทั้ง 4 ประเภท (25kg, 50kg, big bag, TANK)
def load_comprehensive_data():
    # ข้อมูลอ้างอิงเชิงลึกจากฐานข้อมูลต้นทุนจริงของโรงงาน
    matrix = {
        "MICROBYTES 5": {
            "25kg": {
                "CHINA GUANGXI": {"rm": 9000.00, "pkg": 479.46, "elec": 804.95, "op": 145.78, "total": 10430.19},
                "LAOS": {"rm": 7529.41, "pkg": 479.46, "elec": 804.95, "op": 145.78, "total": 8959.60}
            }
        },
        "MICROBYTES 7": {
            "25kg": {
                "CHINA GUANGXI": {"rm": 9000.00, "pkg": 479.46, "elec": 631.28, "op": 145.78, "total": 10256.52},
                "CHINA GUIZHOU": {"rm": 9111.11, "pkg": 479.46, "elec": 631.28, "op": 145.78, "total": 10367.63}
            }
        },
        "MILBAR C45": {
            "25kg": {
                "LAOS B/C": {"rm": 5875.00, "pkg": 304.00, "elec": 431.81, "op": 61.10, "total": 6671.91},
                "LAOS C/D": {"rm": 4337.50, "pkg": 304.00, "elec": 431.81, "op": 61.10, "total": 5134.41}
            },
            "50kg": {
                "LAOS B/C+CHINA": {"rm": 6953.70, "pkg": 280.00, "elec": 431.81, "op": 61.10, "total": 7726.61}
            }
        },
        "MILBAR D45": {
            "25kg": {
                "LAOS B/C": {"rm": 5875.00, "pkg": 304.00, "elec": 631.29, "op": 128.71, "total": 6939.00}
            },
            "50kg": {
                "LAOS (NONG KHAI)": {"rm": 4290.00, "pkg": 250.00, "elec": 631.29, "op": 128.71, "total": 5300.00}
            },
            "big bag": {
                "LAOS B/C": {"rm": 5875.00, "pkg": 160.00, "elec": 631.29, "op": 128.71, "total": 6795.00},
                "LAOS C/D": {"rm": 4337.50, "pkg": 160.00, "elec": 631.29, "op": 128.71, "total": 5257.50}
            },
            "TANK": {
                "LAOS (NONG KHAI)": {"rm": 4290.00, "pkg": 0.00, "elec": 631.29, "op": 128.71, "total": 5050.00}
            }
        },
        "200 MESH": {
            "big bag": {
                "LAOS (NONG KHAI)": {"rm": 4290.00, "pkg": 116.00, "elec": 631.29, "op": 1

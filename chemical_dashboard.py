#!/usr/bin/env python3
"""
ระบบจัดการสารเคมี - Chemical Management System
TH Plant Dashboard with Purchase Request (PR) System
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import io

# ─── Page Config ───
st.set_page_config(
    page_title="ระบบจัดการสารเคมี | Chemical Management",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-primary: #0f1117;
    --bg-card: #1a1d29;
    --accent-blue: #3b82f6;
    --accent-green: #10b981;
    --accent-red: #ef4444;
    --accent-amber: #f59e0b;
    --accent-purple: #8b5cf6;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --border-color: #2d3348;
}

html, body, [class*="css"] {
    font-family: 'Kanit', sans-serif;
}

.main-header {
    background: linear-gradient(135deg, #1e3a5f 0%, #0f1117 50%, #1a0a2e 100%);
    padding: 2rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    border: 1px solid #2d3348;
    position: relative;
    overflow: hidden;
}

.main-header::before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 300px;
    height: 100%;
    background: radial-gradient(circle at center, rgba(59,130,246,0.15), transparent 70%);
}

.main-header h1 {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}

.main-header p {
    color: #94a3b8;
    font-size: 0.95rem;
    margin-top: 0.5rem;
}

.metric-card {
    background: linear-gradient(145deg, #1a1d29, #1f2335);
    border: 1px solid #2d3348;
    border-radius: 14px;
    padding: 1.5rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s;
}

.metric-card:hover {
    border-color: #3b82f6;
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(59,130,246,0.15);
}

.metric-card .label {
    color: #94a3b8;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 500;
}

.metric-card .value {
    font-size: 2rem;
    font-weight: 700;
    color: #f1f5f9;
    font-family: 'JetBrains Mono', monospace;
    margin: 0.3rem 0;
}

.metric-card .sub {
    color: #64748b;
    font-size: 0.75rem;
}

.status-safe {
    color: #10b981;
    background: rgba(16,185,129,0.1);
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
}

.status-warning {
    color: #f59e0b;
    background: rgba(245,158,11,0.1);
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
}

.status-danger {
    color: #ef4444;
    background: rgba(239,68,68,0.1);
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
}

.chemical-card {
    background: linear-gradient(145deg, #1a1d29, #1f2335);
    border: 1px solid #2d3348;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.chemical-card h3 {
    color: #f1f5f9;
    font-weight: 600;
    margin-bottom: 0.8rem;
    font-size: 1.1rem;
}

.progress-bar-bg {
    background: #2d3348;
    border-radius: 8px;
    height: 12px;
    overflow: hidden;
    margin: 0.5rem 0;
}

.progress-bar-fill {
    height: 100%;
    border-radius: 8px;
    transition: width 0.5s ease;
}

.alert-card {
    background: linear-gradient(135deg, rgba(239,68,68,0.1), rgba(239,68,68,0.05));
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.8rem;
}

.alert-card.warning {
    background: linear-gradient(135deg, rgba(245,158,11,0.1), rgba(245,158,11,0.05));
    border-color: rgba(245,158,11,0.3);
}

.pr-form {
    background: linear-gradient(145deg, #1a1d29, #1f2335);
    border: 1px solid #2d3348;
    border-radius: 16px;
    padding: 2rem;
}

.section-title {
    font-size: 1.3rem;
    font-weight: 600;
    color: #f1f5f9;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #3b82f6;
    display: inline-block;
}

table.custom-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    border-radius: 12px;
    overflow: hidden;
    font-size: 0.9rem;
}

table.custom-table th {
    background: #1e2235;
    color: #94a3b8;
    padding: 12px 16px;
    text-align: left;
    font-weight: 500;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

table.custom-table td {
    padding: 12px 16px;
    color: #e2e8f0;
    border-bottom: 1px solid #2d3348;
}

table.custom-table tr:last-child td {
    border-bottom: none;
}

table.custom-table tr:hover td {
    background: rgba(59,130,246,0.05);
}

/* Streamlit overrides */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    border: 1px solid #2d3348;
    border-radius: 10px;
    padding: 10px 24px;
    color: #94a3b8;
    font-family: 'Kanit', sans-serif;
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
    color: white !important;
    border-color: transparent !important;
}

div[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace;
}

.stButton button {
    font-family: 'Kanit', sans-serif;
    border-radius: 10px;
    font-weight: 500;
    transition: all 0.3s;
}
</style>
""", unsafe_allow_html=True)


# ─── DATA DEFINITIONS ───
# Chemical data extracted from the Excel file
# Tank Volume Lookup Table from "Remaining Volume" sheet
VOLUME_TABLE = {
    "HCl": {0: 51724.14, 0.5: 46890.17, 1: 42056.21, 1.5: 37222.24, 2: 32388.28, 2.5: 27554.31, 3: 22720.34, 3.5: 17886.38, 4: 13052.41, 4.5: 8218.45},
    "H2SO4": {0: 42857.14, 0.5: 38665.44, 1: 34473.73, 1.5: 30282.02, 2: 26090.31, 2.5: 21898.61, 3: 17706.90, 3.5: 13515.19, 4: 9323.49, 4.5: 5131.78},
    "NaOH": {0: 41379.31, 0.5: 37543.00, 1: 33706.70, 1.5: 29870.39, 2: 26034.08, 2.5: 22197.78, 3: 18361.47, 3.5: 14525.16, 4: 10688.86, 4.5: 6852.55},
    "H2O2": {0: 26431.72, 0.5: 23961.50, 1: 21491.28, 1.5: 19021.06, 2: 16550.84, 2.5: 14080.62, 3: 11610.40, 3.5: 9140.18, 4: 6669.96, 4.5: 4199.74},
}

CHEMICALS = [
    {
        "id": "HCl",
        "name_th": "กรดเกลือ (HCl)",
        "name_cn": "鹽酸 (HCL)",
        "tank_id": "T11-1001",
        "tank_capacity": 60000,
        "tank_max_level": 4.5,
        "current_level": 1.84,
        "current_stock": 20635.23,
        "specific_gravity": 1.16,
        "unit": "kg",
        "daily_consumption": 112.15,
        "reorder_point": 15000,
        "critical_point": 10000,
        "order_qty": 12000,
        "supplier": "บ.เอเชีย เคมิคอล จำกัด",
        "lead_time_days": 3,
        "price_per_kg": 4.5,
        "color": "#3b82f6"
    },
    {
        "id": "H2SO4",
        "name_th": "กรดกำมะถัน (H2SO4)",
        "name_cn": "硫酸 (H2SO4)",
        "tank_id": "T11-1002A",
        "tank_capacity": 60000,
        "tank_max_level": 4.5,
        "current_level": 2.5,
        "current_stock": 29341.95,
        "specific_gravity": 1.4,
        "unit": "kg",
        "daily_consumption": 0,
        "reorder_point": 15000,
        "critical_point": 10000,
        "order_qty": 10200,
        "supplier": "บ.ไทยอาซาฮี เคมิคอลส์ จำกัด",
        "lead_time_days": 3,
        "price_per_kg": 5.2,
        "color": "#f59e0b"
    },
    {
        "id": "NaOH",
        "name_th": "โซดาไฟ (NaOH)",
        "name_cn": "氫氧化鈉 (NaOH)",
        "tank_id": "T11-2005A",
        "tank_capacity": 60000,
        "tank_max_level": 4.5,
        "current_level": 2.74,
        "current_stock": 30483.29,
        "specific_gravity": 1.45,
        "unit": "kg",
        "daily_consumption": 0.31,
        "reorder_point": 15000,
        "critical_point": 10000,
        "order_qty": 9680,
        "supplier": "บ.โทเรย์ ไฟน์ เคมิคอลส์ จำกัด",
        "lead_time_days": 3,
        "price_per_kg": 8.5,
        "color": "#8b5cf6"
    },
    {
        "id": "H2O2",
        "name_th": "ไฮโดรเจนเปอร์ออกไซด์ (H2O2)",
        "name_cn": "雙氧水 (H2O2)",
        "tank_id": "T11-9007B102",
        "tank_capacity": 30000,
        "tank_max_level": 4.5,
        "current_level": 1.36,
        "current_stock": 7626.06,
        "specific_gravity": 1.135,
        "unit": "kg",
        "daily_consumption": 0,
        "reorder_point": 8000,
        "critical_point": 5000,
        "order_qty": 8000,
        "supplier": "บ.เพอร์ออกไซด์ จำกัด",
        "lead_time_days": 5,
        "price_per_kg": 12.0,
        "color": "#10b981"
    },
    {
        "id": "FeSO4",
        "name_th": "เฟอร์รัสซัลเฟต (FeSO4)",
        "name_cn": "硫酸亞鐵",
        "tank_id": "11-1011A001",
        "tank_capacity": 10000,
        "tank_max_level": 330,
        "current_level": 583,
        "current_stock": 18073,
        "specific_gravity": 1.23,
        "unit": "kg",
        "daily_consumption": 837,
        "reorder_point": 5000,
        "critical_point": 3000,
        "order_qty": 8130,
        "supplier": "บ.เหล็กไทย เคมี จำกัด",
        "lead_time_days": 2,
        "price_per_kg": 3.0,
        "color": "#f97316"
    },
    {
        "id": "PAC",
        "name_th": "โพลีอลูมิเนียมคลอไรด์ (PAC)",
        "name_cn": "多元氯化鋁 PAC",
        "tank_id": "11-2015A001",
        "tank_capacity": 10000,
        "tank_max_level": 330,
        "current_level": 80,
        "current_stock": 2480,
        "specific_gravity": 1.2,
        "unit": "kg",
        "daily_consumption": 393,
        "reorder_point": 4000,
        "critical_point": 2000,
        "order_qty": 5833,
        "supplier": "บ.ไทยโพลีเคมิคอล จำกัด",
        "lead_time_days": 2,
        "price_per_kg": 7.0,
        "color": "#ec4899"
    },
    {
        "id": "NaOH_WT",
        "name_th": "โซดาไฟ WT (NaOH-WT)",
        "name_cn": "氫氧化鈉 WT",
        "tank_id": "11-2005B",
        "tank_capacity": 40000,
        "tank_max_level": 430,
        "current_level": 251,
        "current_stock": 24598,
        "specific_gravity": 1.45,
        "unit": "kg",
        "daily_consumption": 6430,
        "reorder_point": 15000,
        "critical_point": 10000,
        "order_qty": 15172,
        "supplier": "บ.โทเรย์ ไฟน์ เคมิคอลส์ จำกัด",
        "lead_time_days": 3,
        "price_per_kg": 8.5,
        "color": "#6366f1"
    },
    {
        "id": "H2SO4_WT",
        "name_th": "กรดกำมะถัน WT (H2SO4-WT)",
        "name_cn": "硫酸 WT",
        "tank_id": "11-1002E",
        "tank_capacity": 10000,
        "tank_max_level": 180,
        "current_level": 224,
        "current_stock": 6944,
        "specific_gravity": 1.4,
        "unit": "kg",
        "daily_consumption": 0,
        "reorder_point": 3000,
        "critical_point": 2000,
        "order_qty": 5000,
        "supplier": "บ.ไทยอาซาฮี เคมิคอลส์ จำกัด",
        "lead_time_days": 3,
        "price_per_kg": 5.2,
        "color": "#eab308"
    },
]


def get_stock_status(chem):
    """Determine stock status based on current level vs reorder/critical points"""
    pct = (chem["current_stock"] / chem["tank_capacity"]) * 100
    if chem["current_stock"] <= chem["critical_point"]:
        return "critical", "🔴 วิกฤต", pct
    elif chem["current_stock"] <= chem["reorder_point"]:
        return "warning", "🟡 ต้องสั่งซื้อ", pct
    else:
        return "safe", "🟢 ปกติ", pct


def get_days_remaining(chem):
    """Calculate days of stock remaining based on daily consumption"""
    if chem["daily_consumption"] > 0:
        return chem["current_stock"] / chem["daily_consumption"]
    return float('inf')


def interpolate_volume(chem_id, level):
    """Interpolate volume from level using lookup table"""
    if chem_id not in VOLUME_TABLE:
        return None
    table = VOLUME_TABLE[chem_id]
    levels = sorted(table.keys())
    if level <= levels[0]:
        return table[levels[0]]
    if level >= levels[-1]:
        return table[levels[-1]]
    for i in range(len(levels) - 1):
        if levels[i] <= level <= levels[i + 1]:
            ratio = (level - levels[i]) / (levels[i + 1] - levels[i])
            return table[levels[i]] + ratio * (table[levels[i + 1]] - table[levels[i]])
    return None


# ─── Initialize Session State ───
if "pr_list" not in st.session_state:
    st.session_state.pr_list = []
if "pr_counter" not in st.session_state:
    st.session_state.pr_counter = 1


# ─── SIDEBAR ───
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0;">
        <div style="font-size: 2.5rem;">🧪</div>
        <h2 style="font-size: 1.2rem; font-weight: 600; color: #f1f5f9; margin: 0.5rem 0;">
            Chemical Management
        </h2>
        <p style="color: #64748b; font-size: 0.8rem;">TH Plant Control System</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    page = st.radio(
        "📑 เมนู",
        ["📊 Dashboard ภาพรวม", "⚠️ แจ้งเตือนสารเคมี", "📋 สั่งซื้อ PR", "🔬 คำนวณสารเคมี", "📈 ตารางข้อมูลดิบ"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    st.markdown(f"""
    <div style="padding: 0.8rem; background: #1a1d29; border-radius: 10px; border: 1px solid #2d3348;">
        <div style="color: #64748b; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.5px;">วันที่ปัจจุบัน</div>
        <div style="color: #f1f5f9; font-weight: 600; font-size: 0.95rem;">{datetime.now().strftime('%d/%m/%Y')}</div>
        <div style="color: #64748b; font-size: 0.75rem;">{datetime.now().strftime('%H:%M น.')}</div>
    </div>
    """, unsafe_allow_html=True)

    # Summary alerts in sidebar
    alerts = [c for c in CHEMICALS if get_stock_status(c)[0] in ("critical", "warning")]
    if alerts:
        st.markdown(f"""
        <div style="margin-top: 1rem; padding: 0.8rem; background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.3); border-radius: 10px;">
            <div style="color: #ef4444; font-weight: 600; font-size: 0.85rem;">⚠️ แจ้งเตือน {len(alerts)} รายการ</div>
            <div style="color: #fca5a5; font-size: 0.75rem; margin-top: 4px;">มีสารเคมีที่ต้องดำเนินการ</div>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# PAGE 1: DASHBOARD
# ═══════════════════════════════════════════════
if page == "📊 Dashboard ภาพรวม":
    st.markdown("""
    <div class="main-header">
        <h1>📊 Dashboard ภาพรวมสารเคมี</h1>
        <p>ระบบติดตามและจัดการสารเคมี TH Plant — ข้อมูล ณ เดือนมีนาคม 2569 (115年度)</p>
    </div>
    """, unsafe_allow_html=True)

    # ─── Top Metrics ───
    total_chemicals = len(CHEMICALS)
    safe_count = sum(1 for c in CHEMICALS if get_stock_status(c)[0] == "safe")
    warning_count = sum(1 for c in CHEMICALS if get_stock_status(c)[0] == "warning")
    critical_count = sum(1 for c in CHEMICALS if get_stock_status(c)[0] == "critical")
    total_stock_value = sum(c["current_stock"] * c["price_per_kg"] for c in CHEMICALS)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">สารเคมีทั้งหมด</div>
            <div class="value">{total_chemicals}</div>
            <div class="sub">รายการ</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">🟢 สถานะปกติ</div>
            <div class="value" style="color: #10b981;">{safe_count}</div>
            <div class="sub">รายการ</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">🟡 ต้องสั่งซื้อ</div>
            <div class="value" style="color: #f59e0b;">{warning_count}</div>
            <div class="sub">รายการ</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">🔴 วิกฤต</div>
            <div class="value" style="color: #ef4444;">{critical_count}</div>
            <div class="sub">รายการ</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">มูลค่าสต็อกรวม</div>
            <div class="value" style="font-size: 1.4rem;">฿{total_stock_value:,.0f}</div>
            <div class="sub">บาท (โดยประมาณ)</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── Chemical Cards Grid ───
    st.markdown('<div class="section-title">📦 สถานะถังสารเคมีทั้งหมด</div>', unsafe_allow_html=True)
    
    cols = st.columns(2)
    for idx, chem in enumerate(CHEMICALS):
        status, status_label, pct = get_stock_status(chem)
        days_left = get_days_remaining(chem)
        
        if status == "critical":
            bar_color = "#ef4444"
            border_highlight = "border-left: 4px solid #ef4444;"
        elif status == "warning":
            bar_color = "#f59e0b"
            border_highlight = "border-left: 4px solid #f59e0b;"
        else:
            bar_color = "#10b981"
            border_highlight = "border-left: 4px solid #10b981;"
        
        days_text = f"{days_left:.0f} วัน" if days_left < float('inf') else "—"
        
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="chemical-card" style="{border_highlight}">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <h3 style="margin:0;">{chem['name_th']}</h3>
                        <span style="color: #64748b; font-size: 0.8rem;">Tank: {chem['tank_id']} | {chem['name_cn']}</span>
                    </div>
                    <span class="status-{'safe' if status=='safe' else 'warning' if status=='warning' else 'danger'}">{status_label}</span>
                </div>
                <div style="margin-top: 1rem; display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.8rem;">
                    <div>
                        <div style="color: #64748b; font-size: 0.7rem;">คงเหลือ</div>
                        <div style="color: #f1f5f9; font-weight: 600; font-family: 'JetBrains Mono';">{chem['current_stock']:,.1f} {chem['unit']}</div>
                    </div>
                    <div>
                        <div style="color: #64748b; font-size: 0.7rem;">ระดับถัง</div>
                        <div style="color: #f1f5f9; font-weight: 600; font-family: 'JetBrains Mono';">{chem['current_level']}</div>
                    </div>
                    <div>
                        <div style="color: #64748b; font-size: 0.7rem;">ใช้ได้อีก</div>
                        <div style="color: {bar_color}; font-weight: 600; font-family: 'JetBrains Mono';">{days_text}</div>
                    </div>
                </div>
                <div class="progress-bar-bg" style="margin-top: 0.8rem;">
                    <div class="progress-bar-fill" style="width: {min(pct, 100):.1f}%; background: {bar_color};"></div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 4px;">
                    <span style="color: #64748b; font-size: 0.7rem;">0%</span>
                    <span style="color: #94a3b8; font-size: 0.7rem; font-weight: 500;">{pct:.1f}% ความจุ</span>
                    <span style="color: #64748b; font-size: 0.7rem;">100%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ─── Volume Lookup Table ───
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">📐 ตาราง Remaining Volume (Level → kg)</div>', unsafe_allow_html=True)
    
    vol_data = []
    for level in [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]:
        row = {"Level (m)": level}
        for chem_id in ["HCl", "H2SO4", "NaOH", "H2O2"]:
            row[chem_id] = f"{VOLUME_TABLE[chem_id][level]:,.2f}"
        vol_data.append(row)
    
    vol_df = pd.DataFrame(vol_data)
    st.dataframe(vol_df, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════
# PAGE 2: ALERTS
# ═══════════════════════════════════════════════
elif page == "⚠️ แจ้งเตือนสารเคมี":
    st.markdown("""
    <div class="main-header">
        <h1>⚠️ ระบบแจ้งเตือนสารเคมี</h1>
        <p>รายการสารเคมีที่ต้องดำเนินการสั่งซื้อ พร้อมวิเคราะห์ระดับความเร่งด่วน</p>
    </div>
    """, unsafe_allow_html=True)

    # Separate into categories
    critical_list = [c for c in CHEMICALS if get_stock_status(c)[0] == "critical"]
    warning_list = [c for c in CHEMICALS if get_stock_status(c)[0] == "warning"]
    safe_list = [c for c in CHEMICALS if get_stock_status(c)[0] == "safe"]
    
    # Critical Alerts
    if critical_list:
        st.markdown("### 🔴 วิกฤต — ต้องสั่งซื้อทันที")
        for chem in critical_list:
            days = get_days_remaining(chem)
            days_text = f"{days:.0f} วัน" if days < float('inf') else "ไม่มีการใช้งาน"
            st.markdown(f"""
            <div class="alert-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="color: #fca5a5; font-weight: 600; font-size: 1.05rem;">🔴 {chem['name_th']}</div>
                        <div style="color: #f87171; font-size: 0.85rem; margin-top: 4px;">
                            Tank: {chem['tank_id']} | คงเหลือ: <b>{chem['current_stock']:,.1f} {chem['unit']}</b> 
                            | จุดวิกฤต: {chem['critical_point']:,.0f} {chem['unit']}
                            | ใช้ได้อีก: <b>{days_text}</b>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: #fca5a5; font-size: 0.8rem;">แนะนำสั่งซื้อ</div>
                        <div style="color: #f1f5f9; font-weight: 700; font-size: 1.2rem; font-family: 'JetBrains Mono';">{chem['order_qty']:,.0f} {chem['unit']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ ไม่มีสารเคมีในระดับวิกฤต")

    st.markdown("<br>", unsafe_allow_html=True)

    # Warning Alerts
    if warning_list:
        st.markdown("### 🟡 เตือน — ควรวางแผนสั่งซื้อ")
        for chem in warning_list:
            days = get_days_remaining(chem)
            days_text = f"{days:.0f} วัน" if days < float('inf') else "ไม่มีการใช้งาน"
            st.markdown(f"""
            <div class="alert-card warning">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="color: #fbbf24; font-weight: 600; font-size: 1.05rem;">🟡 {chem['name_th']}</div>
                        <div style="color: #fcd34d; font-size: 0.85rem; margin-top: 4px;">
                            Tank: {chem['tank_id']} | คงเหลือ: <b>{chem['current_stock']:,.1f} {chem['unit']}</b>
                            | จุดสั่งซื้อ: {chem['reorder_point']:,.0f} {chem['unit']}
                            | ใช้ได้อีก: <b>{days_text}</b>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: #fbbf24; font-size: 0.8rem;">แนะนำสั่งซื้อ</div>
                        <div style="color: #f1f5f9; font-weight: 700; font-size: 1.2rem; font-family: 'JetBrains Mono';">{chem['order_qty']:,.0f} {chem['unit']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("ℹ️ ไม่มีสารเคมีในระดับเตือน")

    st.markdown("<br>", unsafe_allow_html=True)

    # Safe chemicals summary
    st.markdown("### 🟢 สถานะปกติ")
    for chem in safe_list:
        days = get_days_remaining(chem)
        days_text = f"{days:.0f} วัน" if days < float('inf') else "—"
        pct = (chem["current_stock"] / chem["tank_capacity"]) * 100
        st.markdown(f"""
        <div style="background: rgba(16,185,129,0.05); border: 1px solid rgba(16,185,129,0.2); border-radius: 10px; padding: 0.8rem 1.2rem; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="color: #34d399; font-weight: 500;">{chem['name_th']}</span>
                <span style="color: #64748b; font-size: 0.8rem; margin-left: 1rem;">({chem['tank_id']})</span>
            </div>
            <div style="display: flex; gap: 2rem; align-items: center;">
                <span style="color: #94a3b8; font-size: 0.85rem;">คงเหลือ: <b style="color: #10b981;">{chem['current_stock']:,.1f} {chem['unit']}</b></span>
                <span style="color: #94a3b8; font-size: 0.85rem;">{pct:.1f}%</span>
                <span style="color: #94a3b8; font-size: 0.85rem;">ใช้ได้อีก: {days_text}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Summary Table
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 สรุปตารางทั้งหมด</div>', unsafe_allow_html=True)
    
    summary_data = []
    for c in CHEMICALS:
        status, label, pct = get_stock_status(c)
        days = get_days_remaining(c)
        summary_data.append({
            "สารเคมี": c["name_th"],
            "Tank": c["tank_id"],
            "คงเหลือ (kg)": f"{c['current_stock']:,.1f}",
            "% ความจุ": f"{pct:.1f}%",
            "ใช้/วัน (kg)": f"{c['daily_consumption']:,.1f}",
            "ใช้ได้ (วัน)": f"{days:.0f}" if days < float('inf') else "—",
            "จุดสั่งซื้อ": f"{c['reorder_point']:,.0f}",
            "สถานะ": label,
        })
    
    st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════
# PAGE 3: PURCHASE REQUEST (PR)
# ═══════════════════════════════════════════════
elif page == "📋 สั่งซื้อ PR":
    st.markdown("""
    <div class="main-header">
        <h1>📋 ใบขอซื้อ (Purchase Request)</h1>
        <p>สร้างและจัดการใบขอซื้อสารเคมี พร้อมส่งออกเป็นไฟล์</p>
    </div>
    """, unsafe_allow_html=True)

    col_form, col_preview = st.columns([1, 1])
    
    with col_form:
        st.markdown("### 📝 สร้างใบ PR ใหม่")
        
        selected_chem = st.selectbox(
            "เลือกสารเคมี",
            options=range(len(CHEMICALS)),
            format_func=lambda i: f"{CHEMICALS[i]['name_th']} ({CHEMICALS[i]['tank_id']})"
        )
        
        chem = CHEMICALS[selected_chem]
        status, label, pct = get_stock_status(chem)
        
        st.markdown(f"""
        <div style="background: #1a1d29; border: 1px solid #2d3348; border-radius: 10px; padding: 1rem; margin: 0.5rem 0;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;">
                <div><span style="color: #64748b; font-size: 0.8rem;">คงเหลือ:</span> <b style="color: #f1f5f9;">{chem['current_stock']:,.1f} {chem['unit']}</b></div>
                <div><span style="color: #64748b; font-size: 0.8rem;">สถานะ:</span> {label}</div>
                <div><span style="color: #64748b; font-size: 0.8rem;">ผู้จัดจำหน่าย:</span> <span style="color: #94a3b8;">{chem['supplier']}</span></div>
                <div><span style="color: #64748b; font-size: 0.8rem;">Lead time:</span> <span style="color: #94a3b8;">{chem['lead_time_days']} วัน</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        order_qty = st.number_input("จำนวนที่สั่งซื้อ (kg)", value=chem["order_qty"], step=100, min_value=0)
        unit_price = st.number_input("ราคาต่อหน่วย (บาท/kg)", value=chem["price_per_kg"], step=0.1, min_value=0.0)
        delivery_date = st.date_input("วันที่ต้องการรับสินค้า", value=datetime.now() + timedelta(days=chem["lead_time_days"]))
        notes = st.text_area("หมายเหตุ", placeholder="ระบุรายละเอียดเพิ่มเติม...")
        priority = st.selectbox("ลำดับความสำคัญ", ["🔴 เร่งด่วน", "🟡 ปกติ", "🟢 ไม่เร่งด่วน"])
        
        total_cost = order_qty * unit_price
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(59,130,246,0.1), rgba(139,92,246,0.1)); border: 1px solid rgba(59,130,246,0.3); border-radius: 10px; padding: 1rem; margin: 1rem 0;">
            <div style="color: #94a3b8; font-size: 0.8rem;">มูลค่ารวม</div>
            <div style="color: #f1f5f9; font-weight: 700; font-size: 1.5rem; font-family: 'JetBrains Mono';">฿{total_cost:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("✅ สร้างใบ PR", type="primary", use_container_width=True):
            pr = {
                "pr_no": f"PR-{datetime.now().strftime('%Y%m')}-{st.session_state.pr_counter:04d}",
                "date": datetime.now().strftime('%Y-%m-%d %H:%M'),
                "chemical": chem["name_th"],
                "chemical_id": chem["id"],
                "tank_id": chem["tank_id"],
                "quantity": order_qty,
                "unit": chem["unit"],
                "unit_price": unit_price,
                "total_cost": total_cost,
                "supplier": chem["supplier"],
                "delivery_date": delivery_date.strftime('%Y-%m-%d'),
                "priority": priority,
                "notes": notes,
                "status": "รออนุมัติ"
            }
            st.session_state.pr_list.append(pr)
            st.session_state.pr_counter += 1
            st.success(f"✅ สร้างใบ PR เรียบร้อย: {pr['pr_no']}")
    
    with col_preview:
        st.markdown("### 📄 รายการ PR ที่สร้างแล้ว")
        
        if st.session_state.pr_list:
            for pr in reversed(st.session_state.pr_list):
                priority_color = "#ef4444" if "เร่งด่วน" in pr["priority"] else "#f59e0b" if "ปกติ" in pr["priority"] else "#10b981"
                st.markdown(f"""
                <div style="background: #1a1d29; border: 1px solid #2d3348; border-left: 4px solid {priority_color}; border-radius: 10px; padding: 1.2rem; margin-bottom: 0.8rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="color: #3b82f6; font-weight: 600; font-family: 'JetBrains Mono';">{pr['pr_no']}</div>
                        <span style="background: rgba(59,130,246,0.1); color: #60a5fa; padding: 2px 10px; border-radius: 20px; font-size: 0.75rem;">{pr['status']}</span>
                    </div>
                    <div style="margin-top: 0.8rem; color: #e2e8f0; font-weight: 500;">{pr['chemical']}</div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.3rem; margin-top: 0.5rem; font-size: 0.8rem;">
                        <div style="color: #64748b;">จำนวน: <span style="color: #94a3b8;">{pr['quantity']:,.0f} {pr['unit']}</span></div>
                        <div style="color: #64748b;">มูลค่า: <span style="color: #94a3b8;">฿{pr['total_cost']:,.2f}</span></div>
                        <div style="color: #64748b;">ผู้จำหน่าย: <span style="color: #94a3b8;">{pr['supplier']}</span></div>
                        <div style="color: #64748b;">รับสินค้า: <span style="color: #94a3b8;">{pr['delivery_date']}</span></div>
                    </div>
                    <div style="margin-top: 0.5rem; color: #64748b; font-size: 0.75rem;">สร้างเมื่อ: {pr['date']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Export button
            st.markdown("<br>", unsafe_allow_html=True)
            pr_df = pd.DataFrame(st.session_state.pr_list)
            csv_data = pr_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                "📥 ดาวน์โหลด PR ทั้งหมด (CSV)",
                data=csv_data,
                file_name=f"PR_List_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            if st.button("🗑️ ล้างรายการ PR ทั้งหมด", use_container_width=True):
                st.session_state.pr_list = []
                st.rerun()
        else:
            st.markdown("""
            <div style="text-align: center; padding: 3rem; color: #64748b;">
                <div style="font-size: 3rem;">📭</div>
                <p>ยังไม่มีใบ PR</p>
                <p style="font-size: 0.8rem;">สร้างใบ PR ใหม่จากฟอร์มด้านซ้าย</p>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# PAGE 4: CHEMICAL CALCULATOR
# ═══════════════════════════════════════════════
elif page == "🔬 คำนวณสารเคมี":
    st.markdown("""
    <div class="main-header">
        <h1>🔬 ระบบคำนวณสารเคมี</h1>
        <p>คำนวณปริมาณสารเคมี ระดับถังหลังเติม และวันคงเหลือ</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📏 Level → Volume", "📦 คำนวณการเติม", "📅 พยากรณ์การใช้"])
    
    with tab1:
        st.markdown("#### แปลงระดับถัง → ปริมาณสารเคมี (kg)")
        
        col1, col2 = st.columns(2)
        with col1:
            calc_chem = st.selectbox("เลือกสารเคมี (TH Tank)", list(VOLUME_TABLE.keys()), key="calc_chem1")
        with col2:
            calc_level = st.slider("ระดับถัง (m)", 0.0, 4.5, 2.0, 0.01, key="calc_level1")
        
        result = interpolate_volume(calc_chem, calc_level)
        if result is not None:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(59,130,246,0.1), rgba(139,92,246,0.1)); border: 1px solid rgba(59,130,246,0.3); border-radius: 14px; padding: 2rem; text-align: center; margin-top: 1rem;">
                <div style="color: #94a3b8; font-size: 0.9rem;">ปริมาณสารเคมี {calc_chem} ที่ระดับ {calc_level:.2f} m</div>
                <div style="color: #f1f5f9; font-weight: 700; font-size: 2.5rem; font-family: 'JetBrains Mono'; margin: 0.5rem 0;">{result:,.2f}</div>
                <div style="color: #64748b; font-size: 0.85rem;">กิโลกรัม (kg)</div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("#### คำนวณระดับถังหลังเติมสารเคมี")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            fill_chem = st.selectbox("สารเคมี", list(VOLUME_TABLE.keys()), key="fill_chem")
        with col2:
            current_lv = st.number_input("ระดับถังปัจจุบัน (m)", value=1.5, step=0.01, min_value=0.0, max_value=4.5)
        with col3:
            incoming_kg = st.number_input("จำนวนที่เติม (kg)", value=14000, step=100, min_value=0)
        
        current_vol = interpolate_volume(fill_chem, current_lv)
        if current_vol is not None:
            new_vol = current_vol + incoming_kg
            # Reverse lookup for new level
            table = VOLUME_TABLE[fill_chem]
            levels = sorted(table.keys())
            new_level = levels[0]
            for i in range(len(levels) - 1):
                if table[levels[i]] >= new_vol >= table[levels[i + 1]]:
                    ratio = (table[levels[i]] - new_vol) / (table[levels[i]] - table[levels[i + 1]])
                    new_level = levels[i] + ratio * (levels[i + 1] - levels[i])
                    break
            else:
                if new_vol <= table[levels[-1]]:
                    new_level = levels[-1]
            
            max_safe = 4.0  # Keep under 4m as per data
            is_over = new_level > max_safe
            
            col_r1, col_r2, col_r3 = st.columns(3)
            with col_r1:
                st.metric("ปริมาณปัจจุบัน", f"{current_vol:,.1f} kg")
            with col_r2:
                st.metric("ปริมาณหลังเติม", f"{new_vol:,.1f} kg")
            with col_r3:
                st.metric("ระดับหลังเติม", f"{new_level:.2f} m", delta=f"+{new_level - current_lv:.2f} m")
            
            if is_over:
                st.error(f"⚠️ ระดับหลังเติม ({new_level:.2f} m) เกินระดับปลอดภัย ({max_safe} m) — กรุณาลดจำนวนการเติม!")
            else:
                st.success(f"✅ ระดับหลังเติม ({new_level:.2f} m) อยู่ในเกณฑ์ปลอดภัย (ไม่เกิน {max_safe} m)")
    
    with tab3:
        st.markdown("#### พยากรณ์จำนวนวันคงเหลือ")
        
        col1, col2 = st.columns(2)
        with col1:
            forecast_chem_idx = st.selectbox(
                "เลือกสารเคมี",
                options=range(len(CHEMICALS)),
                format_func=lambda i: CHEMICALS[i]["name_th"],
                key="forecast_chem"
            )
        with col2:
            custom_consumption = st.number_input(
                "อัตราการใช้ต่อวัน (kg/day)",
                value=float(CHEMICALS[forecast_chem_idx]["daily_consumption"]),
                step=10.0,
                min_value=0.0
            )
        
        fc = CHEMICALS[forecast_chem_idx]
        if custom_consumption > 0:
            days = fc["current_stock"] / custom_consumption
            runout_date = datetime.now() + timedelta(days=days)
            
            st.markdown(f"""
            <div style="background: #1a1d29; border: 1px solid #2d3348; border-radius: 14px; padding: 1.5rem; margin-top: 1rem;">
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1.5rem; text-align: center;">
                    <div>
                        <div style="color: #64748b; font-size: 0.8rem;">คงเหลือ</div>
                        <div style="color: #f1f5f9; font-weight: 700; font-size: 1.5rem; font-family: 'JetBrains Mono';">{fc['current_stock']:,.1f} kg</div>
                    </div>
                    <div>
                        <div style="color: #64748b; font-size: 0.8rem;">ใช้ได้อีก</div>
                        <div style="color: {'#ef4444' if days < 7 else '#f59e0b' if days < 14 else '#10b981'}; font-weight: 700; font-size: 1.5rem; font-family: 'JetBrains Mono';">{days:.1f} วัน</div>
                    </div>
                    <div>
                        <div style="color: #64748b; font-size: 0.8rem;">วันที่จะหมด</div>
                        <div style="color: #f1f5f9; font-weight: 700; font-size: 1.5rem; font-family: 'JetBrains Mono';">{runout_date.strftime('%d/%m/%Y')}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Forecast chart
            forecast_days = []
            for d in range(int(days) + 10):
                remaining = fc["current_stock"] - (custom_consumption * d)
                if remaining < 0:
                    remaining = 0
                forecast_days.append({
                    "วัน": d,
                    "คงเหลือ (kg)": remaining,
                    "จุดสั่งซื้อ": fc["reorder_point"],
                    "จุดวิกฤต": fc["critical_point"]
                })
            
            chart_df = pd.DataFrame(forecast_days)
            st.line_chart(chart_df.set_index("วัน"), use_container_width=True)
        else:
            st.info("ℹ️ ไม่มีข้อมูลการใช้ต่อวัน — ไม่สามารถพยากรณ์ได้")


# ═══════════════════════════════════════════════
# PAGE 5: RAW DATA
# ═══════════════════════════════════════════════
elif page == "📈 ตารางข้อมูลดิบ":
    st.markdown("""
    <div class="main-header">
        <h1>📈 ตารางข้อมูลดิบจากไฟล์</h1>
        <p>ข้อมูลทั้งหมดจากไฟล์ 115-3_TH_tank พร้อมตาราง Remaining Volume</p>
    </div>
    """, unsafe_allow_html=True)

    # Display formatted raw data
    st.markdown("### 📋 ข้อมูลสารเคมีหลัก (TH Tank)")
    
    raw_data = []
    for c in CHEMICALS:
        status, label, pct = get_stock_status(c)
        raw_data.append({
            "Tank ID": c["tank_id"],
            "Chemical": c["name_th"],
            "中文名稱": c["name_cn"],
            "Tank Capacity (kg)": f"{c['tank_capacity']:,}",
            "Current Level": c["current_level"],
            "Current Stock (kg)": f"{c['current_stock']:,.2f}",
            "Specific Gravity": c["specific_gravity"],
            "Daily Consumption (kg)": f"{c['daily_consumption']:,.2f}",
            "Reorder Point (kg)": f"{c['reorder_point']:,}",
            "Status": label,
        })
    
    st.dataframe(pd.DataFrame(raw_data), use_container_width=True, hide_index=True)
    
    st.markdown("### 📐 Remaining Volume Lookup Table")
    vol_data = []
    for level in [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]:
        row = {"Level (m)": level}
        for chem_id in ["HCl", "H2SO4", "NaOH", "H2O2"]:
            row[f"{chem_id} (kg)"] = f"{VOLUME_TABLE[chem_id][level]:,.2f}"
        vol_data.append(row)
    st.dataframe(pd.DataFrame(vol_data), use_container_width=True, hide_index=True)

    st.markdown("### 📊 Check Tank Level (จากไฟล์)")
    check_data = [
        {"Chemical": "HCl", "Current Level (m)": 3, "Incoming (kg)": 14000, "After Level (m)": 4.076},
        {"Chemical": "H2SO4", "Current Level (m)": 1, "Incoming (kg)": 14000, "After Level (m)": 1.852},
        {"Chemical": "NaOH", "Current Level (m)": 1.3, "Incoming (kg)": 14050, "After Level (m)": 2.171},
        {"Chemical": "H2O2", "Current Level (m)": 2.5, "Incoming (kg)": 8000, "After Level (m)": 3.757},
    ]
    st.dataframe(pd.DataFrame(check_data), use_container_width=True, hide_index=True)
    st.caption("⚠️ หมายเหตุ: Keep tank level under 4.0m (ตามข้อมูลในไฟล์)")


# ─── Footer ───
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #475569; font-size: 0.8rem;">
    🧪 Chemical Management System | TH Plant | ข้อมูลจากไฟล์ 115-3_TH_tank<br>
    พัฒนาด้วย Streamlit + Python | © 2026
</div>
""", unsafe_allow_html=True)

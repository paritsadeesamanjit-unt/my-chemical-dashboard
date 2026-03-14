#!/usr/bin/env python3
"""
ระบบจัดการสารเคมี - Chemical Management System v2
TH Plant Dashboard with Purchase Request (PR) + Goods Receipt + Stock Management
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import io
import copy

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
    top: 0; right: 0;
    width: 300px; height: 100%;
    background: radial-gradient(circle at center, rgba(59,130,246,0.15), transparent 70%);
}
.main-header h1 {
    font-size: 2rem; font-weight: 700;
    background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.main-header p { color: #94a3b8; font-size: 0.95rem; margin-top: 0.5rem; }

.metric-card {
    background: linear-gradient(145deg, #1a1d29, #1f2335);
    border: 1px solid #2d3348;
    border-radius: 14px;
    padding: 1.5rem;
    position: relative; overflow: hidden;
    transition: all 0.3s;
}
.metric-card:hover {
    border-color: #3b82f6;
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(59,130,246,0.15);
}
.metric-card .label { color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500; }
.metric-card .value { font-size: 2rem; font-weight: 700; color: #f1f5f9; font-family: 'JetBrains Mono', monospace; margin: 0.3rem 0; }
.metric-card .sub { color: #64748b; font-size: 0.75rem; }

.status-safe { color: #10b981; background: rgba(16,185,129,0.1); padding: 2px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: 500; }
.status-warning { color: #f59e0b; background: rgba(245,158,11,0.1); padding: 2px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: 500; }
.status-danger { color: #ef4444; background: rgba(239,68,68,0.1); padding: 2px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: 500; }

.chemical-card {
    background: linear-gradient(145deg, #1a1d29, #1f2335);
    border: 1px solid #2d3348;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.progress-bar-bg { background: #2d3348; border-radius: 8px; height: 12px; overflow: hidden; margin: 0.5rem 0; }
.progress-bar-fill { height: 100%; border-radius: 8px; transition: width 0.5s ease; }

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

.section-title {
    font-size: 1.3rem; font-weight: 600; color: #f1f5f9;
    margin-bottom: 1rem; padding-bottom: 0.5rem;
    border-bottom: 2px solid #3b82f6; display: inline-block;
}

.receipt-card {
    background: linear-gradient(145deg, #1a1d29, #1f2335);
    border: 1px solid #2d3348;
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 0.6rem;
}

.timeline-item {
    border-left: 3px solid #3b82f6;
    padding: 0.8rem 0 0.8rem 1.2rem;
    margin-left: 0.5rem;
    position: relative;
}
.timeline-item::before {
    content: '';
    position: absolute;
    left: -7px; top: 1.2rem;
    width: 11px; height: 11px;
    border-radius: 50%;
    background: #3b82f6;
    border: 2px solid #1a1d29;
}
.timeline-item.receive::before { background: #10b981; }
.timeline-item.receive { border-left-color: #10b981; }
.timeline-item.use::before { background: #f59e0b; }
.timeline-item.use { border-left-color: #f59e0b; }
.timeline-item.pr::before { background: #8b5cf6; }
.timeline-item.pr { border-left-color: #8b5cf6; }
.timeline-item.adjust::before { background: #ec4899; }
.timeline-item.adjust { border-left-color: #ec4899; }

.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] {
    background: transparent; border: 1px solid #2d3348;
    border-radius: 10px; padding: 10px 24px; color: #94a3b8;
    font-family: 'Kanit', sans-serif; font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
    color: white !important; border-color: transparent !important;
}
div[data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace; }
.stButton button { font-family: 'Kanit', sans-serif; border-radius: 10px; font-weight: 500; }
</style>
""", unsafe_allow_html=True)


# ─── DATA DEFINITIONS ───
VOLUME_TABLE = {
    "HCl": {0: 51724.14, 0.5: 46890.17, 1: 42056.21, 1.5: 37222.24, 2: 32388.28, 2.5: 27554.31, 3: 22720.34, 3.5: 17886.38, 4: 13052.41, 4.5: 8218.45},
    "H2SO4": {0: 42857.14, 0.5: 38665.44, 1: 34473.73, 1.5: 30282.02, 2: 26090.31, 2.5: 21898.61, 3: 17706.90, 3.5: 13515.19, 4: 9323.49, 4.5: 5131.78},
    "NaOH": {0: 41379.31, 0.5: 37543.00, 1: 33706.70, 1.5: 29870.39, 2: 26034.08, 2.5: 22197.78, 3: 18361.47, 3.5: 14525.16, 4: 10688.86, 4.5: 6852.55},
    "H2O2": {0: 26431.72, 0.5: 23961.50, 1: 21491.28, 1.5: 19021.06, 2: 16550.84, 2.5: 14080.62, 3: 11610.40, 3.5: 9140.18, 4: 6669.96, 4.5: 4199.74},
}

CHEMICALS_MASTER = [
    {"id": "HCl", "name_th": "กรดเกลือ (HCl)", "name_cn": "鹽酸 (HCL)", "tank_id": "T11-1001",
     "tank_capacity": 60000, "tank_max_level": 4.5, "initial_level": 1.84, "initial_stock": 20635.23,
     "specific_gravity": 1.16, "unit": "kg", "daily_consumption": 112.15,
     "reorder_point": 15000, "critical_point": 10000, "order_qty": 12000,
     "supplier": "บ.เอเชีย เคมิคอล จำกัด", "lead_time_days": 3, "price_per_kg": 4.5, "color": "#3b82f6"},
    {"id": "H2SO4", "name_th": "กรดกำมะถัน (H2SO4)", "name_cn": "硫酸 (H2SO4)", "tank_id": "T11-1002A",
     "tank_capacity": 60000, "tank_max_level": 4.5, "initial_level": 2.5, "initial_stock": 29341.95,
     "specific_gravity": 1.4, "unit": "kg", "daily_consumption": 0,
     "reorder_point": 15000, "critical_point": 10000, "order_qty": 10200,
     "supplier": "บ.ไทยอาซาฮี เคมิคอลส์ จำกัด", "lead_time_days": 3, "price_per_kg": 5.2, "color": "#f59e0b"},
    {"id": "NaOH", "name_th": "โซดาไฟ (NaOH)", "name_cn": "氫氧化鈉 (NaOH)", "tank_id": "T11-2005A",
     "tank_capacity": 60000, "tank_max_level": 4.5, "initial_level": 2.74, "initial_stock": 30483.29,
     "specific_gravity": 1.45, "unit": "kg", "daily_consumption": 0.31,
     "reorder_point": 15000, "critical_point": 10000, "order_qty": 9680,
     "supplier": "บ.โทเรย์ ไฟน์ เคมิคอลส์ จำกัด", "lead_time_days": 3, "price_per_kg": 8.5, "color": "#8b5cf6"},
    {"id": "H2O2", "name_th": "ไฮโดรเจนเปอร์ออกไซด์ (H2O2)", "name_cn": "雙氧水 (H2O2)", "tank_id": "T11-9007B102",
     "tank_capacity": 30000, "tank_max_level": 4.5, "initial_level": 1.36, "initial_stock": 7626.06,
     "specific_gravity": 1.135, "unit": "kg", "daily_consumption": 0,
     "reorder_point": 8000, "critical_point": 5000, "order_qty": 8000,
     "supplier": "บ.เพอร์ออกไซด์ จำกัด", "lead_time_days": 5, "price_per_kg": 12.0, "color": "#10b981"},
    {"id": "FeSO4", "name_th": "เฟอร์รัสซัลเฟต (FeSO4)", "name_cn": "硫酸亞鐵", "tank_id": "11-1011A001",
     "tank_capacity": 10000, "tank_max_level": 330, "initial_level": 583, "initial_stock": 18073,
     "specific_gravity": 1.23, "unit": "kg", "daily_consumption": 837,
     "reorder_point": 5000, "critical_point": 3000, "order_qty": 8130,
     "supplier": "บ.เหล็กไทย เคมี จำกัด", "lead_time_days": 2, "price_per_kg": 3.0, "color": "#f97316"},
    {"id": "PAC", "name_th": "โพลีอลูมิเนียมคลอไรด์ (PAC)", "name_cn": "多元氯化鋁 PAC", "tank_id": "11-2015A001",
     "tank_capacity": 10000, "tank_max_level": 330, "initial_level": 80, "initial_stock": 2480,
     "specific_gravity": 1.2, "unit": "kg", "daily_consumption": 393,
     "reorder_point": 4000, "critical_point": 2000, "order_qty": 5833,
     "supplier": "บ.ไทยโพลีเคมิคอล จำกัด", "lead_time_days": 2, "price_per_kg": 7.0, "color": "#ec4899"},
    {"id": "NaOH_WT", "name_th": "โซดาไฟ WT (NaOH-WT)", "name_cn": "氫氧化鈉 WT", "tank_id": "11-2005B",
     "tank_capacity": 40000, "tank_max_level": 430, "initial_level": 251, "initial_stock": 24598,
     "specific_gravity": 1.45, "unit": "kg", "daily_consumption": 6430,
     "reorder_point": 15000, "critical_point": 10000, "order_qty": 15172,
     "supplier": "บ.โทเรย์ ไฟน์ เคมิคอลส์ จำกัด", "lead_time_days": 3, "price_per_kg": 8.5, "color": "#6366f1"},
    {"id": "H2SO4_WT", "name_th": "กรดกำมะถัน WT (H2SO4-WT)", "name_cn": "硫酸 WT", "tank_id": "11-1002E",
     "tank_capacity": 10000, "tank_max_level": 180, "initial_level": 224, "initial_stock": 6944,
     "specific_gravity": 1.4, "unit": "kg", "daily_consumption": 0,
     "reorder_point": 3000, "critical_point": 2000, "order_qty": 5000,
     "supplier": "บ.ไทยอาซาฮี เคมิคอลส์ จำกัด", "lead_time_days": 3, "price_per_kg": 5.2, "color": "#eab308"},
]


# ─── HELPER FUNCTIONS ───
def get_chemicals():
    """Get chemicals with applied transactions from session state"""
    chems = copy.deepcopy(CHEMICALS_MASTER)
    for txn in st.session_state.get("transactions", []):
        for c in chems:
            if c["id"] == txn["chemical_id"]:
                if txn["type"] == "receive":
                    c["initial_stock"] += txn["quantity"]
                elif txn["type"] == "use":
                    c["initial_stock"] -= txn["quantity"]
                elif txn["type"] == "adjust":
                    c["initial_stock"] = txn["new_stock"]
                break
    return chems


def get_stock_status(chem):
    pct = (chem["initial_stock"] / chem["tank_capacity"]) * 100
    if chem["initial_stock"] <= chem["critical_point"]:
        return "critical", "🔴 วิกฤต", pct
    elif chem["initial_stock"] <= chem["reorder_point"]:
        return "warning", "🟡 ต้องสั่งซื้อ", pct
    else:
        return "safe", "🟢 ปกติ", pct


def get_days_remaining(chem):
    if chem["daily_consumption"] > 0:
        return chem["initial_stock"] / chem["daily_consumption"]
    return float('inf')


def interpolate_volume(chem_id, level):
    if chem_id not in VOLUME_TABLE:
        return None
    table = VOLUME_TABLE[chem_id]
    levels = sorted(table.keys())
    if level <= levels[0]: return table[levels[0]]
    if level >= levels[-1]: return table[levels[-1]]
    for i in range(len(levels) - 1):
        if levels[i] <= level <= levels[i + 1]:
            ratio = (level - levels[i]) / (levels[i + 1] - levels[i])
            return table[levels[i]] + ratio * (table[levels[i + 1]] - table[levels[i]])
    return None


def add_transaction(txn_type, chemical_id, quantity, **kwargs):
    txn = {
        "id": len(st.session_state.transactions) + 1,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "type": txn_type,
        "chemical_id": chemical_id,
        "quantity": quantity,
        **kwargs
    }
    st.session_state.transactions.append(txn)
    return txn


# ─── Initialize Session State ───
if "pr_list" not in st.session_state:
    st.session_state.pr_list = []
if "pr_counter" not in st.session_state:
    st.session_state.pr_counter = 1
if "transactions" not in st.session_state:
    st.session_state.transactions = []
if "gr_counter" not in st.session_state:
    st.session_state.gr_counter = 1

# Get current chemical state
CHEMICALS = get_chemicals()


# ─── SIDEBAR ───
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0;">
        <div style="font-size: 2.5rem;">🧪</div>
        <h2 style="font-size: 1.2rem; font-weight: 600; color: #f1f5f9; margin: 0.5rem 0;">
            Chemical Management
        </h2>
        <p style="color: #64748b; font-size: 0.8rem;">TH Plant Control System v2</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio(
        "📑 เมนู",
        [
            "📊 Dashboard ภาพรวม",
            "⚠️ แจ้งเตือนสารเคมี",
            "📋 สั่งซื้อ PR",
            "📥 รับสารเคมี / บันทึกใช้งาน",
            "🔬 คำนวณสารเคมี",
            "📜 ประวัติรายการ",
            "📈 ตารางข้อมูลดิบ",
        ],
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

    alerts = [c for c in CHEMICALS if get_stock_status(c)[0] in ("critical", "warning")]
    if alerts:
        st.markdown(f"""
        <div style="margin-top: 1rem; padding: 0.8rem; background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.3); border-radius: 10px;">
            <div style="color: #ef4444; font-weight: 600; font-size: 0.85rem;">⚠️ แจ้งเตือน {len(alerts)} รายการ</div>
        </div>
        """, unsafe_allow_html=True)

    txn_count = len(st.session_state.transactions)
    pr_count = len(st.session_state.pr_list)
    st.markdown(f"""
    <div style="margin-top: 0.8rem; padding: 0.8rem; background: #1a1d29; border-radius: 10px; border: 1px solid #2d3348;">
        <div style="color: #64748b; font-size: 0.7rem; text-transform: uppercase;">สถิติ</div>
        <div style="display: flex; justify-content: space-between; margin-top: 4px;">
            <span style="color: #94a3b8; font-size: 0.8rem;">PR: <b style="color: #8b5cf6;">{pr_count}</b></span>
            <span style="color: #94a3b8; font-size: 0.8rem;">ธุรกรรม: <b style="color: #3b82f6;">{txn_count}</b></span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ═══════════════════════════════════════════════════════
if page == "📊 Dashboard ภาพรวม":
    st.markdown("""
    <div class="main-header">
        <h1>📊 Dashboard ภาพรวมสารเคมี</h1>
        <p>ระบบติดตามและจัดการสารเคมี TH Plant — อัพเดตแบบเรียลไทม์ตามการรับเข้า/ใช้งาน</p>
    </div>
    """, unsafe_allow_html=True)

    total_chemicals = len(CHEMICALS)
    safe_count = sum(1 for c in CHEMICALS if get_stock_status(c)[0] == "safe")
    warning_count = sum(1 for c in CHEMICALS if get_stock_status(c)[0] == "warning")
    critical_count = sum(1 for c in CHEMICALS if get_stock_status(c)[0] == "critical")
    total_stock_value = sum(c["initial_stock"] * c["price_per_kg"] for c in CHEMICALS)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.markdown(f'<div class="metric-card"><div class="label">สารเคมีทั้งหมด</div><div class="value">{total_chemicals}</div><div class="sub">รายการ</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="metric-card"><div class="label">🟢 ปกติ</div><div class="value" style="color:#10b981;">{safe_count}</div><div class="sub">รายการ</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="metric-card"><div class="label">🟡 ต้องสั่งซื้อ</div><div class="value" style="color:#f59e0b;">{warning_count}</div><div class="sub">รายการ</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="metric-card"><div class="label">🔴 วิกฤต</div><div class="value" style="color:#ef4444;">{critical_count}</div><div class="sub">รายการ</div></div>', unsafe_allow_html=True)
    with c5: st.markdown(f'<div class="metric-card"><div class="label">มูลค่าสต็อก</div><div class="value" style="font-size:1.4rem;">฿{total_stock_value:,.0f}</div><div class="sub">บาท</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">📦 สถานะถังสารเคมีทั้งหมด</div>', unsafe_allow_html=True)

    cols = st.columns(2)
    for idx, chem in enumerate(CHEMICALS):
        status, status_label, pct = get_stock_status(chem)
        days_left = get_days_remaining(chem)
        bar_color = "#ef4444" if status == "critical" else "#f59e0b" if status == "warning" else "#10b981"
        days_text = f"{days_left:.0f} วัน" if days_left < float('inf') else "—"
        status_class = "danger" if status == "critical" else status
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="chemical-card" style="border-left:4px solid {bar_color};">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                    <div><h3 style="margin:0;color:#f1f5f9;font-size:1.1rem;">{chem['name_th']}</h3>
                    <span style="color:#64748b;font-size:0.8rem;">Tank: {chem['tank_id']} | {chem['name_cn']}</span></div>
                    <span class="status-{status_class}">{status_label}</span>
                </div>
                <div style="margin-top:1rem;display:grid;grid-template-columns:1fr 1fr 1fr;gap:0.8rem;">
                    <div><div style="color:#64748b;font-size:0.7rem;">คงเหลือ</div><div style="color:#f1f5f9;font-weight:600;font-family:'JetBrains Mono';">{chem['initial_stock']:,.1f} {chem['unit']}</div></div>
                    <div><div style="color:#64748b;font-size:0.7rem;">ระดับถัง</div><div style="color:#f1f5f9;font-weight:600;font-family:'JetBrains Mono';">{chem['initial_level']}</div></div>
                    <div><div style="color:#64748b;font-size:0.7rem;">ใช้ได้อีก</div><div style="color:{bar_color};font-weight:600;font-family:'JetBrains Mono';">{days_text}</div></div>
                </div>
                <div class="progress-bar-bg" style="margin-top:0.8rem;"><div class="progress-bar-fill" style="width:{min(pct,100):.1f}%;background:{bar_color};"></div></div>
                <div style="display:flex;justify-content:space-between;margin-top:4px;">
                    <span style="color:#64748b;font-size:0.7rem;">0%</span>
                    <span style="color:#94a3b8;font-size:0.7rem;font-weight:500;">{pct:.1f}% ความจุ</span>
                    <span style="color:#64748b;font-size:0.7rem;">100%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# PAGE: ALERTS
# ═══════════════════════════════════════════════════════
elif page == "⚠️ แจ้งเตือนสารเคมี":
    st.markdown('<div class="main-header"><h1>⚠️ ระบบแจ้งเตือนสารเคมี</h1><p>รายการสารเคมีที่ต้องดำเนินการสั่งซื้อ</p></div>', unsafe_allow_html=True)

    critical_list = [c for c in CHEMICALS if get_stock_status(c)[0] == "critical"]
    warning_list = [c for c in CHEMICALS if get_stock_status(c)[0] == "warning"]
    safe_list = [c for c in CHEMICALS if get_stock_status(c)[0] == "safe"]

    if critical_list:
        st.markdown("### 🔴 วิกฤต — ต้องสั่งซื้อทันที")
        for chem in critical_list:
            days = get_days_remaining(chem)
            days_text = f"{days:.0f} วัน" if days < float('inf') else "—"
            st.markdown(f'<div class="alert-card"><div style="display:flex;justify-content:space-between;align-items:center;"><div><div style="color:#fca5a5;font-weight:600;">🔴 {chem["name_th"]}</div><div style="color:#f87171;font-size:0.85rem;margin-top:4px;">Tank: {chem["tank_id"]} | คงเหลือ: <b>{chem["initial_stock"]:,.1f} {chem["unit"]}</b> | ใช้ได้: <b>{days_text}</b></div></div><div style="text-align:right;"><div style="color:#fca5a5;font-size:0.8rem;">แนะนำสั่งซื้อ</div><div style="color:#f1f5f9;font-weight:700;font-size:1.2rem;font-family:\'JetBrains Mono\';">{chem["order_qty"]:,.0f} {chem["unit"]}</div></div></div></div>', unsafe_allow_html=True)
    else:
        st.success("✅ ไม่มีสารเคมีในระดับวิกฤต")

    if warning_list:
        st.markdown("### 🟡 เตือน — ควรวางแผนสั่งซื้อ")
        for chem in warning_list:
            days = get_days_remaining(chem)
            days_text = f"{days:.0f} วัน" if days < float('inf') else "—"
            st.markdown(f'<div class="alert-card warning"><div style="display:flex;justify-content:space-between;align-items:center;"><div><div style="color:#fbbf24;font-weight:600;">🟡 {chem["name_th"]}</div><div style="color:#fcd34d;font-size:0.85rem;margin-top:4px;">Tank: {chem["tank_id"]} | คงเหลือ: <b>{chem["initial_stock"]:,.1f} {chem["unit"]}</b> | ใช้ได้: <b>{days_text}</b></div></div><div style="text-align:right;"><div style="color:#fbbf24;font-size:0.8rem;">แนะนำสั่งซื้อ</div><div style="color:#f1f5f9;font-weight:700;font-size:1.2rem;font-family:\'JetBrains Mono\';">{chem["order_qty"]:,.0f} {chem["unit"]}</div></div></div></div>', unsafe_allow_html=True)

    st.markdown("### 🟢 สถานะปกติ")
    for chem in safe_list:
        pct = (chem["initial_stock"] / chem["tank_capacity"]) * 100
        st.markdown(f'<div style="background:rgba(16,185,129,0.05);border:1px solid rgba(16,185,129,0.2);border-radius:10px;padding:0.8rem 1.2rem;margin-bottom:0.5rem;display:flex;justify-content:space-between;"><span style="color:#34d399;font-weight:500;">{chem["name_th"]}</span><span style="color:#94a3b8;font-size:0.85rem;">{chem["initial_stock"]:,.1f} {chem["unit"]} ({pct:.1f}%)</span></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# PAGE: PURCHASE REQUEST
# ═══════════════════════════════════════════════════════
elif page == "📋 สั่งซื้อ PR":
    st.markdown('<div class="main-header"><h1>📋 ใบขอซื้อ (Purchase Request)</h1><p>สร้างและจัดการใบขอซื้อสารเคมี</p></div>', unsafe_allow_html=True)

    col_form, col_preview = st.columns([1, 1])

    with col_form:
        st.markdown("### 📝 สร้างใบ PR ใหม่")
        selected_chem = st.selectbox("เลือกสารเคมี", options=range(len(CHEMICALS)),
            format_func=lambda i: f"{CHEMICALS[i]['name_th']} ({CHEMICALS[i]['tank_id']})", key="pr_chem")
        chem = CHEMICALS[selected_chem]
        status, label, pct = get_stock_status(chem)

        st.markdown(f"""
        <div style="background:#1a1d29;border:1px solid #2d3348;border-radius:10px;padding:1rem;margin:0.5rem 0;">
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;">
                <div><span style="color:#64748b;font-size:0.8rem;">คงเหลือ:</span> <b style="color:#f1f5f9;">{chem['initial_stock']:,.1f} {chem['unit']}</b></div>
                <div><span style="color:#64748b;font-size:0.8rem;">สถานะ:</span> {label}</div>
                <div><span style="color:#64748b;font-size:0.8rem;">ผู้จำหน่าย:</span> <span style="color:#94a3b8;">{chem['supplier']}</span></div>
                <div><span style="color:#64748b;font-size:0.8rem;">Lead time:</span> <span style="color:#94a3b8;">{chem['lead_time_days']} วัน</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        order_qty = st.number_input("จำนวนสั่งซื้อ (kg)", value=chem["order_qty"], step=100, min_value=0, key="pr_qty")
        unit_price = st.number_input("ราคา (บาท/kg)", value=chem["price_per_kg"], step=0.1, min_value=0.0, key="pr_price")
        delivery_date = st.date_input("วันรับสินค้า", value=datetime.now() + timedelta(days=chem["lead_time_days"]), key="pr_date")
        notes = st.text_area("หมายเหตุ", key="pr_notes")
        priority = st.selectbox("ความสำคัญ", ["🔴 เร่งด่วน", "🟡 ปกติ", "🟢 ไม่เร่งด่วน"], key="pr_priority")
        total_cost = order_qty * unit_price

        st.markdown(f'<div style="background:linear-gradient(135deg,rgba(59,130,246,0.1),rgba(139,92,246,0.1));border:1px solid rgba(59,130,246,0.3);border-radius:10px;padding:1rem;margin:1rem 0;"><div style="color:#94a3b8;font-size:0.8rem;">มูลค่ารวม</div><div style="color:#f1f5f9;font-weight:700;font-size:1.5rem;font-family:\'JetBrains Mono\';">฿{total_cost:,.2f}</div></div>', unsafe_allow_html=True)

        if st.button("✅ สร้างใบ PR", type="primary", use_container_width=True):
            pr = {
                "pr_no": f"PR-{datetime.now().strftime('%Y%m')}-{st.session_state.pr_counter:04d}",
                "date": datetime.now().strftime('%Y-%m-%d %H:%M'),
                "chemical": chem["name_th"], "chemical_id": chem["id"],
                "tank_id": chem["tank_id"], "quantity": order_qty, "unit": chem["unit"],
                "unit_price": unit_price, "total_cost": total_cost, "supplier": chem["supplier"],
                "delivery_date": delivery_date.strftime('%Y-%m-%d'), "priority": priority,
                "notes": notes, "status": "รออนุมัติ", "received": False
            }
            st.session_state.pr_list.append(pr)
            st.session_state.pr_counter += 1
            add_transaction("pr", chem["id"], order_qty, pr_no=pr["pr_no"], note=f"สร้างใบ PR {pr['pr_no']}")
            st.success(f"✅ สร้างใบ PR: {pr['pr_no']}")
            st.rerun()

    with col_preview:
        st.markdown("### 📄 รายการ PR")
        if st.session_state.pr_list:
            for pr in reversed(st.session_state.pr_list):
                p_color = "#ef4444" if "เร่งด่วน" in pr["priority"] else "#f59e0b" if "ปกติ" in pr["priority"] else "#10b981"
                badge = '✅ รับแล้ว' if pr.get("received") else 'รออนุมัติ'
                badge_color = "#10b981" if pr.get("received") else "#60a5fa"
                st.markdown(f"""
                <div style="background:#1a1d29;border:1px solid #2d3348;border-left:4px solid {p_color};border-radius:10px;padding:1.2rem;margin-bottom:0.8rem;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#3b82f6;font-weight:600;font-family:'JetBrains Mono';">{pr['pr_no']}</span>
                        <span style="color:{badge_color};font-size:0.75rem;">{badge}</span>
                    </div>
                    <div style="color:#e2e8f0;font-weight:500;margin-top:6px;">{pr['chemical']}</div>
                    <div style="font-size:0.8rem;margin-top:4px;color:#64748b;">
                        {pr['quantity']:,.0f} {pr['unit']} | ฿{pr['total_cost']:,.0f} | รับ: {pr['delivery_date']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            pr_df = pd.DataFrame(st.session_state.pr_list)
            st.download_button("📥 ดาวน์โหลด CSV", data=pr_df.to_csv(index=False).encode('utf-8-sig'),
                file_name=f"PR_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)
        else:
            st.markdown('<div style="text-align:center;padding:3rem;color:#64748b;">📭 ยังไม่มีใบ PR</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# PAGE: GOODS RECEIPT + USAGE + ADJUSTMENT ★ MAIN NEW PAGE ★
# ═══════════════════════════════════════════════════════
elif page == "📥 รับสารเคมี / บันทึกใช้งาน":
    st.markdown("""
    <div class="main-header">
        <h1>📥 รับสารเคมี / บันทึกใช้งาน / ปรับสต็อก</h1>
        <p>บันทึกเมื่อสารเคมีมาส่ง • บันทึกการใช้งานรายวัน • ปรับสต็อกด้วยตนเอง — สต็อกอัพเดตอัตโนมัติ</p>
    </div>
    """, unsafe_allow_html=True)

    tab_receive, tab_usage, tab_adjust = st.tabs([
        "📥 รับสารเคมีเข้าคลัง (Goods Receipt)",
        "📤 บันทึกการใช้งานรายวัน (領料)",
        "🔧 ปรับสต็อกด้วยตนเอง (Adjustment)"
    ])

    # ── TAB 1: GOODS RECEIPT ──
    with tab_receive:
        st.markdown("#### 📥 บันทึกรับสารเคมีจากผู้จำหน่าย")
        col_f, col_i = st.columns([3, 2])

        with col_f:
            receipt_mode = st.radio("ประเภทการรับ", ["🔗 อ้างอิงจากใบ PR", "📦 รับเข้าโดยไม่มี PR"], horizontal=True, key="rm")

            if receipt_mode == "🔗 อ้างอิงจากใบ PR":
                pending_prs = [pr for pr in st.session_state.pr_list if not pr.get("received")]
                if pending_prs:
                    pr_opts = {f"{pr['pr_no']} — {pr['chemical']} ({pr['quantity']:,.0f} {pr['unit']})": idx
                               for idx, pr in enumerate(st.session_state.pr_list) if not pr.get("received")}
                    sel_label = st.selectbox("เลือกใบ PR", list(pr_opts.keys()), key="gr_sel")
                    pr_idx = pr_opts[sel_label]
                    pr_ref = st.session_state.pr_list[pr_idx]
                    gr_chem = next((c for c in CHEMICALS if c["id"] == pr_ref["chemical_id"]), CHEMICALS[0])

                    st.info(f"📋 **{pr_ref['pr_no']}** | {pr_ref['chemical']} | สั่ง {pr_ref['quantity']:,.0f} {pr_ref['unit']} | สต็อกก่อนรับ: **{gr_chem['initial_stock']:,.1f} kg**")

                    gr_qty = st.number_input("จำนวนรับจริง (kg)", value=int(pr_ref["quantity"]), step=100, min_value=0, key="grq")
                    gr_dn = st.text_input("เลขที่ใบส่งสินค้า (DN)", key="grdn")
                    gr_inv = st.text_input("เลขที่ Invoice", key="grinv")
                    gr_truck = st.text_input("ทะเบียนรถ", key="grtk")
                    gr_batch = st.text_input("Batch/Lot No.", key="grbt")
                    gr_remark = st.text_area("หมายเหตุ", key="grrm")

                    if gr_qty != pr_ref["quantity"]:
                        st.warning(f"⚠️ รับจริง ({gr_qty:,.0f}) ≠ สั่งซื้อ ({pr_ref['quantity']:,.0f}) — ส่วนต่าง {gr_qty - pr_ref['quantity']:+,.0f} kg")

                    new_s = gr_chem["initial_stock"] + gr_qty
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,rgba(16,185,129,0.1),rgba(16,185,129,0.05));border:1px solid rgba(16,185,129,0.3);border-radius:10px;padding:1rem;margin:1rem 0;">
                        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;text-align:center;">
                            <div><div style="color:#64748b;font-size:0.75rem;">ก่อนรับ</div><div style="color:#f1f5f9;font-weight:700;font-family:'JetBrains Mono';">{gr_chem['initial_stock']:,.1f}</div></div>
                            <div><div style="color:#64748b;font-size:0.75rem;">รับเข้า</div><div style="color:#10b981;font-weight:700;font-family:'JetBrains Mono';">+{gr_qty:,.0f}</div></div>
                            <div><div style="color:#64748b;font-size:0.75rem;">หลังรับ</div><div style="color:#f1f5f9;font-weight:700;font-family:'JetBrains Mono';font-size:1.3rem;">{new_s:,.1f}</div></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    if st.button("✅ ยืนยันรับเข้าคลัง", type="primary", use_container_width=True, key="bgr1"):
                        st.session_state.pr_list[pr_idx]["received"] = True
                        st.session_state.pr_list[pr_idx]["status"] = "รับแล้ว"
                        st.session_state.pr_list[pr_idx]["received_date"] = datetime.now().strftime('%Y-%m-%d %H:%M')
                        st.session_state.pr_list[pr_idx]["received_qty"] = gr_qty
                        add_transaction("receive", pr_ref["chemical_id"], gr_qty,
                            pr_no=pr_ref["pr_no"], delivery_note=gr_dn, invoice=gr_inv,
                            truck=gr_truck, batch=gr_batch,
                            note=f"รับตาม {pr_ref['pr_no']} — {gr_qty:,.0f} kg",
                            gr_no=f"GR-{datetime.now().strftime('%Y%m')}-{st.session_state.gr_counter:04d}")
                        st.session_state.gr_counter += 1
                        st.success(f"✅ รับเข้าสำเร็จ! สต็อกใหม่: {new_s:,.1f} kg")
                        st.balloons()
                        st.rerun()
                else:
                    st.info("📭 ไม่มี PR ที่รอรับ — สร้าง PR ใหม่หรือเลือก 'รับเข้าโดยไม่มี PR'")

            else:  # Standalone receipt
                gr_idx = st.selectbox("เลือกสารเคมี", range(len(CHEMICALS)),
                    format_func=lambda i: f"{CHEMICALS[i]['name_th']} ({CHEMICALS[i]['tank_id']})", key="gr_alone")
                gc = CHEMICALS[gr_idx]
                st.info(f"สต็อกปัจจุบัน: **{gc['initial_stock']:,.1f} {gc['unit']}**")

                gq = st.number_input("จำนวนรับ (kg)", value=0, step=100, min_value=0, key="gqa")
                gs = st.text_input("ผู้จำหน่าย", value=gc["supplier"], key="gsa")
                gdn = st.text_input("DN No.", key="gdna")
                ginv = st.text_input("Invoice No.", key="gina")
                gbatch = st.text_input("Batch/Lot", key="gba")
                grm = st.text_area("หมายเหตุ", key="grma")

                if gq > 0:
                    ns = gc["initial_stock"] + gq
                    st.markdown(f'<div style="background:linear-gradient(135deg,rgba(16,185,129,0.1),rgba(16,185,129,0.05));border:1px solid rgba(16,185,129,0.3);border-radius:10px;padding:1rem;margin:1rem 0;text-align:center;"><span style="color:#f1f5f9;font-family:\'JetBrains Mono\';">{gc["initial_stock"]:,.1f}</span> <span style="color:#10b981;">+ {gq:,.0f}</span> = <b style="color:#f1f5f9;font-size:1.3rem;">{ns:,.1f} kg</b></div>', unsafe_allow_html=True)

                if st.button("✅ รับเข้าคลัง (ไม่มี PR)", type="primary", use_container_width=True, key="bgr2"):
                    if gq <= 0:
                        st.error("❌ ระบุจำนวน > 0")
                    else:
                        add_transaction("receive", gc["id"], gq,
                            pr_no="—", delivery_note=gdn, invoice=ginv, batch=gbatch, supplier=gs,
                            note=f"รับ (ไม่มี PR) {gq:,.0f} kg",
                            gr_no=f"GR-{datetime.now().strftime('%Y%m')}-{st.session_state.gr_counter:04d}")
                        st.session_state.gr_counter += 1
                        st.success("✅ รับเข้าสำเร็จ!")
                        st.balloons()
                        st.rerun()

        with col_i:
            st.markdown("#### 📋 รับล่าสุด")
            rtxn = [t for t in st.session_state.transactions if t["type"] == "receive"]
            if rtxn:
                for t in reversed(rtxn[-8:]):
                    cn = next((c["name_th"] for c in CHEMICALS_MASTER if c["id"] == t["chemical_id"]), t["chemical_id"])
                    st.markdown(f'<div class="receipt-card" style="border-left:4px solid #10b981;"><div style="display:flex;justify-content:space-between;"><span style="color:#10b981;font-weight:600;font-size:0.85rem;">{t.get("gr_no","—")}</span><span style="color:#64748b;font-size:0.75rem;">{t["timestamp"]}</span></div><div style="color:#e2e8f0;margin-top:4px;">{cn} — <span style="color:#10b981;">+{t["quantity"]:,.0f} kg</span></div><div style="color:#64748b;font-size:0.75rem;">PR: {t.get("pr_no","—")} | DN: {t.get("delivery_note","—")}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="text-align:center;padding:2rem;color:#64748b;">📭 ยังไม่มีประวัติ</div>', unsafe_allow_html=True)

    # ── TAB 2: DAILY USAGE ──
    with tab_usage:
        st.markdown("#### 📤 บันทึกการใช้สารเคมีรายวัน")
        col_uf, col_ui = st.columns([3, 2])

        with col_uf:
            ui = st.selectbox("สารเคมี", range(len(CHEMICALS)),
                format_func=lambda i: f"{CHEMICALS[i]['name_th']} ({CHEMICALS[i]['tank_id']})", key="uc")
            uc = CHEMICALS[ui]

            st.info(f"สต็อก: **{uc['initial_stock']:,.1f} {uc['unit']}** | เฉลี่ย/วัน: **{uc['daily_consumption']:,.1f} {uc['unit']}**")

            ud = st.date_input("วันที่ใช้", value=datetime.now(), key="ud")
            uq = st.number_input("จำนวนใช้ (kg)", value=0.0, step=10.0, min_value=0.0, key="uq")
            up = st.selectbox("วัตถุประสงค์", ["Water Treatment", "System Cleaning", "ปรับ pH", "กระบวนการผลิต", "ทดสอบ", "อื่นๆ"], key="up")
            uo = st.text_input("ผู้บันทึก", key="uo")
            un = st.text_area("หมายเหตุ", key="un")

            if uq > 0:
                rem = uc["initial_stock"] - uq
                if rem < 0:
                    st.error(f"❌ ใช้ ({uq:,.1f}) > สต็อก ({uc['initial_stock']:,.1f})")
                else:
                    rc = "#ef4444" if rem <= uc["critical_point"] else "#f59e0b" if rem <= uc["reorder_point"] else "#10b981"
                    st.markdown(f'<div style="background:linear-gradient(135deg,rgba(245,158,11,0.1),rgba(245,158,11,0.05));border:1px solid rgba(245,158,11,0.3);border-radius:10px;padding:1rem;margin:1rem 0;text-align:center;"><span style="color:#f1f5f9;font-family:\'JetBrains Mono\';">{uc["initial_stock"]:,.1f}</span> <span style="color:#f59e0b;">- {uq:,.1f}</span> = <b style="color:{rc};font-size:1.3rem;">{rem:,.1f} kg</b></div>', unsafe_allow_html=True)

            if st.button("✅ บันทึกการใช้", type="primary", use_container_width=True, key="bu"):
                if uq <= 0:
                    st.error("❌ ระบุจำนวน > 0")
                elif uq > uc["initial_stock"]:
                    st.error("❌ เกินสต็อก")
                else:
                    add_transaction("use", uc["id"], uq, use_date=ud.strftime('%Y-%m-%d'),
                        purpose=up, operator=uo, note=f"ใช้ {uc['name_th']} {uq:,.1f} kg — {up}")
                    st.success(f"✅ บันทึกสำเร็จ!")
                    st.rerun()

        with col_ui:
            st.markdown("#### 📋 ใช้งานล่าสุด")
            utxn = [t for t in st.session_state.transactions if t["type"] == "use"]
            if utxn:
                for t in reversed(utxn[-8:]):
                    cn = next((c["name_th"] for c in CHEMICALS_MASTER if c["id"] == t["chemical_id"]), t["chemical_id"])
                    st.markdown(f'<div class="receipt-card" style="border-left:4px solid #f59e0b;"><div style="display:flex;justify-content:space-between;"><span style="color:#f59e0b;font-weight:600;">📤 ใช้งาน</span><span style="color:#64748b;font-size:0.75rem;">{t["timestamp"]}</span></div><div style="color:#e2e8f0;margin-top:4px;">{cn} — <span style="color:#f59e0b;">-{t["quantity"]:,.1f} kg</span></div><div style="color:#64748b;font-size:0.75rem;">{t.get("purpose","—")}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="text-align:center;padding:2rem;color:#64748b;">📭 ยังไม่มีประวัติ</div>', unsafe_allow_html=True)

    # ── TAB 3: ADJUSTMENT ──
    with tab_adjust:
        st.markdown("#### 🔧 ปรับสต็อกด้วยตนเอง (Physical Count / Correction)")
        st.info("ℹ️ ใช้เมื่อตรวจนับสต็อกจริง หรือแก้ข้อมูลผิดพลาด")

        ai = st.selectbox("สารเคมี", range(len(CHEMICALS)),
            format_func=lambda i: f"{CHEMICALS[i]['name_th']} ({CHEMICALS[i]['tank_id']})", key="ac")
        ac = CHEMICALS[ai]
        st.markdown(f"**สต็อกในระบบ:** `{ac['initial_stock']:,.1f} {ac['unit']}`")

        an = st.number_input("ปริมาณจริง (kg)", value=float(ac["initial_stock"]), step=10.0, min_value=0.0, key="an")
        ar = st.selectbox("สาเหตุ", ["ตรวจนับจริง", "แก้ไขข้อผิดพลาด", "สูญเสีย/ระเหย", "คืนสินค้า", "อื่นๆ"], key="ar")
        anote = st.text_area("หมายเหตุ", key="anote")

        diff = an - ac["initial_stock"]
        if abs(diff) > 0.01:
            dc = "#10b981" if diff > 0 else "#ef4444"
            st.markdown(f'<div style="background:rgba(139,92,246,0.05);border:1px solid rgba(139,92,246,0.3);border-radius:10px;padding:1rem;margin:1rem 0;text-align:center;"><span style="color:#f1f5f9;">{ac["initial_stock"]:,.1f}</span> → <span style="color:{dc};">{diff:+,.1f}</span> → <b style="color:#f1f5f9;font-size:1.3rem;">{an:,.1f} kg</b></div>', unsafe_allow_html=True)

        if st.button("✅ ยืนยันปรับสต็อก", type="primary", use_container_width=True, key="ba"):
            if abs(diff) < 0.01:
                st.warning("ไม่มีการเปลี่ยนแปลง")
            else:
                add_transaction("adjust", ac["id"], abs(diff), new_stock=an, old_stock=ac["initial_stock"],
                    reason=ar, note=f"ปรับ {ac['name_th']}: {ac['initial_stock']:,.1f}→{an:,.1f} ({ar})")
                st.success(f"✅ ปรับสต็อกสำเร็จ!")
                st.rerun()


# ═══════════════════════════════════════════════════════
# PAGE: CALCULATOR
# ═══════════════════════════════════════════════════════
elif page == "🔬 คำนวณสารเคมี":
    st.markdown('<div class="main-header"><h1>🔬 ระบบคำนวณสารเคมี</h1><p>Level→Volume, คำนวณการเติม, พยากรณ์</p></div>', unsafe_allow_html=True)

    t1, t2, t3 = st.tabs(["📏 Level→Volume", "📦 คำนวณเติม", "📅 พยากรณ์"])

    with t1:
        c1, c2 = st.columns(2)
        with c1: cc = st.selectbox("สารเคมี", list(VOLUME_TABLE.keys()), key="cc1")
        with c2: cl = st.slider("ระดับ (m)", 0.0, 4.5, 2.0, 0.01, key="cl1")
        r = interpolate_volume(cc, cl)
        if r:
            st.markdown(f'<div style="background:linear-gradient(135deg,rgba(59,130,246,0.1),rgba(139,92,246,0.1));border:1px solid rgba(59,130,246,0.3);border-radius:14px;padding:2rem;text-align:center;margin-top:1rem;"><div style="color:#94a3b8;">{cc} @ {cl:.2f} m</div><div style="color:#f1f5f9;font-weight:700;font-size:2.5rem;font-family:\'JetBrains Mono\';">{r:,.2f}</div><div style="color:#64748b;">kg</div></div>', unsafe_allow_html=True)

    with t2:
        c1, c2, c3 = st.columns(3)
        with c1: fc = st.selectbox("สารเคมี", list(VOLUME_TABLE.keys()), key="fc")
        with c2: flv = st.number_input("ระดับปัจจุบัน (m)", value=1.5, step=0.01, min_value=0.0, max_value=4.5)
        with c3: fkg = st.number_input("เติม (kg)", value=14000, step=100, min_value=0)
        cv = interpolate_volume(fc, flv)
        if cv:
            nv = cv + fkg
            table = VOLUME_TABLE[fc]
            lvls = sorted(table.keys())
            nl = lvls[0]
            for i in range(len(lvls)-1):
                if table[lvls[i]] >= nv >= table[lvls[i+1]]:
                    nl = lvls[i] + (table[lvls[i]]-nv)/(table[lvls[i]]-table[lvls[i+1]]) * (lvls[i+1]-lvls[i])
                    break
            else:
                if nv <= table[lvls[-1]]: nl = lvls[-1]
            r1, r2, r3 = st.columns(3)
            with r1: st.metric("ปัจจุบัน", f"{cv:,.1f} kg")
            with r2: st.metric("หลังเติม", f"{nv:,.1f} kg")
            with r3: st.metric("ระดับใหม่", f"{nl:.2f} m", delta=f"+{nl-flv:.2f}")
            if nl > 4.0: st.error(f"⚠️ เกินระดับปลอดภัย 4.0m!")
            else: st.success(f"✅ ปลอดภัย (≤ 4.0m)")

    with t3:
        c1, c2 = st.columns(2)
        with c1: fi = st.selectbox("สารเคมี", range(len(CHEMICALS)), format_func=lambda i: CHEMICALS[i]["name_th"], key="fi")
        with c2: fcc = st.number_input("ใช้/วัน (kg)", value=float(CHEMICALS[fi]["daily_consumption"]), step=10.0, min_value=0.0)
        fch = CHEMICALS[fi]
        if fcc > 0:
            d = fch["initial_stock"] / fcc
            rd = datetime.now() + timedelta(days=d)
            st.markdown(f'<div style="background:#1a1d29;border:1px solid #2d3348;border-radius:14px;padding:1.5rem;margin-top:1rem;display:grid;grid-template-columns:1fr 1fr 1fr;gap:1.5rem;text-align:center;"><div><div style="color:#64748b;font-size:0.8rem;">คงเหลือ</div><div style="color:#f1f5f9;font-weight:700;font-size:1.5rem;font-family:\'JetBrains Mono\';">{fch["initial_stock"]:,.1f}</div></div><div><div style="color:#64748b;font-size:0.8rem;">ใช้ได้อีก</div><div style="color:{"#ef4444" if d<7 else "#f59e0b" if d<14 else "#10b981"};font-weight:700;font-size:1.5rem;font-family:\'JetBrains Mono\';">{d:.1f} วัน</div></div><div><div style="color:#64748b;font-size:0.8rem;">หมดวันที่</div><div style="color:#f1f5f9;font-weight:700;font-size:1.5rem;font-family:\'JetBrains Mono\';">{rd.strftime("%d/%m/%Y")}</div></div></div>', unsafe_allow_html=True)
            fd = [{"วัน": x, "คงเหลือ (kg)": max(0, fch["initial_stock"]-fcc*x), "จุดสั่งซื้อ": fch["reorder_point"], "จุดวิกฤต": fch["critical_point"]} for x in range(int(d)+10)]
            st.line_chart(pd.DataFrame(fd).set_index("วัน"), use_container_width=True)
        else:
            st.info("ℹ️ ไม่มีอัตราการใช้ — ไม่สามารถพยากรณ์")


# ═══════════════════════════════════════════════════════
# PAGE: TRANSACTION HISTORY
# ═══════════════════════════════════════════════════════
elif page == "📜 ประวัติรายการ":
    st.markdown('<div class="main-header"><h1>📜 ประวัติรายการทั้งหมด</h1><p>PR • รับเข้า • ใช้งาน • ปรับสต็อก</p></div>', unsafe_allow_html=True)

    cf1, cf2 = st.columns(2)
    with cf1:
        ft = st.multiselect("ประเภท", ["receive","use","adjust","pr"], default=["receive","use","adjust","pr"],
            format_func=lambda x: {"receive":"📥 รับเข้า","use":"📤 ใช้งาน","adjust":"🔧 ปรับสต็อก","pr":"📋 PR"}[x])
    with cf2:
        fcm = st.multiselect("สารเคมี", [c["id"] for c in CHEMICALS_MASTER], default=[c["id"] for c in CHEMICALS_MASTER],
            format_func=lambda x: next((c["name_th"] for c in CHEMICALS_MASTER if c["id"]==x), x))

    ftxn = [t for t in st.session_state.transactions if t["type"] in ft and t["chemical_id"] in fcm]

    s1, s2, s3, s4 = st.columns(4)
    with s1: st.markdown(f'<div class="metric-card"><div class="label">📥 รับเข้า</div><div class="value" style="color:#10b981;">{sum(1 for t in ftxn if t["type"]=="receive")}</div></div>', unsafe_allow_html=True)
    with s2: st.markdown(f'<div class="metric-card"><div class="label">📤 ใช้งาน</div><div class="value" style="color:#f59e0b;">{sum(1 for t in ftxn if t["type"]=="use")}</div></div>', unsafe_allow_html=True)
    with s3: st.markdown(f'<div class="metric-card"><div class="label">🔧 ปรับ</div><div class="value" style="color:#8b5cf6;">{sum(1 for t in ftxn if t["type"]=="adjust")}</div></div>', unsafe_allow_html=True)
    with s4: st.markdown(f'<div class="metric-card"><div class="label">📋 PR</div><div class="value" style="color:#3b82f6;">{sum(1 for t in ftxn if t["type"]=="pr")}</div></div>', unsafe_allow_html=True)

    if ftxn:
        tc = {"receive":("📥 รับเข้า","receive","#10b981"), "use":("📤 ใช้งาน","use","#f59e0b"), "adjust":("🔧 ปรับสต็อก","adjust","#ec4899"), "pr":("📋 สร้าง PR","pr","#8b5cf6")}
        for t in reversed(ftxn):
            lb, cs, cl = tc.get(t["type"], ("—","","#64748b"))
            cn = next((c["name_th"] for c in CHEMICALS_MASTER if c["id"]==t["chemical_id"]), t["chemical_id"])
            if t["type"]=="receive": qd=f'<span style="color:#10b981;">+{t["quantity"]:,.1f} kg</span>'
            elif t["type"]=="use": qd=f'<span style="color:#f59e0b;">-{t["quantity"]:,.1f} kg</span>'
            elif t["type"]=="adjust": qd=f'<span style="color:#ec4899;">{t.get("old_stock",0):,.1f}→{t.get("new_stock",0):,.1f}</span>'
            else: qd=f'<span style="color:#8b5cf6;">สั่ง {t["quantity"]:,.0f} kg</span>'
            st.markdown(f'<div class="timeline-item {cs}"><div style="display:flex;justify-content:space-between;"><span style="color:{cl};font-weight:600;">{lb}</span><span style="color:#64748b;font-size:0.75rem;">{t["timestamp"]}</span></div><div style="color:#e2e8f0;margin-top:4px;">{cn} — {qd}</div><div style="color:#94a3b8;font-size:0.8rem;">{t.get("note","")}</div></div>', unsafe_allow_html=True)

        csv = pd.DataFrame(ftxn).to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 ดาวน์โหลด CSV", data=csv, file_name=f"Txn_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)
    else:
        st.markdown('<div style="text-align:center;padding:3rem;color:#64748b;">📭 ยังไม่มีรายการ</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# PAGE: RAW DATA
# ═══════════════════════════════════════════════════════
elif page == "📈 ตารางข้อมูลดิบ":
    st.markdown('<div class="main-header"><h1>📈 ตารางข้อมูลดิบ</h1><p>จากไฟล์ 115-3_TH_tank</p></div>', unsafe_allow_html=True)

    rd = [{"Tank": c["tank_id"], "Chemical": c["name_th"], "中文": c["name_cn"],
           "Capacity": f"{c['tank_capacity']:,}", "Stock (kg)": f"{c['initial_stock']:,.1f}",
           "SG": c["specific_gravity"], "Use/Day": f"{c['daily_consumption']:,.1f}",
           "Reorder": f"{c['reorder_point']:,}", "Status": get_stock_status(c)[1]} for c in CHEMICALS]
    st.dataframe(pd.DataFrame(rd), use_container_width=True, hide_index=True)

    st.markdown("### 📐 Volume Table")
    vd = [{"Level": lv, **{k: f"{VOLUME_TABLE[k][lv]:,.2f}" for k in VOLUME_TABLE}} for lv in [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5]]
    st.dataframe(pd.DataFrame(vd), use_container_width=True, hide_index=True)


# ─── Footer ───
st.markdown("---")
st.markdown('<div style="text-align:center;padding:1rem;color:#475569;font-size:0.8rem;">🧪 Chemical Management System v2 | TH Plant | Streamlit + Python | © 2026</div>', unsafe_allow_html=True)

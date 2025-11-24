import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from io import BytesIO

PASSWORD = "nbfcsecure123"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("Enter password to access dashboard:", type="password")
    if password == PASSWORD:
        st.session_state.authenticated = True
        st.success("Access granted. Welcome!")
        st.rerun()
    elif password:
        st.error("Incorrect password")
    st.stop()

# Set page config
st.set_page_config(
    page_title="NBFC Lending Business Calculator",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Dashboard CSS
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* Global Styles */
* {
    font-family: 'Inter', sans-serif;
}

/* Main app background */
.stApp {
    background: linear-gradient(135deg, #f8fafc 0%, #edf2f7 100%);
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main content area */
.main .block-container {
    padding: 1.5rem 2.5rem;
    max-width: 1600px;
}

/* Dashboard Header */
.dashboard-header {
    background: linear-gradient(135deg, #2b6cb0 0%, #2c5282 100%);
    padding: 2.5rem 3rem;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(43, 108, 176, 0.2);
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
}

.dashboard-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
    border-radius: 50%;
}

.dashboard-header::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: -5%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(255,255,255,0.06) 0%, transparent 70%);
    border-radius: 50%;
}

.dashboard-title {
    font-size: 2.25rem;
    font-weight: 800;
    color: white;
    margin: 0;
    text-shadow: 0 2px 8px rgba(0,0,0,0.15);
    position: relative;
    z-index: 1;
    letter-spacing: -0.5px;
    text-align: center;
}

.dashboard-subtitle {
    font-size: 1.125rem;
    color: rgba(255,255,255,0.95);
    margin: 0.75rem 0 0 0;
    font-weight: 500;
    position: relative;
    z-index: 1;
    text-align: center;
}

/* Section Headers */
.section-header {
    font-size: 1.5rem;
    font-weight: 800;
    color: #1a365d;
    margin: 3rem 0 1.5rem 0;
    padding-bottom: 1rem;
    border-bottom: 3px solid #e2e8f0;
    position: relative;
    letter-spacing: -0.5px;
}

.section-header::before {
    content: '';
    position: absolute;
    bottom: -3px;
    left: 0;
    width: 80px;
    height: 3px;
    background: linear-gradient(90deg, #2b6cb0, #4299e1);
}

/* KPI Card Styles - Modern Dashboard Look */
.kpi-card {
    background: white;
    border-radius: 14px;
    padding: 1rem 1.25rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15), 0 2px 4px rgba(0,0,0,0.1);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    height: 150px;
    border-left: none;
    position: relative;
    border: none;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.kpi-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 16px 32px rgba(0,0,0,0.2), 0 8px 16px rgba(0,0,0,0.15);
}

.kpi-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
}

.kpi-icon {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    background: rgba(255, 255, 255, 0.25);
    backdrop-filter: blur(10px);
}

.kpi-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: #718096;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.25rem;
}

.kpi-value {
    font-size: 1.35rem;
    font-weight: 800;
    color: var(--card-color);
    margin: 0;
    line-height: 1.2;
    word-wrap: break-word;
}

.kpi-trend {
    font-size: 0.8rem;
    font-weight: 600;
    color: #48bb78;
    margin-top: 0.25rem;
    line-height: 1.3;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* Color Variables for KPI Cards */
.kpi-card.blue {
    --card-color: #ffffff;
    --card-bg: rgba(255, 255, 255, 0.2);
    background: linear-gradient(135deg, #3182ce 0%, #2c5282 100%) !important;
    color: white !important;
}

.kpi-card.blue .kpi-label {
    color: rgba(255, 255, 255, 0.9) !important;
}

.kpi-card.blue .kpi-value {
    color: #ffffff !important;
}

.kpi-card.blue .kpi-trend {
    color: rgba(255, 255, 255, 0.95) !important;
}

.kpi-card.green {
    --card-color: #ffffff;
    --card-bg: rgba(255, 255, 255, 0.2);
    background: linear-gradient(135deg, #38a169 0%, #2f855a 100%) !important;
    color: white !important;
}

.kpi-card.green .kpi-label {
    color: rgba(255, 255, 255, 0.9) !important;
}

.kpi-card.green .kpi-value {
    color: #ffffff !important;
}

.kpi-card.green .kpi-trend {
    color: rgba(255, 255, 255, 0.95) !important;
}

.kpi-card.orange {
    --card-color: #ffffff;
    --card-bg: rgba(255, 255, 255, 0.2);
    background: linear-gradient(135deg, #dd6b20 0%, #c05621 100%) !important;
    color: white !important;
}

.kpi-card.orange .kpi-label {
    color: rgba(255, 255, 255, 0.9) !important;
}

.kpi-card.orange .kpi-value {
    color: #ffffff !important;
}

.kpi-card.orange .kpi-trend {
    color: rgba(255, 255, 255, 0.95) !important;
}

.kpi-card.purple {
    --card-color: #ffffff;
    --card-bg: rgba(255, 255, 255, 0.2);
    background: linear-gradient(135deg, #805ad5 0%, #6b46c1 100%) !important;
    color: white !important;
}

.kpi-card.purple .kpi-label {
    color: rgba(255, 255, 255, 0.9) !important;
}

.kpi-card.purple .kpi-value {
    color: #ffffff !important;
}

.kpi-card.purple .kpi-trend {
    color: rgba(255, 255, 255, 0.95) !important;
}

.kpi-card.teal {
    --card-color: #ffffff;
    --card-bg: rgba(255, 255, 255, 0.2);
    background: linear-gradient(135deg, #319795 0%, #2c7a7b 100%) !important;
    color: white !important;
}

.kpi-card.teal .kpi-label {
    color: rgba(255, 255, 255, 0.9) !important;
}

.kpi-card.teal .kpi-value {
    color: #ffffff !important;
}

.kpi-card.teal .kpi-trend {
    color: rgba(255, 255, 255, 0.95) !important;
}

.kpi-card.red {
    --card-color: #ffffff;
    --card-bg: rgba(255, 255, 255, 0.2);
    background: linear-gradient(135deg, #e53e3e 0%, #c53030 100%) !important;
    color: white !important;
}

.kpi-card.red .kpi-label {
    color: rgba(255, 255, 255, 0.9) !important;
}

.kpi-card.red .kpi-value {
    color: #ffffff !important;
}

.kpi-card.red .kpi-trend {
    color: rgba(255, 255, 255, 0.95) !important;
}

/* Chart Container */
.chart-container {
    background: white;
    border-radius: 14px;
    padding: 1.75rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.03);
    margin: 1.5rem 0;
    border: 1px solid #f7fafc;
}

.chart-title {
    font-size: 1.125rem;
    font-weight: 700;
    color: #1a365d;
    margin-bottom: 1rem;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2c5282 0%, #2a4365 100%);
    padding: 0;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 1.5rem 1.25rem;
}

/* Sidebar Title */
[data-testid="stSidebar"] h1 {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 1.125rem !important;
    margin-bottom: 1.5rem !important;
    padding: 1rem !important;
    background: rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
    text-align: center !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
}

/* Sidebar Text */
[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* Sidebar Expanders */
[data-testid="stSidebar"] details summary {
    background: rgba(255, 255, 255, 0.12) !important;
    border-radius: 10px !important;
    padding: 0.875rem 1rem !important;
    margin: 0.5rem 0 !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    font-weight: 600 !important;
    font-size: 0.9375rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}

[data-testid="stSidebar"] details summary:hover {
    background: rgba(255, 255, 255, 0.18) !important;
    border-color: rgba(255, 255, 255, 0.25) !important;
}

[data-testid="stSidebar"] details[open] {
    background: rgba(255, 255, 255, 0.05) !important;
    border-radius: 10px !important;
    padding: 0.5rem !important;
    margin: 0.5rem 0 !important;
}

/* Sidebar Labels */
[data-testid="stSidebar"] label {
    color: #e2e8f0 !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    margin-bottom: 0.5rem !important;
}

/* Sidebar Inputs */
[data-testid="stSidebar"] input[type="number"] {
    background: rgba(255, 255, 255, 0.95) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    color: #2d3748 !important;
    border-radius: 8px !important;
    padding: 0.625rem !important;
    font-weight: 600 !important;
    font-size: 0.9375rem !important;
}

[data-testid="stSidebar"] input[type="number"]:focus {
    border-color: #4299e1 !important;
    box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.2) !important;
    background: rgba(255, 255, 255, 1) !important;
}

/* Sidebar Buttons */
[data-testid="stSidebar"] button {
    background: rgba(66, 153, 225, 0.2) !important;
    color: #ffffff !important;
    border-radius: 6px !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
}

[data-testid="stSidebar"] button:hover {
    background: rgba(66, 153, 225, 0.3) !important;
}

/* Success/Error Messages */
[data-testid="stSidebar"] .stSuccess {
    background: rgba(72, 187, 120, 0.15) !important;
    border-left: 4px solid #48bb78 !important;
    border-radius: 8px !important;
    padding: 0.75rem !important;
    color: #c6f6d5 !important;
}

[data-testid="stSidebar"] .stError {
    background: rgba(245, 101, 101, 0.15) !important;
    border-left: 4px solid #f56565 !important;
    border-radius: 8px !important;
    padding: 0.75rem !important;
    color: #fed7d7 !important;
}

/* Download button styling */
[data-testid="stDownloadButton"] button {
    background: linear-gradient(135deg, #2b6cb0 0%, #2c5282 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 600 !important;
    font-size: 0.9375rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 12px rgba(43, 108, 176, 0.2) !important;
}

[data-testid="stDownloadButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 16px rgba(43, 108, 176, 0.3) !important;
}

/* Table Styling */
[data-testid="stDataFrame"] {
    background: white !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.06) !important;
    overflow: hidden !important;
    border: 1px solid #e2e8f0 !important;
}

[data-testid="stDataFrame"] thead tr th {
    background: linear-gradient(135deg, #1e3a5f 0%, #2c5282 100%) !important;
    color: white !important;
    font-weight: 700 !important;
    padding: 1rem 0.75rem !important;
    font-size: 0.8125rem !important;
    border: none !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    text-align: center !important;
    border-right: 1px solid rgba(255,255,255,0.15) !important;
}

[data-testid="stDataFrame"] thead tr th:last-child {
    border-right: none !important;
}

[data-testid="stDataFrame"] tbody tr {
    transition: all 0.2s ease !important;
    border-left: 4px solid transparent !important;
}

/* Alternating row colors - clean pattern */
[data-testid="stDataFrame"] tbody tr:nth-child(odd):not(:last-child) {
    background: #e0f2fe !important;
}

[data-testid="stDataFrame"] tbody tr:nth-child(even):not(:last-child) {
    background: #ffffff !important;
}

[data-testid="stDataFrame"] tbody tr:hover:not(:last-child) {
    background: linear-gradient(90deg, #bfdbfe 0%, #dbeafe 100%) !important;
    transform: scale(1.002) !important;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2) !important;
    border-left: 4px solid #2563eb !important;
}

[data-testid="stDataFrame"] tbody td {
    color: #374151 !important;
    padding: 0.875rem 0.75rem !important;
    border-bottom: 1px solid #e5e7eb !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    text-align: center !important;
    border-right: 1px solid #f3f4f6 !important;
}

[data-testid="stDataFrame"] tbody td:last-child {
    border-right: none !important;
}

/* First column (Month/Rank) - styled like rank column */
[data-testid="stDataFrame"] tbody td:first-child {
    font-weight: 700 !important;
    color: #1e40af !important;
    font-size: 0.95rem !important;
    width: 60px !important;
    text-align: center !important;
}

/* Last row - special emphasis (TOTAL row) */
[data-testid="stDataFrame"] tbody tr:last-child {
    border-bottom: 3px solid #2563eb !important;
    border-top: 3px solid #2563eb !important;
    background: linear-gradient(90deg, #1e3a8a 0%, #1e40af 100%) !important;
}

[data-testid="stDataFrame"] tbody tr:last-child td {
    font-weight: 800 !important;
    background: linear-gradient(90deg, #1e3a8a 0%, #1e40af 100%) !important;
    color: white !important;
    font-size: 0.95rem !important;
}

[data-testid="stDataFrame"] tbody tr:last-child td:first-child {
    background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%) !important;
    color: white !important;
    font-weight: 900 !important;
    font-size: 1.05rem !important;
}

/* Override hover for TOTAL row */
[data-testid="stDataFrame"] tbody tr:last-child:hover td {
    background: linear-gradient(90deg, #1e3a8a 0%, #2563eb 100%) !important;
    color: white !important;
}

/* Plotly Charts */
[data-testid="stPlotlyChart"] {
    background: white !important;
    border-radius: 14px !important;
    padding: 1.5rem !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.03) !important;
    border: 1px solid #f7fafc !important;
}

/* Summary Section */
.summary-box {
    background: linear-gradient(135deg, #ffffff 0%, #fafbfc 100%);
    border-radius: 14px;
    padding: 2rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.03);
    margin: 1.5rem 0;
    border: 1px solid #e2e8f0;
}

.summary-title {
    font-size: 1.5rem;
    font-weight: 800;
    color: #1a365d;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 3px solid #e2e8f0;
    letter-spacing: -0.5px;
    position: relative;
}

.summary-title::before {
    content: '';
    position: absolute;
    bottom: -3px;
    left: 0;
    width: 80px;
    height: 3px;
    background: linear-gradient(90deg, #2b6cb0, #4299e1);
}

/* Summary Metric Cards */
.summary-metric-card {
    background: white;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
    border: none;
    display: flex;
    align-items: center;
    gap: 0.875rem;
}

.summary-metric-card:hover {
    transform: translateX(4px) translateY(-2px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.15);
}

.summary-metric-icon {
    width: 42px;
    height: 42px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    flex-shrink: 0;
    background: rgba(255, 255, 255, 0.3);
    backdrop-filter: blur(10px);
}

.summary-metric-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
    margin-bottom: 0.125rem;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}

.summary-metric-value {
    font-size: 1.25rem;
    font-weight: 800;
    line-height: 1.2;
    color: white;
}

/* Color variations for summary cards */
.summary-card-blue {
    background: linear-gradient(135deg, #3182ce 0%, #2c5282 100%) !important;
}

.summary-card-green {
    background: linear-gradient(135deg, #38a169 0%, #2f855a 100%) !important;
}

.summary-card-teal {
    background: linear-gradient(135deg, #319795 0%, #2c7a7b 100%) !important;
}

.summary-card-red {
    background: linear-gradient(135deg, #e53e3e 0%, #c53030 100%) !important;
}

.summary-card-orange {
    background: linear-gradient(135deg, #dd6b20 0%, #c05621 100%) !important;
}

.summary-card-purple {
    background: linear-gradient(135deg, #805ad5 0%, #6b46c1 100%) !important;
}

.stMarkdown p {
    color: #4a5568 !important;
    font-size: 0.9375rem !important;
    line-height: 1.75 !important;
}

.stMarkdown strong {
    color: #2d3748 !important;
    font-weight: 700 !important;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .dashboard-header {
        padding: 1.5rem 1.25rem;
    }
    
    .dashboard-title {
        font-size: 1.5rem;
    }
    
    .kpi-card {
        margin-bottom: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)

# Dashboard Header
st.markdown("""
<div class="dashboard-header">
    <div class="dashboard-title">💰 NBFC Lending Business Calculator</div>
    <div class="dashboard-subtitle">Visualize your STPL growth story in real time 📈</div>
</div>
""", unsafe_allow_html=True)

# Sidebar for all inputs with collapsible sections
st.sidebar.markdown("# 🎛️ Input Parameters")

# Projection Period
with st.sidebar.expander("📅 Projection Period", expanded=True):
    num_months = st.number_input("Number of Months", min_value=1, max_value=120, value=12, step=1)

# Capital Deployment Parameters
with st.sidebar.expander("💰 Capital Deployment (₹ Crores)", expanded=False):
    capital_values = []
    if num_months <= 12:
        cap_col1, cap_col2 = st.columns(2)
        for i in range(num_months):
            month_num = i + 1
            if month_num <= 5:
                default_val = [5.0, 4.0, 4.0, 4.0, 3.0][i] if month_num <= 5 else 0.0
            else:
                default_val = 0.0
                
            if i % 2 == 0:
                with cap_col1:
                    val = st.number_input(f"Month {month_num}", min_value=0.0, max_value=200.0, value=default_val, step=0.5, key=f"cap_{month_num}")
            else:
                with cap_col2:
                    val = st.number_input(f"Month {month_num}", min_value=0.0, max_value=200.0, value=default_val, step=0.5, key=f"cap_{month_num}")
            capital_values.append(val)
    else:
        for i in range(num_months):
            month_num = i + 1
            if month_num <= 5:
                default_val = [5.0, 4.0, 4.0, 4.0, 3.0][i]
            else:
                default_val = 0.0
            val = st.number_input(f"Month {month_num}", min_value=0.0, max_value=200.0, value=default_val, step=0.5, key=f"cap_{month_num}")
            capital_values.append(val)

for i in range(48):
    if i < len(capital_values):
        globals()[f"month{i+1}_capital"] = capital_values[i]
    else:
        globals()[f"month{i+1}_capital"] = 0.0

total_capital = sum(capital_values)

# Business Parameters
with st.sidebar.expander("📈 Revenue Parameters", expanded=False):
    processing_fees = st.number_input("Processing Fees (%)", min_value=0.0, max_value=30.0, value=11.8, step=0.1) / 100
    monthly_interest_rate = st.number_input("Monthly Interest Rate (%)", min_value=0.0, max_value=50.0, value=30.0, step=0.5) / 100
    marketing_rate = st.number_input("Marketing Expenses (%)", min_value=0.0, max_value=20.0, value=2.0, step=0.1) / 100
    cost_of_funds_rate = st.number_input("Cost of Funds (% monthly)", min_value=0.0, max_value=30.0, value=1.5, step=0.1) / 100

# Operational expense rates
with st.sidebar.expander("🏢 Operational Expenses", expanded=False):
    opex_month1_value = st.number_input("Month 1 OpEx (₹)", 0, 50000000, 1500000, 50000)
    opex_month1 = opex_month1_value / 1e7

    opex_values = [opex_month1]
    opex_types = ['fixed']  # Month 1 is always fixed
    
    for i in range(1, num_months):
        month_num = i + 1
        st.markdown(f"**Month {month_num}**")
        opex_type = st.radio(
            f"OpEx Type for Month {month_num}",
            options=['Percentage of Previous AUM', 'Fixed Amount'],
            key=f"opex_type_{month_num}",
            horizontal=True
        )
        
        if opex_type == 'Percentage of Previous AUM':
            if month_num <= 3:
                default_val = 6.0
            elif month_num <= 6:
                default_val = 6.0
            else:
                default_val = 6.0
            val = st.number_input(f"Month {month_num} OpEx Rate (%)", min_value=0.0, max_value=30.0, value=default_val, step=0.5, key=f"opex_{month_num}") / 100
            opex_values.append(val)
            opex_types.append('percentage')
        else:
            val = st.number_input(f"Month {month_num} OpEx Amount (₹)", min_value=0, max_value=50000000, value=1500000, step=50000, key=f"opex_{month_num}")
            opex_values.append(val / 1e7)
            opex_types.append('fixed')

for i in range(48):
    if i < len(opex_values):
        globals()[f"opex_month{i+1}"] = opex_values[i]
        if i < len(opex_types):
            globals()[f"opex_type_month{i+1}"] = opex_types[i]
        else:
            globals()[f"opex_type_month{i+1}"] = 'percentage'
    else:
        globals()[f"opex_month{i+1}"] = 0.04
        globals()[f"opex_type_month{i+1}"] = 'percentage'

# Loan parameters
with st.sidebar.expander("🎯 Loan Parameters", expanded=False):
    avg_ticket_size = st.number_input("Average Loan Ticket (₹)", 0, 500000, 30000, 1000)

# Collection parameters
with st.sidebar.expander("📊 Collection Parameters", expanded=False):
    t0_collection = st.number_input("T+0 Collection Rate (%)", min_value=0, max_value=100, value=80, step=1) / 100
    t30_collection = st.number_input("T+30 Collection Rate (%)", min_value=0, max_value=100, value=5, step=1) / 100
    t60_collection = st.number_input("T+60 Collection Rate (%)", min_value=0, max_value=100, value=5, step=1) / 100
    t90_collection = st.number_input("T+90 Collection Rate (%)", min_value=0, max_value=100, value=3, step=1) / 100

    total_collection_rate_percent = (t0_collection + t30_collection + t60_collection + t90_collection) * 100
    if total_collection_rate_percent > 100:
        st.error(f"⚠️ Total collection rate is {total_collection_rate_percent:.1f}% - should not exceed 100%")
    else:
        st.success(f"✅ Total collection rate: {total_collection_rate_percent:.1f}%")

    api_cost_80_percent = st.number_input("API Cost (Per Lead Not Converted) ₹", 0, 100, 35, 5)
    api_cost_20_percent = st.number_input("API Cost (Per Converted Customers) ₹", 0, 150, 80, 5)

# Principal Return
with st.sidebar.expander("💳 Monthly Principal Return (₹ Crores)", expanded=False):
    principal_values = []
    if num_months <= 12:
        prin_col1, prin_col2 = st.columns(2)
        for i in range(num_months):
            month_num = i + 1
            if i % 2 == 0:
                with prin_col1:
                    val = st.number_input(f"Month {month_num} PR", min_value=0.0, value=0.0, step=0.1, key=f"prin_{month_num}")
            else:
                with prin_col2:
                    val = st.number_input(f"Month {month_num} PR", min_value=0.0, value=0.0, step=0.1, key=f"prin_{month_num}")
            principal_values.append(val)
    else:
        for i in range(num_months):
            month_num = i + 1
            val = st.number_input(f"Month {month_num} PR", min_value=0.0, value=0.0, step=0.1, key=f"prin_{month_num}")
            principal_values.append(val)

for i in range(48):
    if i < len(principal_values):
        globals()[f"month{i+1}_principal"] = principal_values[i]
    else:
        globals()[f"month{i+1}_principal"] = 0.0

# Calculation function
def calculate_with_exact_formulas():
    months = num_months
    capital_invested = [capital_values[i] * 1e7 if i < len(capital_values) else 0 for i in range(months)]
    opex_rates = [opex_values[i] if i < len(opex_values) else 0.04 for i in range(months)]
    opex_type_list = [opex_types[i] if i < len(opex_types) else 'percentage' for i in range(months)]
    principal_returns = [principal_values[i] * 1e7 if i < len(principal_values) else 0 for i in range(months)]
    
    amount_invested = []
    amount_available = []
    amount_disbursed = []
    customers = []
    opex = []
    api_expense = []
    marketing_expense = []
    cost_of_funds = []
    bad_debt_default = []
    gst = []
    salary = []
    principal_return = []
    interest_revenue = []
    bad_debt_recovery = []
    processing_fees_revenue = []
    profit_loss = []
    aum = []
    
    for month in range(months):
        amount_invested.append(capital_invested[month])
        
        if month == 0:
            available = capital_invested[month]
        else:
            prev_profit = profit_loss[month-1]
            available = amount_available[month-1] + prev_profit + capital_invested[month]
        
        amount_available.append(available)
        disbursed = available / (1 - processing_fees)
        amount_disbursed.append(disbursed)
        
        num_customers = int(disbursed / avg_ticket_size)
        customers.append(num_customers)
        
        if month == 0:
            op_expense = opex_month1_value
        else:
            # Check if OpEx type is percentage or fixed
            if opex_type_list[month] == 'percentage':
                prev_aum = aum[month-1]
                op_expense = prev_aum * opex_rates[month]
            else:  # fixed amount
                op_expense = opex_rates[month] * 1e7  # Convert back to rupees
        
        opex.append(op_expense)
        
        api_cost = (num_customers * 2 * api_cost_20_percent) + (num_customers * 8 * api_cost_80_percent)
        api_expense.append(api_cost)
        
        marketing_exp = disbursed * marketing_rate
        marketing_expense.append(marketing_exp)
        
        # UPDATED: Monthly cost of funds calculation with principal return adjustment
        # Cost of funds = (Cumulative capital invested - Cumulative principal returns up to previous month) × monthly rate
        cumulative_capital = sum(capital_invested[:month+1])
        cumulative_principal_return = sum(principal_returns[:month]) if month > 0 else 0
        net_capital = cumulative_capital - cumulative_principal_return
        cost_of_funds_expense = net_capital * cost_of_funds_rate
        cost_of_funds.append(cost_of_funds_expense)
        
        if month == 0:
            interest = (disbursed * monthly_interest_rate) / 2
        else:
            current_month_interest = (disbursed * monthly_interest_rate) / 2
            prev_month_interest = (amount_disbursed[month-1] * monthly_interest_rate) / 2
            interest = current_month_interest + prev_month_interest
        
        interest_revenue.append(interest)
        
        bad_debt = (disbursed + interest) * (1 - t0_collection)
        bad_debt_default.append(bad_debt)
        
        recovery = 0
        if month >= 1:
            prev_disbursed_plus_interest = amount_disbursed[month-1] + interest_revenue[month-1]
            recovery += prev_disbursed_plus_interest * t30_collection
        if month >= 2:
            prev2_disbursed_plus_interest = amount_disbursed[month-2] + interest_revenue[month-2]
            recovery += prev2_disbursed_plus_interest * t60_collection
        if month >= 3:
            prev3_disbursed_plus_interest = amount_disbursed[month-3] + interest_revenue[month-3]
            recovery += prev3_disbursed_plus_interest * t90_collection
        
        bad_debt_recovery.append(recovery)
        
        pf = disbursed * processing_fees
        processing_fees_revenue.append(pf)
        
        gst_amount = pf * (18/118)
        gst.append(gst_amount)
        
        monthly_salary = 0
        salary.append(monthly_salary)
        principal_return.append(principal_returns[month])
        
        profit = (interest + recovery + pf) - (op_expense + api_cost + marketing_exp + cost_of_funds_expense + bad_debt + gst_amount + monthly_salary + principal_returns[month])
        profit_loss.append(profit)
        
        current_disbursed_interest = disbursed + interest
        
        if month >= 1:
            prev_disbursed_interest = amount_disbursed[month-1] + interest_revenue[month-1]
        else:
            prev_disbursed_interest = 0
            
        if month >= 2:
            prev2_disbursed_interest = amount_disbursed[month-2] + interest_revenue[month-2]
        else:
            prev2_disbursed_interest = 0
            
        if month >= 3:
            prev3_disbursed_interest = amount_disbursed[month-3] + interest_revenue[month-3]
        else:
            prev3_disbursed_interest = 0
            
        aum_value = (current_disbursed_interest + 
                    prev_disbursed_interest * 0.15 + 
                    prev2_disbursed_interest * 0.10 + 
                    prev3_disbursed_interest * 0.03)
        aum.append(aum_value)
    
    df = pd.DataFrame({
        'month': range(1, months + 1),
        'amount_invested': [x/1e7 for x in amount_invested],
        'amount_available': [x/1e7 for x in amount_available],
        'amount_disbursed': [x/1e7 for x in amount_disbursed],
        'customers': customers,
        'opex': [x/1e7 for x in opex],
        'api_expense': [x/1e7 for x in api_expense],
        'marketing_expense': [x/1e7 for x in marketing_expense],
        'cost_of_funds': [x/1e7 for x in cost_of_funds],
        'bad_debt_default': [x/1e7 for x in bad_debt_default],
        'gst': [x/1e7 for x in gst],
        'salary': [x/1e7 for x in salary],
        'principal_return': [x/1e7 for x in principal_return],
        'interest_revenue': [x/1e7 for x in interest_revenue],
        'bad_debt_recovery': [x/1e7 for x in bad_debt_recovery],
        'processing_fees_revenue': [x/1e7 for x in processing_fees_revenue],
        'profit_loss': [x/1e7 for x in profit_loss],
        'aum': [x/1e7 for x in aum]
    })
    
    return df

def calculate_npa(df, num_months):
    """Calculate NPA (Non-Performing Assets) - booked after 3 months
    Returns separate columns for principal and interest NPA"""
    
    monthly_npa_principal = []
    monthly_npa_interest = []
    monthly_npa_total = []
    
    cumulative_npa_principal = []
    cumulative_npa_interest = []
    cumulative_npa_total = []
    
    cumulative_principal_sum = 0
    cumulative_interest_sum = 0
    
    for month in range(num_months):
        if month < 3:
            # No NPA in first 3 months
            monthly_npa_principal.append(0)
            monthly_npa_interest.append(0)
            monthly_npa_total.append(0)
            cumulative_npa_principal.append(0)
            cumulative_npa_interest.append(0)
            cumulative_npa_total.append(0)
        else:
            # NPA is the unrecovered amount from 3 months ago
            month_3_ago = month - 3
            
            # Separate principal and interest from 3 months ago
            principal_3_months_ago = df['amount_disbursed'].iloc[month_3_ago]
            interest_3_months_ago = df['interest_revenue'].iloc[month_3_ago]
            
            # Total collection rate (T+0 + T+30 + T+60 + T+90)
            total_collection_rate = t0_collection + t30_collection + t60_collection + t90_collection
            
            # Calculate NPA for principal and interest separately
            npa_principal = principal_3_months_ago * (1 - total_collection_rate)
            npa_interest = interest_3_months_ago * (1 - total_collection_rate)
            npa_total = npa_principal + npa_interest
            
            # Monthly NPA
            monthly_npa_principal.append(npa_principal)
            monthly_npa_interest.append(npa_interest)
            monthly_npa_total.append(npa_total)
            
            # Cumulative NPA
            cumulative_principal_sum += npa_principal
            cumulative_interest_sum += npa_interest
            cumulative_npa_principal.append(cumulative_principal_sum)
            cumulative_npa_interest.append(cumulative_interest_sum)
            cumulative_npa_total.append(cumulative_principal_sum + cumulative_interest_sum)
    
    return (monthly_npa_principal, monthly_npa_interest, monthly_npa_total,
            cumulative_npa_principal, cumulative_npa_interest, cumulative_npa_total)

# Calculate metrics
sum_annual_investment = 0
for i, capital in enumerate(capital_values):
    months_remaining = num_months - i
    weight = months_remaining / num_months
    sum_annual_investment += capital * weight

df = calculate_with_exact_formulas()

# Add NPA calculation with bifurcation
(df['monthly_npa_principal'], df['monthly_npa_interest'], df['monthly_npa_total'],
 df['cumulative_npa_principal'], df['cumulative_npa_interest'], df['cumulative_npa_total']) = calculate_npa(df, num_months)

final_month_aum = df['aum'].iloc[-1]
if sum_annual_investment > 0:
    period_roi = ((final_month_aum - sum_annual_investment) / sum_annual_investment) * 100
else:
    period_roi = 0

# Key Performance Indicators
st.markdown('<div class="section-header">Key Performance Indicators</div>', unsafe_allow_html=True)

# First Row: 4 cards
col1, col2, col3, col4 = st.columns(4, gap="small")

with col1:
    st.markdown(f"""
    <div class="kpi-card blue">
        <div class="kpi-header">
            <div>
                <div class="kpi-label">Capital Invested</div>
            </div>
            <div class="kpi-icon">💰</div>
        </div>
        <div class="kpi-value">₹{total_capital:.1f} Cr</div>
        <div class="kpi-trend">Total deployment</div>
    </div>
    """, unsafe_allow_html=True)
    
with col2:
    st.markdown(f"""
    <div class="kpi-card green">
        <div class="kpi-header">
            <div>
                <div class="kpi-label">Period ROI</div>
            </div>
            <div class="kpi-icon">📈</div>
        </div>
        <div class="kpi-value">{period_roi:.1f}%</div>
        <div class="kpi-trend">{num_months} months</div>
    </div>
    """, unsafe_allow_html=True)
    
with col3:
    total_profit_loss = df['profit_loss'].sum()
    st.markdown(f"""
    <div class="kpi-card orange">
        <div class="kpi-header">
            <div>
                <div class="kpi-label">Total Profit/Loss</div>
            </div>
            <div class="kpi-icon">🎯</div>
        </div>
        <div class="kpi-value">₹{total_profit_loss:.2f} Cr</div>
        <div class="kpi-trend">{num_months} months cumulative</div>
    </div>
    """, unsafe_allow_html=True)
    
with col4:
    final_month_aum = df['aum'].iloc[-1]
    st.markdown(f"""
    <div class="kpi-card teal">
        <div class="kpi-header">
            <div>
                <div class="kpi-label">Month {num_months} AUM</div>
            </div>
            <div class="kpi-icon">🏆</div>
        </div>
        <div class="kpi-value">₹{final_month_aum:.2f} Cr</div>
        <div class="kpi-trend">Assets under management</div>
    </div>
    """, unsafe_allow_html=True)

# Add spacing between rows
st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)

# Second Row: 3 cards (centered)
col_spacer1, col5, col6, col7, col_spacer2 = st.columns([0.5, 1, 1, 1, 0.5], gap="small")

with col5:
    final_month_disbursed = df['amount_disbursed'].iloc[-1]
    st.markdown(f"""
    <div class="kpi-card purple">
        <div class="kpi-header">
            <div>
                <div class="kpi-label">Month {num_months} Disbursed</div>
            </div>
            <div class="kpi-icon">📊</div>
        </div>
        <div class="kpi-value">₹{final_month_disbursed:.2f} Cr</div>
        <div class="kpi-trend">Latest month</div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    total_principal_return = df['principal_return'].sum()
    st.markdown(f"""
    <div class="kpi-card blue">
        <div class="kpi-header">
            <div>
                <div class="kpi-label">Total Principal Return</div>
            </div>
            <div class="kpi-icon">💳</div>
        </div>
        <div class="kpi-value">₹{total_principal_return:.2f} Cr</div>
        <div class="kpi-trend">{num_months} months cumulative</div>
    </div>
    """, unsafe_allow_html=True)

with col7:
    total_npa_kpi = df['cumulative_npa_total'].iloc[-1]
    cum_npa_principal = df['cumulative_npa_principal'].iloc[-1]
    cum_npa_interest = df['cumulative_npa_interest'].iloc[-1]
    st.markdown(f"""
    <div class="kpi-card red">
        <div class="kpi-header">
            <div>
                <div class="kpi-label">Total NPA</div>
            </div>
            <div class="kpi-icon">⚠️</div>
        </div>
        <div class="kpi-value">₹{total_npa_kpi:.2f} Cr</div>
        <div class="kpi-trend">Principal: ₹{cum_npa_principal:.2f} Cr | Interest: ₹{cum_npa_interest:.2f} Cr</div>
    </div>
    """, unsafe_allow_html=True)

# Charts Section
st.markdown('<div class="section-header">Business Health at a Glance</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Pie Chart: Capital Invested vs Latest Month AUM
    fig_capital_pie = go.Figure(data=[go.Pie(
        labels=['Capital Invested', f'Month {num_months} AUM'],
        values=[total_capital, final_month_aum],
        hole=0.4,
        marker=dict(colors=['#3182ce', '#38a169']),
        textinfo='label+percent+value',
        texttemplate='<b>%{label}</b><br>₹%{value:.2f} Cr<br>(%{percent})',
        hovertemplate='<b>%{label}</b><br>₹%{value:.2f} Cr<br>%{percent}<extra></extra>'
    )])
    
    fig_capital_pie.update_layout(
        title="Capital Invested vs Latest Month AUM",
        height=400,
        template="plotly_white",
        title_font=dict(size=16, color='#2d3748', family='Inter'),
        font=dict(family='Inter', size=12),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    st.plotly_chart(fig_capital_pie, use_container_width=True)

with col2:
    # Histogram: Invested vs Disbursed with Profit Line
    fig_invest_disburse = go.Figure()
    
    # Add bars for Invested (Blue)
    fig_invest_disburse.add_trace(go.Bar(
        x=df['month'],
        y=df['amount_invested'],
        name='Capital Invested',
        marker_color='#4A90E2'
    ))
    
    # Add bars for Disbursed (Yellow/Gold)
    fig_invest_disburse.add_trace(go.Bar(
        x=df['month'],
        y=df['amount_disbursed'],
        name='Amount Disbursed',
        marker_color='#F5C842'
    ))
    
    # Add line for Profit on secondary axis (Red/Coral)
    fig_invest_disburse.add_trace(go.Scatter(
        x=df['month'],
        y=df['profit_loss'],
        name='Profit/Loss',
        mode='lines+markers',
        line=dict(color='#E57373', width=3),
        marker=dict(size=8, color='#E57373'),
        yaxis='y2'
    ))
    
    fig_invest_disburse.update_layout(
        title="Capital Invested vs Disbursed (with Profit Overlay)",
        xaxis=dict(title="Month", dtick=1),
        yaxis=dict(
            title="Amount (₹ Crores)",
            side='left'
        ),
        yaxis2=dict(
            title="Profit/Loss (₹ Crores)",
            overlaying='y',
            side='right'
        ),
        height=400,
        template="plotly_white",
        title_font=dict(size=16, color='#2d3748', family='Inter'),
        font=dict(family='Inter', size=12),
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        )
    )
    st.plotly_chart(fig_invest_disburse, use_container_width=True)

# Complete calculations table
st.markdown('<div class="section-header">Monthly Financial & Operational Register</div>', unsafe_allow_html=True)

display_df = df.round(3)
column_names = {
    'month': 'Month',
    'amount_invested': 'Invested (₹Cr)',
    'amount_available': 'Available (₹Cr)',
    'amount_disbursed': 'Disbursed (₹Cr)',
    'customers': 'Customers',
    'opex': 'OpEx (₹Cr)',
    'api_expense': 'API (₹Cr)',
    'marketing_expense': 'Marketing (₹Cr)',
    'cost_of_funds': 'Cost of Funds (₹Cr)',
    'bad_debt_default': 'Bad Debt (₹Cr)',
    'gst': 'GST (₹Cr)',
    'interest_revenue': 'Interest (₹Cr)',
    'bad_debt_recovery': 'Recovery (₹Cr)',
    'processing_fees_revenue': 'PF (₹Cr)',
    'principal_return': 'Principal Return (₹Cr)',
    'monthly_npa_principal': 'M-NPA Principal (₹Cr)',
    'monthly_npa_interest': 'M-NPA Interest (₹Cr)',
    'monthly_npa_total': 'M-NPA Total (₹Cr)',
    'cumulative_npa_principal': 'Cum-NPA Principal (₹Cr)',
    'cumulative_npa_interest': 'Cum-NPA Interest (₹Cr)',
    'cumulative_npa_total': 'Cum-NPA Total (₹Cr)',
    'profit_loss': 'Profit (₹Cr)',
    'aum': 'AUM (₹Cr)'
}

display_df = display_df.drop('salary', axis=1)
display_df = display_df.rename(columns=column_names)

# Reorder columns as requested
column_order = [
    'Month',
    'Invested (₹Cr)',
    'Available (₹Cr)',
    'Disbursed (₹Cr)',
    'Customers',
    'PF (₹Cr)',
    'Interest (₹Cr)',
    'GST (₹Cr)',
    'OpEx (₹Cr)',
    'API (₹Cr)',
    'Marketing (₹Cr)',
    'Bad Debt (₹Cr)',
    'Recovery (₹Cr)',
    'Cost of Funds (₹Cr)',
    'Principal Return (₹Cr)',
    'Profit (₹Cr)',
    'AUM (₹Cr)',
    'M-NPA Principal (₹Cr)',
    'M-NPA Interest (₹Cr)',
    'M-NPA Total (₹Cr)',
    'Cum-NPA Principal (₹Cr)',
    'Cum-NPA Interest (₹Cr)',
    'Cum-NPA Total (₹Cr)'
]

display_df = display_df[column_order]

# Add totals row
totals_row = pd.DataFrame([{
    'Month': 'TOTAL',
    'Invested (₹Cr)': df['amount_invested'].sum(),
    'Available (₹Cr)': df['amount_available'].sum(),
    'Disbursed (₹Cr)': df['amount_disbursed'].sum(),
    'Customers': '',
    'PF (₹Cr)': df['processing_fees_revenue'].sum(),
    'Interest (₹Cr)': df['interest_revenue'].sum(),
    'GST (₹Cr)': df['gst'].sum(),
    'OpEx (₹Cr)': df['opex'].sum(),
    'API (₹Cr)': df['api_expense'].sum(),
    'Marketing (₹Cr)': df['marketing_expense'].sum(),
    'Bad Debt (₹Cr)': '',
    'Recovery (₹Cr)': '',
    'Cost of Funds (₹Cr)': df['cost_of_funds'].sum(),
    'Principal Return (₹Cr)': df['principal_return'].sum(),
    'Profit (₹Cr)': df['profit_loss'].sum(),
    'AUM (₹Cr)': '',
    'M-NPA Principal (₹Cr)': df['monthly_npa_principal'].sum(),
    'M-NPA Interest (₹Cr)': df['monthly_npa_interest'].sum(),
    'M-NPA Total (₹Cr)': '',
    'Cum-NPA Principal (₹Cr)': '',
    'Cum-NPA Interest (₹Cr)': '',
    'Cum-NPA Total (₹Cr)': ''
}])

display_df = pd.concat([display_df, totals_row], ignore_index=True)

# Create Excel download button
def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Monthly Calculations')
        
        # Get the workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets['Monthly Calculations']
        
        # Auto-adjust column widths
        for idx, col in enumerate(df.columns):
            max_length = max(
                df[col].astype(str).map(len).max(),
                len(str(col))
            )
            worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)
    
    output.seek(0)
    return output

excel_data = convert_df_to_excel(display_df)

st.download_button(
    label="📥 Download Excel File",
    data=excel_data,
    file_name=f"NBFC_Monthly_Calculations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
    mime="application/vnd.openxmlxl.sheet",
    use_container_width=True
)

st.dataframe(display_df, use_container_width=True, hide_index=True, height=400)

# Financial Summary
st.markdown('<div class="section-header">Financial Summary</div>', unsafe_allow_html=True)

total_revenue = df['interest_revenue'] + df['processing_fees_revenue'] + df['bad_debt_recovery']
total_costs = (df['opex'] + df['api_expense'] + df['marketing_expense'] + 
               df['cost_of_funds'] + df['bad_debt_default'] + df['gst'] + 
               df['salary'] + df['principal_return'])

total_revenue_sum = total_revenue.sum()
total_costs_sum = total_costs.sum()
net_profit_sum = df['profit_loss'].sum()
final_month_available = df['amount_available'].iloc[-1]
total_customers_sum = df['customers'].sum()
final_month_aum_summary = df['aum'].iloc[-1]
total_npa_sum = df['cumulative_npa_total'].iloc[-1]
total_marketing = df['marketing_expense'].sum()
total_api_cost = df['api_expense'].sum()
total_pf = df['processing_fees_revenue'].sum()
total_interest = df['interest_revenue'].sum()

# Create two main columns: Input Parameters and Output Parameters
input_col, output_col = st.columns([1, 1], gap="large")

with input_col:
    st.markdown('<h3 style="color: #1a365d; font-weight: 700; margin-bottom: 1.5rem;">Input Parameters</h3>', unsafe_allow_html=True)
    
    # Create 2 sub-columns for input parameters
    input_sub_col1, input_sub_col2 = st.columns(2)
    
    with input_sub_col1:
        st.markdown(f"""
        <div class="summary-metric-card summary-card-blue">
            <div class="summary-metric-icon">📅</div>
            <div>
                <div class="summary-metric-label">Projection Period</div>
                <div class="summary-metric-value">{num_months} Months</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="summary-metric-card summary-card-teal">
            <div class="summary-metric-icon">💳</div>
            <div>
                <div class="summary-metric-label">Average Ticket Size</div>
                <div class="summary-metric-value">₹{avg_ticket_size:,}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="summary-metric-card summary-card-purple">
            <div class="summary-metric-icon">💵</div>
            <div>
                <div class="summary-metric-label">Monthly Interest Rate</div>
                <div class="summary-metric-value">{monthly_interest_rate*100:.1f}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="summary-metric-card summary-card-blue">
            <div class="summary-metric-icon">🏢</div>
            <div>
                <div class="summary-metric-label">Month 1 OpEx</div>
                <div class="summary-metric-value">₹{opex_month1_value/100000:.2f} L</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="summary-metric-card summary-card-teal">
            <div class="summary-metric-icon">🔌</div>
            <div>
                <div class="summary-metric-label">API Cost (Converted)</div>
                <div class="summary-metric-value">₹{api_cost_20_percent}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with input_sub_col2:
        st.markdown(f"""
        <div class="summary-metric-card summary-card-green">
            <div class="summary-metric-icon">💰</div>
            <div>
                <div class="summary-metric-label">Total Capital Deployed</div>
                <div class="summary-metric-value">₹{total_capital:.2f} Cr</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="summary-metric-card summary-card-orange">
            <div class="summary-metric-icon">📄</div>
            <div>
                <div class="summary-metric-label">Processing Fees</div>
                <div class="summary-metric-value">{processing_fees*100:.1f}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="summary-metric-card summary-card-red">
            <div class="summary-metric-icon">📊</div>
            <div>
                <div class="summary-metric-label">Total Collection Rate</div>
                <div class="summary-metric-value">{total_collection_rate_percent:.1f}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        total_principal_return_input = sum(principal_values)
        st.markdown(f"""
        <div class="summary-metric-card summary-card-green">
            <div class="summary-metric-icon">💳</div>
            <div>
                <div class="summary-metric-label">Total Principal Return</div>
                <div class="summary-metric-value">₹{total_principal_return_input:.2f} Cr</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="summary-metric-card summary-card-orange">
            <div class="summary-metric-icon">📢</div>
            <div>
                <div class="summary-metric-label">Marketing Rate</div>
                <div class="summary-metric-value">{marketing_rate*100:.1f}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Centered Cost of Funds card
    st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
    centered_col1, centered_col2, centered_col3 = st.columns([1, 2, 1])
    with centered_col2:
        st.markdown(f"""
        <div class="summary-metric-card summary-card-purple">
            <div class="summary-metric-icon">💼</div>
            <div>
                <div class="summary-metric-label">Cost of Funds (Monthly)</div>
                <div class="summary-metric-value">{cost_of_funds_rate*100:.1f}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with output_col:
    st.markdown('<h3 style="color: #1a365d; font-weight: 700; margin-bottom: 1.5rem;">Output Parameters</h3>', unsafe_allow_html=True)
    
    # Create 2 sub-columns for output parameters
    out_col1, out_col2 = st.columns(2)
    
    with out_col1:
        st.markdown(f"""
        <div class="summary-metric-card summary-card-teal">
            <div class="summary-metric-icon">🏆</div>
            <div>
                <div class="summary-metric-label">Month {num_months} AUM</div>
                <div class="summary-metric-value">₹{final_month_aum_summary:.2f} Cr</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="summary-metric-card summary-card-teal">
            <div class="summary-metric-icon">📈</div>
            <div>
                <div class="summary-metric-label">Total Revenue</div>
                <div class="summary-metric-value">₹{total_revenue_sum:.2f} Cr</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="summary-metric-card summary-card-green">
            <div class="summary-metric-icon">💵</div>
            <div>
                <div class="summary-metric-label">Total Interest</div>
                <div class="summary-metric-value">₹{total_interest:.2f} Cr</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="summary-metric-card summary-card-purple">
            <div class="summary-metric-icon">🔌</div>
            <div>
                <div class="summary-metric-label">Total API Cost</div>
                <div class="summary-metric-value">₹{total_api_cost:.2f} Cr</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="summary-metric-card summary-card-purple">
            <div class="summary-metric-icon">👥</div>
            <div>
                <div class="summary-metric-label">Total Customers</div>
                <div class="summary-metric-value">{total_customers_sum:,}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with out_col2:
        st.markdown(f"""
        <div class="summary-metric-card summary-card-orange">
            <div class="summary-metric-icon">🎯</div>
            <div>
                <div class="summary-metric-label">Net Profit/Loss</div>
                <div class="summary-metric-value">₹{net_profit_sum:.2f} Cr</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="summary-metric-card summary-card-red">
            <div class="summary-metric-icon">💳</div>
            <div>
                <div class="summary-metric-label">Total Costs</div>
                <div class="summary-metric-value">₹{total_costs_sum:.2f} Cr</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="summary-metric-card summary-card-blue">
            <div class="summary-metric-icon">📄</div>
            <div>
                <div class="summary-metric-label">Total Processing Fees</div>
                <div class="summary-metric-value">₹{total_pf:.2f} Cr</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="summary-metric-card summary-card-orange">
            <div class="summary-metric-icon">📢</div>
            <div>
                <div class="summary-metric-label">Total Marketing</div>
                <div class="summary-metric-value">₹{total_marketing:.2f} Cr</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="summary-metric-card summary-card-green">
            <div class="summary-metric-icon">📊</div>
            <div>
                <div class="summary-metric-label">Month {num_months} Available</div>
                <div class="summary-metric-value">₹{final_month_available:.2f} Cr</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Centered Total NPA card
    st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
    out_centered_col1, out_centered_col2, out_centered_col3 = st.columns([1, 2, 1])
    with out_centered_col2:
        st.markdown(f"""
        <div class="summary-metric-card summary-card-red">
            <div class="summary-metric-icon">⚠️</div>
            <div>
                <div class="summary-metric-label">Total NPA</div>
                <div class="summary-metric-value">₹{total_npa_sum:.2f} Cr</div>
            </div>
        </div>
        """, unsafe_allow_html=True)



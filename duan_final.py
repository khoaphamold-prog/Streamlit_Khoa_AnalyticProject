import os
import pandas as pd
import plotly.express as px
import streamlit as st

# =========================================================
# 1. CẤU HÌNH TRANG & GIAO DIỆN (E-COMMERCE THEME)
# =========================================================
st.set_page_config(
    page_title="Superstore Executive Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Bảng màu Plotly tươi trẻ chuẩn E-Commerce
PALETTE = ["#FF6B6B", "#6C5CE7", "#00CEC9", "#FFA502", "#00B894", "#E84393"]
px.defaults.color_discrete_sequence = PALETTE

# Cấu hình ẩn thanh công cụ Plotly để không bị đè lên tiêu đề
CHART_CONFIG = {"displayModeBar": False}

# Custom CSS giao diện
st.markdown(
    """
    <style>
    /* Nền chính Gradient dịu mắt */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Thanh điều hướng bên trái (Sidebar) */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1e2f 0%, #11111d 100%);
    }
    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }

    /* Tiêu đề chính dạng Gradient */
    h1 {
        background: linear-gradient(90deg, #ff6b6b, #6c5ce7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        margin-bottom: 0.2rem !important;
    }

    /* Thẻ KPI khắc phục triệt để lỗi đứt chữ (...) */
    [data-testid="stMetric"] {
        background: #ffffff;
        padding: 16px 18px;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(108, 92, 231, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-left: 6px solid #ff6b6b;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 14px 30px rgba(108, 92, 231, 0.15);
    }
    [data-testid="stMetricLabel"] {
        color: #636e72 !important;
        font-weight: 600;
        font-size: 0.88rem !important;
    }
    [data-testid="stMetricValue"] {
        color: #2d3436 !important;
        font-size: 1.55rem !important;
        font-weight: 800 !important;
        white-space: nowrap !important;
    }

    /* Định dạng Tabs dạng viên thuốc (Pill Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.7);
        padding: 6px 8px;
        border-radius: 14px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        border-radius: 10px;
        color: #636e72;
        font-weight: 600;
        border: none !important;
        padding: 0 18px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #ff6b6b 0%, #ff8e53 100%) !important;
        color: #ffffff !important;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.35);
    }

    /* Hộp thông báo / Insight */
    .stAlert {
        border-radius: 12px;
        background-color: #ffffff;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
    }
    </style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# 2. HÀM BỔ TRỢ & ĐỌC DỮ LIỆU
# =========================================================
def format_compact_number(val, prefix="$"):
    """Rút gọn con số lớn (vd: 8,500,000 -> $8.50M) để tránh bị tràn thẻ KPI"""
    if pd.isna(val):
        return "N/A"
    abs_val = abs(val)
    sign = "-" if val < 0 else ""
    if abs_val >= 1e6:
        return f"{sign}{prefix}{abs_val/1e6:.2f}M"
    elif abs_val >= 1e3:
        return f"{sign}{prefix}{abs_val/1e3:.1f}K"
    else:
        return f"{sign}{prefix}{abs_val:,.0f}"


# Xác định đường dẫn thư mục chứa các file CSV
possible_paths = ["output", "./output", "data/processed", "."]
DATA_DIR = "."
for path in possible_paths:
    if os.path.exists(os.path.join(path, "category_profitability.csv")):
        DATA_DIR = path
        break


@st.cache_data
def load_data(folder):
    df_cat = pd.read_csv(os.path.join(folder, "category_profitability.csv"))
    df_disc = pd.read_csv(os.path.join(folder, "discount_impact.csv"))
    df_loss = pd.read_csv(os.path.join(folder, "loss_subcat.csv"))
    df_region = pd.read_csv(os.path.join(folder, "regional_margin.csv"))
    df_pareto = pd.read_csv(os.path.join(folder, "pareto_analysis.csv"))
    df_rfm = pd.read_csv(os.path.join(folder, "rfm_analysis.csv"))
    df_ship = pd.read_csv(os.path.join(folder, "shipping_analysis.csv"))
    df_monthly = pd.read_csv(os.path.join(folder, "monthly_trend.csv"))
    df_pairs = pd.read_csv(os.path.join(folder, "product_pairs.csv"))

    if "Discount" in df_disc.columns and "Discount_Pct" not in df_disc.columns:
        df_disc["Discount_Pct"] = df_disc["Discount"] * 100

    return (
        df_cat,
        df_disc,
        df_loss,
        df_region,
        df_pareto,
        df_rfm,
        df_ship,
        df_monthly,
        df_pairs,
    )


# Tải dữ liệu
try:
    (
        df_cat,
        df_disc,
        df_loss,
        df_region,
        df_pareto,
        df_rfm,
        df_ship,
        df_monthly,
        df_pairs,
    ) = load_data(DATA_DIR)
except Exception as e:
    st.error(f"⚠️ Không thể tải tập dữ liệu CSV từ thư mục '{DATA_DIR}': {e}")
    st.stop()


# =========================================================
# 3. SIDEBAR BỘ LỌC & ĐIỀU KHIỂN
# =========================================================
st.sidebar.header("🔍 Bộ Lọc & Điều Khiển")
selected_region = st.sidebar.selectbox(
    "📍 Chọn Khu Vực:", ["Tất cả"] + list(df_region["Region"].unique())
)
selected_category = st.sidebar.selectbox(
    "📦 Chọn Danh Mục:", ["Tất cả"] + list(df_cat["Category"].unique())
)

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Mô Phỏng Chiết Khấu")
discount_cap = (
    st.sidebar.slider("Mức trần chiết khấu tối đa (%):", 0, 50, 20, 5) / 100.0
)

# Lọc dữ liệu khu vực
filtered_region = df_region.copy()


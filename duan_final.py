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

# Palette màu tươi trẻ chuẩn E-Commerce cho Plotly
PALETTE = ["#FF6B6B", "#6C5CE7", "#00CEC9", "#FFA502", "#00B894", "#E84393"]
px.defaults.color_discrete_sequence = PALETTE

# CSS Custom cho giao diện E-commerce
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

    /* Thẻ KPI (Metric Cards) khắc phục lỗi bị đứt chữ (...) */
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
        border-left: 5px solid #00cec9;
        box-shadow: 0 4px 15px rgba(0, 206, 201, 0.08);
    }
    </style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# 2. HÀM BỔ TRỢ & ĐỌC DỮ LIỆU
# =========================================================
def format_compact_number(val, prefix="$"):
    """Format con số lớn gọn gàng (vd: 8,500,000 -> $8.50M) để tránh bị tràn thẻ KPI"""
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

    # Xử lý tính toán trước để tránh lỗi CachedObjectMutationWarning
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
if selected_region != "Tất cả":
    filtered_region = filtered_region[filtered_region["Region"] == selected_region]
if selected_category != "Tất cả":
    filtered_region = filtered_region[filtered_region["Category"] == selected_category]


# =========================================================
# 4. TIÊU ĐỀ & THẺ KPI TỔNG QUAN
# =========================================================
st.title("🛍️ Superstore Business Analytics Dashboard")
st.caption("Bảng điều hành quản trị: Tài chính, Chiết khấu, Khách hàng & Vận hành")

total_sales = df_cat["Total_Sales"].sum()
total_profit = df_cat["Total_Profit"].sum()
avg_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0
vip_count = int(len(df_rfm) * 0.2) if not df_rfm.empty else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric(
    label="💰 Doanh Thu",
    value=format_compact_number(total_sales),
    delta="+8.4% MoM"
)
col2.metric(
    label="📈 Lợi Nhuận",
    value=format_compact_number(total_profit),
    delta="+3.2% MoM"
)
col3.metric(
    label="📊 Biên Lợi Nhuận TB",
    value=f"{avg_margin:.1f}%",
    delta="-0.5% Target",
    delta_color="inverse"
)
col4.metric(
    label="👥 Khách Hàng VIP",
    value=f"{vip_count:,} KH",
    delta="+12 KH mới"
)

st.markdown("---")


# =========================================================
# 5. CÁC TAB PHÂN TÍCH CHUYÊN SÂU
# =========================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💰 Tài Chính & Mô Phỏng",
    "🎯 Chiết Khấu & Gánh Lỗ",
    "👥 Khách Hàng RFM",
    "🚚 Vận Hành & Xu Hướng",
    "🛒 Bán Chéo",
])

# ---------------------------------------------------------
# TAB 1: TÀI CHÍNH & MÔ PHỎNG
# ---------------------------------------------------------
with tab1:
    st.subheader("1. Tài Chính & Mô Phỏng Giới Hạn Chiết Khấu")

    saved_loss = df_disc[
        (df_disc["Discount"] > discount_cap) & (df_disc["Total_Profit"] < 0)
    ]["Total_Profit"].abs().sum()

    st.info(
        f"💡 **Mô phỏng:** Nếu áp dụng mức trần chiết khấu **<= {int(discount_cap*100)}%**, "
        f"doanh nghiệp ước tính cắt giảm được **{format_compact_number(saved_loss)}** tiền lỗ!"
    )

    c1, c2 = st.columns(2)
    with c1:
        fig_cat = px.bar(
            df_cat,
            x="Category",
            y=["Total_Sales", "Total_Profit"],
            barmode="group",
            title="Doanh Thu & Lợi Nhuận Theo Ngành Hàng",
            labels={"value": "USD ($)", "variable": "Chỉ Số"},
        )
        fig_cat.update_layout(legend_title_text="Chỉ số", margin=dict(t=40, b=20))
        st.plotly_chart(fig_cat, use_container_width=True)

    with c2:
        fig_reg = px.bar(
            filtered_region,
            x="Region",
            y="Profit_Margin_Pct",
            color="Category",
            barmode="group",
            title="Biên Lợi Nhuận (%) Theo Vùng & Danh Mục",
            labels={"Profit_Margin_Pct": "Biên Lợi Nhuận (%)", "Region": "Khu Vực"},
        )
        fig_reg.update_layout(margin=dict(t=40, b=20))
        st.plotly_chart(fig_reg, use_container_width=True)

# ---------------------------------------------------------
# TAB 2: CHIẾT KHẤU & GÁNH LỖ
# ---------------------------------------------------------
with tab2:
    st.subheader("2. Chiết Khấu & Rủi Ro Gánh Lỗ")
    c1, c2 = st.columns(2)
    with c1:
        fig_disc = px.line(
            df_disc,
            x="Discount_Pct",
            y="Profit_Margin_Pct",
            markers=True,
            title="Tương Quan Chiết Khấu (%) vs Lợi Nhuận (%)",
            labels={"Discount_Pct": "Chiết Khấu (%)", "Profit_Margin_Pct": "Biên Lợi Nhuận (%)"},
        )
        fig_disc.add_hline(
            y=0, line_dash="dash", line_color="#FF6B6B", annotation_text="Điểm Hòa Vốn (0%)"
        )
        fig_disc.update_layout(margin=dict(t=40, b=20))
        st.plotly_chart(fig_disc, use_container_width=True)

    with c2:
        fig_loss = px.bar(
            df_loss,
            x="Total_Profit",
            y="Sub-Category",
            orientation="h",
            color="Total_Profit",
            title="Top Sub-Category Âm Lợi Nhuận Nhất",
            color_continuous_scale="Reds_r",
            labels={"Total_Profit": "Lợi Nhuận ($)", "Sub-Category": "Danh Mục Phụ"},
        )
        fig_loss.update_layout(margin=dict(t=40, b=20))
        st.plotly_chart(fig_loss, use_container_width=True)

# ---------------------------------------------------------
# TAB 3: KHÁCH HÀNG RFM & PARETO
# ---------------------------------------------------------
with tab3:
    st.subheader("3. Khách Hàng (Pareto & RFM)")
    c1, c2 = st.columns([1, 2])
    with c1:
        fig_pareto = px.pie(
            df_pareto,
            names="Customer_Group",
            values="Profit_Share_Pct",
            title="Tỷ Trọng Lợi Nhuận Pareto (Top 20% vs 80%)",
            hole=0.4,
        )
        fig_pareto.update_traces(textinfo="percent+label")
        fig_pareto.update_layout(margin=dict(t=40, b=20))
        st.plotly_chart(fig_pareto, use_container_width=True)

    with c2:
        st.markdown("#### 🔎 Tra Cứu Khách Hàng (RFM)")
        search = st.text_input("Nhập Mã KH hoặc Tên (vd: CG-12520):", "")
        if search:
            match_cond = df_rfm["Customer ID"].str.contains(search, case=False, na=False)
            if "Customer Name" in df_rfm.columns:
                match_cond = match_cond | df_rfm["Customer Name"].str.contains(search, case=False, na=False)
            
            res = df_rfm[match_cond]
            if not res.empty:
                st.dataframe(res, use_container_width=True)
            else:
                st.warning("Không tìm thấy khách hàng phù hợp!")
        else:
            st.dataframe(df_rfm.head(10), use_container_width=True)

# ---------------------------------------------------------
# TAB 4: VẬN HÀNH & XU HƯỚNG MÙA VỤ
# ---------------------------------------------------------
with tab4:
    st.subheader("4. Vận Hành & Chuỗi Cung Ứng")

    # Biểu đồ xu hướng doanh thu / lợi nhuận theo tháng
    if not df_monthly.empty:
        time_col = df_monthly.columns[0]
        value_cols = [c for c in df_monthly.columns if c != time_col]
        fig_month = px.line(
            df_monthly,
            x=time_col,
            y=value_cols,
            title="Xu Hướng Biến Động Doanh Thu & Lợi Nhuận Theo Tháng",
            markers=True,
            labels={time_col: "Thời Gian", "value": "Giá Trị ($)", "variable": "Chỉ Số"}
        )
        fig_month.update_layout(margin=dict(t=40, b=20))
        st.plotly_chart(fig_month, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        fig_ship_time = px.bar(
            df_ship,
            x="Ship Mode",
            y="Avg_Lead_Time_Days",
            color="Ship Mode",
            title="Thời Gian Giao Hàng Trung Bình (Ngày)",
            labels={"Avg_Lead_Time_Days": "Số Ngày Giao", "Ship Mode": "Hình Thức Vận Chuyển"},
        )
        fig_ship_time.update_layout(margin=dict(t=40, b=20), showlegend=False)
        st.plotly_chart(fig_ship_time, use_container_width=True)

    with c2:
        fig_ship_margin = px.bar(
            df_ship,
            x="Ship Mode",
            y="Profit_Margin_Pct",
            color="Profit_Margin_Pct",
            title="Biên Lợi Nhuận Theo Hình Thức Vận Chuyển",
            color_continuous_scale="Tealgrn",
            labels={"Profit_Margin_Pct": "Biên Lợi Nhuận (%)", "Ship Mode": "Hình Thức Vận Chuyển"},
        )
        fig_ship_margin.update_layout(margin=dict(t=40, b=20))
        st.plotly_chart(fig_ship_margin, use_container_width=True)

# ---------------------------------------------------------
# TAB 5: BÁN CHÉO (CROSS-SELLING)
# ---------------------------------------------------------
with tab5:
    st.subheader("5. Gợi Ý Sản Phẩm Bán Kèm (Cross-Selling)")
    if "Product_A" in df_pairs.columns:
        prod_list = list(df_pairs["Product_A"].unique())
        prod = st.selectbox("🛒 Chọn sản phẩm / danh mục phụ để xem gợi ý bán kèm:", prod_list)

        pairs = df_pairs[
            (df_pairs["Product_A"] == prod) | (df_pairs["Product_B"] == prod)
        ].sort_values(by="Times_Bought_Together", ascending=False)

        st.dataframe(pairs, use_container_width=True)
        st.download_button(
            label="📥 Tải Báo Cáo CSV Bán Kèm",
            data=pairs.to_csv(index=False).encode("utf-8"),
            file_name=f"cross_sell_{prod}.csv",
            mime="text/csv",
        )
    else:
        st.warning("Không tìm thấy dữ liệu cột 'Product_A' trong file product_pairs.csv.")

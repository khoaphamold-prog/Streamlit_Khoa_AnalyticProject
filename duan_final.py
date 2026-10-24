import os
import pandas as pd
import plotly.express as px
import streamlit as st

import os
import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG & GIAO DIỆN TƯƠI TRẺ (E-COMMERCE THEME)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Superstore Executive Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Bảng màu Plotly tươi trẻ dành cho E-commerce
PALETTE = ["#FF6B6B", "#6C5CE7", "#00CEC9", "#FFA502", "#00B894", "#E84393"]
px.defaults.color_discrete_sequence = PALETTE

# CSS Custom cho Streamlit Background & UI elements
st.markdown(
    """
    <style>
    /* 1. Nền chính của toàn bộ App (Gradient nhạt tươi sáng) */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
        font-family: 'Inter', sans-serif;
    }

    /* 2. Styling cho Thanh bên (Sidebar) */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1e2f 0%, #11111d 100%);
        color: #ffffff;
    }
    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }

    /* 3. Tiêu đề Dashboard chính */
    h1 {
        background: linear-gradient(90deg, #ff6b6b, #6c5ce7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }

    /* 4. Thẻ KPI (Metrics) tươi trẻ với viền Gradient */
    [data-testid="stMetric"] {
        background: #ffffff;
        padding: 16px 20px;
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
        font-size: 0.9rem;
    }
    [data-testid="stMetricValue"] {
        color: #2d3436 !important;
        font-weight: 700;
    }

    /* 5. Định dạng các Tabs thành nút hình viên thuốc (Pill Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(255, 255, 255, 0.6);
        padding: 8px;
        border-radius: 14px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
    }
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 10px;
        color: #636e72;
        font-weight: 600;
        border: none !important;
        padding: 0 20px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #ff6b6b 0%, #ff8e53 100%) !important;
        color: #ffffff !important;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.35);
    }

    /* 6. Hộp thông tin st.info */
    .stAlert {
        border-radius: 12px;
        background-color: #ffffff;
        border-left: 5px solid #00cec9;
        box-shadow: 0 4px 15px rgba(0, 206, 201, 0.1);
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🛍️ Superstore Business Analytics Dashboard")
st.caption("Bảng điều hành quản trị: Tài chính, Chiết khấu, Khách hàng & Vận hành")

# 2. Xác định đường dẫn file CSV
possible_paths = ["output", "./output", "data/processed", "."]
DATA_DIR = "."
for path in possible_paths:
    if os.path.exists(os.path.join(path, "category_profitability.csv")):
        DATA_DIR = path
        break


@st.cache_data
def load_data(folder):
    return (
        pd.read_csv(os.path.join(folder, "category_profitability.csv")),
        pd.read_csv(os.path.join(folder, "discount_impact.csv")),
        pd.read_csv(os.path.join(folder, "loss_subcat.csv")),
        pd.read_csv(os.path.join(folder, "regional_margin.csv")),
        pd.read_csv(os.path.join(folder, "pareto_analysis.csv")),
        pd.read_csv(os.path.join(folder, "rfm_analysis.csv")),
        pd.read_csv(os.path.join(folder, "shipping_analysis.csv")),
        pd.read_csv(os.path.join(folder, "monthly_trend.csv")),
        pd.read_csv(os.path.join(folder, "product_pairs.csv")),
    )


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

    # 3. Sidebar điều khiển
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
        st.sidebar.slider("Mức trần chiết khấu tối đa (%):", 0, 50, 20, 5)
        / 100.0
    )

    filtered_region = df_region.copy()
    if selected_region != "Tất cả":
        filtered_region = filtered_region[
            filtered_region["Region"] == selected_region
        ]
    if selected_category != "Tất cả":
        filtered_region = filtered_region[
            filtered_region["Category"] == selected_category
        ]

    # 4. Thẻ KPI
    total_sales = df_cat["Total_Sales"].sum()
    total_profit = df_cat["Total_Profit"].sum()
    avg_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Doanh Thu", f"${total_sales:,.0f}")
    col2.metric("📈 Lợi Nhuận", f"${total_profit:,.0f}")
    col3.metric("📊 Biên Lợi Nhuận TB", f"{avg_margin:.1f}%")
    col4.metric("👥 Khách Hàng VIP", f"{int(len(df_rfm)*0.2):,} KH")

    st.markdown("---")

    # 5. Các Tab phân tích
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💰 Tài Chính & Mô Phỏng",
        "🎯 Chiết Khấu & Gánh Lỗ",
        "👥 Khách Hàng RFM",
        "🚚 Vận Hành",
        "🛒 Bán Chéo",
    ])

    with tab1:
        st.subheader("1. Tài Chính & Mô Phỏng Giới Hạn Chiết Khấu")
        saved = (
            df_disc[
                (df_disc["Discount"] > discount_cap)
                & (df_disc["Total_Profit"] < 0)
            ]["Total_Profit"]
            .abs()
            .sum()
        )
        st.info(
            f"💡 **Mô phỏng:** Nếu giới hạn chiết khấu **<= {int(discount_cap*100)}%**, tiết kiệm ước tính **${saved:,.0f}** khoản lỗ!"
        )

        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(
                px.bar(
                    df_cat,
                    x="Category",
                    y=["Total_Sales", "Total_Profit"],
                    barmode="group",
                    title="Doanh Thu & Lợi Nhuận Theo Ngành Hàng",
                ),
                use_container_width=True,
            )
        with c2:
            st.plotly_chart(
                px.bar(
                    filtered_region,
                    x="Region",
                    y="Profit_Margin_Pct",
                    color="Category",
                    barmode="group",
                    title="Biên Lợi Nhuận (%) Theo Vùng",
                ),
                use_container_width=True,
            )

    with tab2:
        st.subheader("2. Chiết Khấu & Rủi Ro Gánh Lỗ")
        c1, c2 = st.columns(2)
        with c1:
            df_disc["Discount_Pct"] = df_disc["Discount"] * 100
            fig = px.line(
                df_disc,
                x="Discount_Pct",
                y="Profit_Margin_Pct",
                markers=True,
                title="Tương Quan Chiết Khấu (%) vs Lợi Nhuận (%)",
            )
            fig.add_hline(y=0, line_dash="dash", line_color="red")
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.plotly_chart(
                px.bar(
                    df_loss,
                    x="Total_Profit",
                    y="Sub-Category",
                    orientation="h",
                    color="Total_Profit",
                    title="Top Sub-Category Âm Lợi Nhuận",
                ),
                use_container_width=True,
            )

    with tab3:
        st.subheader("3. Khách Hàng (Pareto & RFM)")
        c1, c2 = st.columns([1, 2])
        with c1:
            st.plotly_chart(
                px.pie(
                    df_pareto,
                    names="Customer_Group",
                    values="Profit_Share_Pct",
                    title="Tỷ Trọng Lợi Nhuận Pareto",
                ),
                use_container_width=True,
            )
        with c2:
            st.markdown("#### 🔎 Tra Cứu Khách Hàng (RFM)")
            search = st.text_input("Mã KH (vd: CG-12520):", "")
            if search:
                res = df_rfm[
                    df_rfm["Customer ID"].str.contains(
                        search, case=False, na=False
                    )
                ]
                if not res.empty:
                    st.dataframe(res, use_container_width=True)
                else:
                    st.warning("Không tìm thấy!")
            else:
                st.dataframe(df_rfm.head(10), use_container_width=True)

    with tab4:
        st.subheader("4. Vận Hành & Chuỗi Cung Ứng")
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(
                px.bar(
                    df_ship,
                    x="Ship Mode",
                    y="Avg_Lead_Time_Days",
                    color="Ship Mode",
                    title="Thời Gian Giao Hàng TB (Ngày)",
                ),
                use_container_width=True,
            )
        with c2:
            st.plotly_chart(
                px.bar(
                    df_ship,
                    x="Ship Mode",
                    y="Profit_Margin_Pct",
                    color="Profit_Margin_Pct",
                    title="Biên Lợi Nhuận Theo Ship Mode",
                ),
                use_container_width=True,
            )

    with tab5:
        st.subheader("5. Gợi Ý Sản Phẩm Bán Kèm (Cross-Selling)")
        prod = st.selectbox(
            "🛒 Chọn sản phẩm/danh mục phụ:",
            list(df_pairs["Product_A"].unique()),
        )
        pairs = df_pairs[
            (df_pairs["Product_A"] == prod) | (df_pairs["Product_B"] == prod)
        ].sort_values(by="Times_Bought_Together", ascending=False)
        st.dataframe(pairs, use_container_width=True)
        st.download_button(
            "📥 Tải Báo Cáo CSV",
            pairs.to_csv(index=False).encode("utf-8"),
            f"cross_sell_{prod}.csv",
            "text/csv",
        )

except Exception as e:
    st.error(f"⚠️ Chưa thể tải dữ liệu: {e}")

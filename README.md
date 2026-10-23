# Streamlit_Khoa_AnalyticProject
dự án cuối kỳ môn phân tích dữ liệu 
# 📊 Superstore Business Analytics Dashboard

Dự án xây dựng bảng điều hành quản trị phân tích kinh doanh (Executive Dashboard) cho dữ liệu Superstore, giúp doanh nghiệp tối ưu hóa hiệu quả tài chính, kiểm soát mức chiết khấu, phân khúc khách hàng và nâng cao hiệu quả vận hành chuỗi cung ứng.

---

## 🚀 Tính năng chính

Dashboard được chia thành 5 phân hệ phân tích chuyên sâu:

1. ** Tài Chính & Mô Phỏng Giới Hạn Chiết Khấu:**
   * Tổng quan về Doanh thu, Lợi nhuận và Biên lợi nhuận trung bình.
   * Công cụ mô phỏng giúp dự báo số tiền tiết kiệm được khi thiết lập mức trần chiết khấu (Discount Cap).
   * Biểu đồ so sánh doanh thu và lợi nhuận theo ngành hàng và vùng địa lý.

2. ** Chiết Khấu & Rủi Ro Gánh Lỗ:**
   * Phân tích điểm huề vốn và ngưỡng chiết khấu khiến đơn hàng bắt đầu bị âm lợi nhuận.
   * Xác định danh sách các nhóm sản phẩm phụ (Sub-Category) đang bị lỗ nặng nhất.

3. ** Phân Tích Khách Hàng (Pareto & RFM):**
   * **Quy tắc Pareto (80/20):** Đánh giá tỷ trọng đóng góp doanh thu và lợi nhuận của nhóm khách hàng VIP.
   * **Mô hình RFM (Recency, Frequency, Monetary):** Tra cứu chi tiết chỉ số hành vi mua sắm của từng khách hàng.

4. ** Vận Hành & Chuỗi Cung Ứng:**
   * Thống kê thời gian xử lý đơn hàng trung bình (Lead Time) theo từng phương thức giao hàng (Ship Mode).
   * Đánh giá biên lợi nhuận thực tế theo các hình thức vận chuyển.

5. ** Gợi Ý Bán Chéo (Cross-Selling):**
   * Khai thác giỏ hàng (Basket Analysis) để tìm ra các cặp danh mục sản phẩm thường được mua cùng nhau.
   * Hỗ trợ tra cứu nhanh và xuất báo cáo dữ liệu gợi ý dưới dạng file CSV.

---

##  Công nghệ sử dụng

* **Ngôn ngữ lập trình:** Python 3.x
* **Giao diện Web App:** [Streamlit](https://streamlit.io/)
* **Trực quan hóa dữ liệu:** Plotly Express
* **Xử lý & Phân tích dữ liệu:** Pandas, DuckDB
* **Triển khai (Deployment):** Streamlit Community Cloud & Cloudflare Workers

---

## 📁 Cấu trúc dự án

```text
├── duan_final.py            # Mã nguồn chính chạy ứng dụng Streamlit
├── requirements.txt         # Khai báo các thư viện Python phụ thuộc
├── category_profitability.csv
├── discount_impact.csv
├── loss_subcat.csv
├── monthly_trend.csv
├── pareto_analysis.csv
├── product_pairs.csv
├── regional_margin.csv
├── rfm_analysis.csv
├── shipping_analysis.csv
└── README.md                # Tài liệu giới thiệu dự án

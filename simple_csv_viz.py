# 파일명: simple_csv_viz.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import io

st.title("CSV 자동 시각화 앱")

# 1. CSV 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("데이터 미리보기:", df.head())

    # 2. 컬럼별 타입 확인
    num_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    st.write(f"숫자형 컬럼: {num_cols}")
    st.write(f"범주형 컬럼: {cat_cols}")

    # 3. 숫자형 컬럼 히스토그램
    st.subheader("숫자형 컬럼 히스토그램")
    for col in num_cols:
        fig, ax = plt.subplots()
        df[col].hist(ax=ax, bins=20, color='skyblue')
        ax.set_title(f"{col} 히스토그램")
        st.pyplot(fig)

    # 4. 범주형 컬럼 막대그래프
    st.subheader("범주형 컬럼 막대그래프")
    for col in cat_cols:
        fig = px.bar(df[col].value_counts().reset_index(), x='index', y=col)
        fig.update_layout(title=f"{col} 막대그래프", xaxis_title=col, yaxis_title="Count")
        st.plotly_chart(fig)

    # 5. HTML로 저장 및 다운로드
    st.subheader("HTML 다운로드")
    html_buffer = io.StringIO()
    html_buffer.write("<html><body>")
    html_buffer.write("<h1>CSV 자동 시각화 결과</h1>")
    for col in num_cols:
        fig, ax = plt.subplots()
        df[col].hist(ax=ax, bins=20, color='skyblue')
        img_file = f"{col}_hist.png"
        fig.savefig(img_file)
        plt.close(fig)
        html_buffer.write(f"<h2>{col} 히스토그램</h2><img src='{img_file}'><br>")
    for col in cat_cols:
        fig = px.bar(df[col].value_counts().reset_index(), x='index', y=col)
        fig.write_html(f"{col}_bar.html")
        html_buffer.write(f"<h2>{col} 막대그래프</h2><iframe src='{col}_bar.html' width='600' height='400'></iframe><br>")
    html_buffer.write("</body></html>")

    st.download_button("HTML 다운로드", data=html_buffer.getvalue(), file_name="visualization.html", mime="text/html")

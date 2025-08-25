import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import io

# 앱 제목
st.title("CSV 파일 자동 시각화")

# 1. CSV 파일 업로드
uploaded_file = st.file_uploader("여기에 CSV 파일을 업로드 해주세요", type=["csv"])
if uploaded_file is not None:
    # 업로드한 CSV 읽어오기
    df = pd.read_csv(uploaded_file)
    st.write("데이터를 미리 볼 수 있습니다:", df.head())

    # 숫자형과 범주형 컬럼 나누기
    num_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    st.write(f"숫자형 컬럼: {num_cols}")
    st.write(f"범주형 컬럼: {cat_cols}")

    # 2. 숫자형 컬럼 히스토그램
    st.subheader("숫자형 컬럼 히스토그램")
    for col in num_cols:
        fig, ax = plt.subplots()
        # 숫자형 데이터만 남기고 NaN, inf 제거
        data = pd.to_numeric(df[col], errors='coerce')
        data = data[np.isfinite(data)]
        if len(data) > 0:
            ax.hist(data, bins=20, color='skyblue')
            ax.set_title(f"{col} 히스토그램")
            st.pyplot(fig)
        else:
            st.write(f"{col} 컬럼에는 유효한 숫자가 없어서 히스토그램을 만들 수 없습니다.")

    # 3. 범주형 컬럼 막대그래프
    st.subheader("범주형 컬럼 막대그래프")
    for col in cat_cols:
        counts = df[col].dropna().value_counts()
        if len(counts) > 0:
            fig = px.bar(counts.reset_index(), x='index', y=col)
            fig.update_layout(title=f"{col} 막대그래프", xaxis_title=col, yaxis_title="Count")
            st.plotly_chart(fig)
        else:
            st.write(f"{col} 컬럼에는 데이터가 없어 막대그래프를 만들 수 없습니다.")

    # 4. HTML 파일로 다운로드
    st.subheader("HTML 다운로드")
    html_buffer = io.StringIO()
    html_buffer.write("<html><body><h1>CSV 자동 시각화 결과</h1>")

    # 숫자형 컬럼 이미지 저장
    for col in num_cols:
        data = pd.to_numeric(df[col], errors='coerce')
        data = data[np.isfinite(data)]
        if len(data) > 0:
            fig, ax = plt.subplots()
            ax.hist(data, bins=20, color='skyblue')
            img_file = f"{col}_hist.png"
            fig.savefig(img_file)
            plt.close(fig)
            html_buffer.write(f"<h2>{col} 히스토그램</h2><img src='{img_file}'><br>")

    # 범주형 컬럼 이미지 저장
    for col in cat_cols:
        counts = df[col].dropna().value_counts()
        if len(counts) > 0:
            fig = px.bar(counts.reset_index(), x='index', y=col)
            html_file = f"{col}_bar.html"
            fig.write_html(html_file)
            html_buffer.write(f"<h2>{col} 막대그래프</h2><iframe src='{html_file}' width='600' height='400'></iframe><br>")

    html_buffer.write("</body></html>")

    # HTML 다운로드 버튼
    st.download_button(
        "여기를 눌러 HTML로 저장하세요",
        data=html_buffer.getvalue(),
        file_name="visualization.html",
        mime="text/html"
    )

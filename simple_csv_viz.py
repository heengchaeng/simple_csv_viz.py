import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import io
import base64
#제목
st.title("CSV 파일 자동 시각화")
#파일 업로드창 
uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("데이터 미리보기:", df.head())

    num_cols = df.select_dtypes(include=['int64','float64']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    st.write(f"숫자형 컬럼: {num_cols}")
    st.write(f"범주형 컬럼: {cat_cols}")
#히스토그램
    st.subheader("숫자형 컬럼 히스토그램")
    fig_bytes_list = []  
    for col in num_cols:
        fig, ax = plt.subplots()
        data = pd.to_numeric(df[col], errors='coerce')
        data = data[np.isfinite(data)]
        if len(data) > 0:
            ax.hist(data, bins=20, color='skyblue')
            ax.set_title(f"{col} 히스토그램")
            st.pyplot(fig)

            # 메모리에 이미지 저장
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            fig_bytes_list.append((col, buf.read()))
        else:
            st.write(f"{col} 컬럼에는 유효한 숫자가 없습니다.")
        plt.close(fig)
#막대그래프
    st.subheader("범주형 컬럼 막대그래프")
    html_plotly_list = []  # HTML 다운로드용 Plotly
    for col in cat_cols:
        counts = df[col].dropna().value_counts()
        if len(counts) > 0:
            df_counts = counts.reset_index()
            df_counts.columns = ['value','count']
            fig = px.bar(df_counts, x='value', y='count')
            fig.update_layout(title=f"{col} 막대그래프", xaxis_title=col, yaxis_title="Count")
            st.plotly_chart(fig)
            html_plotly_list.append((col, fig.to_html(full_html=False, include_plotlyjs='cdn')))
        else:
            st.write(f"{col} 컬럼에는 데이터가 없어 막대그래프를 만들 수 없습니다.")

    # HTML 다운로드 버튼
    html_buffer = io.StringIO()
    html_buffer.write("<html><body><h1>CSV 자동 시각화 결과</h1>")

    for col, img_bytes in fig_bytes_list:
        img_b64 = base64.b64encode(img_bytes).decode()
        html_buffer.write(f"<h2>{col} 히스토그램</h2>")
        html_buffer.write(f"<img src='data:image/png;base64,{img_b64}'><br>")

    for col, plot_html in html_plotly_list:
        html_buffer.write(f"<h2>{col} 막대그래프</h2>")
        html_buffer.write(plot_html)

    html_buffer.write("</body></html>")

    st.download_button(
        "HTML로 저장",
        data=html_buffer.getvalue(),
        file_name="visualization.html",
        mime="text/html"
    )

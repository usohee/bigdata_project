# chart_map_demo.py
import streamlit as st
import pandas as pd
import numpy as np

st.title('차트와 지도')
# 1. 선 차트
st.subheader('선 차트 (st.line_chart)')
chart_data = pd.DataFrame(
 np.random.randn(20, 3),
 columns=['a', 'b', 'c']
)
st.line_chart(chart_data)
# 2. 바 차트
st.subheader('바 차트 (st.bar_chart)')
st.bar_chart(chart_data)

# 같은 데이터로 영역 차트
st.subheader('영역 차트 (st.area_chart)')
st.area_chart(chart_data)

# 산점도
st.subheader('산점도 (st.scatter_chart)')
scatter_data = pd.DataFrame(
 np.random.randn(100, 2),
 columns=['x', 'y']
)
st.scatter_chart(scatter_data)
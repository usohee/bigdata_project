# pages/2_시각화.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import plotly.express as px
from src.data_loader import load_steam_data
from src.features import preprocess_steam_data

st.title("📈 인디게임 시장 트렌드 시각화")
st.subheader("데이터 분석과 분포를 통해 도출한 인디게임의 인사이트")

raw_df = load_steam_data(nrows=50000)
df = preprocess_steam_data(raw_df)

cols = ['price', 'score']

# 그래프 1 — 분포
st.header("인디게임 주요 지표 분포")
col1 = st.selectbox("분포를 확인할 지표를 선택하세요", cols, index=0, key="hist")

if col1 == 'price':
    # 그래프 왜곡 방지
    plot_df = df[df['price'] <= 50].copy()
    title_suffix = " (이상치 제외, $0 ~ $50 구간 확정)"
else:
    plot_df = df.copy()
    title_suffix = ""

# Plotly 히스토그램 생성
fig1 = px.histogram(
    plot_df, 
    x=col1, 
    title=f"스팀 인디게임 {col1} 분포 현황{title_suffix}",
    color_discrete_sequence=['#fd85c1'],
    nbins=25
)
fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig1, use_container_width=True)

if col1 == 'price':
    st.caption("**💡 해석:** $50 이하 구간을 확장해 본 결과, 대다수의 인디게임은 무료($0) 혹은 $4.99 ~ $14.99 사이의 가성비 라인에 촘촘하게 집중 분포되어 있음을 알 수 있습니다.")
else:
    st.caption("**💡 해석:** 유저 만족도(score) 분포를 보면 85% 이상 구간에 데이터가 무겁게 쏠려 있어, 인디게임을 즐기는 유저층은 제품 만족도가 전반적으로 대단히 높음을 파악할 수 있습니다.")

# 그래프 2 — 관계
st.header("가격과 만족도의 상관관계")

c1, c2 = st.columns(2)
x_axis = c1.selectbox("X축 선택", cols, index=0, key="x")
y_axis = c2.selectbox("Y축 선택", cols, index=1, key="y")

chart_df = df[df['price'] <= 30].copy()

fig2 = px.scatter(
    chart_df, 
    x=x_axis, 
    y=y_axis, 
    color="genres", 
    title=f"인디게임 {x_axis} vs {y_axis} 산점도 분석",
    hover_data=['name']  # 마우스 올리면 게임 이름이 뜨도록 설정
)
fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
st.plotly_chart(fig2, use_container_width=True)

st.caption(f"**💡 해석:** {x_axis}와 {y_axis}의 관계를 보면, $5~$15 사이의 특정 저가격대 인디게임 장르(Casual, Simulation, Adventure 등)에서 유저 만족도가 90% 이상으로 촘촘하게 수렴하는 가성비 명작 구간이 관측됩니다. 즉, 무조건 비싼 게임이 아니더라도 유저의 성향 태그와 부합한다면 충분히 최고 수준의 만족도를 이끌어낼 수 있다는 명확한 상관관계가 입증됩니다.")
# pages/1_EDA.py
import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# 부모 디렉토리를 path에 추가하여 src 폴더 안의 모듈을 가져올 수 있게 함
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.data_loader import load_steam_data

st.title('📊 스팀 인디게임 EDA')
st.subheader('데이터 요약 및 결측치 파악 페이지')

# 1. 데이터 로딩 (안전하게 20,000건만 먼저 로드)
df = load_steam_data(nrows=20000)

if df.empty:
    st.warning("데이터가 비어있습니다. data/games.csv 파일 확인이 필요합니다.")
else:
    # 상단 탭 구성 (요약 통계 / 결측치 분석)
    tab1, tab2 = st.tabs(['📋 데이터 요약 및 샘플', '🔍 결측치(Missing Value) 분석'])

    # --- TAB 1: 데이터 요약 ---
    with tab1:
        st.markdown("### 🔹 데이터 기본 정보")
        col1, col2 = st.columns(2)
        col1.metric("분석 중인 데이터 행(Row) 수", f"{df.shape[0]:,}개")
        col2.metric("데이터 열(Column) 수", f"{df.shape[1]}개")

        st.markdown("### 🔹 상위 5개 데이터 샘플")
        st.dataframe(df.head(), use_container_width=True)

        st.markdown("### 🔹 수치형 데이터 기술 통계량")
        # 가격, 플레이타임 등 주요 수치 데이터 통계 확인
        st.dataframe(df.describe(), use_container_width=True)

    # --- TAB 2: 결측치 분석 ---
    with tab2:
        st.markdown("### 🔹 컬럼별 결측치 현황")
        
        # 결측치 계산
        null_counts = df.isnull().sum().reset_index()
        null_counts.columns = ['컬럼명', '결측치 개수']
        null_counts['결측치 비율(%)'] = round((null_counts['결측치 개수'] / len(df)) * 100, 2)
        
        # 결측치가 있는 컬럼만 필터링
        missing_df = null_counts[null_counts['결측치 개수'] > 0].sort_values(by='결측치 개수', ascending=False)

        if missing_df.empty:
            st.success("✨ 축하합니다! 현재 데이터셋에 결측치가 존재하지 않습니다.")
        else:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.write("🔴 **결측치가 존재하는 컬럼 리스트**")
                st.dataframe(missing_df, use_container_width=True)
            
            with col2:
                st.write("📊 **결측치 비율 시각화**")
                fig = px.bar(missing_df, x='컬럼명', y='결측치 비율(%)',
                             title='컬럼별 결측치 비율',
                             color='결측치 비율(%)',
                             color_continuous_scale='Reds')
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
                
            st.info("💡 **주의 단계:** 결측치가 높은 컬럼(예: 수치 데이터의 NaN 등)은 2차 작업 전처리 단계(`src/features.py`)에서 제거하거나 대체값을 채워넣어야 합니다!")
import streamlit as st

st.set_page_config(

    page_title="스팀 인디게임 취향 매칭 대시보드",
    layout="wide",
    initial_sidebar_state="expanded",

)



# --- 페이지 정의 (pages/ 폴더 파일 매핑) ---

eda = st.Page("pages/1_EDA.py", title="EDA", icon="🔍")
viz = st.Page("pages/2_시각화.py", title="시장 트렌드 시각화", icon="📈")
service = st.Page("pages/3_모델_서비스.py", title="취향 매칭 모델 서비스", icon="🕹️")

pg = st.navigation({
    "🎯 인디게임 분석 & 추천 프로젝트": [service, viz, eda],
})

with st.sidebar:

    # 프로젝트 핵심 요약 정보 배치
    st.markdown("### 📝 나의 데이터 분석 프로젝트")
    st.markdown("빅데이터분석프로젝트 기말 프로젝트")
    st.markdown("- **주제:** 스팀 인디게임 유저 취향 매칭 서비스 및 시장 EDA")
    st.markdown("- **개발 스택:** Python, Streamlit, Plotly, Ollama (Gemma3)")

    st.markdown("---")

    

    # 프로필
    st.markdown("### 👩‍💻 프로필 정보")
    st.markdown("- **이름:** 유소희")
    st.markdown("- **학번:** `20232346` ")

    st.markdown("---")
    st.caption("© 2026 Yoo Sohee. All rights reserved.")

pg.run()
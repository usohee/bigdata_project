# pages/3_모델_서비스.py
import streamlit as st
import pandas as pd
import sys
import os
import ollama

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.data_loader import load_steam_data
from src.features import preprocess_steam_data

st.title('⚖️ AI 취향 매칭 추천')
st.subheader('당신의 성향을 분석해 숨겨진 명작 인디게임을 추천합니다.')

raw_df = load_steam_data(nrows=50000)
df = preprocess_steam_data(raw_df)

st.markdown("### 🎮 밸런스 게임: 당신의 게임 취향은?")

q1 = st.radio(
    "1. 게임할 때 가장 눈과 마음이 즐거운 요소는?",
    [
        "📖 깊이 있는 서사와 감동 (Story Rich / Narrative)",
        "🎨 아기자기하고 정교한 2D 픽셀 도트 그래픽 (Pixel Art)",
        "🎵 영화 같은 몰입감을 주는 환상적인 배경과 사운드 (Atmospheric / Soundtrack)",
        "⚔️ 화끈하고 빠른 액션과 타격감 (Action / Hack and Slash)",
        "🧩 차근차근 풀어나가는 전략과 퍼즐 (Strategy / Puzzle)"
    ]
)

q2 = st.radio(
    "2. 오늘 당신의 정신 상태에 맞는 난이도는?",
    [
        "☕ 힐링하는 극강의 순한맛 (Cozy / Relaxing / Cute)",
        "🎲 매판 새로운 맵과 영구 죽음! 스릴 넘치는 로그라이크 (Roguelike / Roguelite)",
        "🧠 세밀한 컨트롤과 패배의 쓴맛을 즐기는 하드코어 Souls-like (Difficult / Souls-like)",
        "🤝 전 세계 유저와 함께 즐기는 멀티 플레이 (Multiplayer / Co-op)",
        "🌍 정답 없는 드넓은 세상을 자유롭게 유랑하는 오픈월드 탐험 (Open World / Exploration)"
    ]
)

price_limit = st.slider("💵 최대 허용 가격 (USD)", 0.0, 60.0, 20.0)

if st.button("✨ 내 취향의 인디게임 찾아보기", use_container_width=True):
    # 가격 필터링
    filtered_df = df[df['price'] <= price_limit].copy()
    
    if filtered_df.empty:
        st.warning("설정하신 가격대 조건에 맞는 게임이 없습니다. 슬라이더를 조절해 보세요!")
    else:
        filtered_df['match_score'] = 0
        
        # Q1 선택지별 태그/장르 기반 매칭 가중치 연산
        if "소설" in q1:
            filtered_df['match_score'] += filtered_df['tags'].str.contains('Story Rich|Visual Novel|Narrative', case=False, na=False).astype(int) * 5
        elif "픽셀" in q1:
            filtered_df['match_score'] += filtered_df['tags'].str.contains('Pixel Art|Retro|2D', case=False, na=False).astype(int) * 5
        elif "영화" in q1:
            filtered_df['match_score'] += filtered_df['tags'].str.contains('Atmospheric|Soundtrack', case=False, na=False).astype(int) * 5
        elif "액션" in q1:
            filtered_df['match_score'] += filtered_df['tags'].str.contains('Action|Hack and Slash|Fast-Paced', case=False, na=False).astype(int) * 5
        elif "머리" in q1:
            filtered_df['match_score'] += filtered_df['tags'].str.contains('Strategy|Puzzle|Tactical', case=False, na=False).astype(int) * 5
            
        # Q2 선택지별 태그/장르 기반 매칭 가중치 연산
        if "힐링" in q2:
            filtered_df['match_score'] += filtered_df['tags'].str.contains('Casual|Relaxing|Cozy|Cute|Wholesome', case=False, na=False).astype(int) * 5
        elif "로그라이크" in q2:
            filtered_df['match_score'] += filtered_df['tags'].str.contains('Roguelike|Roguelite|Procedural Generation', case=False, na=False).astype(int) * 5
        elif "Souls-like" in q2:
            filtered_df['match_score'] += filtered_df['tags'].str.contains('Difficult|Souls-like|Hard|Permadeath', case=False, na=False).astype(int) * 5
        elif "멀티" in q2:
            filtered_df['match_score'] += filtered_df['tags'].str.contains('Multiplayer|Co-op', case=False, na=False).astype(int) * 5
        elif "오픈월드" in q2:
            filtered_df['match_score'] += filtered_df['tags'].str.contains('Open World|Exploration|Adventure', case=False, na=False).astype(int) * 5

        # 매칭 점수, 평점 기준 정렬 후 상위 3개 추천
        recommendations = filtered_df.sort_values(by=['match_score', 'score'], ascending=False).head(3)
        
        st.divider()
        st.markdown("### 🃏 소희님이 선택한 취향 저격 인디게임 TOP 3")
        
        for idx, row in recommendations.iterrows():
            with st.container(border=True):
                st.markdown(f"## 🎯 {row['name']}")
                
                # 인디게임 메타데이터 배지 UI 구성
                p_text = "FREE" if row['price'] == 0 else f"${row['price']:.2f}"
                st.markdown(f"`💵 가격: {p_text}`  `👍 유저 만족도: {row['score']:.1f}%`  `🎮 장르: {row['genres']}`")
                
                st.markdown(f"**📝 게임 소개**\n{row['short_description']}")
                st.caption(f"**🏷️ 연관 태그:** {row['tags']}")
                
                st.markdown("---")
                st.markdown("🤖 **AI 도슨트의 취향 저격 서평**")
                
                llm_prompt = f"""
                너는 친절하고 위트 있는 게임 전문 도슨트야.
                유저가 선택한 취향 필터({q1}, {q2})와 매칭된 게임 정보들을 바탕으로, 
                왜 이 게임이 이 유저에게 완벽히 어울리는지 친근한 어조로 딱 2줄 요약해서 한줄평을 써줘.
                
                [게임 정보]
                - 게임 이름: {row['name']}
                - 설명: {row['short_description']}
                - 장르: {row['genres']}
                """
                
                try:
                    with st.spinner("AI 도슨트가 한줄평을 작성하는 중..."):
                        res = ollama.chat(
                            model="gemma3:4b",
                            messages=[{"role": "user", "content": llm_prompt}]
                        )
                        st.info(res["message"]["content"])
                except Exception as e:
                    st.caption("⚠️ 로컬 Ollama 모델을 불러올 수 없어 기본 매칭 알고리즘 결과만 표시합니다.")
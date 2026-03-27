import streamlit as st

st.set_page_config(page_title="단계별 입력", page_icon="📝")
st.title('📝 단계별 정보 입력')

# ---- 상태 초기화 ----
if 'step' not in st.session_state:
    st.session_state.step = 1

# ---- 진행률 표시 ----
progress = st.session_state.step / 3
st.progress(progress, text=f'Step {st.session_state.step} / 3')

# ---- Step 1: 기본 정보 ----
if st.session_state.step == 1:
    st.subheader('Step 1: 기본 정보')
    name = st.text_input('이름', key='name_input') # key 중복 방지
    age = st.number_input('나이', min_value=1, max_value=100, value=20, key='age_input')
    
    if st.button('다음 →'):
        if name:
            # 다음 단계로 넘어가기 전 데이터를 저장
            st.session_state.saved_name = name
            st.session_state.saved_age = age
            st.session_state.step = 2
            st.rerun()
        else:
            st.warning('이름을 입력해주세요.')

# ---- Step 2: 관심 분야 ----
elif st.session_state.step == 2:
    st.subheader('Step 2: 관심 분야')
    interests = st.multiselect(
        '관심 분야를 선택하세요',
        ['데이터 분석', '웹 개발', 'AI/ML', '모바일', '게임', '보안'],
        key='interests_input'
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button('← 이전'):
            st.session_state.step = 1
            st.rerun() # 버튼을 눌렀을 때만 리런해야 합니다!
            
    with col2:
        if st.button('다음 →'):
            st.session_state.saved_interests = interests
            st.session_state.step = 3
            st.rerun()

# ---- Step 3: 확인 ----
elif st.session_state.step == 3:
    st.subheader('Step 3: 입력 확인')
    # 저장된 데이터를 안전하게 가져옴 (get 사용)
    st.write(f"**이름**: {st.session_state.get('saved_name', '미입력')}")
    st.write(f"**나이**: {st.session_state.get('saved_age', '미입력')}")
    interests_list = st.session_state.get('saved_interests', [])
    st.write(f"**관심 분야**: {', '.join(interests_list) if interests_list else '없음'}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button('← 이전'):
            st.session_state.step = 2
            st.rerun()
            
    with col2:
        if st.button('✅ 제출'):
            st.balloons()
            st.success('제출이 완료되었습니다!')
            # 초기화 (사용자 편의를 위해 버튼 클릭 시에만 삭제)
            for key in ['step', 'saved_name', 'saved_age', 'saved_interests']:
                if key in st.session_state:
                    del st.session_state[key]
            # 다시 1단계로 가고 싶다면 아래 주석 해제
            # st.rerun()
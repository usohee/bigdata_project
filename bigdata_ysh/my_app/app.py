import streamlit as st

home = st.Page("Home.py", title="홈", icon="🏠", default=True)
chart = st.Page("pages/1_📈_차트_데모.py", title="차트", icon="📈")
map = st.Page("pages/2_🌍_지도_데모.py", title="지도", icon="🌍")
data = st.Page("pages/3_📊_데이터_데모.py", title="데이터", icon="📊")


pg = st.navigation([home, chart, map, data])
pg.run()
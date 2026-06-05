import pandas as pd

def preprocess_steam_data(df):
    """
    보정된 DataFrame을 받아 인디게임만 깔끔하게 필터링하는 함수
    """
    if df.empty:
        return df
        
    # 인디 게임만 필터링
    df = df.dropna(subset=['genres']).copy()
    df = df[df['genres'].str.contains('Indie', case=False)].copy()
    
    return df
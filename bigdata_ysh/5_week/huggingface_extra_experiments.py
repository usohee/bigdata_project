# 추가 실험 1: 긴 문장도 분석 가능한가?
long_text = "Despite some minor flaws in the beginning, the movie gradually became more interesting and by the end I was completely captivated by the story."
result = classifier(long_text)
print(result) # → 전체 문맥을 고려하여 판단
# 추가 실험 2: 빈 문자열은?
result = classifier("") # → 에러 또는 낮은 확신도
# 추가 실험 3: 숫자만 넣으면?
result = classifier("12345") # → 의미 없는 결과

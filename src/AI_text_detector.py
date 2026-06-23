# app.py (Main Streamlit Application)
# =================================================================
# 🛡️ [STAGE 1] GLOBAL MASTER TRACKER INITIALIZATION (최상단 고정)
# =================================================================
# 파이썬 엔진이 스트림릿을 구우러 들어가기 전에 문지기부터 완벽하게 세웁니다.
from tracker_hub import log_app_usage

# 앱이 켜지는 순간 최초 1회만 트래킹 데이터 적재
log_app_usage("ai_detector_web", "app_opened")

# =================================================================
# 🎨 [STAGE 2] CORE FRAMEWORKS & UI LIBRARIES
# =================================================================
import streamlit as st
import numpy as np

# 1. 먼저 글을 저장할 공간(변수)이 세션에 없으면 빈 값으로 만들어 줍니다.
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = ""

# 1. AI-specific cliched keyword list
AI_CLICHE_KEYWORDS = ['첫째로', '결론적으로', '다각도로', '궁극적으로', '명확한', '매끄러운']

def analyze_text(text):
    """
    Analyzes text to calculate Burstiness and AI keyword density.
    """
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    if not sentences:
        return 0, 0, 0

    # Calculate Burstiness (Standard deviation of sentence lengths)
    sentence_lengths = [len(s) for s in sentences]
    burstiness = float(np.std(sentence_lengths))  # Human has higher variation

    # Calculate AI Cliche Density
    cliche_count = sum(1 for word in AI_CLICHE_KEYWORDS if word in text)
    
    # Calculate Temporary AI Suspicion Index (Simple Heuristic)
    # Higher cliche count and lower burstiness = Higher AI probability
    ai_index = min(100, int((cliche_count * 20) + max(0, (30 - burstiness) * 2)))
    
    return burstiness, cliche_count, ai_index

# --- Streamlit UI Layout ---
st.title("🕵️ 요즘 AI가 쓴 글, 진짜 구별할 수 있을까?")
st.caption("텍스트의 패턴과 가변성(Burstiness)을 분석합니다.")

user_input = st.text_area("분석할 텍스트를 입력하세요:", height=200)

if st.button("패턴 분석 시작"):
    print("--- [디버그] 버튼 클릭 감지됨 ---")
    st.write("버튼 클릭 확인!") # 👈 웹 화면에 강제로 글자를 띄워봅니다.
    if user_input.strip():
        burstiness, cliches, ai_index = analyze_text(user_input)
        
        # 🚨 여기에 print 문을 하나 더 넣어서 확인합니다!
        print("🔍 버튼이 눌렸고, 트래커 함수를 호출합니다.")
        
        log_app_usage(
            app_name="ai_detector_web",
            action="click_analyze_button",
            details={
                "input_length": len(user_input),
                "calculated_burstiness": burstiness,
                "detected_cliches": cliches,
                "ai_suspicion_index": ai_index,
                "detected_keywords": [word for word in AI_CLICHE_KEYWORDS if word in user_input]
            }
        )

        # 💡 [수정] 세션 상태에 결과 데이터들을 딕셔너리나 객체로 통째로 저장
        st.session_state.analysis_result = {
            "ai_index": ai_index,
            "burstiness": burstiness,
            "cliches": cliches,
            "detected_keywords": [w for w in AI_CLICHE_KEYWORDS if w in user_input]
        }
    else:
        st.warning("텍스트를 입력해 주세요.")

# --- 💡 [수정] 화면 출력 로직을 버튼 바깥으로 완전히 분리 ---
if st.session_state.analysis_result:
    res = st.session_state.analysis_result  # 세션에서 데이터 꺼내기
    
    st.write("🔍 패턴 분석을 완료했습니다. 결과는 다음과 같습니다...")
    st.subheader("📊 분석 결과")
    st.metric(label="AI 의심 지수", value=f"{res['ai_index']} %")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="문장 길이 가변성 (Burstiness)", value=f"{res['burstiness']:.2f}")
        st.caption("인간의 글은 가변성 점수가 높은 편입니다.")
    with col2:
        st.metric(label="AI 상투어 감지", value=f"{res['cliches']} 개")
        st.caption(f"감지된 키워드: {res['detected_keywords']}")
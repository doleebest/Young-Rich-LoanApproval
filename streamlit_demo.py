import os
from dotenv import load_dotenv
import streamlit as st
from datetime import datetime
from chatbot_logic import initialize_conversation, initialize_pinecone

# .env 파일에서 환경 변수 로드
load_dotenv()

# 앱 로드 시 캐시 삭제
st.cache_data.clear()

# 필요한 환경 변수 불러오기
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Streamlit 설정
st.set_page_config(page_title="FinanceChat", page_icon=":books:", layout="centered")
st.title("💳 **Card Chatbot**")
st.divider()

# 사이드바에 디버그 모드 설정 추가
st.sidebar.title("Settings")
st.sidebar.subheader("옵션")
st.sidebar.checkbox("참조된 문서 확인하기", key="show_docs")

# 모델 로딩 진행 상황 표시
with st.spinner("모델을 로딩 중입니다... 잠시만 기다려 주세요."):
    # Pinecone 설정 및 초기화
    if 'vectorstore' not in st.session_state:
        st.session_state.vectorstore = initialize_pinecone()

    # 대화 초기화
    if 'conversation' not in st.session_state:
        st.session_state.conversation = initialize_conversation(st.session_state.vectorstore)

# 대화 기록 초기화
if 'messages' not in st.session_state:
    st.session_state['messages'] = [{'role': 'assistant', 'content': "안녕하세요! 무엇이 궁금하신가요?", 'timestamp': datetime.now().strftime('%p %I:%M')}]

# 메시지 표시 함수
def display_message(role, content, timestamp):
    alignment = 'flex-end' if role == "user" else 'flex-start'
    bg_color = '#FFEB3B' if role == "user" else '#E1E1E1'
    text_align = 'right' if role == "user" else 'left'
    label = "🙋 User" if role == "user" else "🤖 Assistant"
    timestamp_position = 'left: -60px;' if role == "user" else 'right: -60px;'

    return f"""
        <div style='display: flex; justify-content: {alignment}; margin-bottom: 10px;'>
            <div style='max-width: 60%; position: relative;'>
                <div style='text-align: {text_align}; color: #888;'>{label}</div>
                <div style='background-color: {bg_color}; padding: 10px; border-radius: 10px; color: black; border: 1px solid #C0C0C0;'>
                    {content}
                </div>
                <div style='font-size: 0.8em; color: #555; position: absolute; {timestamp_position} bottom: 0; margin: 0 5px;'>{timestamp}</div>
            </div>
        </div>
    """

# 이전 대화 기록 표시
chat_container = st.container()
with chat_container:
    for message in st.session_state['messages']:
        st.markdown(display_message(message['role'], message['content'], message['timestamp']), unsafe_allow_html=True)

# 사용자 입력 받기
input_container = st.container()

def send_message():
    user_input = st.session_state.get('user_input', '')

    # 사용자 입력을 문자열로 변환
    user_input = str(user_input) if user_input else ''

    if user_input:
        timestamp = datetime.now().strftime('%p %I:%M')
        st.session_state['messages'].append({"role": "user", "content": user_input, "timestamp": timestamp})

        with chat_container:
            st.markdown(display_message("user", user_input, timestamp), unsafe_allow_html=True)

        with input_container:
            with st.spinner("답변 생성 중..."):
                # 대화 입력 데이터를 구성합니다.
                input_data = {
                    "input": user_input  # 올바른 문자열 형식으로 입력
                }

                # 구성 가능한 설정을 추가합니다.
                config = {
                    "configurable": {"session_id": "session123"}  # 예시 세션 ID 사용
                }

                try:
                    # invoke 호출
                    result = st.session_state.conversation.invoke(input_data, config)

                    # LLM의 응답 추출 (마크다운 지원)
                    full_response = result.get("answer", "죄송합니다. 답변을 생성할 수 없습니다.")
                    response_timestamp = datetime.now().strftime('%p %I:%M')
                    st.session_state['messages'].append({"role": "assistant", "content": full_response, "timestamp": response_timestamp})

                    # 봇의 응답을 출력
                    with chat_container:
                        st.markdown(display_message("assistant", full_response, response_timestamp), unsafe_allow_html=True)

                    if st.session_state.show_docs and result.get("context"):
                        with st.expander("🔍 참조된 문서들"):
                            for idx, doc in enumerate(result["context"]):
                                st.markdown(
                                    f"""
                                    <div style='padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin-bottom: 10px;'>
                                        <strong>📄 문서 {idx + 1}</strong><br>
                                        <strong>카드 이름:</strong> {doc.metadata.get('card_name', 'N/A')}<br>
                                        <strong>회사:</strong> {doc.metadata.get('company', 'N/A')}<br>
                                        <strong>혜택:</strong> {doc.metadata.get('benefit', 'N/A')}<br>
                                        <strong>내용:</strong> {doc.page_content}
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )

                except Exception as e:
                    st.error(f"오류 발생: {e}")

        # 입력 필드 초기화
        st.session_state.pop('user_input', None)  # 직접적으로 세션 상태에서 키를 제거하여 초기화

# 사용자 입력 필드 (엔터 키로 전송)
user_input = st.text_input(
    "💬 질문을 입력해주세요:",
    placeholder="카드 혜택을 알고 싶으신가요? 여기에 질문을 입력하세요...",
    key="user_input",
    on_change=send_message  # 입력이 변경될 때마다 send_message 함수 호출
)

# 스타일 추가 (기본 스타일 유지, 심플하게)
st.markdown(
    """
    <style>
    .stTextInput, .stAlert {
        border-radius: 10px;
        margin-left: 20px;
    }
    .css-1gkdjib.e1yohnl3 {
        height: 70vh;
        overflow-y: auto;
    }
    .css-1gkdjib.e1yohnl3 > div {
        margin-bottom: 10px;
    }
    .css-145kmo2.e1ewe7hr3 {
        margin-top: auto;
    }
    .stTextInput {
        width: 100%;
        height: 38px;
        margin: 0;
        border-radius: 8px;
        align-items: center;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

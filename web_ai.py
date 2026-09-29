# -*- coding: utf-8 -*-
import streamlit as st
from google import genai

# 1. Cấu hình giao diện trang Web (Đặt tên tab và icon)
st.set_page_config(page_title="Trợ lý AI Đa Năng", page_icon="🤖", layout="centered")

# Tiêu đề chính hiển thị trên trang web
st.title("🤖 Trợ Lý AI Của Bạn")
st.caption("🚀 Được cấp nguồn bởi Google Gemini 3.8 Flash - Giải mọi câu hỏi")

# 2. ĐIỀN API KEY CỦA BẠN VÀO ĐÂY
API_KEY = st.secrets["GEMINI_API_KEY"]

# Khởi tạo AI Client
try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error(f"Lỗi khởi tạo cấu hình: {e}")

# 3. Tạo bộ nhớ lịch sử chat (để AI nhớ được nội dung đã nói ở trên)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị các tin nhắn cũ ra màn hình nếu có
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Ô nhập liệu câu hỏi giống ChatGPT (Nằm ở dưới cùng màn hình)
if user_query := st.chat_input("Nhập câu hỏi của bạn vào đây (Toán, Văn, Code...)..."):
    
    # Hiển thị câu hỏi của bạn lên màn hình web
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Gửi câu hỏi sang cho AI xử lý
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("AI đang suy nghĩ..."):
            try:
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=user_query,
                )
                ai_response = response.text
                # Hiển thị câu trả lời dạng văn bản đẹp mắt
                message_placeholder.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"Đã xảy ra lỗi khi gọi AI: {e}")

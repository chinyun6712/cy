import streamlit as st
import google.generativeai as genai

# 1. 页面设置
st.set_page_config(page_title="我的 AI 助手")
st.title("🤖 欢迎体验我的 AI 作品")

# 2. 获取 API Key (从 Streamlit Secrets 获取，为了安全)
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("请在 Streamlit 后台设置 GOOGLE_API_KEY")
    st.stop()

# 3. 配置 Gemini (这里是关键，你可以根据你在 AI Studio 的设置调整)
genai.configure(api_key=api_key)

# --- 如果你在 AI Studio 有特殊的 system instruction，可以在这里修改 ---
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
}

# 使用的模型名称，通常是 gemini-1.5-flash 或 gemini-1.5-pro
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # system_instruction="你是一个专业的翻译助手...", # 如果有设定角色，把这行注释取消并填入
)
# -------------------------------------------------------------

# 4. 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. 处理用户输入
if prompt := st.chat_input("请输入你的问题..."):
    # 显示用户的话
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 调用 Gemini
    try:
        # 这里把历史记录发给 AI，让它有记忆
        chat = model.start_chat(history=[
            {"role": m["role"], "parts": [m["content"]]} 
            for m in st.session_state.messages[:-1] # 排除最新的一条，因为下面马上要发
        ])
        
        response = chat.send_message(prompt)
        
        # 显示 AI 的回复
        with st.chat_message("model"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "model", "content": response.text})
        
    except Exception as e:
        st.error(f"发生错误: {e}")

from openai import OpenAI
import streamlit as st


with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

st.title("🖌️ DALL·E")

if "image_urls" not in st.session_state:
    st.session_state["image_urls"] = []

quality = st.radio(
    '图片质量',
    ('标准', '高清'),
    index=0,
    horizontal=True,
)

QUALITY_TO_OPTION = {
    '标准': 'standard',
    '高清': 'hd',
}

style = st.radio(
    '图片风格',
    ('生动', '自然'),
    index=0,
    horizontal=True,
)

STYLE_TO_OPTION = {
    '生动': 'vivid',
    '自然': 'natural',
}

AVAILABLE_SIZES = {
    '1024x1024',
    '1024×1792',
    '1792x1024',
}

size = st.selectbox(
    '分辨率',
    AVAILABLE_SIZES,
)

for image_url, user_prompt in st.session_state.image_urls:
    st.image(image_url, caption=user_prompt)

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    
    client = OpenAI(api_key=openai_api_key)

    with st.spinner("生成中...💫"):
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality=QUALITY_TO_OPTION[quality],
            style=STYLE_TO_OPTION[style],
            n=1,
        )

    image_url = response.data[0].url
    st.image(image_url, caption=prompt)
    st.session_state.image_urls.append((image_url, prompt))

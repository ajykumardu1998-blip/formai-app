import streamlit as st
import os
import json
from PIL import Image
from openai import OpenAI
from streamlit_mic_recorder import mic_recorder

st.set_page_config(page_title="FormAI by Ajay", page_icon="🚀", layout="wide")

st.title("🚀 FormAI by Ajay")
st.caption("👨‍💻 Developed by **Ajay Kumar** | Autonomous Voice & Form Agent")
st.markdown("---")

os.makedirs("uploads", exist_ok=True)
os.makedirs("processed", exist_ok=True)

with st.sidebar:
    st.header("⚙️ क्रेडेंशियल्स")
    api_key = st.text_input("OpenRouter API Key दर्ज करें:", type="password")
    st.markdown("---")
    
    st.header("📞 कस्टमर सपोर्ट")
    st.markdown("👤 **फाउंडर:** अजय कुमार (Ajay Kumar)")
    st.markdown("📱 **मोबाइल:** [+91-8920798182](tel:8920798182)")
    
    whatsapp_link = "https://wa.me/918920798182?text=नमस्ते%20अजय%20जी,%20मुझे%20FormAI%20में%20मदद%20चाहिए।"
    st.markdown(f'<a href="{whatsapp_link}" target="_blank"><button style="width: 100%; background-color: #25D366; color: white; border: none; padding: 8px 16px; border-radius: 6px; font-weight: bold; cursor: pointer;">💬 WhatsApp पर सहायता पाएं</button></a>', unsafe_allow_html=True)
    st.markdown("---")

if not api_key:
    st.info("👋 नमस्ते अजय जी! शुरू करने के लिए कृपया साइडबार में अपनी OpenRouter API Key पेस्ट करें।")
    st.stop()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def smart_resize(input_path, output_path, target_max_kb):
    img = Image.open(input_path).convert('RGB')
    quality = 95
    while quality > 15:
        img.save(output_path, "JPEG", quality=quality, optimize=True)
        if (os.path.getsize(output_path) / 1024) <= target_max_kb:
            break
        quality -= 5
    return output_path

tab_form, tab_help = st.tabs(["📝 फॉर्म फिलिंग (FormAI)", "💬 24x7 हेल्प डेस्क (Instant AI Support)"])

with tab_form:
    st.subheader("1. कौन सा फॉर्म भरना है?")
    c1, c2 = st.columns([1, 2])

    with c1:
        st.write("बोलकर बताएं:")
        voice_input = mic_recorder(start_prompt="🔴 माइक चालू करें", stop_prompt="⏹️ बंद करें", key='recorder')

    with c2:
        typed_input = st.text_input("या फॉर्म का नाम टाइप करें (जैसे: GDS, Railway, SSC):")

    form_query = typed_input

    if form_query:
        if "doc_requirements" not in st.session_state or st.session_state.get("current_form") != form_query:
            with st.spinner("AI नियम और आवश्यक डॉक्यूमेंट्स चेक कर रहा है..."):
                prompt = f"""
                यूज़र यह फॉर्म भरना चाहता है: "{form_query}"
                इस फॉर्म के लिए अनिवार्य डॉक्यूमेंट्स और फोटो साइज नियम बताएं।
                केवल शुद्ध JSON लौटाएं:
                {{
                    "form_title": "फॉर्म का नाम",
                    "docs_list": ["डॉक्यूमेंट 1", "डॉक्यूमेंट 2", "पासपोर्ट फोटो", "सिग्नेचर"],
                    "photo_kb": 50,
                    "sign_kb": 20
                }}
                """
                completion = client.chat.completions.create(
                    model="google/gemini-2.0-flash-exp:free",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )
                st.session_state["doc_requirements"] = json.loads(completion.choices[0].message.content)
                st.session_state["current_form"] = form_query

        rules = st.session_state["doc_requirements"]
        st.success(f"📋 **{rules['form_title']}** के लिए आवश्यक सूची:")
        for item in rules["docs_list"]:
            st.write(f"- 📄 {item}")

        st.markdown("---")
        st.subheader("2. मांगे गए डॉक्यूमेंट्स अपलोड करें")
        uploaded_files = st.file_uploader("सभी फोटो व डॉक्यूमेंट्स चुनें:", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

        if uploaded_files:
            st.write(f"📁 कुल {len(uploaded_files)} फाइलें अपलोड हुईं।")
            if st.button("⚡ FormAI by Ajay: फॉर्म प्रोसेस करें"):
                with st.status("FormAI एजेंट पूरी प्रक्रिया चला रहा है...", expanded=True) as status:
                    saved_paths = []
                    for f in uploaded_files:
                        path = os.path.join("uploads", f.name)
                        with open(path, "wb") as buffer:
                            buffer.write(f.getbuffer())
                        saved_paths.append(path)

                    st.write("📐 फोटो और साइन ऑटो-रीसाइज़ हो रहे हैं...")
                    for p in saved_paths:
                        name_l = p.lower()
                        if "photo" in name_l or "pic" in name_l:
                            smart_resize(p, "processed/photo_ready.jpg", rules.get('photo_kb', 50))
                        elif "sign" in name_l:
                            smart_resize(p, "processed/sign_ready.jpg", rules.get('sign_kb', 20))

                    status.update(label="🎉 डॉक्यूमेंट्स सफलतापूर्वक तैयार हो गए!", state="complete")

with tab_help:
    st.subheader("💬 लाइव हेल्प डेस्क & सपोर्ट")
    if "help_messages" not in st.session_state:
        st.session_state.help_messages = [
            {"role": "assistant", "content": "नमस्ते! मैं **FormAI by Ajay** का आधिकारिक सपोर्ट असिस्टेंट हूँ। Ajay Kumar जी से सीधे संपर्क के लिए 8920798182 पर संपर्क कर सकते हैं।"}
        ]

    for msg in st.session_state.help_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_help_msg := st.chat_input("अपनी समस्या यहाँ लिखें..."):
        st.session_state.help_messages.append({"role": "user", "content": user_help_msg})
        with st.chat_message("user"):
            st.markdown(user_help_msg)

        with st.chat_message("assistant"):
            sys_msg = "आप FormAI by Ajay (फाउंडर: Ajay Kumar, मोबाइल: 8920798182) के AI सपोर्ट हैं। यूज़र को विनम्रता से हिंदी में हल बताएं।"
            res = client.chat.completions.create(
                model="google/gemini-2.0-flash-exp:free",
                messages=[
                    {"role": "system", "content": sys_msg},
                    {"role": "user", "content": user_help_msg}
                ]
            )
            reply = res.choices[0].message.content
            st.markdown(reply)
            st.session_state.help_messages.append({"role": "assistant", "content": reply})

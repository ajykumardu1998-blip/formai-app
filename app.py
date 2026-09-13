import streamlit as st
import os
import json
import io
import zipfile
from PIL import Image
from openai import OpenAI
from streamlit_mic_recorder import mic_recorder

st.set_page_config(page_title="ऑनलाइन अजय डॉक्यूमेंटेशन | FormAI", page_icon="🚀", layout="wide")

# 1. 24x7 रनिंग अलर्ट पट्टी: नए सरकारी फॉर्म, गाइडलाइन और हेल्पलाइन
st.markdown("""
<div style="
    background: linear-gradient(90deg, #120000, #3d0000, #120000);
    padding: 10px 0;
    border-top: 2px solid #ff3333;
    border-bottom: 2px solid #ffcc00;
    box-shadow: 0 4px 14px rgba(255, 0, 0, 0.35);
    margin-bottom: 20px;
    border-radius: 8px;
    overflow: hidden;
">
    <marquee behavior="scroll" direction="left" scrollamount="7" style="color: #ffffff; font-size: 16px; font-weight: 700;">
        🔥 <span style="background-color: #e60000; color: #fff; padding: 2px 7px; border-radius: 4px; font-size: 12px; margin-right: 6px;">LATEST GOVT FORMS</span>
        📢 SSC GD कांस्टेबल, Railway RRB टेक्नीशियन, इंडिया पोस्ट GDS, दिल्ली DSSSB और आर्मी अग्निवीर के नए ऑनलाइन फॉर्म शुरू! 
        ⚠️ महत्वपूर्ण गाइडलाइन: फोटो 3 महीने से पुरानी न हो, बैकग्राउंड सफेद रखें, सिग्नेचर स्पष्ट होना चाहिए। 
        ⚡ हेल्पलाइन: +91-8920798182 (अजय कुमार) — 24 घंटे ऑनलाइन फॉर्म सुविधा उपलब्ध ⚡
    </marquee>
</div>
""", unsafe_allow_html=True)

st.title("🚀 FormAI by Ajay")
st.caption("👨‍💻 Founder: **Ajay Kumar** | 24/7 Autonomous Govt Form & Document Agent")
st.markdown("---")

os.makedirs("uploads", exist_ok=True)
os.makedirs("processed", exist_ok=True)

# आपकी असली वेरिफाइड UPI ID
REAL_UPI_ID = "paytm.s3qpm6x@pty"

# 2. साइडबार: क्रेडेंशियल्स, कस्टमर सपोर्ट और 100% ओरिजिनल QR पेमेंट
with st.sidebar:
    st.header("⚙️ क्रेडेंशियल्स")
    api_key = st.text_input("OpenRouter API Key दर्ज करें:", type="password")
    st.markdown("---")
    
    st.header("📞 24×7 सहायता केंद्र")
    st.markdown("👤 **संचालक:** अजय कुमार (Ajay Kumar)")
    st.markdown("📱 **मोबाइल:** [+91-8920798182](tel:8920798182)")
    st.markdown(f"💳 **UPI ID:** `{REAL_UPI_ID}`")
    
    whatsapp_link = "https://wa.me/918920798182?text=नमस्ते%20अजय%20जी,%20मैंने%20पेमेंट%20कर%20दी%20है,%20कृपया%20मेरा%20फॉर्म%20चेक%20करें।"
    st.markdown(f'<a href="{whatsapp_link}" target="_blank"><button style="width: 100%; background-color: #25D366; color: white; border: none; padding: 10px; border-radius: 8px; font-weight: bold; cursor: pointer;">💬 WhatsApp पर सहायता व स्क्रीनशॉट भेजें</button></a>', unsafe_allow_html=True)
    st.markdown("---")

    # पेमेंट सेक्शन
    st.header("💳 फीस व ऑनलाइन पेमेंट")
    st.markdown("फॉर्म प्रोसेसिंग फीस जमा करने के लिए:")
    
    # 1-Click Pay बटन
    upi_intent_url = f"upi://pay?pa={REAL_UPI_ID}&pn=Ajay%20Kumar&cu=INR&tn=Online%20Ajay%20Documentation"
    st.markdown(f'<a href="{upi_intent_url}"><button style="width: 100%; background-color: #002970; color: white; border: none; padding: 10px; border-radius: 8px; font-weight: bold; cursor: pointer; margin-bottom: 12px;">📲 Paytm / PhonePe / GPay से पे करें</button></a>', unsafe_allow_html=True)

    # आपकी असली UPI ID से बना सटीक QR कोड
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={upi_intent_url}"
    st.image(qr_url, caption="QR कोड स्कैन करें (Ajay Kumar)", width=230)

    st.markdown("---")
    st.subheader("✅ पेमेंट वेरिफिकेशन")
    utr_number = st.text_input("पेमेंट के बाद UTR / Ref No. यहाँ डालें:")
    if st.button("पेमेंट सबमिट करें"):
        if utr_number:
            st.success(f"धन्यवाद! Ref: {utr_number} दर्ज हो गया है। अजय जी जल्द ही आपका फॉर्म वेरीफाई करेंगे।")
        else:
            st.warning("कृपया 12 अंकों का UTR नंबर दर्ज करें।")

if not api_key:
    st.info("👋 नमस्ते अजय जी! सिस्टम शुरू करने के लिए साइडबार में अपनी OpenRouter API Key दर्ज करें।")
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

tab_form, tab_chat = st.tabs(["📝 फॉर्म प्रोसेस & फोटो-डॉक्यूमेंट्स", "💬 24×7 AI हेल्प डेस्क"])

with tab_form:
    st.subheader("1. कौन सा फॉर्म भरना है?")
    c1, c2 = st.columns([1, 2])

    with c1:
        st.write("बोलकर बताएं:")
        voice_input = mic_recorder(start_prompt="🔴 माइक चालू करें", stop_prompt="⏹️ बंद करें", key='recorder')

    with c2:
        typed_input = st.text_input("या फॉर्म का नाम टाइप करें (जैसे: SSC GD, Railway, GDS, Army, DSSSB):")

    form_query = typed_input

    if form_query:
        if "doc_requirements" not in st.session_state or st.session_state.get("current_form") != form_query:
            with st.spinner("AI नियमों, अंतिम तिथि और जरूरी डॉक्यूमेंट्स की जांच कर रहा है..."):
                prompt = f"""
                यूज़र यह फॉर्म भरना चाहता है: "{form_query}"
                इस फॉर्म के लिए आवश्यक डॉक्यूमेंट्स और फोटो/हस्ताक्षर साइज नियम बताएं।
                केवल शुद्ध JSON लौटाएं:
                {{
                    "form_title": "{form_query}",
                    "docs_list": ["10वीं मार्कशीट", "आधार कार्ड", "पासपोर्ट फोटो (20-50 KB)", "हस्ताक्षर (10-20 KB)"],
                    "photo_kb": 50,
                    "sign_kb": 20
                }}
                """
                try:
                    completion = client.chat.completions.create(
                        model="meta-llama/llama-3.3-70b-instruct:free",
                        messages=[{"role": "user", "content": prompt}],
                        response_format={"type": "json_object"}
                    )
                    st.session_state["doc_requirements"] = json.loads(completion.choices[0].message.content)
                except Exception:
                    st.session_state["doc_requirements"] = {
                        "form_title": form_query.upper(),
                        "docs_list": ["10वीं की मार्कशीट", "आधार कार्ड", "पासपोर्ट साइज फोटो (50 KB)", "हस्ताक्षर (20 KB)"],
                        "photo_kb": 50,
                        "sign_kb": 20
                    }
                st.session_state["current_form"] = form_query

        rules = st.session_state["doc_requirements"]
        st.success(f"📋 **{rules.get('form_title', form_query)}** के लिए आवश्यक सूची:")
        for item in rules.get("docs_list", []):
            st.write(f"- 📄 {item}")

        st.markdown("---")
        st.subheader("2. फोटो और डॉक्यूमेंट्स इनपुट")
        
        col_cam, col_up = st.columns(2)
        with col_cam:
            st.markdown("📷 **लाइव कैमरा से फोटो लें:**")
            camera_pic = st.camera_input("कैमरे से पासपोर्ट फोटो लें")

        with col_up:
            st.markdown("📁 **गैलरी / फाइल से चुनें:**")
            uploaded_files = st.file_uploader("मार्कशीट, आधार व अन्य डॉक्यूमेंट्स चुनें:", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

        all_inputs = []
        if camera_pic:
            all_inputs.append(("camera_photo.jpg", camera_pic.getvalue()))
        if uploaded_files:
            for uf in uploaded_files:
                all_inputs.append((uf.name, uf.getvalue()))

        if all_inputs:
            st.info(f"कुल {len(all_inputs)} फाइलें तैयार हैं।")
            if st.button("⚡ FormAI: ऑटो-रीसाइज़ व तैयार करें"):
                with st.status("डॉक्यूमेंट्स सरकारी साइज में सेट हो रहे हैं...", expanded=True) as status:
                    processed_files = []
                    for filename, buffer_data in all_inputs:
                        path = os.path.join("uploads", filename)
                        with open(path, "wb") as f:
                            f.write(buffer_data)

                        name_l = filename.lower()
                        out_path = os.path.join("processed", f"ready_{filename}")
                        if "cam" in name_l or "photo" in name_l or "pic" in name_l:
                            smart_resize(path, out_path, rules.get('photo_kb', 50))
                            processed_files.append(out_path)
                        elif "sign" in name_l:
                            smart_resize(path, out_path, rules.get('sign_kb', 20))
                            processed_files.append(out_path)
                        else:
                            smart_resize(path, out_path, 200)
                            processed_files.append(out_path)

                    status.update(label="🎉 सभी डॉक्यूमेंट्स तैयार हैं!", state="complete")

                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                    for fp in processed_files:
                        zip_file.write(fp, os.path.basename(fp))

                st.download_button(
                    label="📦 सभी तैयार फाइलें डाउनलोड करें (ZIP)",
                    data=zip_buffer.getvalue(),
                    file_name="Online_Ajay_Documentation_Files.zip",
                    mime="application/zip"
                )

with tab_chat:
    st.subheader("💬 ऑनलाइन अजय 24×7 स्मार्ट AI चैटबॉट")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": f"नमस्ते! मैं **ऑनलाइन अजय डॉक्यूमेंटेशन** का 24×7 लाइव सपोर्ट AI हूँ। किसी भी सरकारी फॉर्म, फीस या जरूरी कागजात के बारे में यहाँ पूछें। अजय कुमार जी से बात करने के लिए 8920798182 पर संपर्क करें।"}
        ]

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_msg := st.chat_input("अपना सवाल यहाँ लिखें..."):
        st.session_state.chat_history.append({"role": "user", "content": user_msg})
        with st.chat_message("user"):
            st.markdown(user_msg)

        with st.chat_message("assistant"):
            sys_msg = f"आप 'ऑनलाइन अजय डॉक्यूमेंटेशन' (संचालक: Ajay Kumar, मोबाइल: 8920798182, UPI ID: {REAL_UPI_ID}) के 24×7 उपलब्ध स्मार्ट AI चैटबॉट हैं। सरकारी फॉर्म फीस, लास्ट डेट, डॉक्यूमेंट्स और पेमेंट प्रक्रिया की सही जानकारी हिंदी में दें।"
            try:
                res = client.chat.completions.create(
                    model="meta-llama/llama-3.3-70b-instruct:free",
                    messages=[
                        {"role": "system", "content": sys_msg},
                        {"role": "user", "content": user_msg}
                    ]
                )
                reply = res.choices[0].message.content
            except Exception:
                reply = "नमस्ते! सर्वर व्यस्त है। सीधे व्हाट्सएप बटन पर क्लिक करके अजय कुमार जी से संपर्क करें।"
            st.markdown(reply)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})


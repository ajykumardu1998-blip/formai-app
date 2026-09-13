import streamlit as st
import urllib.parse
from google import genai
from google.genai import types

st.set_page_config(
    page_title="ऑनलाइन अजय डॉक्यूमेंटेशन",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Online Ajay Documentation")
st.caption("संचालक: अजय कुमार | हेल्पलाइन: +91-8920798182")
st.markdown("---")

# क्रेडेंशियल्स
GEMINI_KEY = "AQ.Ab8RN6LaEQ1ttrD68qZ2naKaR_CpzJstuiR9RSaHXtaPmDUoMg"
REAL_UPI_ID = "paytm.s3qpm6x@pty"
WHATSAPP_NUMBER = "918920798182"

# Gemini क्लाइंट
client = genai.Client(api_key=GEMINI_KEY)

# साइडबार
with st.sidebar:
    st.header("📞 सहायता केंद्र")
    st.markdown("👤 **अजय कुमार**")
    st.markdown(f"📱 [+{WHATSAPP_NUMBER}](tel:{WHATSAPP_NUMBER})")
    st.markdown(f"💳 **UPI:** `{REAL_UPI_ID}`")
    
    wa_msg = urllib.parse.quote("नमस्ते अजय जी! मुझे ऑनलाइन फॉर्म भरवाने में सहायता चाहिए।")
    st.link_button("💬 WhatsApp पर संपर्क करें", f"https://wa.me/{WHATSAPP_NUMBER}?text={wa_msg}")
    
    st.markdown("---")
    st.header("💳 फीस व पेमेंट")
    direct_upi_link = f"upi://pay?pa={REAL_UPI_ID}&pn=Ajay%20Kumar&cu=INR"
    st.link_button("Paytm / UPI से पे करें", direct_upi_link)
    
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={direct_upi_link}"
    st.image(qr_url, caption="QR कोड स्कैन करें", width=200)

# चैट सेक्शन
st.subheader("स्मार्ट Gemini AI असिस्टेंट")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "नमस्ते अजय भाई! मैं आपका Gemini AI असिस्टेंट हूँ। सरकारी भर्ती, फॉर्म, उम्र या फीस के बारे में कुछ भी पूछिए।"}
    ]

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_msg = st.chat_input("अपना सवाल यहाँ लिखें और भेजें...")

if user_msg:
    st.session_state.chat_history.append({"role": "user", "content": user_msg})
    with st.chat_message("user"):
        st.markdown(user_msg)

    with st.chat_message("assistant"):
        with st.spinner("Gemini सोच रहा है..."):
            try:
                sys_prompt = "आप ऑनलाइन अजय डॉक्यूमेंटेशन (संचालक: अजय कुमार, 8920798182) के AI सहायक हैं। सरकारी भर्ती, फॉर्म, योग्यता, उम्र, फीस और नियमों का सटीक जवाब सरल हिंदी में दें।"
                res = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=user_msg,
                    config=types.GenerateContentConfig(
                        system_instruction=sys_prompt,
                        temperature=0.7
                    )
                )
                reply = res.text
            except Exception as e:
                reply = f"कनेक्शन एरर: {e}"
            
            st.markdown(reply)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})

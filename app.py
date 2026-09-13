import io
import os
import zipfile
from google import genai
from google.genai import types
from PIL import Image
import streamlit as st

st.set_page_config(
    page_title="ऑनलाइन अजय डॉक्यूमेंटेशन | AI सर्विस सेंटर",
    page_icon="🚀",
    layout="wide",
)

# 24x7 अलर्ट पट्टी
st.markdown(
    """
<div style="background: linear-gradient(90deg, #120000, #400000, #120000); padding: 12px 0; border-top: 2px solid #ff3333; border-bottom: 2px solid #ffcc00; margin-bottom: 20px; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(255,0,0,0.3);">
    <marquee behavior="scroll" direction="left" scrollamount="7" style="color: #ffffff; font-size: 15px; font-weight: bold;">
        🔥 <span style="background-color: #e60000; padding: 2px 8px; border-radius: 4px;">LATEST GOVT FORMS</span>
        📢 SSC GD कांस्टेबल, Railway RRB, इंडिया पोस्ट GDS, दिल्ली DSSSB और आर्मी अग्निवीर भर्ती शुरू! 
        ⚠️ फोटो 50KB व हस्ताक्षर 20KB में तुरंत सेट कराएं। ⚡ संचालक: अजय कुमार (हेल्पलाइन: 8920798182) — 24 घंटे ऑनलाइन सेवा उपलब्ध ⚡
    </marquee>
</div>
""",
    unsafe_allow_html=True,
)

st.title("🚀 Online Ajay Documentation")
st.caption(
    "👨‍💻 Founder: **Ajay Kumar** | 24/7 Smart Cyber Cafe & Document Agent"
    " (Powered by Google Gemini)"
)
st.markdown("---")

os.makedirs("uploads", exist_ok=True)
os.makedirs("processed", exist_ok=True)

# परमानेंट क्रेडेंशियल्स
GEMINI_KEY = "AQ.Ab8RN6IzcVfBVpTL72B4hzX3ZI-igomdURxweRXz0urq3bDwfQ"
REAL_UPI_ID = "paytm.s3qpm6x@pty"

client = genai.Client(api_key=GEMINI_KEY)

# साइडबार (पेमेंट व संपर्क)
with st.sidebar:
  st.header("📞 24×7 सहायता केंद्र")
  st.markdown("👤 **संचालक:** अजय कुमार (Ajay Kumar)")
  st.markdown("📱 **मोबाइल:** [+91-8920798182](tel:8920798182)")
  st.markdown(f"💳 **UPI ID:** `{REAL_UPI_ID}`")

  wa_url = "https://wa.me/918920798182?text=नमस्ते%20अजय%20जी,%20मुझे%20ऑनलाइन%20फॉर्म%20भरवाना%20है।"
  st.markdown(
      f'<a href="{wa_url}" target="_blank"><button style="width: 100%;'
      " background-color: #25D366; color: white; border: none; padding: 10px;"
      " border-radius: 8px; font-weight: bold; cursor: pointer; margin-bottom:"
      ' 10px;">💬 WhatsApp पर बात करें</button></a>',
      unsafe_allow_html=True,
  )
  st.markdown("---")

  st.header("💳 फीस ऑनलाइन जमा करें")
  upi_intent = f"upi://pay?pa={REAL_UPI_ID}&pn=Ajay%20Kumar&cu=INR&tn=Online%20Ajay%20Documentation"
  st.markdown(
      f'<a href="{upi_intent}"><button style="width: 100%; background-color:'
      " #002970; color: white; border: none; padding: 10px; border-radius:"
      " 8px; font-weight: bold; cursor: pointer; margin-bottom: 12px;">📲"
      " Paytm / PhonePe / GPay से पे करें</button></a>",
      unsafe_allow_html=True,
  )

  qr_api = f"https://api.qrserver.com/v1/create-qr-code/?size=240x240&data={upi_intent}"
  st.image(qr_api, caption="QR कोड स्कैन करें (Ajay Kumar)", width=220)


def smart_resize(input_path, output_path, target_max_kb):
  img = Image.open(input_path).convert("RGB")
  quality = 95
  while quality > 15:
    img.save(output_path, "JPEG", quality=quality, optimize=True)
    if (os.path.getsize(output_path) / 1024) <= target_max_kb:
      break
    quality -= 5
  return output_path


PORTALS = {
    "GDS": "https://indiapostgdsonline.gov.in/",
    "SSC": "https://ssc.gov.in/",
    "RAILWAY": "https://www.rrbapply.gov.in/",
    "ARMY": "https://joinindianarmy.nic.in/",
    "DSSSB": "https://dsssbonline.nic.in/",
}

tab_chat, tab_form, tab_ocr = st.tabs([
    "💬 24×7 Gemini AI चैट (लाइव बात करें)",
    "📝 फॉर्म भरें व डॉक्यूमेंट रीसाइज़",
    "🔍 ऑटो मार्कशीट/आधार स्कैनर (OCR)",
])

# --- TAB 1: Gemini AI चैटबॉट ---
with tab_chat:
  st.subheader("🗣️ अजय कुमार का स्मार्ट Gemini AI असिस्टेंट")
  st.write(
      "सरकारी फॉर्म, लास्ट डेट, उम्र सीमा, फीस या डॉक्यूमेंट नियमों की जानकारी"
      " सीधे पूछें:"
  )

  if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{
        "role": "assistant",
        "content": (
            "नमस्ते भाई! 🙏 मैं अजय कुमार जी का स्मार्ट AI असिस्टेंट (Google"
            " Gemini) हूँ। आप मुझसे किसी भी सरकारी भर्ती (जैसे GDS, SSC,"
            " Railway, Army, Police), उम्र सीमा, जरूरी डॉक्यूमेंट्स या फॉर्म"
            " फीस के बारे में पूछ सकते हैं। बताइए किस फॉर्म की जानकारी चाहिए?"
        ),
    }]

  for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
      st.markdown(msg["content"])

  if user_msg := st.chat_input("यहाँ अपना सवाल लिखें..."):
    st.session_state.chat_history.append({"role": "user", "content": user_msg})
    with st.chat_message("user"):
      st.markdown(user_msg)

    with st.chat_message("assistant"):
      with st.spinner("Gemini सोचकर जवाब दे रहा है..."):
        try:
          sys_instruct = (
              "आप 'ऑनलाइन अजय डॉक्यूमेंटेशन' (संचालक: अजय कुमार, मोबाइल:"
              " 8920798182) के AI सहायक हैं। आप बिल्कुल इंसानों की तरह सहज,"
              " आदरपूर्वक और शुद्ध हिंदी में बात करते हैं। सरकारी नौकरी, फॉर्म"
              " भरने की प्रक्रिया, फीस, उम्र सीमा और फोटो/साइन की गाइडलाइन का"
              " सटीक और आसान जवाब दें।"
          )
          res = client.models.generate_content(
              model="gemini-2.5-flash",
              contents=user_msg,
              config=types.GenerateContentConfig(
                  system_instruction=sys_instruct, temperature=0.6
              ),
          )
          bot_reply = res.text
        except Exception:
          bot_reply = (
              "नमस्ते भाई! सर्वर थोड़ा व्यस्त है। फॉर्म भरवाने के लिए आप सीधे"
              " अजय कुमार जी से 8920798182 पर WhatsApp या कॉल कर सकते हैं।"
          )

        st.markdown(bot_reply)
        st.session_state.chat_history.append(
            {"role": "assistant", "content": bot_reply}
        )

# --- TAB 2: फॉर्म आवेदन व रीसाइज़र ---
with tab_form:
  st.subheader("1. सरकारी भर्ती चुनें")
  form_target = st.text_input(
      "फॉर्म का नाम दर्ज करें (उदा: GDS, SSC, Railway):", value="GDS"
  )

  p_url = None
  for k in PORTALS:
    if k in form_target.upper():
      p_url = PORTALS[k]
      break

  if p_url:
    st.info(
        f"🌐 **{form_target.upper()}** आधिकारिक पोर्टल: [यहाँ क्लिक करके सीधे"
        f" वेबसाइट खोलें]({p_url})"
    )

  st.success(
      f"📋 **{form_target.upper()}** के लिए अनिवार्य: 10वीं मार्कशीट, आधार"
      " कार्ड, फोटो (50 KB से कम), हस्ताक्षर (20 KB से कम)"
  )

  st.markdown("---")
  st.subheader("2. आवेदक की जानकारी")
  c1, c2 = st.columns(2)
  with c1:
    user_name = st.text_input("आवेदक का नाम (10th मार्कशीट अनुसार):")
    father_name = st.text_input("पिता का नाम:")
  with c2:
    dob_val = st.text_input("जन्मतिथि (DD/MM/YYYY):")
    phone_val = st.text_input("मोबाइल नंबर:")

  st.markdown("---")
  st.subheader("3. लाइव कैमरा व डॉक्यूमेंट अपलोड (ऑटो 50KB/20KB)")

  use_camera = st.checkbox("📷 लाइव कैमरा खोलें (पासपोर्ट फोटो खींचने के लिए)")
  cam_image = None
  if use_camera:
    cam_image = st.camera_input("फोटो क्लिक करें")

  files_up = st.file_uploader(
      "📁 गैलरी से फोटो, साइन व मार्कशीट चुनें:",
      type=["jpg", "jpeg", "png"],
      accept_multiple_files=True,
  )

  all_docs = []
  if cam_image:
    all_docs.append(("live_photo.jpg", cam_image.getvalue()))
  if files_up:
    for f in files_up:
      all_docs.append((f.name, f.getvalue()))

  if all_docs:
    if st.button("⚡ डॉक्यूमेंट्स को 50KB/20KB में ऑटो-रीसाइज़ करें"):
      with st.status(
          "डॉक्यूमेंट्स सरकारी साइज में तैयार हो रहे हैं...", expanded=True
      ) as status:
        done_files = []
        for fname, bdata in all_docs:
          in_path = os.path.join("uploads", fname)
          with open(in_path, "wb") as fp:
            fp.write(bdata)

          fn_low = fname.lower()
          out_path = os.path.join("processed", f"ready_{fname}")
          if "sign" in fn_low:
            smart_resize(in_path, out_path, 20)
          elif "photo" in fn_low or "cam" in fn_low or "pic" in fn_low:
            smart_resize(in_path, out_path, 50)
          else:
            smart_resize(in_path, out_path, 200)
          done_files.append(out_path)

        status.update(
            label="🎉 सभी डॉक्यूमेंट्स सही साइज में बन चुके हैं!",
            state="complete",
        )

      z_buf = io.BytesIO()
      with zipfile.ZipFile(z_buf, "w") as zf:
        for df in done_files:
          zf.write(df, os.path.basename(df))

      st.download_button(
          label="📦 तैयार डॉक्यूमेंट्स डाउनलोड करें (ZIP)",
          data=z_buf.getvalue(),
          file_name="Govt_Ready_Docs.zip",
          mime="application/zip",
      )

      # डायरेक्ट WhatsApp पर कस्टमर डेटा भेजना
      wa_msg = (
          f"नमस्ते अजय जी, मैंने फॉर्म डिटेल भर दी है:%0Aफॉर्म:"
          f" {form_target.upper()}%0Aनाम: {user_name}%0Aपिता का नाम:"
          f" {father_name}%0ADOB: {dob_val}%0Aमोबाइल: {phone_val}"
      )
      send_wa_url = f"https://wa.me/918920798182?text={wa_msg}"
      st.markdown(
          f'<br><a href="{send_wa_url}" target="_blank"><button'
          ' style="background-color: #25D366; color: white; border: none;'
          " padding: 12px 24px; border-radius: 8px; font-weight: bold; cursor:"
          ' pointer; font-size: 16px;">📲 यह फॉर्म डेटा अजय जी को WhatsApp पर'
          " भेजें</button></a>",
          unsafe_allow_html=True,
      )

# --- TAB 3: स्मार्ट OCR स्कैनर ---
with tab_ocr:
  st.subheader("🔍 AI मार्कशीट व आधार कार्ड स्कैनर")
  st.write(
      "मार्कशीट या आधार की फोटो अपलोड करें—Gemini AI उसमें से नाम, पिता का नाम और"
      " DOB खुद निकाल देगा:"
  )

  doc_pic = st.file_uploader(
      "दस्तावेज़ की साफ़ फोटो चुनें:",
      type=["jpg", "jpeg", "png"],
      key="ocr_uploader",
  )
  if doc_pic and st.button("⚡ AI से डेटा स्कैन करें"):
    with st.spinner("Gemini AI दस्तावेज़ पढ़ रहा है..."):
      try:
        raw_img = Image.open(doc_pic)
        ocr_prompt = (
            "इस दस्तावेज़ (मार्कशीट या आधार कार्ड) को ध्यान से पढ़ें और निम्नलिखित"
            " जानकारी निकालें:\n1. पूरा नाम\n2. पिता का नाम\n3. जन्मतिथि (DOB)\n4."
            " रोल नंबर/पहचान संख्या (यदि हो)\nसाफ़ और स्पष्ट हिंदी में लिखें।"
        )
        ocr_res = client.models.generate_content(
            model="gemini-2.5-flash", contents=[raw_img, ocr_prompt]
        )
        st.success("✅ दस्तावेज़ से मिला विवरण:")
        st.markdown(ocr_res.text)
      except Exception as ex:
        st.error(
            "स्कैन करने में समस्या आई, कृपया फोटो साफ़ खींचकर दोबारा अपलोड करें।"
        )



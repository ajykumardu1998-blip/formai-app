import io
import os
import urllib.parse
import zipfile
from google import genai
from google.genai import types
from PIL import Image
import streamlit as st

st.set_page_config(
    page_title="ऑनलाइन अजय डॉक्यूमेंटेशन | 24x7 AI सेंटर",
    page_icon="🚀",
    layout="wide",
)

# 24x7 रनिंग अलर्ट पट्टी
st.markdown(
    """
<div style="background: linear-gradient(90deg, #111111, #4a0000, #111111); padding: 12px 0; border-top: 2px solid #ff3333; border-bottom: 2px solid #ffcc00; margin-bottom: 20px; border-radius: 8px; overflow: hidden;">
    <marquee behavior="scroll" direction="left" scrollamount="7" style="color: #ffffff; font-size: 15px; font-weight: bold;">
        LATEST GOVT FORMS: SSC GD Constable, Railway RRB, India Post GDS, Army Agniveer | Helpline: +91-8920798182 (Ajay Kumar) | 24 Hours Online Service Available
    </marquee>
</div>
""",
    unsafe_allow_html=True,
)

st.title("🚀 Online Ajay Documentation")
st.caption(
    "Founder: Ajay Kumar | 24/7 Autonomous Cyber Cafe & Document Agent"
    " (Powered by Google Gemini)"
)
st.markdown("---")

os.makedirs("uploads", exist_ok=True)
os.makedirs("processed", exist_ok=True)

# क्रेडेंशियल्स
GEMINI_KEY = "AQ.Ab8RN6IzcVfBVpTL72B4hzX3ZI-igomdURxweRXz0urq3bDwfQ"
REAL_UPI_ID = "paytm.s3qpm6x@pty"
WHATSAPP_NUMBER = "918920798182"

client = genai.Client(api_key=GEMINI_KEY)

# साइडबार
with st.sidebar:
  st.header("24x7 Support & Contact")
  st.markdown("Operator: **Ajay Kumar**")
  st.markdown("Helpline: [+91-8920798182](tel:8920798182)")
  st.markdown(f"UPI ID: `{REAL_UPI_ID}`")

  initial_msg = urllib.parse.quote(
      "नमस्ते अजय जी! मुझे ऑनलाइन फॉर्म भरवाने में सहायता चाहिए।"
  )
  wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={initial_msg}"
  st.markdown(
      f'<a href="{wa_link}" target="_blank"><button style="width: 100%;'
      " background-color: #25D366; color: white; border: none; padding: 10px;"
      " border-radius: 8px; font-weight: bold; cursor: pointer; margin-bottom:"
      ' 12px;">WhatsApp पर संपर्क करें</button></a>',
      unsafe_allow_html=True,
  )
  st.markdown("---")

  st.link_button("Paytm / UPI से पे करें", upi_intent)
    
  st.image(qr_api, caption="Scan QR to Pay (Ajay Kumar)", width=220)


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

tab_chat, tab_form, tab_ocr = st.tabs(
    ["Gemini AI चैट", "फॉर्म व डॉक्यूमेंट रीसाइज़", "मार्कशीट/आधार स्कैनर"]
)

# --- TAB 1: Gemini AI चैटबॉट ---
with tab_chat:
  st.subheader("स्मार्ट Gemini AI असिस्टेंट (अजय कुमार)")
  st.write(
      "सरकारी भर्ती, योग्यता, उम्र सीमा, फीस या डॉक्यूमेंट्स के नियमों के बारे"
      " में यहाँ पूछें:"
  )

  if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{
        "role": "assistant",
        "content": (
            "नमस्ते भाई! मैं अजय कुमार जी का Google Gemini AI असिस्टेंट हूँ।"
            " सरकारी भर्ती (GDS, SSC, Railway, Army आदि), लास्ट डेट, फीस या"
            " जरूरी कागजात के बारे में कुछ भी पूछिए।"
        ),
    }]

  for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
      st.markdown(msg["content"])

  if user_msg := st.chat_input("अपना सवाल यहाँ लिखें..."):
    st.session_state.chat_history.append({"role": "user", "content": user_msg})
    with st.chat_message("user"):
      st.markdown(user_msg)

    with st.chat_message("assistant"):
      with st.spinner("Gemini सोच रहा है..."):
        try:
          sys_prompt = (
              "आप 'ऑनलाइन अजय डॉक्यूमेंटेशन' (संचालक: अजय कुमार, मोबाइल:"
              " 8920798182) के AI सहायक हैं। भारतीय सरकारी भर्तियों, उम्र"
              " सीमा, फीस, योग्यता और फोटो/हस्ताक्षर के नियमों का बिल्कुल सटीक"
              " और सरल जवाब शुद्ध हिंदी में दें।"
          )
          res = client.models.generate_content(
              model="gemini-2.5-flash",
              contents=user_msg,
              config=types.GenerateContentConfig(
                  system_instruction=sys_prompt, temperature=0.6
              ),
          )
          bot_reply = res.text
        except Exception:
          bot_reply = (
              "माफ़ करना भाई, सर्वर व्यस्त है। सीधे सहायता के लिए अजय कुमार जी"
              " से 8920798182 पर संपर्क करें।"
          )

        st.markdown(bot_reply)
        st.session_state.chat_history.append(
            {"role": "assistant", "content": bot_reply}
        )

# --- TAB 2: फॉर्म आवेदन व रीसाइज़र ---
with tab_form:
  st.subheader("1. भर्ती चयन")
  form_target = st.text_input("फॉर्म का नाम लिखें (उदा: GDS, SSC):", value="GDS")

  portal_url = None
  for k in PORTALS:
    if k in form_target.upper():
      portal_url = PORTALS[k]
      break

  if portal_url:
    st.info(
        f"🌐 {form_target.upper()} का आधिकारिक पोर्टल: [यहाँ क्लिक करके सीधे"
        f" वेबसाइट खोलें]({portal_url})"
    )

  st.success(
      f"📋 {form_target.upper()} नियम: फोटो 50 KB से कम, हस्ताक्षर 20 KB से"
      " कम अनिवार्य हैं।"
  )

  st.markdown("---")
  st.subheader("2. आवेदक की जानकारी")
  c1, c2 = st.columns(2)
  with c1:
    u_name = st.text_input("आवेदक का नाम (10th मार्कशीट अनुसार):")
    f_name = st.text_input("पिता का नाम:")
  with c2:
    dob = st.text_input("जन्मतिथि (DD/MM/YYYY):")
    ph = st.text_input("मोबाइल नंबर:")

  st.markdown("---")
  st.subheader("3. डॉक्यूमेंट रीसाइज़ (50KB / 20KB)")

  use_cam = st.checkbox("लाइव कैमरा ऑन करें (पासपोर्ट फोटो के लिए)")
  cam_pic = None
  if use_cam:
    cam_pic = st.camera_input("फोटो कैप्चर करें")

  files_up = st.file_uploader(
      "गैलरी से फोटो व हस्ताक्षर चुनें:",
      type=["jpg", "jpeg", "png"],
      accept_multiple_files=True,
  )

  all_docs = []
  if cam_pic:
    all_docs.append(("live_photo.jpg", cam_pic.getvalue()))
  if files_up:
    for f in files_up:
      all_docs.append((f.name, f.getvalue()))

  if all_docs and st.button("डॉक्यूमेंट्स 50KB/20KB में रीसाइज़ करें"):
    with st.status("रीसाइज़िंग चालू है...", expanded=True) as status:
      done_files = []
      for fname, bdata in all_docs:
        in_p = os.path.join("uploads", fname)
        with open(in_p, "wb") as fp:
          fp.write(bdata)

        out_p = os.path.join("processed", f"ready_{fname}")
        if "sign" in fname.lower():
          smart_resize(in_p, out_p, 20)
        else:
          smart_resize(in_p, out_p, 50)
        done_files.append(out_p)

      status.update(label="सभी डॉक्यूमेंट्स तैयार हो चुके हैं!", state="complete")

    z_buf = io.BytesIO()
    with zipfile.ZipFile(z_buf, "w") as zf:
      for df in done_files:
        zf.write(df, os.path.basename(df))

    st.download_button(
        "रीसाइज़ डॉक्यूमेंट्स डाउनलोड करें (ZIP)",
        z_buf.getvalue(),
        "ready_docs.zip",
        "application/zip",
    )

    wa_text = f"""*ऑनलाइन अजय डॉक्यूमेंटेशन - नया फॉर्म आवेदन*
फॉर्म का नाम: {form_target.upper()}
आवेदक का नाम: {u_name}
पिता का नाम: {f_name}
जन्मतिथि: {dob}
मोबाइल: {ph}
स्टेटस: डॉक्यूमेंट्स 50KB/20KB में तैयार हैं।"""

    enc_msg = urllib.parse.quote(wa_text)
    wa_submit_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={enc_msg}"
    st.markdown(
        f'<br><a href="{wa_submit_url}" target="_blank"><button'
        ' style="background-color: #25D366; color: white; border: none;'
        " padding: 12px 22px; border-radius: 8px; font-weight: bold; cursor:"
        ' pointer; font-size: 15px;">📲 यह पूरा फॉर्म डेटा अजय जी को WhatsApp पर'
        " भेजें</button></a>",
        unsafe_allow_html=True,
    )

# --- TAB 3: OCR स्कैनर ---
with tab_ocr:
  st.subheader("AI मार्कशीट व आधार कार्ड स्कैनर")
  st.write(
      "मार्कशीट या आधार कार्ड की साफ़ फोटो अपलोड करें—Gemini AI उसमें से विवरण"
      " निकाल देगा:"
  )

  doc_pic = st.file_uploader(
      "दस्तावेज़ की फोटो अपलोड करें:", type=["jpg", "jpeg", "png"], key="ocr"
  )
  if doc_pic and st.button("AI से स्कैन करें"):
    with st.spinner("Gemini AI दस्तावेज़ पढ़ रहा है..."):
      try:
        raw_img = Image.open(doc_pic)
        prompt = (
            "इस दस्तावेज़ को ध्यान से पढ़ें और निम्नलिखित जानकारी साफ़ निकालें:"
            " 1. नाम 2. पिता का नाम 3. जन्मतिथि (DOB) 4. रोल नंबर/पहचान संख्या।"
        )
        ocr_res = client.models.generate_content(
            model="gemini-2.5-flash", contents=[raw_img, prompt]
        )
        st.success("दस्तावेज़ से मिला विवरण:")
        st.markdown(ocr_res.text)

        ocr_wa_text = (
            f"*दस्तावेज़ स्कैन विवरण (अजय डॉक्यूमेंटेशन):*\n{ocr_res.text}"
        )
        ocr_enc = urllib.parse.quote(ocr_wa_text)
        st.markdown(
            f'<br><a href="https://wa.me/{WHATSAPP_NUMBER}?text={ocr_enc}"'
            ' target="_blank"><button style="background-color: #25D366; color:'
            " white; border: none; padding: 10px 18px; border-radius: 8px;"
            ' font-weight: bold; cursor: pointer;">यह डेटा WhatsApp पर'
            " भेजें</button></a>",
            unsafe_allow_html=True,
        )
      except Exception:
        st.error(
            "दस्तावेज़ स्कैन नहीं हो सका, कृपया साफ़ फोटो दोबारा अपलोड करें।"
        )

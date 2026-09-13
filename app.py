import io
import os
import urllib.parse
import zipfile
from google import genai
from google.genai import types
from PIL import Image
import streamlit as st

st.set_page_config(
    page_title="ऑनलाइन अजय डॉक्यूमेंटेशन | Gemini AI",
    page_icon="🚀",
    layout="wide",
)

st.title("🚀 Online Ajay Documentation")
st.caption(
    "संचालक: अजय कुमार | 24/7 Smart Cyber Cafe & Online Form Center (Powered"
    " by Google Gemini)"
)
st.markdown("---")

os.makedirs("uploads", exist_ok=True)
os.makedirs("processed", exist_ok=True)

# आपके क्रेडेंशियल्स
GEMINI_KEY = "AQ.Ab8RN6IzcVfBVpTL72B4hzX3ZI-igomdURxweRXz0urq3bDwfQ"
REAL_UPI_ID = "paytm.s3qpm6x@pty"
WHATSAPP_NUMBER = "918920798182"

client = genai.Client(api_key=GEMINI_KEY)

# साइडबार
with st.sidebar:
  st.header("📞 सहायता केंद्र")
  st.markdown("👤 **अजय कुमार**")
  st.markdown("📱 [+91-8920798182](tel:8920798182)")
  st.markdown(f"💳 **UPI:** `{REAL_UPI_ID}`")

  wa_msg = urllib.parse.quote(
      "नमस्ते अजय जी! मुझे ऑनलाइन फॉर्म भरवाने में मदद चाहिए।"
  )
  st.link_button(
      "💬 WhatsApp पर संपर्क करें",
      f"https://wa.me/{WHATSAPP_NUMBER}?text={wa_msg}",
  )

  st.markdown("---")
  st.header("💳 फीस व पेमेंट")
  direct_upi_link = f"upi://pay?pa={REAL_UPI_ID}&pn=Ajay%20Kumar&cu=INR"
  st.link_button("Paytm / UPI से पे करें", direct_upi_link)

  qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=220x220&data={direct_upi_link}"
  st.image(qr_url, caption="QR कोड स्कैन करें", width=200)


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
}

tab_chat, tab_form, tab_ocr = st.tabs(
    ["Gemini AI चैट", "फॉर्म व रीसाइज़", "मार्कशीट स्कैनर"]
)

# TAB 1: Gemini चैट
with tab_chat:
  st.subheader("स्मार्ट Gemini AI असिस्टेंट")
  if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{
        "role": "assistant",
        "content": (
            "नमस्ते भाई! मैं अजय कुमार जी का Gemini AI असिस्टेंट हूँ। सरकारी"
            " नौकरी (GDS, SSC, Railway), उम्र, फीस या डॉक्यूमेंट्स के बारे में"
            " कुछ भी पूछिए।"
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
      with st.spinner("Gemini जवाब सोच रहा है..."):
        try:
          sys_prompt = (
              "आप ऑनलाइन अजय डॉक्यूमेंटेशन (संचालक: अजय कुमार, 8920798182) के"
              " AI सहायक हैं। सरकारी भर्ती, योग्यता, उम्र, फीस और फोटो/साइन के"
              " नियमों का सटीक जवाब सरल हिंदी में दें।"
          )
          res = client.models.generate_content(
              model="gemini-2.5-flash",
              contents=user_msg,
              config=types.GenerateContentConfig(
                  system_instruction=sys_prompt, temperature=0.6
              ),
          )
          reply = res.text
        except Exception:
          reply = (
              "सर्वर व्यस्त है, कृपया सीधे अजय जी से 8920798182 पर संपर्क करें।"
          )
        st.markdown(reply)
        st.session_state.chat_history.append(
            {"role": "assistant", "content": reply}
        )

# TAB 2: फॉर्म
with tab_form:
  st.subheader("1. भर्ती चयन")
  form_target = st.text_input("फॉर्म का नाम लिखें:", value="GDS")

  portal_url = None
  for k in PORTALS:
    if k in form_target.upper():
      portal_url = PORTALS[k]
      break
  if portal_url:
    st.link_button(
        f"🌐 {form_target.upper()} की आधिकारिक वेबसाइट खोलें", portal_url
    )

  st.success(
      f"{form_target.upper()} के नियम: फोटो 50KB और हस्ताक्षर 20KB से कम"
      " चाहिए।"
  )

  st.markdown("---")
  st.subheader("2. आवेदक विवरण")
  c1, c2 = st.columns(2)
  with c1:
    u_name = st.text_input("आवेदक का नाम:")
    f_name = st.text_input("पिता का नाम:")
  with c2:
    dob = st.text_input("जन्मतिथि (DD/MM/YYYY):")
    ph = st.text_input("मोबाइल नंबर:")

  st.markdown("---")
  st.subheader("3. डॉक्यूमेंट रीसाइज़ (50KB / 20KB)")
  use_cam = st.checkbox("लाइव कैमरा चालू करें")
  cam_pic = None
  if use_cam:
    cam_pic = st.camera_input("फोटो खींचें")

  files_up = st.file_uploader(
      "फोटो व साइन अपलोड करें:",
      type=["jpg", "jpeg", "png"],
      accept_multiple_files=True,
  )
  all_docs = []
  if cam_pic:
    all_docs.append(("live_photo.jpg", cam_pic.getvalue()))
  if files_up:
    for f in files_up:
      all_docs.append((f.name, f.getvalue()))

  if all_docs and st.button("डॉक्यूमेंट्स 50KB/20KB में सेट करें"):
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

    z_buf = io.BytesIO()
    with zipfile.ZipFile(z_buf, "w") as zf:
      for df in done_files:
        zf.write(df, os.path.basename(df))

    st.download_button(
        "📦 रीसाइज़ फाइलें डाउनलोड करें (ZIP)",
        z_buf.getvalue(),
        "ready_docs.zip",
        "application/zip",
    )

    wa_text = (
        f"*फॉर्म आवेदन विवरण*\nफॉर्म: {form_target.upper()}\nनाम:"
        f" {u_name}\nपिता: {f_name}\nDOB: {dob}\nमोबाइल: {ph}"
    )
    enc_wa = urllib.parse.quote(wa_text)
    st.link_button(
        "📲 यह फॉर्म डेटा अजय जी को WhatsApp पर भेजें",
        f"https://wa.me/{WHATSAPP_NUMBER}?text={enc_wa}",
    )

# TAB 3: OCR
with tab_ocr:
  st.subheader("AI दस्तावेज़ स्कैनर")
  doc_pic = st.file_uploader(
      "दस्तावेज़ की फोटो चुनें:", type=["jpg", "jpeg", "png"], key="ocr_box"
  )
  if doc_pic and st.button("AI से स्कैन करें"):
    with st.spinner("Gemini AI पढ़ रहा है..."):
      try:
        raw_img = Image.open(doc_pic)
        prompt = (
            "दस्तावेज़ से नाम, पिता का नाम और जन्मतिथि निकालें। संवेदनशील"
            " पहचान संख्या को शामिल न करें।"
        )
        ocr_res = client.models.generate_content(
            model="gemini-2.5-flash", contents=[raw_img, prompt]
        )
        st.success("विवरण:")
        st.markdown(ocr_res.text)

        ocr_enc = urllib.parse.quote(f"*दस्तावेज़ विवरण:*\n{ocr_res.text}")
        st.link_button(
            "📲 यह डेटा WhatsApp पर भेजें",
            f"https://wa.me/{WHATSAPP_NUMBER}?text={ocr_enc}",
        )
      except Exception:
        st.error("स्कैन नहीं हो सका, कृपया साफ़ फोटो डालें।")

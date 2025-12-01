import base64
import streamlit as st
from openai import OpenAI

# ดึง API key จาก Streamlit secrets (จะไปเซ็ตทีหลังบนเว็บ)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="OCR with ChatGPT Vision", page_icon="🔍")
st.title("🔍 OCR Image → Text ด้วย ChatGPT Vision")

st.write(
    """
อัปโหลดรูปภาพที่มีข้อความ (เช่น โค้ดใต้ฝาขวด, ป้าย, เอกสารเล็ก ๆ)  
แล้วให้โมเดลของ ChatGPT ช่วยอ่านข้อความให้โดยอัตโนมัติ
"""
)

uploaded_file = st.file_uploader(
    "เลือกไฟล์รูปภาพ",
    type=["png", "jpg", "jpeg", "webp"],
)

if uploaded_file is not None:
    # แสดงรูปตัวอย่าง
    st.image(uploaded_file, caption="ภาพที่อัปโหลด", use_column_width=True)

    if st.button("อ่านข้อความจากรูป"):
        try:
            with st.spinner("กำลังส่งรูปให้ ChatGPT วิเคราะห์..."):
                # อ่านไฟล์รูปเป็น base64 data URL
                image_bytes = uploaded_file.read()
                b64 = base64.b64encode(image_bytes).decode("utf-8")
                mime_type = uploaded_file.type or "image/jpeg"
                image_data_url = f"data:{mime_type};base64,{b64}"

                # เรียก Vision model ผ่าน Responses API
                response = client.responses.create(
                    model="gpt-4.1",
                    input=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "input_text",
                                    "text": (
                                        "You are an OCR assistant. "
                                        "Read all clearly printed text in this image. "
                                        "If there is a main code (letters and digits), "
                                        "return ONLY that code in UPPERCASE with no spaces "
                                        "or extra explanation. Otherwise, just return "
                                        "all readable text."
                                    ),
                                },
                                {
                                    "type": "input_image",
                                    "image_url": image_data_url,
                                },
                            ],
                        }
                    ],
                )

            text = response.output_text.strip()

            st.subheader("ผลลัพธ์ OCR:")
            if text:
                st.code(text, language="text")
            else:
                st.info("ไม่พบข้อความที่อ่านได้ชัดเจนในภาพนี้")

        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดขณะเรียก OpenAI API: {e}")
else:
    st.info("กรุณาอัปโหลดรูปภาพก่อน เพื่อเริ่มอ่านข้อความ 😊")




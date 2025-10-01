import streamlit as st
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from streamlit_image_comparison import image_comparison

st.set_page_config(page_title="Pencil Sketch App 🎨")

st.title("📷 حول صورك إلى رسومات بالقلم الرصاص ✏️")
st.write("ارفع صورة أو أكثر، واختر طريقة العرض (Slider أو جنب بعض) ✨")

# رفع صور متعددة
uploaded_files = st.file_uploader(
    "📤 ارفع صورة أو أكثر (JPG / PNG)", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.markdown(f"## 📸 {uploaded_file.name}")

        # قراءة الصورة
        image = Image.open(uploaded_file).convert("RGB")
        image_np = np.array(image)

        # تحويل لسكيتش
        gray_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        inverted_image = 255 - gray_image
        blurred = cv2.GaussianBlur(inverted_image, (21, 21), 0)
        sketch = cv2.divide(gray_image, 255 - blurred, scale=256.0)

        # اختيار طريقة العرض
        display_mode = st.radio(
            f"طريقة العرض - {uploaded_file.name}", 
            ["🎭 Before/After Slider", "🖼️ جنب بعض"],
            key=f"display_{uploaded_file.name}"
        )

        if display_mode == "🎭 Before/After Slider":
            image_comparison(
                img1=image,        # Before
                img2=sketch,       # After
                label1="📸 Before",
                label2="✏️ After"
            )
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📸 الصورة الأصلية")
                st.image(image, use_column_width=True)
            with col2:
                st.subheader("✏️ الرسمة بالقلم الرصاص")
                st.image(sketch, use_column_width=True, clamp=True)

        # زر التحميل
        format_option = st.radio(
            f"اختر صيغة التحميل - {uploaded_file.name}", 
            ("PNG", "JPEG"), 
            key=f"format_{uploaded_file.name}"
        )

        buf = BytesIO()
        Image.fromarray(sketch).save(buf, format=format_option)

        st.download_button(
            label=f"📥 تحميل {uploaded_file.name} كـ {format_option}",
            data=buf.getvalue(),
            file_name=f"{uploaded_file.name.split('.')[0]}_sketch.{format_option.lower()}",
            mime=f"image/{format_option.lower()}"
        )
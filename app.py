import streamlit as st
import io
from PIL import Image, ImageFilter
from rembg import remove

st.set_page_config(page_title="Sticker Maker", page_icon="✂️")
st.title("✂️ DIY Sticker Maker")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    col1, col2 = st.columns(2)
    image = Image.open(uploaded_file)
    col1.image(image, caption="Original")

    if st.button("Make Sticker"):
        with st.spinner("Cutting out..."):
            # Remove background
            output_bytes = remove(uploaded_file.getvalue())
            img = Image.open(io.BytesIO(output_bytes)).convert("RGBA")
            
            # Add white border
            alpha = img.getchannel('A')
            mask = alpha.point(lambda p: 255 if p > 0 else 0)
            border_mask = mask.filter(ImageFilter.MaxFilter(15))
            
            sticker_bg = Image.new("RGBA", img.size, "white")
            canvas = Image.new("RGBA", img.size, (0,0,0,0))
            final = Image.alpha_composite(Image.composite(sticker_bg, canvas, border_mask), img)
            
            col2.image(final, caption="Sticker Result")
            
            # Download button
            buf = io.BytesIO()
            final.save(buf, format="PNG")
            st.download_button("Download PNG", buf.getvalue(), "sticker.png", "image/png")

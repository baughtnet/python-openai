# python program to send prompts and receive images back from dalle-3
# user will be prompted to enter a prompt
# dalle-3 will generate an image based on the prompt
# user image will be displayed
# interface will be via a webpage

from openai import OpenAI
import os
import streamlit as st

# import api key
api_key = os.getenv("OPENAI_API")
client = OpenAI(api_key=api_key)

size1 = "1024x1024"
size2 = "1024x1792"
size3 = "1792x1024"

standard = "standard"
hd = "hd"

vivid = "vivid"
natural = "natural"

style = [vivid, natural]
sizes = [size1, size2, size3]
quality = [standard, hd]

# set page title
st.title("DALLE-3 Image Generator")
st.subheader("Powered by OpenAI")

prompt = st.text_area("Enter Prompt")

selected_style = st.selectbox("Select Image Style", style)
selected_size = st.selectbox("Select Image Size", sizes)
selected_quality = st.selectbox("Select Image Quality", quality)

if st.button("Submit"):
    if prompt:
        OpenAI.api_key = api_key
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size=selected_size,
            quality=selected_quality,
            style=selected_style,
        )
    image_url = response.data[0].url
    st.image(image_url)
else:
    st.error("Please enter a prompt")

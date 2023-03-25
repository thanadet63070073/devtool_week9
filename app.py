import streamlit as st 
import requests
import base64
import matplotlib.pyplot as plt
import numpy as np
import cv2
import json
import os

# encode image as base64 string
def encode_image(image):
    _, encoded_image = cv2.imencode(".jpg", image)
    return "data:image/jpeg;base64," + base64.b64encode(encoded_image).decode()

# decode base64 string to image
def decode_image(image_string):
    encoded_data = image_string.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

st.header("Edge Detection 👏")

st.write("This is my first app")

firstName = st.text_input('ENTER YOUR FIRST NAME')
surname = st.text_input('ENTER YOUR SURNAME')
number = st.text_input('ENTER YOUR NUMBER')

uploaded_file = st.file_uploader("Choose a image file", type=['jpg', 'png', 'jpeg'])
if uploaded_file is not None:
    with open(os.path.join("Img", uploaded_file.name),"wb") as f:
        f.write(uploaded_file.getbuffer())
    

if st.button("submit"):
    if uploaded_file is not None:
        image_file = "./Img/" + uploaded_file.name
        url        = "http://44.206.241.44:8088"

        # Load the image
        image        = cv2.imread(image_file)
        image        = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_string = encode_image(image)

        payload = {
            "image": image_string,
            "name": firstName,
            "surname": surname,
            "number": number
        }

        response = requests.post(f"{url}/process-image", json=payload)
        data = json.loads(response.content)

        processed_image_string = data["processed_image"]
        processed_image        = decode_image(processed_image_string)

        # Create a figure and set the title
        fig = plt.figure(figsize=(12, 4))
        fig.suptitle('Comparison of Images')

        # Add the first image to the left subplot
        ax1 = fig.add_subplot(1, 2, 1)
        ax1.imshow(image)
        ax1.set_title('Original image')

        # Add the second image to the right subplot
        ax2 = fig.add_subplot(1, 2, 2)
        ax2.imshow(processed_image)
        ax2.set_title('Processed image')

        # Show the plot
        st.pyplot(fig)
        
        st.write("Your input here 👇")
        st.write("Your Name : " + data["name"] + " " + data["surname"])
        st.write("Your Number : " + data["number"])
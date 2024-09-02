from dotenv import load_dotenv
load_dotenv() ##load all the enviourment variables

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

##function to load Gemini Pro Vision
model=genai.GenerativeModel('gemini-1.5-flash')
def get_gemini_response(input,image,prompt):
  try:
    response=model.generate_content([input,image[0],prompt])
    return response.text
  except Exception as e:
      st.error(f"Error generating response: {e}")
      return None

def input_image_details(uploaded_file):
    if uploaded_file is not None:
           bytes_data=uploaded_file.getvalue()
           image_parts=[{
               "mime_type":uploaded_file.type,
               "data":bytes_data
           }]
           return image_parts
    else :
        raise FileNotFoundError("File doesnot found")

##Initialize our streamlit app
st.set_page_config(page_title="Multilanguage Invoice Extractor")
st.header("Multilanguage Invoice Extractor")
input=st.text_input("Input Prompt :" ,key="input")
uploaded_file=st.file_uploader("Choose the image of the invoice ...." ,type=['jpg','jpeg','png'])
image_file= None
if uploaded_file is not None:
    image_file=uploaded_file
    image=Image.open(image_file)
    st.image(image, caption="Uploaded Image.",use_column_width=True)

submit=st.button("Tell me about the invoice")

input_prompt="""
you are a expert in understanding invoices.we will upload a image as invoice
and you will have to answer any question based on the uploaded invoice image
"""
## if submit button is clicked
if submit:
 try:
   image_data=input_image_details(image_file)
   response=get_gemini_response(input_prompt,image_data,input)
   st.subheader("The Response is")
   st.write(response)
 except Exception as e:
     st.error(f"Error processing request: {e}")
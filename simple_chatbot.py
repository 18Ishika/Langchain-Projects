from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import streamlit as st
load_dotenv()

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY","")
llm=ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash",
    temperature=0.3,
    google_api_key=GOOGLE_API_KEY
    )

def get_response(input,chat_history):
    chat_history.append(f"Human: {input}")
    formatted_text='\n'.join(chat_history)
    response=llm.invoke(formatted_text)
    chat_history.append(f"AI: {response.content}")
    return response.content

st.title("A simple chatbot")
st.write("Chat with Google Gemini 1.5 flash")


if "chat_history" not in st.session_state:
    st.session_state.chat_history=[]

input=st.text_input('You:',key="input")
if input:
    response=get_response(input,st.session_state.chat_history)
    st.text_area("AI:",value=response,height=150,key='response')

if st.session_state.chat_history:
    st.markdown("---")
    st.markdown("## Chat History")
    for msg in st.session_state.chat_history:
        if msg.startswith("Human:"):
            st.markdown(f"**You:** {msg[7:]}")
        elif msg.startswith("AI:"):
            st.markdown(f"**AI:** {msg[4:]}")
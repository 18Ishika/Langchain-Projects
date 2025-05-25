from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate

load_dotenv()
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY","")

llm=ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash",
    temperature=0.3,
    google_api_key=GOOGLE_API_KEY
)
def get_context(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])

        transcript = " ".join(chunk["text"] for chunk in transcript_list)

    except TranscriptsDisabled:
        #display the errror at streamlit interface
        print("No captions available for this video.")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([transcript])


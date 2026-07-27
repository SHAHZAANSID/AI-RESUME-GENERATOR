import streamlit as st
# streamlit: web based app making
# light python framework

st.title("AI Resume Maker")

st.markdown("""## User can create or download AI
created resume based on high ATS score""")

#========AGENT CODE=========
import IPython as ip
import os
import time
import langchain
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
import pytesseract as pyt
from tavily import TavilyClient
from langchain.messages import SystemMessage, HumanMessage
import numpy as np
import streamlit as st
from langchain_community.document_loaders import PyMuPDFLoader

# =============API KEY LOAD==============
GOOGLE_API_KEY = st.sidebar.text_input("GOOGLE_API_KEY", type = "password")
GROQ_API_KEY = st.sidebar.text_input("GROQ_API_KEY", type = "password")
TAVILY_API_KEY = st.sidebar.text_input("TAVILY_API_KEY", type = "password")

# ==========model building==============
model = ChatGoogleGenerativeAI(
    model = "gemini-3.5-flash-lite",
    google_api_key = GOOGLE_API_KEY
)

def search_recent_news_jobs(query):
  """This function helps to search recent news or
  recent jobs related to given search query suppose
  user write Python Developer jobs it should return
  trending news and jobs link"""

  client = TavilyClient(
      api_key = TAVILY_API_KEY
  )
  return client.search(query)

# agent creation
from langchain.agents import create_agent

agent = create_agent(
    model = model,
    tools = [search_recent_news_jobs]
)

# prompt generater
def prompt_generater(agent):
  """This function helps to give detailsd prompt
  followed by chain of thoughts and persona based
  prompting, main task is to give detailed prompt
  to build resume for students or Experienced person
  based on there given personal information"""

  prompt = """You are a senior HR resume analyzer,
  main task is to give detailed prompt
  to build resume for students or Experienced person
  based on there given personal information.
  System Instruction I want model to generate
  resume in HTML format, include that in prompt"""

  response = agent.invoke(prompt)
  file_name = 'prompt.py'
  with open(file_name, 'w') as f:
    f.write(response.content[-1]['text'])
    return "Prompt file generated successfully, agent can read it"
      
prompt_generator(model
# tool 2:
def resume_maker_prompt():
  """This function just gives updated prompt for model"""
  with open('prompt.py', 'r') as f:
    prompt = f.read()
    return prompt

resume_maker_prompt()
# =============GENERATE RESUME=============
prompt = """You are a helpful AI assistant with job resume maker,
your task is to give HTML format resume,
with proper designing using recent CSS and JS
code, with professional design format.
user will upload data and return HTML format resume"""

final_prompt = prompt + resume_maker_prompt()

user_details = """user details: given below:
Give Python Developer Resume.
name: MOHAMMAD SHAHZAAN contact: 9058669494 email: shahzaansid@gmail.com
education: bachlor of computer applications(BCA) 12th & 10th icse
languages: python, JS, c, c++, java, SQL
certificates: Be 10x, genAI and AgenticAI
"""

query = final_prompt + user_details

if st.button("Generate Resume"):
  with st.spinner("Running Agent..."):

    response = agent.invoke({'messages':[{'role':'user','content':query}]})
    code = response['messages'][-1].content[-1]['text']

    #st.markdown(code)
    st.html(code, width = "strength", unsafe_allow_javascript = True









import streamlit as st
import base64


# streamlit: Web based app making
# lite python framework

st.title("AI Resume Maker")

st.markdown("""## User can create or
download AI created Resume based on high ATS
Score""")


#==================AGENT CODE===================
# Step 2: Load Modules

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
from PIL import Image

# ================API KEY LOAD===================

GOOGLE_API_KEY = st.sidebar.text_input("GOOGLE_API_KEY",type="password")
GROQ_API_KEY = st.sidebar.text_input("GROQ_API_KEY",type="password")
TAVILY_API_KEY = st.sidebar.text_input("TAVILY_API_KEY",type="password")

if not (GOOGLE_API_KEY) and not (GROQ_API_KEY) and not (TAVILY_API_KEY):
    st.sidebar.warning("PASS API KEYS")
    st.stop()
else: 
    st.success("API KEYS LOADED")
    
# ===============MODEL BUILDING=============
model = ChatGoogleGenerativeAI(
    model = 'gemini-3.5-flash-lite',
    google_api_key = GOOGLE_API_KEY
)

# tool
def search_recent_news_jobs(query):
  """This function helps to search
  recent news or recent jobs
  related to given search query
  suppose user write Python Developer jobs
  It should return trending news and jobs link"""
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


# ==== PROMPT GENERATOR================
def prompt_generator(agent = agent):
  """This function help to give detailed prompt
  followed by Chain of thoughts and
  persona based prompting, main task is to give
  detailed prompt to build Resume for
  Students or Experienced person
  Based on their given personal information."""

  prompt = """You are a senior HR resume analyzer,
  main task is to give
  detailed prompt to build Resume for
  Students or Experienced person
  Based on their given personal information.
  System Instruction I want Model to generate resume
  in HTML format , include that in prompt"""

  response = agent.invoke(prompt)
  file_name = 'prompt.py'
  with open(file_name, 'w') as f:
    f.write(response.content[-1]['text'])
  return "Prompt file generated Successfully, agent can read it"

prompt_generator(model)
# tool 2:
def resume_maker_prompt():
  """This function just gives
  updated prompt for model"""

  with open('prompt.py', 'r') as f:
    prompt = f.read()
  return prompt

resume_maker_prompt()

# ==================u[upload image===============

uploaded_file = st.sidebar.file_uploader(
    "Choose an image file",
    type=["jpg", "jpeg", "png", "webp"]
)

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)

        st.sidebar.image(image, caption="Uploaded Image", use_container_width=True)

        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        base_name = os.path.splitext(uploaded_file.name)[0]
        save_path = f"{base_name}.jpg"

        # 3. Save the image to the current working directory
        image.save(save_path, "JPEG")
        st.sidebar.success(f"🎉 Image successfully saved as `{save_path}`!")

    except Exception as e:
        st.error(f"Error processing image: {e}")

# ===========GENERATE RESUME========
prompt = """
You are a Senior UI/UX Designer and Professional HR Resume Expert.

Your task is to generate a world-class ATS-friendly resume in ONE HTML file.

Design Requirements:

Modern Canva Pro style
Different color theme every generation
Professional gradient headings
CSS Grid Layout
Two-column design
Rounded cards
Glassmorphism effects
Soft shadows
Google Font: Poppins
Font Awesome Icons
Smooth hover animations
Responsive Design
Elegant spacing
Beautiful typography
Skills displayed as colorful badges
Education displayed as a timeline
Projects inside modern cards
Contact section with icons
Professional summary in a highlighted card
Modern footer

Color Theme:
Choose a unique modern palette every time.
Examples:
- Navy + Cyan
- Purple + Pink
- Emerald + Teal
- Orange + Dark Gray
- Black + Gold

Do NOT always use blue.

Use modern CSS.

Everything must be inside ONE HTML file.

Do not use external CSS files.

Do not use external JS files.

Include CSS and JavaScript inside the HTML.

The resume should look like it was designed by a professional UI designer.

IMPORTANT:

Wherever the profile photo should appear, use EXACTLY this:

<img src="PROFILE_IMAGE_PLACEHOLDER" style="width:120px;height:120px;border-radius:50%;object-fit:cover;">

Return ONLY HTML code.
"""

final_prompt = prompt + resume_maker_prompt()

user_info = st.text_area("Enter your information")

user_details = f"""user details: given below:
Resume info: {user_info}
Photo: {uploaded_file}
Photo present in current directory with name as uploaded_file,
and once resume generated give download button in same html code.
Default if not given: Give Python Developoer Resume"""

query = final_prompt + user_details

OPTIONS = ["Delhi", "Noaida", "gurgaon", "Gurugram", "Kanpur", "Lakhnow", "Banglore", "Pune"]

LOCATION = st.sidebar.multiselect('SELECT LOCATION: ',
                                  options = OPTIONS)

JOB_PROFILE = ["PYTHON DEVELOPER",'GEN AI',
               'FULL-STACK DEVELOPER','DATA ANALYST']

PROFILE = st.sidebar.multiselect("SELECT JOB ROLE",
                                 options = JOB_PROFILE)


job_prompt = f"""Based on {PROFILE} jobs in {LOCATION}, I
want latest job news in using tavily,
try top 10 search or whatever available
and give result like naukri theme design with
job name, job desc, salary,
apply link and OUTPUT must be in HTML no markdowns"""

if st.button('generate resume'):
  with st.spinner("running agent"):

    response = agent.invoke({'messages': [{'role':'user','content':query}]})
    print(response['messages'][-1].content)
    code=response['messages'][-1].content[-1]['text']
    #st.html(code , width="stretch" , unsafe_allow_javascript=True)
    # swap in the actual uploaded photo instead of the placeholder tag
    if uploaded_file  is not None:
        with open(save_path, "rb") as img_file:
            b64_image = base64.b64encode(img_file.read()).decode()
        data_uri = f"data:image/jpeg;base64,{b64_image}"
        code = code.replace("PROFILE_IMAGE_PLACEHOLDER", data_uri)
      
    st.html(code , width="stretch" , unsafe_allow_javascript=True)
    st.divider()
    response = agent.invoke({'messages': [{'role':'user','content': job_prompt}]})

    job_code = response['messages'][-1].content[-1]['text']



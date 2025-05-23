import streamlit as st
from PIL import Image

st.set_page_config(
    page_icon=":page_with_curl:", page_title="Resume | Aakrit", layout="wide"
)

st.markdown(
    """

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous"> 
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>


<nav class="navbar fixed-bottom" >
 <div class="container-fluid">
  <!-- CSS-only toggle for mobile -->
  <input type="checkbox" id="navbarToggle" />
  <label id="navbarToggleLabel" for="navbarToggle" class="navbar-toggler">
      <span class="navbar-toggler-icon"></span>
  </label>
  
  <!--
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#mainNav" aria-controls="mainNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  -->
  
  <div class="navbar-collapse" id="mainNav">
    <ul class="navbar-nav ms-auto">
      <li class="nav-item">
        <a class="nav-link" href="#summary">Summary</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#education">Education</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#work-experience">Work Experience</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#skills">Skills</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#research-papers">Research Papers</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#tools-built">Tools Built</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#social-media">Social Media</a>
      </li>
    </ul>
  </div>
  <div class="container-fluid nav-brand">
  <a class="navbar-brand" href="#aakrit-sharma-lamsal" title="Go to Top" >Aakrit Sharma Lamsal</a>
 </div>
 </div>
</nav>
""",
    unsafe_allow_html=True,
)

with open("style.css") as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)


#####################
# Header

image = Image.open("aakrit-cv-pic.png")
st.image(image, width=150)

st.write(
    """
# Aakrit Sharma Lamsal
# B. Tech. CSE | Software Engineer | Data Science Enthusiast
#### *Resume* 
"""
)
st.markdown("## Summary", unsafe_allow_html=True)
st.info(
    """
- Driven software engineer with 2+ years of experience leveraging AI and data science expertise to tackle real-world challenges.
- Successfully spearheaded the development and deployment of NLP models, Retrieval Augmented Generation(RAG) using LLMs.
- Gained hands-on experience with streamlining CI/CD pipelines and building user-friendly POC dashboards.
-  Skilled in diverse areas like machine learning, NLP, data analysis, SQL, ORMs, and API development.
"""
)


#####################
# Custom function for printing text
def txt(a, b):
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(a)
    with col2:
        st.markdown(b)


def txt2(a, b):
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown(f"`{a}`")
    with col2:
        st.markdown(b)


def txt3(a, b):
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(a)
    with col2:
        st.markdown(b)


def txt4(a, b, c):
    col1, col2, col3 = st.columns([1.5, 2, 2])
    with col1:
        st.markdown(f"`{a}`")
    with col2:
        st.markdown(b)
    with col3:
        st.markdown(c)


def tools_built(nm: str, desc: str, link: str):
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown(
            f'{nm} - <a href="{link}" target="_blank" style="color:#f38023e7;font-style:italics;">link</a>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(f" - {desc}")


#####################
st.markdown(
    """
## Education
"""
)

txt(
    "**HighSchool Degree - NEB Board** (Science with Physics major), *United Academy*, Kumaripati, Lalitpur, Nepal",
    "2015-2017",
)
st.markdown(
    """
- Percentage: `78.9%`
"""
)

txt(
    "**Bachelors of Technology** (Computer Science Engineering), *Vellore Institute of Technology*, India",
    "2018-2022",
)
st.markdown(
    """
- GPA: `8.77`
- Obtained SAARC Scholarship for academic achievements.
"""
)

#####################
st.markdown(
    """
## Work Experience
"""
)

txt("**Software Engineer Intern**, Intralinks, SSC", "Feb,2022-June,2022")
st.markdown(
    """
- Worked with MERN stack in building a global translation repository capable of translating page text and attributes in 18 different languages.
- Used ReactJS, and Mongodb to store page data and company provided translation terms.
- Built web application using ExpressJS and presented a demo to the dev teams for incorporating the application into the existing user-end applications.
"""
)

txt("**Associate Software Engineer, AI-COE**, Intralinks, SSC", "2022-2024")
st.markdown(
    """
- Worked in the AI-COE team with focus on building AI models and services to cater users with various intelligent features. 
- Actively worked on reviewing research papers to and bring concepts into implementations.
- Built and developed model layer APIs and pipelines to handle load and cater various services in a microservices archetecture software development approach.
- Worked with various databases, including vector databases to aid AI models and handle AI workflows.
- Analysed company gathered data for experimenting with various AI model training with the goal to assist and optimize user experience.
- Trained, tested, and validated multiple AI models including building Proof of Concepts demo dashboard using streamlit, gradio, and Flask.
"""
)


#######
st.markdown(
    """
## Research Papers
 """
)

txt(
    "**Directed Energy Deposition via Artificial Intelligence Enabled Approaches**, https://onlinelibrary.wiley.com/doi/10.1155/2022/2767371",
    "2022",
)
st.markdown(
    """
- Research article on AI approach to Directed Energy Deposition
- Reviewed `115+` research papers to write a detailed review of AI approach to manufacturing process using Directed Energy Deposition 
"""
)

st.markdown(
    """
## Tools built
"""
)

tools_built(
    "Text Extraction",
    "Extracts text from scanned media such as image and pdf. Uses poppler utils and pytesseract to process the user upload and extract the text from image.",
    "https://extract-text.streamlit.app",
)
tools_built(
    "Object Detector",
    "Detects objects from any image and list them out along with bounding box.",
    "https://huggingface.co/spaces/aakrit7/detect-and-list-objects",
)

tools_built(
    "Agentic Chatbot",
    "Agent based LLM using Langchain and Langgraph capable of scraping news article and assist user. Scraping tool will be called by LLM to fetch news from user given prompt and added to the context.",
    "HTTP://ai-news-interpreter.streamlit.app",
)

tools_built(
    "Resume Analyzer",
    "Analyses and gives constructive and meaningful feedback to improve the resume for a targeted job position. Uses langchain, pdf2image, and Google Gen AI's multimodal capabilities. The tool is not just for analyzing the content, but also the formatting and overall structure of the resume. Embedded with chat features to discuss on the resume.",
    "https://resume-analyzer-101.streamlit.app",
)

tools_built(
    "LLM Standoff",
    "Utilizes huggingface models using langchain to compare various LLM responses for a given prompt. Helps to analyze and compare opensource models for our specific usecase. ",
    "https://huggingface.co/spaces/aakrit7/gradio_model_comparison",
)

tools_built(
    "LLM Ayee",
    "A smart, pirate themed LLM that can assist users with various text based tasks. Built in humor added to the LLM output along with the conversation chain for chaining chat history into the LLM context.",
    "https://huggingface.co/spaces/aakrit7/pirate-llm-gradio",
)

tools_built(
    "Web Portfolio via Streamlit",
    "A customized UI portfolio made using streamlit. Custom styling and design for an appealing portfolio to showcase various clients about the projects, achievements, and experience.",
    "https://aakrit-resume.streamlit.app",
)

#####################
st.markdown(
    """
## Skills
"""
)
txt3("Programming", "`Python`, `Linux`")
txt3("Data processing/wrangling", "`SQL`, `pandas`, `numpy`")
txt3("Data visualization", "`matplotlib`, `seaborn`")
txt3("Machine Learning", "`scikit-learn`, `scipy`, `langchain`, `langgraph`")
txt3("Deep Learning", "`pytorch`, `TensorFlow`, `keras`")
txt3("Web development", "`Flask`, `HTML`, `CSS`, `Django`, `FastAPI`")
txt3("Model deployment", "`streamlit`, `gradio`,`AWS`")
txt3("CI/CD", "`Jenkins`, `Github actions`")

#####################
st.markdown(
    """
## Social Media
"""
)

txt2("LinkedIn", "https://www.linkedin.com/in/asl7")
txt2("GitHub", "https://github.com/aakrit1155/")
txt2("ORCID", "https://orcid.org/0000-0003-3105-8056")
txt2("HuggingFace", "https://huggingface.co/spaces/aakrit7/")
txt2("Streamlit Profile", "https://share.streamlit.io/user/aakrit1155")

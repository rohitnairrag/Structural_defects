import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import datetime as dt

# ----------------- CONFIG -----------------
# Configure the model
key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# ----------------- CUSTOM STYLING -----------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #e2e8f0;
    }

    .stApp {
        background: #0d1117; /* blackish background */
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 2px solid #2d3748;
        padding: 20px 10px;
    }

    /* Titles */
    .main-title {
        font-size: 36px;
        font-weight: 700;
        color: #f8f9fa;
        text-align: center;
        margin-top: -10px;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 18px;
        font-weight: 400;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 25px;
    }

    /* Tips box */
    .tips-box {
        background-color: #161b22;
        padding: 18px 22px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.5);
        margin-bottom: 30px;
        font-size: 15px;
        line-height: 1.6;
    }

    /* Input labels */
    label {
        font-weight: 600 !important;
        color: #63b3ed !important;
    }

    /* Buttons */
    div.stButton > button {
        background-color: #e67e22;
        color: white;
        font-weight: 600;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #ca6f1e;
        transform: scale(1.03);
    }

    /* Report section */
    .report-title {
        font-size: 22px;
        font-weight: 700;
        margin-top: 30px;
        margin-bottom: 15px;
        color: #f8f9fa;
    }

    /* Images */
    img {
        border-radius: 12px !important;
        box-shadow: 0px 4px 12px rgba(255,255,255,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------- SIDEBAR -----------------
st.sidebar.image(
    "https://static.thenounproject.com/png/building-inspection-icon-5472788-512.png", 
    use_container_width=True
)
st.sidebar.title("📤 :orange[Upload Your Structure Image]")
uploaded_image = st.sidebar.file_uploader("Upload Here", type=['jpeg', 'jpg', 'png'])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.sidebar.subheader("🖼️ :blue[Uploaded Image]")
    st.sidebar.image(image)

# ----------------- MAIN PAGE -----------------
st.markdown('<div class="main-title">🏗️ Structural Defects</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">🤖 AI-assisted defect identifier for the construction industry</div>', unsafe_allow_html=True)

# Tips (bullet points with clean indentation)
tips = """
👷 **How to use this app:**  

- ① **Upload the structure image** 🏢  
- ② **Click "Generate Report"** 📑  
- ③ **Download your AI-powered defect report** 💾  
"""
st.markdown(f'<div class="tips-box">{tips}</div>', unsafe_allow_html=True)

# Report Inputs
rep_title = st.text_input("📝 Report Title:")
prep_by = st.text_input("👨‍💻 Report Prepared by:")
prep_for = st.text_input("👷 Report Prepared for:")

# ----------------- PROMPT -----------------
prompt = f"""
Assume you are a structural engineer. The user has provided an image of a structure. 
You need to identify the structural defects in the image and generate a report. 
The report should contain the following:

- Start with title, prepared by, and prepared for details from user input.  
- Use {rep_title} as report title, {prep_by} as prepared by, {prep_for} as prepared for.  
- Mention current date: {dt.datetime.now().date()}.  
- Identify and classify defects (e.g., cracks, spalling, corrosion, honeycombing).  
- There could be multiple defects; identify each separately.  
- For each defect: description, potential impact, severity (low/medium/high).  
- Estimate time before permanent damage.  
- Suggest short-term & long-term solutions with estimated cost (INR) & time.  
- Add preventive measures for future.  
- Format in bullet points and tables where possible.  
- Report should not exceed 3 pages.  
"""

# ----------------- REPORT GENERATION -----------------
if st.button("🚧 Generate Report"):
    if uploaded_image is None:
        st.warning("⚠️ Please upload a building/structure image to generate the report.")
    else:
        with st.spinner("⏳ Inspecting structure & generating report..."):
            response = model.generate_content(
                [prompt, image], 
                generation_config={"temperature": 0.7, "top_k": 0}
            )

            st.markdown('<div class="report-title">📄 Inspection Report</div>', unsafe_allow_html=True)
            st.write(response.text)

        # Save as .txt
        with open("structural_defect_report.txt", "w") as file:
            file.write(response.text)

        with open("structural_defect_report.txt", "rb") as file:
            st.download_button(
                label="📥 Download Report",
                data=file,
                file_name="structural_defect_report.txt",
                mime="text/plain"
            )

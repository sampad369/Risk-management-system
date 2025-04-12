import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key="AIzaSyDKeOfvEGUep4jpI0C0d4HKf5ScjCcR-XA")

# Set up the model
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

# Initialize models for both agents
risk_analysis_model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

risk_management_model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Define agent prompts
RISK_ANALYSIS_PROMPT = """You are a Risk Analysis AI Agent. Your task is to:
1. Analyze the provided business context, project details, or operational scenario
2. Identify potential risks across various categories (financial, operational, strategic, compliance, etc.)
3. Assess the likelihood and potential impact of each risk
4. Provide a comprehensive risk assessment report

Format your response with:
- Risk Category
- Specific Risk Description
- Likelihood (Low/Medium/High)
- Potential Impact (Low/Medium/High)
- Initial Observations

Input: {user_input}"""

RISK_MANAGEMENT_PROMPT = """You are a Risk Management AI Agent. Your task is to:
1. Review the identified risks from the Risk Analysis Agent
2. Develop mitigation strategies for each significant risk
3. Suggest contingency plans for high-impact risks
4. Recommend monitoring and control mechanisms
5. Provide a prioritized action plan

Format your response with:
- Risk Description
- Mitigation Strategy
- Responsible Party
- Timeline
- Monitoring Approach

Identified Risks: {risk_analysis_results}"""

# Streamlit UI
st.set_page_config(page_title="AI-Powered Risk Management System", layout="wide")

st.title("AI-Powered Risk Management System")
st.subheader("Powered by Gemini API")

# Initialize session state
if 'risk_analysis_results' not in st.session_state:
    st.session_state.risk_analysis_results = None
if 'risk_management_plan' not in st.session_state:
    st.session_state.risk_management_plan = None

# Sidebar for system info
with st.sidebar:
    st.header("System Configuration")
    st.markdown("""
    **Agents:**
    - Risk Analysis Agent
    - Risk Management Agent
    """)
    st.divider()
    st.info("This system helps identify and manage risks using AI agents powered by Gemini.")

# Main interface tabs
tab1, tab2 = st.tabs(["Risk Analysis", "Risk Management"])

with tab1:
    st.header("Risk Analysis Agent")
    user_input = st.text_area(
        "Describe your business scenario, project details, or operational context for risk analysis:",
        height=200,
        placeholder="e.g., 'We are launching a new fintech product in Southeast Asia targeting underbanked populations...'")

    if st.button("Analyze Risks"):
        if user_input.strip():
            with st.spinner("Analyzing potential risks..."):
                try:
                    # Call Risk Analysis Agent
                    response = risk_analysis_model.generate_content(
                        RISK_ANALYSIS_PROMPT.format(user_input=user_input)
                    )
                    st.session_state.risk_analysis_results = response.text
                    st.success("Risk analysis completed!")
                    st.markdown("### Risk Analysis Report")
                    st.markdown(st.session_state.risk_analysis_results)
                except Exception as e:
                    st.error(f"Error in risk analysis: {str(e)}")
        else:
            st.warning("Please provide context for risk analysis")

with tab2:
    st.header("Risk Management Agent")

    if st.session_state.risk_analysis_results:
        st.markdown("### Identified Risks from Analysis Agent")
        st.markdown(st.session_state.risk_analysis_results)

        if st.button("Develop Risk Management Plan"):
            with st.spinner("Creating mitigation strategies..."):
                try:
                    # Call Risk Management Agent
                    response = risk_management_model.generate_content(
                        RISK_MANAGEMENT_PROMPT.format(risk_analysis_results=st.session_state.risk_analysis_results)
                    )
                    st.session_state.risk_management_plan = response.text
                    st.success("Risk management plan created!")
                    st.markdown("### Risk Management Plan")
                    st.markdown(st.session_state.risk_management_plan)
                except Exception as e:
                    st.error(f"Error in creating management plan: {str(e)}")
    else:
        st.warning("Please complete the risk analysis first")

# Add some styling
st.markdown("""
<style>
    .stTextArea textarea {
        min-height: 200px;
    }
    .stMarkdown {
        padding: 15px;
        background-color: #f8f9fa;
        border-radius: 10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)
import streamlit as st
from core.config import GROQ_API_KEY
from ui.candidate_form import candidate_form
from ui.interview_flow import ask_questions, evaluate_answers
from core.llm_wrapper import LLMWrapper
import json, re

# -----------------------
st.set_page_config(page_title="TalentScout Chatbot", layout="wide")
st.title("🚀 TalentScout — Intelligent Hiring Assistant")

# ---------------- Sidebar Settings ----------------
with st.sidebar:
    st.header("Settings")
    provider = st.selectbox("LLM Provider", ["Groq"], index=0).lower()
    api_key = st.text_input(f"{provider.upper()} API Key", value=GROQ_API_KEY if GROQ_API_KEY else "", type="password")
    model_name = st.selectbox("Model", ["llama3-8b-8192", "llama-3.1-8b-instant"], index=0)
    
    if st.button("Clear Chat"):
        for key in ["messages", "candidate", "questions", "current_q", "answers", "chain", 
                    "consent", "bot_intro", "agree_yes", "agree_no"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()


# ---------------- Initialize session state ----------------
for key in ["messages","candidate","questions","current_q","answers"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key != "candidate" else {}
if "consent" not in st.session_state:
    st.session_state.consent = None
if "bot_intro" not in st.session_state:
    st.session_state.bot_intro = False

# ---------------- Bot Introduction ----------------
if not st.session_state.bot_intro:
    # Load chain if not already loaded
    if "chain" not in st.session_state and api_key:
        @st.cache_resource
        def load_chain(provider, api_key, model_name):
            return LLMWrapper(provider=provider, api_key=api_key, model_name=model_name)
        st.session_state.chain = load_chain(provider, api_key, model_name)

    # Generate bot introduction dynamically
    bot_intro_text = ""
    if st.session_state.chain:
        intro_prompt = """
Introduce yourself as TalentScout in a friendly style.
Explain you are an intelligent hiring assistant. Mention that you will guide
the candidate through the form, collect education and work experience details,
and generate tailored technical interview questions.
Respond only with the introduction text, no JSON, no extra formatting.
End with "Do you want to proceed?"
"""
        try:
            full_response = "".join([c for c in st.session_state.chain.stream(intro_prompt)])
            # Clean up response in case LLM outputs JSON accidentally
            if full_response.strip().startswith("{") and "message" in full_response:
                data = json.loads(full_response)
                bot_intro_text = data.get("message", "")
            else:
                bot_intro_text = full_response.strip()
        except Exception:
            bot_intro_text = (
                "Hi there! I'm TalentScout, your intelligent hiring assistant. "
                "I'm here to help you navigate the hiring process with ease. "
                "I can guide you through the candidate information form, collect your education and work experience, "
                "and generate tailored technical interview questions. Do you want to proceed?"
            )
    else:
        bot_intro_text = (
            "Hi there! I'm TalentScout, your intelligent hiring assistant. "
            "I'm here to help you navigate the hiring process with ease. "
            "I can guide you through the candidate information form, collect your education and work experience, "
            "and generate tailored technical interview questions. Do you want to proceed?"
        )

    st.subheader("🤖 TalentScout says:")
st.info(bot_intro_text)

# Initialize toggle state in session_state
if "agree_yes" not in st.session_state:
    st.session_state.agree_yes = False
if "agree_no" not in st.session_state:
    st.session_state.agree_no = False

# Toggle checkboxes
agree_yes = st.checkbox("✅ Yes, I want to proceed", value=st.session_state.agree_yes)
agree_no = st.checkbox("❌ No, I do not want to proceed", value=st.session_state.agree_no)

# Enforce toggle behavior
if agree_yes:
    st.session_state.agree_yes = True
    st.session_state.agree_no = False
elif agree_no:
    st.session_state.agree_yes = False
    st.session_state.agree_no = True
else:
    st.session_state.agree_yes = False
    st.session_state.agree_no = False

# Handle consent
if st.session_state.agree_yes:
    st.session_state.consent = True
    st.session_state.bot_intro = True
    st.success("Great! Let's start the process.")
elif st.session_state.agree_no:
    st.session_state.consent = False
    st.session_state.bot_intro = True
    st.warning("Thank you for your time. You can restart anytime.")
    st.stop()
# else -> both unchecked, wait for user input


# ---------------- Candidate Form ----------------
if st.session_state.consent:
    if candidate_form():
        chain = st.session_state.get("chain")
        if chain:
            candidate = st.session_state.candidate
            prompt_text = f"""
Candidate: {candidate}

Generate ONLY 3 to 5 technical interview questions TOTAL.
Return STRICT JSON ONLY.
JSON Format:
{{
  "questions": [
    {{"question": "string", "expected_answer_outline": "string"}}
  ]
}}
"""
            try:
                full_response = "".join([c for c in chain.stream(prompt_text)])
                try:
                    q_json = json.loads(full_response.strip())
                except json.JSONDecodeError:
                    match = re.search(r"\{.*\}", full_response, re.DOTALL)
                    q_json = json.loads(match.group()) if match else {}
                st.session_state.questions = q_json.get("questions", [])[:5]
                if st.session_state.questions:
                    st.success("✅ Candidate info collected. Let's start the interview!")
            except Exception as e:
                st.error(f"Error generating questions: {e}")

# ---------------- Interview Flow ----------------
ask_questions(st.session_state.get("chain"))
evaluate_answers(st.session_state.get("chain"))

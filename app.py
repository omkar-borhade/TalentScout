import streamlit as st
from core.config import GROQ_API_KEY
from ui.candidate_form import candidate_form
from ui.interview_flow import ask_questions, evaluate_answers
from chains.question_chain import get_question_chain

# -----------------------
# Streamlit App
# -----------------------
st.set_page_config(page_title="TalentScout Chatbot", layout="wide")
st.title("🚀 TalentScout — Intelligent Hiring Assistant")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("GROQ API Key", value=GROQ_API_KEY if GROQ_API_KEY else "", type="password")
    model_name = st.selectbox("Model", ["llama3-8b-8192", "llama-3.1-8b-instant"], index=0)
    if st.button("Clear Chat"):
        for key in ["messages","candidate","questions","current_q","answers","chain"]:
            if key in st.session_state: del st.session_state[key]
        st.rerun()

if "messages" not in st.session_state: st.session_state.messages = []
if "candidate" not in st.session_state: st.session_state.candidate = {}
if "questions" not in st.session_state: st.session_state.questions = []
if "current_q" not in st.session_state: st.session_state.current_q = 0
if "answers" not in st.session_state: st.session_state.answers = []

if candidate_form():
    if "chain" not in st.session_state:
        @st.cache_resource
        def load_chain(api_key, model_name):
            return get_question_chain(api_key, model_name)
        st.session_state.chain = load_chain(api_key, model_name)

    chain = st.session_state.chain
    if chain:
        candidate = st.session_state.candidate
        prompt_text = f"""
Candidate: {candidate}

Generate ONLY 2 technical interview questions TOTAL.
Return STRICT JSON ONLY, nothing else.
JSON Format:
{{
  "questions": [
    {{"question": "string", "expected_answer_outline": "string"}},
    {{"question": "string", "expected_answer_outline": "string"}}
  ]
}}
"""
        try:
            full_response = "".join([c for c in chain.stream({"question": prompt_text})])
            import json, re
            try:
                q_json = json.loads(full_response.strip())
            except json.JSONDecodeError:
                match = re.search(r"\{.*\}", full_response, re.DOTALL)
                q_json = json.loads(match.group()) if match else {}
            st.session_state.questions = q_json.get("questions", [])[:2]
            if st.session_state.questions:
                st.success("✅ 2 Questions Generated. Let's start!")
        except Exception as e:
            st.error(f"Error generating questions: {e}")

ask_questions(st.session_state.get("chain"))
evaluate_answers(st.session_state.get("chain"))

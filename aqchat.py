import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os, json, hashlib
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# -----------------------
# Config
# -----------------------
default_api_key = os.getenv("GROQ_API_KEY")
EXIT_KEYWORDS = {"exit", "quit", "bye", "goodbye", "stop", "end"}
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
DATA_FILE = os.path.join(DATA_DIR, "candidates.json")
SALT = os.getenv("DATA_SALT", "replace_with_random_salt")

# -----------------------
# Helpers
# -----------------------
def _hash(value: str) -> str:
    return hashlib.sha256((SALT + str(value)).encode("utf-8")).hexdigest()[:16]

def anonymize_candidate(candidate: dict) -> dict:
    return {
        "id": _hash(candidate.get("email","")+candidate.get("phone","")),
        "name_hash": _hash(candidate.get("name","")),
        "email_hash": _hash(candidate.get("email","")),
        "phone_hash": _hash(candidate.get("phone","")),
        "years_exp": candidate.get("years_exp"),
        "desired_positions": candidate.get("desired_positions"),
        "location": candidate.get("location"),
        "tech_stack": candidate.get("tech_stack", []),
        "created_at": datetime.utcnow().isoformat()+"Z"
    }

def save_candidate(candidate: dict):
    records = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                records = json.load(f)
        except Exception:
            records = []
    records.append(candidate)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

# -----------------------
# Streamlit UI
# -----------------------
st.set_page_config(page_title="TalentScout Chatbot", layout="wide")
st.title("🚀 TalentScout — Intelligent Hiring Assistant")

# Sidebar
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("GROQ API Key", value=default_api_key if default_api_key else "", type="password")
    model_name = st.selectbox("Model", ["llama3-8b-8192", "llama-3.1-8b-instant"], index=0)
    if st.button("Clear Chat"):
        for key in ["messages","candidate","questions","current_q","answers"]:
            if key in st.session_state: del st.session_state[key]
        st.rerun()

# -----------------------
# Session State
# -----------------------
if "messages" not in st.session_state: st.session_state.messages = []
if "candidate" not in st.session_state: st.session_state.candidate = {}
if "questions" not in st.session_state: st.session_state.questions = []
if "current_q" not in st.session_state: st.session_state.current_q = 0
if "answers" not in st.session_state: st.session_state.answers = []

# -----------------------
# Candidate Form
# -----------------------
with st.form("candidate_form"):
    st.subheader("Candidate Information")
    name = st.text_input("Full Name", st.session_state.candidate.get("name",""))
    email = st.text_input("Email", st.session_state.candidate.get("email",""))
    phone = st.text_input("Phone Number", st.session_state.candidate.get("phone",""))
    years_exp = st.number_input("Years of Experience", min_value=0, max_value=80, value=int(st.session_state.candidate.get("years_exp",0)))
    desired_positions = st.text_input("Desired Positions (comma separated)", ",".join(st.session_state.candidate.get("desired_positions",[])))
    location = st.text_input("Current Location", st.session_state.candidate.get("location",""))
    tech_stack_raw = st.text_area("Tech Stack (comma separated)", ",".join(st.session_state.candidate.get("tech_stack_raw",[])))
    submitted = st.form_submit_button("Save & Start Mini Interview")

if submitted:
    tech_list = [t.strip() for t in tech_stack_raw.split(",") if t.strip()]
    candidate = {
        "name": name.strip(),
        "email": email.strip(),
        "phone": phone.strip(),
        "years_exp": int(years_exp),
        "desired_positions": [p.strip() for p in desired_positions.split(",") if p.strip()],
        "location": location.strip(),
        "tech_stack": tech_list,
        "tech_stack_raw": tech_stack_raw
    }
    st.session_state.candidate = candidate
    save_candidate(anonymize_candidate(candidate))

    st.session_state.questions, st.session_state.answers, st.session_state.current_q = [], [], 0

    if "chain" not in st.session_state:
        @st.cache_resource
        def get_chain(api_key, model_name):
            if not api_key: return None
            llm = ChatGroq(groq_api_key=api_key, model_name=model_name, temperature=0.2, streaming=True)
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are TalentScout Assistant. ONLY return valid JSON, no explanations."),
                ("user", "{question}")
            ])
            return prompt | llm | StrOutputParser()
        
        st.session_state.chain = get_chain(api_key, model_name)

    # chain = get_chain(api_key, model_name)
    chain = st.session_state.chain

    if not chain:
        st.warning("Enter your Groq API key.")
    else:
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

            # Try parsing strictly
            try:
                q_json = json.loads(full_response.strip())
            except json.JSONDecodeError:
                # Fallback: extract JSON substring if extra text wrapped
                import re
                match = re.search(r"\{.*\}", full_response, re.DOTALL)
                if match:
                    q_json = json.loads(match.group())
                else:
                    raise

            st.session_state.questions = q_json.get("questions", [])[:2]
            if st.session_state.questions:
                st.success("✅ 2 Questions Generated. Let's start!")
            else:
                st.error("⚠️ No questions found in response.")

        except Exception as e:
            st.error(f"Error generating questions: {e}")
            st.text(full_response)  # Debug: show raw response


# -----------------------
# Question Flow
# -----------------------
if st.session_state.questions and st.session_state.current_q < len(st.session_state.questions):
    q = st.session_state.questions[st.session_state.current_q]
    st.markdown(f"**Question {st.session_state.current_q+1}: {q['question']}**")
    user_ans = st.text_area("Your Answer:", key=f"ans_{st.session_state.current_q}")
    if st.button("Submit Answer", key=f"submit_{st.session_state.current_q}"):
        st.session_state.answers.append({"q": q, "a": user_ans})
        st.session_state.current_q += 1
        st.rerun()

# -----------------------
# Final Evaluation Display
# -----------------------
if st.session_state.current_q >= 2 and st.session_state.answers:
    st.subheader("📊 Final Evaluation")

    chain = st.session_state.chain
    if not chain:
        st.warning("LLM chain not initialized. Please enter your API key.")
    else:
        eval_prompt = f"""
Evaluate the following answers. Score each (1–10) + give feedback.
Also return a final average score.
{json.dumps(st.session_state.answers, indent=2)}
JSON Format:
{{
  "results": [
    {{"question": "...", "score": 7, "feedback": "..."}}
  ],
  "final_average_score": 8
}}
"""
        try:
            # Stream evaluation from LLM
            evaluation_raw = "".join([c for c in chain.stream({"question": eval_prompt})])

            # Parse JSON safely
            import re
            try:
                evaluation_json = json.loads(evaluation_raw)
            except json.JSONDecodeError:
                match = re.search(r"\{.*\}", evaluation_raw, re.DOTALL)
                if match:
                    evaluation_json = json.loads(match.group())
                else:
                    st.error("Could not parse evaluation JSON")
                    st.text(evaluation_raw)
                    evaluation_json = None

            if evaluation_json:
                # Display each question's feedback
                for idx, item in enumerate(evaluation_json.get("results", []), 1):
                    st.markdown(f"**Question {idx}: {item.get('question')}**")
                    st.write(f"- Score: {item.get('score')}")
                    st.write(f"- Feedback: {item.get('feedback')}")
                    st.markdown("---")

                # Display final average
                final_score = evaluation_json.get("final_average_score")
                st.success(f"**Final Average Score: {final_score}**")

        except Exception as e:
            st.error(f"Error generating evaluation: {e}")
            st.text(evaluation_raw if 'evaluation_raw' in locals() else "No response received")

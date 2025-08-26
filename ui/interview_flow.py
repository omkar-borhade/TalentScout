import streamlit as st
import json, re

def ask_questions(chain):
    if st.session_state.questions and st.session_state.current_q < len(st.session_state.questions):
        q = st.session_state.questions[st.session_state.current_q]
        st.markdown(f"**Question {st.session_state.current_q+1}: {q['question']}**")
        user_ans = st.text_area("Your Answer:", key=f"ans_{st.session_state.current_q}")
        if st.button("Submit Answer", key=f"submit_{st.session_state.current_q}"):
            st.session_state.answers.append({"q": q, "a": user_ans})
            st.session_state.current_q += 1
            st.rerun()

def evaluate_answers(chain):
    # New check: only evaluate after all questions answered
    if st.session_state.questions and st.session_state.current_q >= len(st.session_state.questions) and st.session_state.answers:

        st.subheader("📊 Final Evaluation")
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
            evaluation_raw = "".join([c for c in chain.stream({"question": eval_prompt})])
            try:
                evaluation_json = json.loads(evaluation_raw)
            except json.JSONDecodeError:
                match = re.search(r"\{.*\}", evaluation_raw, re.DOTALL)
                evaluation_json = json.loads(match.group()) if match else None

            if evaluation_json:
                for idx, item in enumerate(evaluation_json.get("results", []), 1):
                    st.markdown(f"**Question {idx}: {item.get('question')}**")
                    st.write(f"- Score: {item.get('score')}")
                    st.write(f"- Feedback: {item.get('feedback')}")
                    st.markdown("---")
                st.success(f"**Final Average Score: {evaluation_json.get('final_average_score')}**")
        except Exception as e:
            st.error(f"Error generating evaluation: {e}")

## 🚀 TalentScout – Intelligent Recruitment Assistant

TalentScout is an AI-powered recruitment assistant designed to streamline the initial candidate screening process for technology-focused recruitment agencies. The platform collects candidate information, evaluates technical skills, and prepares the candidate for a mini-interview automatically.

This project demonstrates the integration of Streamlit for UI, dynamic forms, and advanced LLM features for intelligent question generation.

 **Note:** To run this project, you require a **Groq provider**, its **API key**, and one of the following models:  
 - "llama3-8b-8192"  
 - "llama-3.1-8b-instant"

## 🎥 Demo Video

https://github.com/omkar-borhade/TalentScout/demovideo/demo.mp4

 🌟 Features

📝 Dynamic Candidate Form
- Collects personal information: name, email, phone, and location.
- Handles both freshers and experienced professionals:
  - Freshers: Degree, domain, CGPA, 10th & 12th marks.
  - Experienced: Last company, years worked, and position.
- Desired position selection (single-select).
- Add / Remove skill slots dynamically.

 💻 Dynamic Technical Skills Section
- Add multiple technical skills using dropdown or custom text input.
- Mutually exclusive: selecting from dropdown hides the custom input, typing custom skill hides the dropdown.
- Pressing Enter immediately adds the custom skill to the list.
- Prevents duplicate skill selection in dropdowns.
- Add / Remove skill slots dynamically.

 📎 Additional Information
- LinkedIn profile, GitHub/portfolio link.
- Preferred job location.

 🔒 Data Storage & Anonymization
- Candidate details are anonymized before saving.
- Supports session management to retain form state during submission.

 🎯 Mini-Interview Ready
- Saves candidate data and initializes a mini-interview process.


 Technical Details

Technologies & Libraries Used:
- Python 3.x
- Streamlit – for interactive UI and forms
- JSON – for data storage
- OpenAI / LLM wrapper – for AI-powered question generation
- Custom utility functions in `core/utils.py`
- Modular LLM chains (`chains/eval_chain.py`, `chains/question_chain.py`) for interview workflow
- Session state handling in Streamlit for dynamic forms
- Optional: vector DB integration for future candidate skill similarity search

Architectural Decisions:
- Modular design separating UI (`ui/`), core logic (`core/`), and LLM question generation (`chains/`).
- Dynamic technical skill management to prevent duplicate entries.
- Dropdown + custom input combination for flexibility.
- Mini-interview flow initialized automatically after candidate submission.


 Prompt Design

- Prompts are crafted to first collect candidate basic info.
- Technical questions are generated based on the skills listed by the candidate.
- Prompts are designed to be context-aware:
  - Different prompts for freshers vs experienced candidates.
  - Adaptive questions based on previous answers in the mini-interview flow.
- LLM chain handles question ranking and relevance.


 Challenges & Solutions

- **Dynamic skill input handling**: Ensured dropdown and custom skill inputs are mutually exclusive and prevent duplicates.
  - Solution: Track selected skills and update session state accordingly.
- **Immediate addition of custom skills**: Prevent double pressing enter.
  - Solution: Added `on_change` callback to update skill state instantly.
- **Form state persistence**: Maintain previously entered data when adding/removing skill slots.
  - Solution: Used `st.session_state` for all dynamic inputs.
- **Dropdown latency for repeated selections**: Avoid showing already selected skills.
  - Solution: Filter options based on session state and previous selections.


 Usage Guide

1. Open the app in your browser via the Streamlit URL.
-app api key  if  you  have  also use modal **"llama3-8b-8192", "llama-3.1-8b-instant"** also use  **"Groq"** provider
- bot  introduce  him and  ask  you to  further  procide  click  yes  if  you want

2. Fill in the Candidate Information form:
- Select or type technical skills using the dynamic skill fields.
- For freshers, fill degree, domain, CGPA, and academic marks.
- For experienced candidates, fill last company, years, and position.
3. Click "Save & Start Mini Interview" to save candidate data and start the automated interview process.


 ⚙️ Installation

1. Clone the repository:
   git clone <repository-url>
   cd TalentScout

2. Create and activate a virtual environment:
   python -m venv venv
   # Windows
   venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Run the Streamlit app:
   streamlit run app/main.py


 🖥️ Usage

1. Open the app in your browser via the Streamlit URL.
2. Fill in the Candidate Information form:
   - Select or type technical skills using the dynamic skill fields.
   - For freshers, fill degree, domain, CGPA, and academic marks.
   - For experienced candidates, fill last company, years, and position.
3. Click Save & Start Mini Interview to save candidate data and start the automated interview process.

📁 Project Structure

```
TalentScout/
│
├── app.py                        # Streamlit main app
├── aqchat.py                     # Chat interface or integration
├── chains/                       # LLM chains
│   ├── __init__.py
│   ├── eval_chain.py
│   └── question_chain.py
├── core/                         # Core utilities and LLM wrappers
│   ├── __init__.py
│   ├── config.py
│   ├── llm_wrapper.py
│   └── utils.py
├── data/
│   └── candidates.json            # Candidate storage
├── ui/
│   ├── __init__.py
│   ├── candidate_form.py
│   └── interview_flow.py
├── .gitignore
├── .python-version
├── README.md
├── pyproject.toml
├── requirements.txt
└── uv.lock
```


 🔮 Future Improvements
- Integrate AI-powered interview question generation per candidate’s tech stack.
- Support multiple positions per candidate.


🤝 Contributing
Contributions are welcome! Please fork the repository and submit a pull request for improvements or bug fixes.

 📜 License
This project is licensed under the MIT License.

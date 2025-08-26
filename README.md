🚀 TalentScout – Intelligent Recruitment Assistant

TalentScout is an AI-powered recruitment assistant designed to streamline the initial candidate screening process for technology-focused recruitment agencies. The platform collects candidate information, evaluates technical skills, and prepares the candidate for a mini-interview automatically.

This project demonstrates the integration of Streamlit for UI, dynamic forms, and advanced LLM features for intelligent question generation.

🌟 Features

📝 Dynamic Candidate Form
- Collects personal information: name, email, phone, and location.
- Handles both freshers and experienced professionals:
  - Freshers: Degree, domain, CGPA, 10th & 12th marks.
  - Experienced: Last company, years worked, and position.
- Desired position selection (single-select).

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

⚙️ Installation

1. Clone the repository:
   git clone <repository-url>
   cd TalentScout

2. Create and activate a virtual environment:
   python -m venv venv
   # Linux / Mac
   source venv/bin/activate
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

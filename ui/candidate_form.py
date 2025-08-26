
import streamlit as st
from core.utils import save_candidate, anonymize_candidate

def candidate_form():
    st.subheader("Candidate Information")

    # --- Basic Info ---
    name = st.text_input("Full Name", st.session_state.candidate.get("name", ""))
    email = st.text_input("Email", st.session_state.candidate.get("email", ""))
    phone = st.text_input("Phone Number", st.session_state.candidate.get("phone", ""))
    years_exp = st.number_input(
        "Years of Experience",
        min_value=0, max_value=80,
        value=int(st.session_state.candidate.get("years_exp", 0)),
        key="years_exp"
    )

    # Desired Position (single select)
    job_roles = ["Select Position..."] + [
        "Software Engineer", "Data Scientist", "Machine Learning Engineer",
        "Full Stack Developer", "Backend Developer", "Frontend Developer",
        "DevOps Engineer", "Cloud Engineer", "QA Engineer", "Product Manager"
    ]
    desired_positions_list = st.session_state.candidate.get("desired_positions", [])
    default_index = job_roles.index(desired_positions_list[0]) if desired_positions_list and desired_positions_list[0] in job_roles else 0
    desired_position = st.selectbox(
        "Desired Position",
        options=job_roles,
        index=default_index
    )
    if desired_position == "Select Position...":
        desired_position = ""

    location = st.text_input("Current Location", st.session_state.candidate.get("location", ""))

    # --- Conditional Fields ---
    fresher_info, exp_info = {}, {}
    if years_exp == 0:
        st.subheader("Education Details (Fresher)")
        fresher_info["degree"] = st.text_input("Degree", st.session_state.candidate.get("degree", ""))
        fresher_info["domain"] = st.text_input("Domain / Branch", st.session_state.candidate.get("domain", ""))
        fresher_info["cgpa"] = st.text_input("CGPA / Percentage", st.session_state.candidate.get("cgpa", ""))
        fresher_info["marks_12th"] = st.text_input("12th Marks (%)", st.session_state.candidate.get("marks_12th", ""))
        fresher_info["marks_10th"] = st.text_input("10th Marks (%)", st.session_state.candidate.get("marks_10th", ""))
    else:
        st.subheader("Work Experience Details")
        exp_info["last_company"] = st.text_input("Last Company Worked", st.session_state.candidate.get("last_company", ""))
        years_val = 0
        val = st.session_state.candidate.get("years_in_company", "")
        try:
            years_val = int(val)
        except:
            years_val = 0

        exp_info["years_in_company"] = st.number_input(
            "Years Worked in Last Company",
            min_value=0, max_value=50,
            value=years_val
        )
        exp_info["position_in_company"] = st.text_input(
            "Position in Last Company", st.session_state.candidate.get("position_in_company", "")
        )

    st.subheader("Technical Skills")

    common_skills = ["Python", "Java", "JavaScript", "C++", "React", "Node.js", "Django", "SQL", "AWS", "Docker"]

    # Initialize session state
    if "skills" not in st.session_state:
        st.session_state.skills = [{"value": "", "type": "none"}]  # 'dropdown', 'custom', 'none'

    def add_skill():
        st.session_state.skills.append({"value": "", "type": "none"})

    def remove_skill():
        if len(st.session_state.skills) > 1:
            st.session_state.skills.pop()

    # Callback for custom skill input
    def update_custom_skill(idx):
        val = st.session_state[f"skill_custom_{idx}"]
        if val.strip() != "":
            st.session_state.skills[idx]["value"] = val.strip()
            st.session_state.skills[idx]["type"] = "custom"

    # Track dropdown selections to avoid duplicates
    selected_dropdowns = [s["value"] for s in st.session_state.skills if s["type"] == "dropdown"]

    for i, skill in enumerate(st.session_state.skills):
        st.markdown(f"**Skill {i+1}**")

        # Dropdown selection
        if skill["type"] in ["none", "dropdown"]:
            options = ["Select Skill..."] + [s for s in common_skills if s not in selected_dropdowns or s == skill["value"]]
            choice = st.selectbox(
                "",
                options,
                index=options.index(skill["value"]) if skill["value"] in options else 0,
                key=f"skill_dropdown_{i}"
            )
            if choice != "" and choice != "Select Skill...":
                st.session_state.skills[i]["value"] = choice
                st.session_state.skills[i]["type"] = "dropdown"
            elif skill["type"] != "custom":
                st.session_state.skills[i]["type"] = "none"
            selected_dropdowns.append(choice)

        # Custom text input
        if skill["type"] in ["none", "custom"]:
            st.text_input(
                "",
                value=skill["value"] if skill["type"] == "custom" else "",
                key=f"skill_custom_{i}",
                placeholder="Type custom skill here...",
                on_change=update_custom_skill,
                args=(i,)
            )

    # Add / Remove skill buttons
    col1, col2 = st.columns(2)
    with col1:
        st.button("➕ Add Skill", on_click=add_skill)
    with col2:
        if len(st.session_state.skills) > 1:
            st.button("➖ Remove Last Skill", on_click=remove_skill)

    # Final list of skills
    final_skills = [s["value"] for s in st.session_state.skills if s["value"].strip() != ""]



    # --- Additional Info ---
    st.subheader("Additional Information")
    linkedin = st.text_input("LinkedIn Profile", st.session_state.candidate.get("linkedin", ""))
    github = st.text_input("GitHub/Portfolio Link", st.session_state.candidate.get("github", ""))
    preferred_location = st.text_input("Preferred Job Location", st.session_state.candidate.get("preferred_location", ""))

     # --- Submit & Validation ---
    if st.button("Save & Start Mini Interview"):
        errors = []

        # Required fields check
        if not name.strip(): errors.append("Name is required.")
        if not email.strip(): errors.append("Email is required.")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email.strip()):
            errors.append("Email format is invalid.")
        if not phone.strip(): errors.append("Phone number is required.")
        elif not phone.strip().isdigit(): errors.append("Phone number must be numeric.")
        if not desired_position.strip(): errors.append("Please select a desired position.")
        if not location.strip(): errors.append("Location is required.")
        if not final_skills: errors.append("At least one skill must be added.")

        if errors:
            for err in errors:
                st.error(err)
            return False

       # Build main candidate dict
        candidate = {
            "name": name.strip(),
            "email": email.strip(),
            "phone": phone.strip(),
            "years_exp": int(years_exp),
            "desired_positions": [desired_position],
            "location": location.strip(),
            "linkedin": linkedin.strip(),
            "github": github.strip(),
            "preferred_location": preferred_location.strip(),
            "tech_stack": final_skills,
        }

        # Merge conditional fields
        if years_exp == 0:
            candidate.update(fresher_info)  # include fresher details
        else:
            candidate.update(exp_info)      # include experience details

        st.session_state.candidate = candidate
        save_candidate(anonymize_candidate(candidate))
        st.session_state.questions, st.session_state.answers, st.session_state.current_q = [], [], 0
        st.success("✅ Candidate saved!")
        return True

    return False
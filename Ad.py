import streamlit as st

# --- STREAMLIT UI CONFIGURATION ---
st.set_page_config(
    page_title="CollegeVine Simulator: Early Decision Strategy Engine",
    page_icon="🦅",
    layout="wide"
)

# --- SESSION STATE INITIALIZATION ---
if "transcript" not in st.session_state:
    st.session_state.transcript = {
        "8th Grade": [
            {"course": "AP Precalculus", "weight": "AP", "grade": "A", "credits": 1.0},
            {"course": "Honors English 9", "weight": "Honors", "grade": "A", "credits": 1.0},
            {"course": "German 1", "weight": "Regular", "grade": "A", "credits": 1.0},
            {"course": "US History", "weight": "Regular", "grade": "A", "credits": 1.0},
            {"course": "Physical Science", "weight": "Regular", "grade": "A", "credits": 1.0}
        ],
        "9th Grade": [], "10th Grade": [], "11th Grade": [], "12th Grade": []
    }

if "activities" not in st.session_state:
    st.session_state.activities = [
        {"name": "Financial Literacy & Business Camp", "tier": 1, "desc": "Founder. Free 2-week camp (9 AM - 3 PM).", "scale_plan": "User managed scaling path."},
        {"name": "German-English Music & Language Exchange", "tier": 1, "desc": "Founder. Hybrid chamber strings and language partner meetup.", "scale_plan": "User managed scaling path."},
        {"name": "AATG Study Abroad Competition", "tier": 2, "desc": "National German Exam candidate targeting travel scholarship.", "scale_plan": "User managed scaling path."},
        {"name": "CSYO Chamber Strings Cello", "tier": 2, "desc": "Cellist in Columbus Symphony Youth Orchestra.", "scale_plan": "User managed scaling path."},
        {"name": "Olentangy Marching Band", "tier": 3, "desc": "Instrumental performer. Fulfills Olentangy PE Waiver.", "scale_plan": "User managed scaling path."}
    ]

if "test_scores" not in st.session_state:
    st.session_state.test_scores = {
        "SAT Best Composite": 0,
        "ACT Composite": 0,
        "AP Exams Passed (Score 4/5)": 0,
        "AATG National German Exam Score": ""
    }

if "rec_letters" not in st.session_state:
    st.session_state.rec_letters = [
        {"role": "Math Teacher (AP Precalc/Calc)", "target": "Advanced Math Rigor & Analytical Spark", "status": "Plan to Secure"},
        {"role": "German Teacher (AP German)", "target": "Huntsman Language Mastery", "status": "Plan to Secure"},
        {"role": "Dr. Isil Erel (OSU Chair in Finance)", "target": "Elite Academic Research Validation", "status": "Cold Emailing / Outreach Phase"}
    ]

if "huntsman_essay_focus" not in st.session_state:
    st.session_state.huntsman_essay_focus = "The structural intersections of classical string history, Gujarati heritage, and modern transatlantic trade frameworks."

# --- PROBABILITY & METRICS LOGIC ---
def calculate_metrics():
    total_points, total_credits = 0.0, 0.0
    grade_points = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}

    for year, courses in st.session_state.transcript.items():
        for c in courses:
            cred = c["credits"]
            total_credits += cred
            base = grade_points.get(c["grade"], 4.0)
            bonus = 1.0 if c["weight"] == "AP" else (0.5 if c["weight"] == "Honors" else 0.0)
            total_points += (base + bonus) * cred

    return (total_points / total_credits) if total_credits > 0 else 4.0, total_credits

def calculate_chances(gpa, total_credits):
    wharton_base, huntsman_base = 5.0, 2.5

    # Transcript Rigor Weight
    wharton_base += (total_credits * 0.5) + (st.session_state.test_scores["AP Exams Passed (Score 4/5)"] * 1.5)
    huntsman_base += (total_credits * 0.4) + (st.session_state.test_scores["AP Exams Passed (Score 4/5)"] * 1.2)

    # Standardized Testing Modifiers
    sat = st.session_state.test_scores["SAT Best Composite"]
    act = st.session_state.test_scores["ACT Composite"]
    if sat >= 1550 or act >= 35:
        wharton_base += 6.0
        huntsman_base += 5.0
    elif sat >= 1500 or act >= 33:
        wharton_base += 3.0
        huntsman_base += 2.5

    # Extracurricular Tiers
    t1 = sum(1 for a in st.session_state.activities if a["tier"] == 1)
    t2 = sum(1 for a in st.session_state.activities if a["tier"] == 2)
    wharton_base += (t1 * 4.0) + (t2 * 1.5)
    huntsman_base += (t1 * 5.0) + (t2 * 2.0)

    # Recommendation Letter Status Modifiers (Dynamic Updates)
    for r in st.session_state.rec_letters:
        if r["status"] == "Secured & Confirmed":
            if "Erel" in r["role"]:
                wharton_base += 5.0
                huntsman_base += 4.5
            else:
                wharton_base += 1.0
                huntsman_base += 1.5

    if gpa < 3.9:
        wharton_base -= 5.0
        huntsman_base -= 4.0

    return {
        "ED_Wharton": max(min(wharton_base * 2.8, 49.5), 2.0),
        "ED_Huntsman": max(min(huntsman_base * 2.5, 38.0), 1.0)
    }

current_gpa, total_creds = calculate_metrics()
chances = calculate_chances(current_gpa, total_creds)

# --- WEB APP INTERFACE LAYOUT ---
st.title("🦅 CollegeVine Simulator: Early Decision Strategy Engine")
st.caption("UPenn Wharton & Huntsman Dual-Degree Modeler | Olentangy Schools Curriculum Path")

# --- SIDEBAR DISPLAY PANEL ---
with st.sidebar:
    st.header("👤 Applicant Data")
    st.markdown("**🇨🇦 Citizenship:** Canadian Citizen\n\n**🎡 Heritage:** Gujarati")
    st.markdown("**🌍 Language Focus:** German (Targeting CEFR C1/C2)")
    st.error("🚨 APPLICATION TRACK: EARLY DECISION")
    st.caption("Calculations scale dynamically based on transcript rigor, test records, and recommendation changes.")

# --- MAIN WORKSPACE ---
col_metrics, col_entry = st.columns(2)

with col_metrics:
    st.subheader("🎯 CollegeVine Chancing Diagnostics")

    st.markdown(f"**Wharton Early Decision Acceptance Probability: {chances['ED_Wharton']:.1f}%**")
    st.progress(min(chances['ED_Wharton'] / 100.0, 1.0))
    st.caption("Wharton Global ED Acceptance Target Bounds (Average Baseline Peer Pool: 14.5%)")

    st.markdown(f"**Huntsman Early Decision Acceptance Probability: {chances['ED_Huntsman']:.1f}%**")
    st.progress(min(chances['ED_Huntsman'] / 100.0, 1.0))
    st.caption("Huntsman Program Joint-Degree ED Target Bounds (Average Baseline Peer Pool: 5.0%)")

    st.markdown("---")
    st.subheader("📊 Academic Record & 4-Year Transcript")
    st.metric("Simulated Weighted GPA", f"{current_gpa:.2f}", f"{total_creds:.1f} Total Credits Logged")

    for year in ["8th Grade", "9th Grade", "10th Grade", "11th Grade", "12th Grade"]:
        with st.expander(f"📅 {year} Transcript View", expanded=(year == "8th Grade")):
            courses = st.session_state.transcript[year]
            if not courses:
                st.info("No courses cataloged for this academic year tier.")
            else:
                # Table rendering for courses
                st.table(courses)

    st.subheader("📝 Standardized Test Portfolio")
    # Table rendering for scores
    st.table([{"Test Metric": k, "Logged Score": v if v != 0 else "No Score"} for k, v in st.session_state.test_scores.items()])

    st.subheader("🏆 Prioritized Extracurricular Activity Rankings")
    ranked_ecs = sorted(st.session_state.activities, key=lambda x: x["tier"])
    for i, act in enumerate(ranked_ecs, 1):
        st.markdown(f"**Rank {i}: {act['name']}** `(Tier {act['tier']})`")
        st.markdown(f"* Description: {act['desc']}\n* Scaling Blueprint: {act['scale_plan']}")
        st.markdown("---")

with col_entry:
    st.subheader("🛠️ Profile Data Entry & Updates")

    with st.expander("📬 Update Letter of Recommendation Status"):
        rec_roles = [r["role"] for r in st.session_state.rec_letters]
        selected_rec = st.selectbox("Select Recommendation Profile to Calibrate:", rec_roles)
        new_status = st.selectbox("Set Current Standing Status:", ["Cold Emailing / Outreach Phase", "Requested / In Discussion", "Secured & Confirmed"])

        if st.button("Save Letter Status", use_container_width=True):
            for r in st.session_state.rec_letters:
                if r["role"] == selected_rec:
                    r["status"] = new_status
            st.success(f"Status updated for {selected_rec}! Probability matrices recalibrated.")
            st.rerun()

    with st.expander("📚 Log a Custom Verified Course"):
        target_year = st.selectbox("Select Academic Year Target:", ["8th Grade", "9th Grade", "10th Grade", "11th Grade", "12th Grade"])
        new_course_name = st.text_input("Official Course Name:")
        new_weight = st.selectbox("Select Core Classification Weight:", ["Regular", "Honors", "AP"])
        new_grade = st.selectbox("Select Final/Projected Grade:", ["A", "B", "C", "D", "F"])

        if st.button("Commit Course to Transcript Logs", use_container_width=True):
            banned_terms = ["art", "visual", "industrial", "french", "spanish", "shop", "drawing", "sculpture"]
            if new_course_name.strip() == "":
                st.warning("Please supply a valid text title.")
            elif any(term in new_course_name.lower() for term in banned_terms):
                st.error("Access Denied: Course selection violates strict exclusion filters.")
            else:
                st.session_state.transcript[target_year].append({"course": new_course_name.strip(), "weight": new_weight, "grade": new_grade, "credits": 1.0})
                st.success(f"Successfully integrated '{new_course_name}' into logs!")
                st.rerun()

    with st.expander("💯 Update Standardized Test Scores"):
        new_sat = st.number_input("SAT Composite Score (400-1600):", min_value=0, max_value=1600, step=10, value=st.session_state.test_scores["SAT Best Composite"])
        new_act = st.number_input("ACT Composite Score (0-36):", min_value=0, max_value=36, step=1, value=st.session_state.test_scores["ACT Composite"])
new_aps = st.number_input("AP Exams Passed with a 4 or 5:", min_value=0, max_value=20, step=1, value=st.session_state.test_scores["AP Exams Passed (Score 4/5)"])
init_aatg = st.session_state.test_scores["AATG National German Exam Score"]
new_aatg = st.text_input("AATG National German Exam Score / Rank percentile:", value=str(init_aatg) if init_aatg != 0 else "")

if st.button("Save Test Metrics", use_container_width=True):
    st.session_state.test_scores["SAT Best Composite"] = new_sat
    st.session_state.test_scores["ACT Composite"] = new_act
    st.session_state.test_scores["AP Exams Passed (Score 4/5)"] = new_aps
    st.session_state.test_scores["AATG National German Exam Score"] = new_aatg
    st.success("Test portfolio updated!")
    st.rerun()

with st.expander("🧬 Log or Scale an Extracurricular Activity"):
    ec_action = st.radio("Choose Action Type:", ["Add Completely New Activity Profile", "Update Scaling Strategy on Active Project"])
    if ec_action == "Add Completely New Activity Profile":
        new_ec_name = st.text_input("Organization / Initiative Name:")
        new_ec_desc = st.text_area("Baseline Focus Scope Description:")
        new_ec_scale = st.text_area("Initial Scaling Action Roadmap Plan:")
        new_ec_tier = st.slider("Select Tier Level Scale (1=Founder/National, 2=Selective Regional, 3=School Group):", 1, 4, 3)
        if st.button("Commit Activity to Rankings Database", use_container_width=True):
            if new_ec_name.strip() == "":
                st.warning("Please specify an active name identity token.")
            else:
                st.session_state.activities.append({"name": new_ec_name.strip(), "tier": new_ec_tier, "desc": new_ec_desc.strip(), "scale_plan": new_ec_scale.strip()})
                st.success(f"Successfully tracked and re-ranked '{new_ec_name}' profiling parameters!")
                st.rerun()
    else:
        if not st.session_state.activities:
            st.info("No active profiles loaded to run scaling evaluations against.")
        else:
            act_names = [a["name"] for a in st.session_state.activities]
            selected_act_name = st.selectbox("Select Target Project Workspace:", act_names)
            updated_scale_text = st.text_area("Input your personal long-term manual growth metrics:")
            if st.button("Apply Blueprint Milestone Adjustments", use_container_width=True):
                for a in st.session_state.activities:
                    if a["name"] == selected_act_name:
                        a["scale_plan"] = updated_scale_text.strip()
                st.success(f"Updated application projection tracks for '{selected_act_name}'!")
                st.rerun()

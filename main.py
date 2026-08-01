import streamlit as st
import sqlite3
import pandas as pd
from datetime import date, datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "counselling.db")

st.set_page_config(page_title="KNUST Counselling Center", page_icon="🧠", layout="wide")

# ----------------------------
# DATABASE SETUP
# ----------------------------
def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            counsellor_name TEXT,
            college_affiliation TEXT,
            student_id TEXT,
            student_name TEXT,
            age TEXT,
            gender TEXT,
            program TEXT,
            level TEXT,
            phone TEXT,
            emergency_contact_name TEXT,
            emergency_contact_phone TEXT,
            date_of_visit TEXT,
            visit_number INTEGER,
            consent TEXT,
            complaints TEXT,
            presenting_problem TEXT,
            psychiatric_history TEXT,
            medical_history TEXT,
            family_history TEXT,
            social_history TEXT,
            appearance TEXT,
            mood TEXT,
            affect TEXT,
            speech TEXT,
            thought_process TEXT,
            insight TEXT,
            judgement TEXT,
            risk_assessment TEXT,
            risk_details TEXT,
            safety_plan TEXT,
            protective_factors TEXT,
            impression TEXT,
            intervention TEXT,
            intervention_documentation TEXT,
            next_appointment TEXT,
            next_appointment_date TEXT,
            referral TEXT,
            referral_other TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_visit_number(student_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM sessions WHERE student_id = ?", (student_id,))
    count = c.fetchone()[0]
    conn.close()
    return count + 1

def insert_session(data):
    conn = get_conn()
    c = conn.cursor()
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))
    c.execute(f"INSERT INTO sessions ({columns}) VALUES ({placeholders})", tuple(data.values()))
    conn.commit()
    conn.close()

def get_student_history(student_id):
    conn = get_conn()
    df = pd.read_sql_query(
        "SELECT * FROM sessions WHERE student_id = ? ORDER BY id ASC",
        conn, params=(student_id,)
    )
    conn.close()
    return df

def get_all_sessions():
    conn = get_conn()
    df = pd.read_sql_query("SELECT * FROM sessions ORDER BY id DESC", conn)
    conn.close()
    return df

init_db()

# ----------------------------
# CONSTANTS
# ----------------------------
RISK_OPTIONS = ["Nil", "Self Harm", "Suicidal Ideation", "Suicidal Plan", "Suicidal Intent", "Substance Use"]
IMPRESSION_OPTIONS = ["Depression", "Anxiety Disorder", "Psychosis", "Behavioural Problem",
                       "Adjustment Reaction Disorder", "Bipolar Disorder", "PTSD/Trauma-related", "Other"]
INTERVENTION_OPTIONS = ["CBT", "Family Therapy", "Motivational Interview", "Counselling",
                         "Psychoeducation", "Referral", "Crisis Intervention"]
REFERRAL_OPTIONS = ["Not Applicable", "Medical Officer", "Clinical Psychiatry Specialist", "Others"]
MSE_OPTIONS = {
    "appearance": ["Well-groomed", "Unkempt", "Appropriate dress", "Inappropriate dress", "Other"],
    "mood": ["Euthymic", "Depressed", "Anxious", "Irritable", "Elevated", "Other"],
    "affect": ["Full range", "Restricted", "Blunted", "Flat", "Labile", "Other"],
    "speech": ["Normal rate/tone", "Pressured", "Slowed", "Slurred", "Mute", "Other"],
    "thought_process": ["Logical/coherent", "Tangential", "Circumstantial", "Flight of ideas", "Disorganized", "Other"],
    "insight": ["Good", "Fair", "Poor", "Absent"],
    "judgement": ["Good", "Fair", "Poor", "Impaired"],
}

# ----------------------------
# SIDEBAR: STUDENT LOOKUP
# ----------------------------
st.sidebar.title("🔍 Student Lookup")
lookup_id = st.sidebar.text_input("Enter Student ID to view history")

if lookup_id:
    history = get_student_history(lookup_id.strip())
    if history.empty:
        st.sidebar.info("No prior records found for this Student ID.")
    else:
        flagged_rows = history[history["risk_assessment"].str.contains(
            "Self Harm|Suicidal|Substance Use", case=False, na=False, regex=True)]
        if not flagged_rows.empty:
            latest_flags = flagged_rows.iloc[-1]["risk_assessment"]
            st.sidebar.error(f"⚠️ RISK FLAGGED\nHistory includes: {latest_flags}")
        else:
            st.sidebar.success("No risk flags on record.")
        st.sidebar.write(f"Total visits: {len(history)}")

st.sidebar.divider()
st.sidebar.caption("This is a demo build. Data is stored locally in SQLite for preview purposes only — not for real student data.")

# ----------------------------
# MAIN: TABS
# ----------------------------
st.title("🧠 KNUST Counselling Center")
st.caption("Digital Intake & Session Documentation Form (Demo)")

tab1, tab2 = st.tabs(["📝 New Session Entry", "📋 All Records"])

with tab1:
    with st.form("session_form", clear_on_submit=True):

        st.subheader("1. Biodata")
        col1, col2, col3 = st.columns(3)
        with col1:
            counsellor_name = st.text_input("Counsellor Name")
            student_id = st.text_input("Student ID *")
            age = st.text_input("Age")
        with col2:
            college_affiliation = st.text_input("College Affiliation")
            student_name = st.text_input("Student Name")
            gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])
        with col3:
            date_of_visit = st.date_input("Date of Visit", value=date.today())
            program = st.text_input("Program of Study")
            level = st.selectbox("Level", ["100", "200", "300", "400", "500", "600", "Postgraduate", "N/A"])

        col4, col5 = st.columns(2)
        with col4:
            phone = st.text_input("Student Phone Number")
        with col5:
            st.write("")

        col6, col7 = st.columns(2)
        with col6:
            emergency_contact_name = st.text_input("Emergency Contact Name")
        with col7:
            emergency_contact_phone = st.text_input("Emergency Contact Phone")

        st.divider()

        st.subheader("2. Clinical Assessment")
        consent = st.radio("Consent Obtained", ["Yes", "No"], horizontal=True)
        complaints = st.text_area("Complaints (student's own words)")
        presenting_problem = st.text_area("Presenting Problem")

        st.markdown("**Past History**")
        colh1, colh2 = st.columns(2)
        with colh1:
            psychiatric_history = st.text_area("Psychiatric History", height=80)
            family_history = st.text_area("Family History", height=80)
        with colh2:
            medical_history = st.text_area("Medical History", height=80)
            social_history = st.text_area("Social History", height=80)

        st.markdown("**Observation / Mental Status Exam**")
        colm1, colm2, colm3 = st.columns(3)
        with colm1:
            appearance = st.selectbox("Appearance", MSE_OPTIONS["appearance"])
            speech = st.selectbox("Speech", MSE_OPTIONS["speech"])
        with colm2:
            mood = st.selectbox("Mood", MSE_OPTIONS["mood"])
            thought_process = st.selectbox("Thought Process", MSE_OPTIONS["thought_process"])
        with colm3:
            affect = st.selectbox("Affect", MSE_OPTIONS["affect"])
            insight = st.selectbox("Insight", MSE_OPTIONS["insight"])
        judgement = st.selectbox("Judgement", MSE_OPTIONS["judgement"])

        st.markdown("**Risk Assessment**")
        risk_assessment = st.multiselect("Select all that apply", RISK_OPTIONS, default=["Nil"])
        risk_details = st.text_area(
            "Risk details (if applicable) — e.g. presence of plan, intent, means, frequency",
            height=80
        )
        protective_factors = st.text_area("Protective Factors (e.g. support system, coping skills, future plans)", height=80)
        safety_plan = st.text_area("Safety Plan (required if any risk flagged besides 'Nil')", height=80)

        impression = st.multiselect("Impression / Clinical Diagnosis", IMPRESSION_OPTIONS)

        st.divider()

        st.subheader("3. Intervention & Follow-Up")
        intervention = st.multiselect("Intervention", INTERVENTION_OPTIONS)
        intervention_documentation = st.text_area("Intervention Documentation")

        colf1, colf2 = st.columns(2)
        with colf1:
            next_appointment = st.radio("Next Appointment Scheduled?", ["Yes", "No"], horizontal=True)
        with colf2:
            next_appointment_date = st.date_input("Next Appointment Date (if applicable)", value=None)

        colr1, colr2 = st.columns(2)
        with colr1:
            referral = st.selectbox("Referral", REFERRAL_OPTIONS)
        with colr2:
            referral_other = st.text_input("If 'Others', please specify")

        submitted = st.form_submit_button("💾 Save Session Record", use_container_width=True)

        if submitted:
            if not student_id.strip():
                st.error("Student ID is required.")
            else:
                visit_number = get_visit_number(student_id.strip())
                data = {
                    "counsellor_name": counsellor_name,
                    "college_affiliation": college_affiliation,
                    "student_id": student_id.strip(),
                    "student_name": student_name,
                    "age": age,
                    "gender": gender,
                    "program": program,
                    "level": level,
                    "phone": phone,
                    "emergency_contact_name": emergency_contact_name,
                    "emergency_contact_phone": emergency_contact_phone,
                    "date_of_visit": str(date_of_visit),
                    "visit_number": visit_number,
                    "consent": consent,
                    "complaints": complaints,
                    "presenting_problem": presenting_problem,
                    "psychiatric_history": psychiatric_history,
                    "medical_history": medical_history,
                    "family_history": family_history,
                    "social_history": social_history,
                    "appearance": appearance,
                    "mood": mood,
                    "affect": affect,
                    "speech": speech,
                    "thought_process": thought_process,
                    "insight": insight,
                    "judgement": judgement,
                    "risk_assessment": ", ".join(risk_assessment),
                    "risk_details": risk_details,
                    "safety_plan": safety_plan,
                    "protective_factors": protective_factors,
                    "impression": ", ".join(impression),
                    "intervention": ", ".join(intervention),
                    "intervention_documentation": intervention_documentation,
                    "next_appointment": next_appointment,
                    "next_appointment_date": str(next_appointment_date) if next_appointment_date else "",
                    "referral": referral,
                    "referral_other": referral_other,
                    "created_at": datetime.now().isoformat(),
                }
                insert_session(data)
                st.success(f"Session saved. This was visit #{visit_number} for student {student_id}.")
                if any(r != "Nil" for r in risk_assessment):
                    st.warning("⚠️ Risk flags were recorded for this session. Ensure appropriate follow-up and safety planning is in place.")

with tab2:
    st.subheader("All Session Records")
    df = get_all_sessions()
    if df.empty:
        st.info("No records yet. Add a session in the 'New Session Entry' tab.")
    else:
        search = st.text_input("Filter by Student ID")
        if search:
            df = df[df["student_id"].str.contains(search, case=False, na=False)]
        st.dataframe(df, use_container_width=True, height=500)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download as CSV", csv, "counselling_records.csv", "text/csv")

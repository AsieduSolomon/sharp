import streamlit as st
import sqlite3
import pandas as pd
from datetime import date, datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "counselling.db")

st.set_page_config(
    page_title="KNUST Counselling Center",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------
# DESIGN SYSTEM — CSS
# ----------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
    --bg: #F6F7F9;
    --surface: #FFFFFF;
    --border: #E1E4EA;
    --text-primary: #17202B;
    --text-secondary: #5B6472;
    --accent: #2C5F6F;
    --accent-light: #EAF1F2;
    --risk: #A63D2A;
    --risk-light: #FBEDEA;
    --success: #3F6F52;
    --success-light: #EEF4EF;
}

html, body, [class*="css"]  {
    font-family: 'IBM Plex Sans', sans-serif;
    color: var(--text-primary);
}
.stApp { background-color: var(--bg); }

#MainMenu, footer, header {visibility: hidden;}
div[data-testid="stDecoration"] {display: none;}

.kc-letterhead {
    border-bottom: 1px solid var(--border);
    padding: 0 0 20px 0;
    margin-bottom: 32px;
}
.kc-letterhead .kc-institution {
    font-family: 'Source Serif 4', serif;
    font-size: 28px;
    font-weight: 600;
    letter-spacing: -0.01em;
    color: var(--text-primary);
    margin: 0;
}
.kc-letterhead .kc-subtitle {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12.5px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--text-secondary);
    margin-top: 4px;
}

.kc-section {
    display: flex;
    align-items: baseline;
    gap: 12px;
    margin: 36px 0 4px 0;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
}
.kc-section .kc-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    color: var(--accent);
    letter-spacing: 0.04em;
}
.kc-section .kc-title {
    font-family: 'Source Serif 4', serif;
    font-size: 19px;
    font-weight: 600;
    color: var(--text-primary);
}

.kc-subhead {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11.5px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-secondary);
    margin: 22px 0 10px 0;
}

.kc-flag {
    border-left: 3px solid var(--risk);
    background: var(--risk-light);
    padding: 12px 16px;
    border-radius: 3px;
    margin-bottom: 12px;
}
.kc-flag .kc-flag-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--risk);
    font-weight: 500;
}
.kc-flag .kc-flag-body {
    font-size: 14px;
    color: var(--text-primary);
    margin-top: 4px;
}

.kc-clear {
    border-left: 3px solid var(--success);
    background: var(--success-light);
    padding: 12px 16px;
    border-radius: 3px;
    margin-bottom: 12px;
}
.kc-clear .kc-flag-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--success);
    font-weight: 500;
}
.kc-clear .kc-flag-body {
    font-size: 14px;
    color: var(--text-primary);
    margin-top: 4px;
}

.kc-meta {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: var(--text-secondary);
}

section[data-testid="stSidebar"] {
    background-color: var(--surface);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .kc-sidebar-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11.5px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-secondary);
    margin-bottom: 6px;
}

.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"], .stDateInput input {
    border-radius: 4px !important;
    border-color: var(--border) !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent) !important;
}

.stButton button, .stFormSubmitButton button {
    background-color: var(--accent);
    color: #FFFFFF;
    border: none;
    border-radius: 4px;
    font-family: 'IBM Plex Sans', sans-serif;
    font-weight: 500;
    letter-spacing: 0.01em;
    padding: 0.55em 1.2em;
}
.stButton button:hover, .stFormSubmitButton button:hover {
    background-color: #234B57;
    color: #FFFFFF;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    border-bottom: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    font-family: 'IBM Plex Sans', sans-serif;
    font-weight: 500;
    font-size: 14px;
    color: var(--text-secondary);
    padding: 10px 4px;
}
.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom-color: var(--accent) !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 6px;
}

hr { border-color: var(--border); }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------
# DATABASE
# ----------------------------------------------------------------
def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            counsellor_name TEXT, college_affiliation TEXT, student_id TEXT,
            student_name TEXT, age TEXT, gender TEXT, program TEXT, level TEXT,
            phone TEXT, emergency_contact_name TEXT, emergency_contact_phone TEXT,
            date_of_visit TEXT, visit_number INTEGER, consent TEXT,
            complaints TEXT, presenting_problem TEXT,
            psychiatric_history TEXT, medical_history TEXT, family_history TEXT, social_history TEXT,
            appearance TEXT, mood TEXT, affect TEXT, speech TEXT,
            thought_process TEXT, insight TEXT, judgement TEXT,
            risk_assessment TEXT, risk_details TEXT, safety_plan TEXT, protective_factors TEXT,
            impression TEXT, intervention TEXT, intervention_documentation TEXT,
            next_appointment TEXT, next_appointment_date TEXT,
            referral TEXT, referral_other TEXT, created_at TEXT
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
    df = pd.read_sql_query("SELECT * FROM sessions WHERE student_id = ? ORDER BY id ASC", conn, params=(student_id,))
    conn.close()
    return df

def get_all_sessions():
    conn = get_conn()
    df = pd.read_sql_query("SELECT * FROM sessions ORDER BY id DESC", conn)
    conn.close()
    return df

init_db()

# ----------------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------------
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

def section(number, title):
    st.markdown(f"""
        <div class="kc-section">
            <span class="kc-num">{number}</span>
            <span class="kc-title">{title}</span>
        </div>
    """, unsafe_allow_html=True)

def subhead(label):
    st.markdown(f'<div class="kc-subhead">{label}</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------
# SIDEBAR — RECORD LOOKUP
# ----------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="kc-sidebar-title">Record Lookup</div>', unsafe_allow_html=True)
    lookup_id = st.text_input("Student ID", label_visibility="collapsed", placeholder="Enter student ID")

    if lookup_id:
        history = get_student_history(lookup_id.strip())
        if history.empty:
            st.markdown('<div class="kc-meta">No prior records found for this student ID.</div>', unsafe_allow_html=True)
        else:
            flagged_rows = history[history["risk_assessment"].str.contains(
                "Self Harm|Suicidal|Substance Use", case=False, na=False, regex=True)]
            if not flagged_rows.empty:
                latest_flags = flagged_rows.iloc[-1]["risk_assessment"]
                st.markdown(f"""
                    <div class="kc-flag">
                        <div class="kc-flag-label">Risk on record</div>
                        <div class="kc-flag-body">{latest_flags}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class="kc-clear">
                        <div class="kc-flag-label">Status</div>
                        <div class="kc-flag-body">No risk flags on record</div>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown(f'<div class="kc-meta">Total visits: {len(history)}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div class="kc-meta">Demo build. Records are stored locally for preview '
        'purposes and should not be used for real student data.</div>',
        unsafe_allow_html=True
    )

# ----------------------------------------------------------------
# LETTERHEAD
# ----------------------------------------------------------------
st.markdown("""
    <div class="kc-letterhead">
        <p class="kc-institution">KNUST Counselling Center</p>
        <div class="kc-subtitle">Session Documentation &amp; Case Record System</div>
    </div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["New Session Entry", "All Records"])

# ----------------------------------------------------------------
# TAB 1 — NEW SESSION
# ----------------------------------------------------------------
with tab1:
    with st.form("session_form", clear_on_submit=True):

        section("01", "Biodata")
        col1, col2, col3 = st.columns(3)
        with col1:
            counsellor_name = st.text_input("Counsellor Name")
            student_id = st.text_input("Student ID")
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
            pass

        col6, col7 = st.columns(2)
        with col6:
            emergency_contact_name = st.text_input("Emergency Contact Name")
        with col7:
            emergency_contact_phone = st.text_input("Emergency Contact Phone")

        section("02", "Clinical Assessment")
        consent = st.radio("Consent Obtained", ["Yes", "No"], horizontal=True)
        complaints = st.text_area("Complaints (student's own words)")
        presenting_problem = st.text_area("Presenting Problem")

        subhead("Past History")
        colh1, colh2 = st.columns(2)
        with colh1:
            psychiatric_history = st.text_area("Psychiatric History", height=80)
            family_history = st.text_area("Family History", height=80)
        with colh2:
            medical_history = st.text_area("Medical History", height=80)
            social_history = st.text_area("Social History", height=80)

        subhead("Observation — Mental Status Exam")
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

        subhead("Risk Assessment")
        risk_assessment = st.multiselect("Select all that apply", RISK_OPTIONS, default=["Nil"])
        risk_details = st.text_area("Risk details (plan, intent, means, frequency, if applicable)", height=80)
        protective_factors = st.text_area("Protective Factors", height=80)
        safety_plan = st.text_area("Safety Plan (required if risk flagged beyond 'Nil')", height=80)

        subhead("Impression")
        impression = st.multiselect("Clinical Impression", IMPRESSION_OPTIONS, label_visibility="collapsed")

        section("03", "Intervention & Follow-Up")
        intervention = st.multiselect("Intervention", INTERVENTION_OPTIONS)
        intervention_documentation = st.text_area("Intervention Documentation")

        colf1, colf2 = st.columns(2)
        with colf1:
            next_appointment = st.radio("Next Appointment Scheduled?", ["Yes", "No"], horizontal=True)
        with colf2:
            next_appointment_date = st.date_input("Next Appointment Date", value=None)

        colr1, colr2 = st.columns(2)
        with colr1:
            referral = st.selectbox("Referral", REFERRAL_OPTIONS)
        with colr2:
            referral_other = st.text_input("If 'Others', specify")

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Save Session Record", use_container_width=True)

        if submitted:
            if not student_id.strip():
                st.error("Student ID is required.")
            else:
                visit_number = get_visit_number(student_id.strip())
                data = {
                    "counsellor_name": counsellor_name, "college_affiliation": college_affiliation,
                    "student_id": student_id.strip(), "student_name": student_name, "age": age,
                    "gender": gender, "program": program, "level": level, "phone": phone,
                    "emergency_contact_name": emergency_contact_name,
                    "emergency_contact_phone": emergency_contact_phone,
                    "date_of_visit": str(date_of_visit), "visit_number": visit_number,
                    "consent": consent, "complaints": complaints, "presenting_problem": presenting_problem,
                    "psychiatric_history": psychiatric_history, "medical_history": medical_history,
                    "family_history": family_history, "social_history": social_history,
                    "appearance": appearance, "mood": mood, "affect": affect, "speech": speech,
                    "thought_process": thought_process, "insight": insight, "judgement": judgement,
                    "risk_assessment": ", ".join(risk_assessment), "risk_details": risk_details,
                    "safety_plan": safety_plan, "protective_factors": protective_factors,
                    "impression": ", ".join(impression), "intervention": ", ".join(intervention),
                    "intervention_documentation": intervention_documentation,
                    "next_appointment": next_appointment,
                    "next_appointment_date": str(next_appointment_date) if next_appointment_date else "",
                    "referral": referral, "referral_other": referral_other,
                    "created_at": datetime.now().isoformat(),
                }
                insert_session(data)
                st.success(f"Session saved — visit {visit_number} for student {student_id}.")
                if any(r != "Nil" for r in risk_assessment):
                    st.markdown(f"""
                        <div class="kc-flag">
                            <div class="kc-flag-label">Follow-up required</div>
                            <div class="kc-flag-body">Risk flags were recorded for this session. Confirm safety planning and follow-up are in place.</div>
                        </div>
                    """, unsafe_allow_html=True)

# ----------------------------------------------------------------
# TAB 2 — ALL RECORDS
# ----------------------------------------------------------------
with tab2:
    section("—", "All Session Records")
    df = get_all_sessions()
    if df.empty:
        st.markdown('<div class="kc-meta">No records yet. Add a session in the New Session Entry tab.</div>', unsafe_allow_html=True)
    else:
        search = st.text_input("Filter by Student ID", placeholder="Student ID")
        if search:
            df = df[df["student_id"].str.contains(search, case=False, na=False)]
        st.dataframe(df, use_container_width=True, height=500)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download as CSV", csv, "counselling_records.csv", "text/csv")

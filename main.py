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

html { color-scheme: light only; }

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

/* Multiselect tags */
span[data-baseweb="tag"] {
    background-color: var(--accent) !important;
    border-radius: 3px !important;
}

/* Radio / checkbox accent */
.stRadio [aria-checked="true"] div:first-child {
    background-color: var(--accent) !important;
    border-color: var(--accent) !important;
}
.stCheckbox [aria-checked="true"] {
    background-color: var(--accent) !important;
    border-color: var(--accent) !important;
}

/* Select box focus / dropdown highlight */
div[data-baseweb="select"]:focus-within > div {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent) !important;
}
li[aria-selected="true"] {
    background-color: var(--accent-light) !important;
}

/* Date input focus */
.stDateInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent) !important;
}

/* Links */
a, a:visited { color: var(--accent) !important; }

/* Force every widget label / question text to a fixed dark color.
   Without this, mobile devices in system dark mode make labels
   render white-on-white, since Streamlit's own label color follows
   the system theme unless explicitly overridden. */
label, 
[data-testid="stWidgetLabel"], 
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] span,
.stTextInput label, .stTextArea label, .stSelectbox label,
.stMultiSelect label, .stRadio label, .stDateInput label,
.stRadio div[role="radiogroup"] label span,
.stCheckbox label span,
div[data-testid="stMarkdownContainer"] p,
div[data-testid="stMarkdownContainer"] span,
.stApp, .stApp p, .stApp span, .stApp div {
    color: var(--text-primary) !important;
}

/* Re-apply the intentional lighter colors after the broad rule above,
   since the wildcard would otherwise flatten everything to one color */
.kc-letterhead .kc-subtitle,
.kc-meta,
.kc-flag-label,
.kc-subhead,
section[data-testid="stSidebar"] .kc-sidebar-title {
    color: var(--text-secondary) !important;
}
.kc-flag .kc-flag-label { color: var(--risk) !important; }
.kc-clear .kc-flag-label { color: var(--success) !important; }
.kc-section .kc-num { color: var(--accent) !important; }
.stButton button, .stButton button span,
.stFormSubmitButton button, .stFormSubmitButton button span,
.stDownloadButton button, .stDownloadButton button span {
    color: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)

# The settings below replace what used to live in .streamlit/config.toml,
# so the whole app is now defined in this single file:
#   theme.base                     = "light"    -> handled by CSS variables above
#   theme.primaryColor             = "#2C5F6F"  -> var(--accent) above
#   theme.backgroundColor          = "#FFFFFF"  -> surfaces/cards above
#   theme.secondaryBackgroundColor = "#F6F7F9"  -> var(--bg) above
#   theme.textColor                = "#17202B"  -> var(--text-primary) above
#   client.toolbarMode             = "minimal"  -> #MainMenu/header hidden above
#   browser.gatherUsageStats       = False       -> set programmatically below
try:
    st._config.set_option("browser.gatherUsageStats", False)
except Exception:
    pass

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

from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# ----------------------------------------------------------------
# PDF REPORT GENERATION
# ----------------------------------------------------------------
PDF_ACCENT = colors.HexColor("#2C5F6F")
PDF_RISK = colors.HexColor("#A63D2A")
PDF_RISK_BG = colors.HexColor("#FBEDEA")
PDF_TEXT = colors.HexColor("#17202B")
PDF_MUTED = colors.HexColor("#5B6472")
PDF_BORDER = colors.HexColor("#D6DAE2")

def _pdf_styles():
    ss = getSampleStyleSheet()
    return {
        "institution": ParagraphStyle("institution", fontName="Times-Bold", fontSize=17,
                                       textColor=PDF_TEXT, leading=20),
        "doctype": ParagraphStyle("doctype", fontName="Helvetica", fontSize=8.5,
                                   textColor=PDF_MUTED, leading=11, alignment=TA_RIGHT),
        "section": ParagraphStyle("section", fontName="Times-Bold", fontSize=11.5,
                                   textColor=PDF_TEXT, spaceBefore=14, spaceAfter=6),
        "label": ParagraphStyle("label", fontName="Helvetica-Bold", fontSize=7.3,
                                 textColor=PDF_MUTED, leading=10),
        "value": ParagraphStyle("value", fontName="Helvetica", fontSize=9.3,
                                 textColor=PDF_TEXT, leading=13),
        "value_empty": ParagraphStyle("value_empty", fontName="Helvetica-Oblique", fontSize=9.3,
                                       textColor=PDF_MUTED, leading=13),
        "risk_label": ParagraphStyle("risk_label", fontName="Helvetica-Bold", fontSize=7.3,
                                      textColor=PDF_RISK, leading=10),
        "risk_value": ParagraphStyle("risk_value", fontName="Helvetica-Bold", fontSize=9.5,
                                      textColor=PDF_RISK, leading=13),
        "visit_head": ParagraphStyle("visit_head", fontName="Times-Bold", fontSize=13,
                                      textColor=PDF_TEXT, spaceBefore=0, spaceAfter=2),
        "visit_meta": ParagraphStyle("visit_meta", fontName="Helvetica", fontSize=8.5,
                                      textColor=PDF_MUTED, spaceAfter=8),
    }

def _pdf_field(label, value, styles, width=None):
    """One labeled field: small caption above, value below, thin rule under."""
    v = (value or "").strip()
    val_style = styles["value"] if v else styles["value_empty"]
    flow = [
        Paragraph(label.upper(), styles["label"]),
        Spacer(1, 1.5),
        Paragraph(v if v else "Not recorded", val_style),
        Spacer(1, 3),
        HRFlowable(width="100%", thickness=0.5, color=PDF_BORDER, spaceAfter=8),
    ]
    return flow

def _pdf_biodata_table(row, styles):
    def cell(label, value):
        return [Paragraph(label.upper(), styles["label"]), Paragraph(str(value or "—"), styles["value"])]

    data = [
        [cell("Student ID", row.get("student_id")), cell("Student Name", row.get("student_name")),
         cell("Age", row.get("age")), cell("Gender", row.get("gender"))],
        [cell("College", row.get("college_affiliation")), cell("Program", row.get("program")),
         cell("Level", row.get("level")), cell("Phone", row.get("phone"))],
        [cell("Emergency Contact", row.get("emergency_contact_name")),
         cell("Emergency Phone", row.get("emergency_contact_phone")),
         cell("Counsellor", row.get("counsellor_name")),
         cell("Consent Obtained", row.get("consent"))],
    ]
    table = Table(data, colWidths=[42 * mm] * 4)
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, PDF_BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return table

def _pdf_risk_block(row, styles):
    risk = (row.get("risk_assessment") or "").strip()
    flagged = bool(risk) and risk.lower() != "nil"
    inner = [Paragraph("RISK ASSESSMENT", styles["risk_label"] if flagged else styles["label"])]
    inner.append(Spacer(1, 2))
    inner.append(Paragraph(risk if risk else "Not recorded",
                            styles["risk_value"] if flagged else styles["value"]))
    if flagged:
        details = (row.get("risk_details") or "").strip()
        plan = (row.get("safety_plan") or "").strip()
        if details:
            inner += [Spacer(1, 5), Paragraph("RISK DETAILS", styles["label"]),
                      Paragraph(details, styles["value"])]
        if plan:
            inner += [Spacer(1, 5), Paragraph("SAFETY PLAN", styles["label"]),
                      Paragraph(plan, styles["value"])]
        box = Table([[inner]], colWidths=[170 * mm])
        box.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 0, colors.white),
            ("LINEBEFORE", (0, 0), (0, 0), 2.5, PDF_RISK),
            ("BACKGROUND", (0, 0), (-1, -1), PDF_RISK_BG),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ]))
        return [box, Spacer(1, 10)]
    else:
        return inner + [Spacer(1, 10)]

def _pdf_visit_flowables(row, styles, visit_label):
    flow = []
    flow.append(Paragraph(visit_label, styles["visit_head"]))
    meta = f"{row.get('date_of_visit', '—')}  ·  Counsellor: {row.get('counsellor_name') or '—'}  ·  College: {row.get('college_affiliation') or '—'}"
    flow.append(Paragraph(meta, styles["visit_meta"]))

    flow.append(Paragraph("PRESENTING CONCERN", styles["section"]))
    flow += _pdf_field("Complaints", row.get("complaints"), styles)
    flow += _pdf_field("Presenting Problem", row.get("presenting_problem"), styles)

    flow.append(Paragraph("HISTORY", styles["section"]))
    flow += _pdf_field("Psychiatric History", row.get("psychiatric_history"), styles)
    flow += _pdf_field("Medical History", row.get("medical_history"), styles)
    flow += _pdf_field("Family History", row.get("family_history"), styles)
    flow += _pdf_field("Social History", row.get("social_history"), styles)

    flow.append(Paragraph("MENTAL STATUS EXAM", styles["section"]))
    mse = (f"Appearance: {row.get('appearance', '—')}   |   Mood: {row.get('mood', '—')}   |   "
           f"Affect: {row.get('affect', '—')}   |   Speech: {row.get('speech', '—')}")
    mse2 = (f"Thought Process: {row.get('thought_process', '—')}   |   Insight: {row.get('insight', '—')}   |   "
            f"Judgement: {row.get('judgement', '—')}")
    flow.append(Paragraph(mse, styles["value"]))
    flow.append(Paragraph(mse2, styles["value"]))
    flow.append(Spacer(1, 6))
    flow.append(HRFlowable(width="100%", thickness=0.5, color=PDF_BORDER, spaceAfter=8))

    flow.append(Paragraph("RISK & PROTECTIVE FACTORS", styles["section"]))
    flow += _pdf_risk_block(row, styles)
    flow += _pdf_field("Protective Factors", row.get("protective_factors"), styles)

    flow.append(Paragraph("IMPRESSION", styles["section"]))
    flow += _pdf_field("Clinical Impression", row.get("impression"), styles)

    flow.append(Paragraph("INTERVENTION & FOLLOW-UP", styles["section"]))
    flow += _pdf_field("Intervention", row.get("intervention"), styles)
    flow += _pdf_field("Intervention Documentation", row.get("intervention_documentation"), styles)
    next_appt = row.get("next_appointment", "—")
    next_date = row.get("next_appointment_date") or "Not scheduled"
    flow += _pdf_field("Next Appointment", f"{next_appt} — {next_date}" if next_appt == "Yes" else "No", styles)
    ref = row.get("referral", "—")
    if ref == "Others" and row.get("referral_other"):
        ref = f"Others — {row.get('referral_other')}"
    flow += _pdf_field("Referral", ref, styles)

    return flow

def _pdf_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(PDF_MUTED)
    canvas.drawString(20 * mm, 12 * mm,
                       "Confidential clinical record — KNUST Counselling Center. Not for unauthorized disclosure.")
    canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, f"Page {doc.page}")
    canvas.restoreState()

def _pdf_header_flowables(styles, doctype_label):
    generated = datetime.now().strftime("%d %b %Y, %H:%M")
    head_table = Table(
        [[Paragraph("KNUST Counselling Center", styles["institution"]),
          Paragraph(f"{doctype_label}<br/>Generated {generated}", styles["doctype"])]],
        colWidths=[110 * mm, 60 * mm]
    )
    head_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    return [
        head_table,
        Spacer(1, 6),
        HRFlowable(width="100%", thickness=1.6, color=PDF_ACCENT, spaceAfter=14),
    ]

def generate_session_pdf(row: dict) -> bytes:
    """Single-visit session report."""
    buf = BytesIO()
    styles = _pdf_styles()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                             topMargin=18 * mm, bottomMargin=18 * mm,
                             leftMargin=20 * mm, rightMargin=20 * mm)
    story = []
    story += _pdf_header_flowables(styles, "Session Record")
    story.append(_pdf_biodata_table(row, styles))
    story.append(Spacer(1, 12))
    visit_label = f"Visit {row.get('visit_number', '—')}"
    story += _pdf_visit_flowables(row, styles, visit_label)
    doc.build(story, onFirstPage=_pdf_footer, onLaterPages=_pdf_footer)
    buf.seek(0)
    return buf.read()

def generate_case_file_pdf(student_id: str, rows: list) -> bytes:
    """Full case file — all visits for one student, most recent biodata first."""
    buf = BytesIO()
    styles = _pdf_styles()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                             topMargin=18 * mm, bottomMargin=18 * mm,
                             leftMargin=20 * mm, rightMargin=20 * mm)
    story = []
    story += _pdf_header_flowables(styles, f"Case File — {student_id}")
    latest = rows[-1]
    story.append(_pdf_biodata_table(latest, styles))
    story.append(Spacer(1, 10))

    story.append(Paragraph("VISIT SUMMARY", styles["section"]))
    summary_data = [["Visit", "Date", "Counsellor", "Risk", "Impression"]]
    for r in rows:
        summary_data.append([
            str(r.get("visit_number", "—")),
            str(r.get("date_of_visit", "—")),
            str(r.get("counsellor_name") or "—"),
            str(r.get("risk_assessment") or "Nil"),
            str(r.get("impression") or "—"),
        ])
    summary = Table(summary_data, colWidths=[16 * mm, 26 * mm, 38 * mm, 45 * mm, 45 * mm], repeatRows=1)
    summary.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("TEXTCOLOR", (0, 0), (-1, 0), PDF_MUTED),
        ("TEXTCOLOR", (0, 1), (-1, -1), PDF_TEXT),
        ("LINEBELOW", (0, 0), (-1, 0), 0.75, PDF_TEXT),
        ("LINEBELOW", (0, 1), (-1, -1), 0.4, PDF_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(summary)
    story.append(PageBreak())

    for i, r in enumerate(rows):
        story += _pdf_visit_flowables(r, styles, f"Visit {r.get('visit_number', i + 1)}")
        if i < len(rows) - 1:
            story.append(PageBreak())

    doc.build(story, onFirstPage=_pdf_footer, onLaterPages=_pdf_footer)
    buf.seek(0)
    return buf.read()

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
            case_pdf = generate_case_file_pdf(lookup_id.strip(), history.to_dict("records"))
            st.download_button(
                "Download Case File (PDF)",
                data=case_pdf,
                file_name=f"case_file_{lookup_id.strip()}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

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
                st.session_state["_last_session_pdf"] = generate_session_pdf(data)
                st.session_state["_last_session_id"] = f"{student_id}_visit{visit_number}"

    if st.session_state.get("_last_session_pdf"):
        st.download_button(
            "Download Session Report (PDF)",
            data=st.session_state["_last_session_pdf"],
            file_name=f"session_report_{st.session_state.get('_last_session_id', 'record')}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

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

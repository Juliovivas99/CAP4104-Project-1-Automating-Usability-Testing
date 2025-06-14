import streamlit as st
import pandas as pd
import os
import csv
from datetime import datetime

st.set_page_config(page_title="Usability Testing Automation Tool", layout="centered")

# Ensure data directory exists
data_dir = 'data'
os.makedirs(data_dir, exist_ok=True)

# CSV file paths
consent_csv = os.path.join(data_dir, 'consent_data.csv')
demographic_csv = os.path.join(data_dir, 'demographic_data.csv')
task_csv = os.path.join(data_dir, 'task_data.csv')
exit_csv = os.path.join(data_dir, 'exit_data.csv')

# Helper to append to CSV with header if new
def append_csv(file, fieldnames, row):
    file_exists = os.path.isfile(file)
    with open(file, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

# Add custom CSS for a professional look
st.markdown('''
    <style>
    body, .stApp { font-family: "Segoe UI", "Roboto", "Arial", sans-serif; background: #181c24; color: #f5f6fa; }
    .main { background: #181c24; }
    .stButton>button {
        font-size: 1.1rem;
        padding: 0.5em 1.5em;
        border-radius: 8px;
        background: #3b82f6;
        color: white;
        border: none;
        margin: 0.2em 0.5em 0.2em 0;
        transition: background 0.2s;
    }
    .stButton>button:hover {
        background: #2563eb;
    }
    .task-card {
        background: #23293a;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.10);
        padding: 2em 2em 1.5em 2em;
        margin-bottom: 2em;
        border: 1px solid #2d3340;
    }
    .task-title { font-size: 1.3rem; font-weight: 600; color: #60a5fa; margin-bottom: 0.2em; }
    .task-instructions { font-size: 1.05rem; color: #cbd5e1; margin-bottom: 1em; }
    .stSlider>div { color: #60a5fa; }
    .stTextArea textarea { background: #1e2230; color: #f5f6fa; border-radius: 8px; }
    .stRadio>div { color: #60a5fa; }
    .stForm label { color: #60a5fa; }
    .stDataFrame { background: #23293a; border-radius: 10px; }
    .stAlert { border-radius: 8px; }
    </style>
''', unsafe_allow_html=True)

# --- Streamlit App ---
st.title("Usability Testing Automation Tool")

# Tabs
TABS = ["Home", "Consent", "Demographics", "Task", "Exit Questionnaire", "Report"]
tab = st.sidebar.radio("Navigation", TABS)

# --- Home Tab ---
if tab == "Home":
    st.header("Welcome")
    st.write("""
    This tool guides you through a full usability testing workflow:
    1. Consent
    2. Demographics
    3. Task
    4. Exit Questionnaire
    5. Report
    Please use the sidebar to navigate through each step.
    """)

# --- Consent Tab ---
if tab == "Consent":
    st.header("Consent Form")
    consent_text = st.text_area(
        "Consent Information (customizable)",
        value="""Thank you for participating in this usability test. Your responses will be recorded and used for research purposes only. Participation is voluntary, and you may withdraw at any time. No personally identifying information will be shared. By checking the box below, you provide your digital consent to participate.
        """,
        height=150
    )
    consent_given = st.checkbox("I have read and consent to participate.")
    if st.button("Submit Consent"):
        timestamp = datetime.now().isoformat()
        row = {
            'timestamp': timestamp,
            'consent_given': consent_given,
            'consent_text': consent_text.strip().replace('\n', ' ')
        }
        append_csv(consent_csv, ['timestamp', 'consent_given', 'consent_text'], row)
        if consent_given:
            st.success("Consent recorded. Thank you!")
        else:
            st.warning("Consent not given. You cannot proceed without consent.")

# --- Demographics Tab ---
if tab == "Demographics":
    st.header("Demographic Questionnaire")
    with st.form("demographic_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        occupation = st.text_input("Occupation")
        familiarity = st.radio(
            "How familiar are you with similar tools?",
            ["Not at all", "Slightly", "Moderately", "Very", "Extremely"]
        )
        submitted = st.form_submit_button("Submit Demographics")
        if submitted:
            row = {
                'timestamp': datetime.now().isoformat(),
                'name': name,
                'age': age,
                'occupation': occupation,
                'familiarity': familiarity
            }
            append_csv(demographic_csv, ['timestamp', 'name', 'age', 'occupation', 'familiarity'], row)
            st.success("Demographic data recorded.")

# --- Task Tab ---
if tab == "Task":
    st.header("Usability Tasks")
    st.markdown("<div style='font-size:1.1rem; color:#cbd5e1; margin-bottom:2em;'>Please complete each task below by following the instructions. Each task will be timed and your feedback will be recorded. The Health Tracker App will open in a new tab.</div>", unsafe_allow_html=True)

    TASKS = [
        {
            'number': 1,
            'title': 'Log your daily health data',
            'instructions': "Go to the Health Tracker App and enter today's calories intake and exercise minutes.",
        },
        {
            'number': 2,
            'title': 'Check the weather',
            'instructions': "In the Health App, search for the weather forecast in any city.",
        },
        {
            'number': 3,
            'title': 'Review your health progress',
            'instructions': "Use the app to review your entered health data and interpret your progress.",
        },
    ]
    app_url = "https://juliovivas99-cap4104-project-2-app-zdwchh.streamlit.app"

    if 'task_states' not in st.session_state:
        st.session_state['task_states'] = [{} for _ in TASKS]

    for idx, task in enumerate(TASKS):
        with st.container():
            st.markdown(f"<div class='task-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='task-title'>Task {task['number']}: {task['title']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='task-instructions'>{task['instructions']}</div>", unsafe_allow_html=True)
            st.markdown(f"<a href='{app_url}' target='_blank' style='color:#38bdf8; font-weight:500;'>Open Health Tracker App in new tab</a>", unsafe_allow_html=True)

            state = st.session_state['task_states'][idx]
            if 'started' not in state:
                state['started'] = False
            if 'start_time' not in state:
                state['start_time'] = None
            if 'duration' not in state:
                state['duration'] = None
            if 'finished' not in state:
                state['finished'] = False

            col1, col2 = st.columns(2)
            with col1:
                if not state['started'] and not state['finished']:
                    if st.button(f"Start Task {task['number']}", key=f"start_{idx}"):
                        state['started'] = True
                        state['start_time'] = datetime.now()
                        state['duration'] = None
                elif state['started'] and not state['finished']:
                    st.write(f"Started at: {state['start_time'].strftime('%H:%M:%S')}")
            with col2:
                if state['started'] and not state['finished']:
                    if st.button(f"Finish Task {task['number']}", key=f"finish_{idx}"):
                        end_time = datetime.now()
                        duration = (end_time - state['start_time']).total_seconds()
                        state['duration'] = duration
                        state['started'] = False
                        state['finished'] = True
                        st.success(f"Task completed in {duration:.2f} seconds.")

            if state['duration'] is not None:
                st.write(f"**Time taken:** {state['duration']:.2f} seconds")

            if state['finished']:
                with st.form(f"feedback_form_{idx}"):
                    success = st.checkbox("Was the task completed successfully?", key=f"success_{idx}")
                    difficulty = st.slider("How difficult was the task? (1=Easy, 5=Hard)", 1, 5, 3, key=f"difficulty_{idx}")
                    feedback = st.text_area("Optional feedback", key=f"feedback_{idx}")
                    submitted = st.form_submit_button("Submit Task Data", disabled=state.get('submitted', False))
                    if submitted and not state.get('submitted', False):
                        row = {
                            'timestamp': datetime.now().isoformat(),
                            'task_number': task['number'],
                            'task_title': task['title'],
                            'success': 'Yes' if success else 'No',
                            'difficulty': difficulty,
                            'feedback': feedback,
                            'duration_seconds': state['duration']
                        }
                        append_csv(task_csv, ['timestamp', 'task_number', 'task_title', 'success', 'difficulty', 'feedback', 'duration_seconds'], row)
                        st.success("Task data recorded.")
                        state['submitted'] = True
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

# --- Exit Questionnaire Tab ---
if tab == "Exit Questionnaire":
    st.header("Exit Questionnaire")
    with st.form("exit_form"):
        satisfaction = st.slider("Overall satisfaction with the tool", 1, 5, 3)
        difficulty = st.slider("Perceived difficulty of the task", 1, 5, 3)
        feedback = st.text_area("Open feedback (optional)")
        submitted = st.form_submit_button("Submit Exit Questionnaire")
        if submitted:
            row = {
                'timestamp': datetime.now().isoformat(),
                'satisfaction': satisfaction,
                'difficulty': difficulty,
                'feedback': feedback
            }
            append_csv(exit_csv, ['timestamp', 'satisfaction', 'difficulty', 'feedback'], row)
            st.success("Exit questionnaire data recorded.")

# --- Report Tab ---
if tab == "Report":
    st.header("Usability Test Report")
    st.write("Summary of all collected data.")

    def load_csv(file):
        if os.path.isfile(file):
            return pd.read_csv(file)
        else:
            return pd.DataFrame()

    consent_df = load_csv(consent_csv)
    demo_df = load_csv(demographic_csv)
    task_df = load_csv(task_csv)
    exit_df = load_csv(exit_csv)

    st.subheader("Consent Data")
    st.dataframe(consent_df)

    st.subheader("Demographic Data")
    st.dataframe(demo_df)

    st.subheader("Task Data")
    st.dataframe(task_df)

    st.subheader("Exit Questionnaire Data")
    st.dataframe(exit_df)

    # Summary stats
    st.markdown("---")
    st.subheader("Summary Statistics")
    if not task_df.empty:
        avg_time = task_df['duration_seconds'].mean()
        st.write(f"**Average Task Time:** {avg_time:.2f} seconds")
    else:
        st.write("No task data yet.")
    if not exit_df.empty:
        avg_satisfaction = exit_df['satisfaction'].mean()
        avg_difficulty = exit_df['difficulty'].mean()
        st.write(f"**Average Satisfaction:** {avg_satisfaction:.2f} / 5")
        st.write(f"**Average Difficulty:** {avg_difficulty:.2f} / 5")
        # Optional: bar charts
        st.bar_chart(exit_df[['satisfaction', 'difficulty']])
    else:
        st.write("No exit questionnaire data yet.") 
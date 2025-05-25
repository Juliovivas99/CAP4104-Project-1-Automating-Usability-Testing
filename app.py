import streamlit as st
import pandas as pd
import os
import csv
from datetime import datetime

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

# --- Streamlit App ---
st.set_page_config(page_title="Usability Testing Automation Tool", layout="centered")
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
        value="""
        Thank you for participating in this usability test. Your responses will be recorded and used for research purposes only. Participation is voluntary, and you may withdraw at any time. No personally identifying information will be shared. By checking the box below, you provide your digital consent to participate.
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
    st.header("Task 1: Example Task")
    st.write("Please complete the following task:")
    st.info("Task: Example Task. (Replace with your real task description.)")

    if 'task_started' not in st.session_state:
        st.session_state['task_started'] = False
    if 'task_start_time' not in st.session_state:
        st.session_state['task_start_time'] = None
    if 'task_duration' not in st.session_state:
        st.session_state['task_duration'] = None

    col1, col2 = st.columns(2)
    with col1:
        if not st.session_state['task_started']:
            if st.button("Start Task"):
                st.session_state['task_started'] = True
                st.session_state['task_start_time'] = datetime.now()
                st.session_state['task_duration'] = None
        else:
            st.write(f"Task started at: {st.session_state['task_start_time'].strftime('%H:%M:%S')}")
    with col2:
        if st.session_state['task_started']:
            if st.button("Stop Task"):
                end_time = datetime.now()
                duration = (end_time - st.session_state['task_start_time']).total_seconds()
                st.session_state['task_duration'] = duration
                st.session_state['task_started'] = False
                st.success(f"Task completed in {duration:.2f} seconds.")

    if st.session_state['task_duration'] is not None:
        st.write(f"**Task Duration:** {st.session_state['task_duration']:.2f} seconds")

    success = st.radio("Task Outcome", ["Success", "Failure"])
    notes = st.text_area("Observer Notes (optional)")
    if st.button("Submit Task Data"):
        if st.session_state['task_duration'] is None:
            st.warning("Please start and stop the timer before submitting.")
        else:
            row = {
                'timestamp': datetime.now().isoformat(),
                'duration_seconds': st.session_state['task_duration'],
                'success': success,
                'notes': notes
            }
            append_csv(task_csv, ['timestamp', 'duration_seconds', 'success', 'notes'], row)
            st.success("Task data recorded.")
            st.session_state['task_duration'] = None
            st.session_state['task_start_time'] = None

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
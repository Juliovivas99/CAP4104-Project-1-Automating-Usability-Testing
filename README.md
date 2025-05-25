# CAP4104 Project 1 - Automating Usability Testing

This repository contains a Streamlit app for automating usability testing, developed for the HCI course (CAP4104).

## Features

- **Consent Form**: Customizable consent text, digital agreement, and timestamped logging.
- **Demographic Questionnaire**: Collects participant info (name, age, occupation, familiarity).
- **Task Page**: Timer, success/failure, observer notes, and task data logging.
- **Exit Questionnaire**: Satisfaction, difficulty (Likert scale), and open feedback.
- **Report Page**: Aggregates and visualizes all collected data with summary statistics.
- **CSV Data Storage**: All data is saved in the `data/` folder as CSV files for easy analysis.

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd "CAP4104 Project 1 - Automating Usability Testing"
   ```
2. **Create and activate a virtual environment (recommended):**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```sh
   pip install streamlit pandas
   ```
4. **Run the app:**
   ```sh
   streamlit run app.py
   ```

## File Structure

- `app.py` — Main Streamlit app.
- `data/` — Folder containing all CSV data files (created automatically).
- `README.md` — This file.
- `.gitignore` — Excludes `venv/` from version control.

## Workflow Overview

1. **Home**: Introduction and navigation.
2. **Consent**: Participant reviews and agrees to consent terms.
3. **Demographics**: Participant provides background information.
4. **Task**: Participant completes a usability task, with timing and observer notes.
5. **Exit Questionnaire**: Participant rates satisfaction, difficulty, and provides feedback.
6. **Report**: View all collected data and summary statistics.

## Example Data

Sample CSV files will be generated in the `data/` folder as you use the app.

---

**For questions or feedback, please contact the repository owner.**

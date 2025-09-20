# AI-Driven ESG Risk Analyzer

A full-stack web application that uses Natural Language Processing (NLP) to automatically analyze corporate sustainability reports and provide an interactive dashboard for assessing Environmental, Social, and Governance (ESG) risks.

This project was developed as the capstone for the 1M1B Green Internship (Batch 5).

**Live Demo:** [Link will be added after deployment]

---

## Key Features

*   **Automated NLP Analysis:** A Python backend using Flask and spaCy to process PDF reports, flag risk-related keywords, and perform sentiment analysis on the surrounding context.
*   **Advanced Risk Scoring:** Implements a custom algorithm to calculate a single, comparable "Overall Risk Score" for each report based on the severity and frequency of flagged risks.
*   **Interactive Dashboard:** A professional React frontend that provides a clean user interface with summary cards, charts for data visualization, and a detailed findings table.
*   **Dynamic Filtering & Sorting:** Allows users to dynamically filter the detailed results by ESG category, sort by risk severity, and adjust a minimum severity threshold to focus on the most critical issues.
*   **Data Export:** Users can export the filtered and sorted analysis data to a CSV file for further offline analysis in tools like Excel or Google Sheets.

## Tech Stack

*   **Backend:** Python, Flask, spaCy, Pandas, VaderSentiment, Gunicorn
*   **Frontend:** React.js, Chart.js, JavaScript (ES6), HTML/CSS
*   **Deployment:** The backend is deployed on Render and the frontend is deployed on Netlify.

---

## How to Run Locally

### Prerequisites

*   Python 3.8+
*   Node.js and npm
*   Git

### 1. Backend Server Setup

```bash
# Clone the repository
git clone https://github.com/your-username/AI-ESG-Risk-Analyzer.git
cd AI-ESG-Risk-Analyzer

# Navigate to the backend directory
cd backend

# Create and activate a virtual environment
# On Windows:
python -m venv venv
venv\Scripts\activate
# On Mac/Linux:
# python3 -m venv venv
# source venv/bin/activate

# Install the required Python packages
pip install -r requirements.txt

# Download the spaCy language model
python -m spacy download en_core_web_sm

# Add your PDF reports to the 'backend/data' folder

# Run the Flask server
python app.py

### Frontend Server Setup
# Open a new, separate terminal and navigate to the frontend directory
cd frontend

# Install the required npm packages (only needed the first time)
npm install

# Run the React development server
npm start


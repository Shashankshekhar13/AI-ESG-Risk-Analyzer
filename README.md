# AI-ESG-Risk-Analyzer

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat&logo=python)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18-blue?style=flat&logo=react)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](https://opensource.org/licenses/MIT)
[![Deployment](https://img.shields.io/badge/Deployment-Render%20%26%20Netlify-brightgreen?style=flat)](https://render.com/)

A sophisticated full-stack web application designed to automate the detection and analysis of Environmental, Social, and Governance (ESG) risks within corporate sustainability reports. By harnessing Natural Language Processing (NLP), this tool converts unstructured textual data into actionable insights, facilitating faster, data-driven, and transparent risk assessments for investors, regulators, and corporations. Developed as the capstone project for the 1M1B Green Internship (Batch 5).

**Live Demo**: [tinyurl.com/Risk-finder](https://tinyurl.com/Risk-finder)

## Table of Contents

- [Problem and Goal](#problem-and-goal)
- [Key Features](#key-features)
- [Screenshots](#screenshots)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Deployment](#deployment)
- [Project Timeline](#project-timeline)
- [Key Learnings and Project Impact](#key-learnings-and-project-impact)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Problem and Goal

### The Problem
The manual review of extensive corporate sustainability reports—often spanning hundreds of pages—is a time-consuming, inefficient process that frequently overlooks subtle yet critical ESG risks.

### The Goal
To develop an automated solution that accelerates ESG risk assessment, enhances data-driven decision-making, and improves transparency.

### The Opportunity
Leveraging cutting-edge AI technology, this project transforms unstructured report data into structured, actionable insights, empowering stakeholders to make informed decisions in sustainable finance and governance.

## Key Features

- **Automated NLP Analysis**: Utilizes a Python Flask backend with NLTK, spaCy, and PyMuPDF to process PDF reports, identify risk-related keywords, and apply sentiment analysis to contextual data.
- **Advanced Risk Scoring**: Features a proprietary algorithm calculating an "Overall Risk Score" (out of 10) based on risk severity (1-5 scale) and frequency across ESG categories.
- **Interactive Dashboard**: A React-based frontend with summary cards, Chart.js-powered interactive charts, and a detailed risk findings table for real-time insights.
- **Dynamic Filtering & Sorting**: Enables users to filter by ESG category (Environmental, Social, Governance), adjust severity thresholds, and sort by risk severity for focused analysis.
- **Data Export**: Allows exporting filtered data to CSV for integration with tools like Excel or advanced analytics platforms.
- **Mobile Responsiveness**: Offers a fully responsive design, ensuring seamless performance across desktop and mobile devices.
- **Tableau Prototype**: An initial proof-of-concept dashboard visualizing backend outputs via CSV, showcasing risks by company and category.

## Screenshots

![Title Slide - AI-Driven ESG Risk Analysis Overview](images/title_slide.png)  
*Overview of the AI-Driven ESG Risk Analysis project.*

![Problem & Goal - Addressing ESG Challenges](images/problem_goal_slide.png)  
*Highlighting the problem of manual ESG review and the project’s objectives.*

![Building the Data Engine - Backend Development](images/data_engine_slide.png)  
*Showcasing the Python Flask API and NLP pipeline development.*

![Tableau Prototype - Early Visualization](images/tableau_prototype_slide.png)  
*Demonstration of the initial Tableau dashboard prototype.*

![Interactive Web Application - Frontend Evolution](images/web_app_slide.png)  
*Display of the React-based dashboard with live Google report analysis.*

![Final Features & Deployment - Live Application](images/final_features_slide.png)  
*Illustration of the deployed app with advanced features and responsiveness.*

![Explore the Final Project - Access Links](images/explore_project_slide.png)  
*Links to the live app, GitHub, and demo resources.*

![Key Learnings & Impact - Technical Growth](images/learnings_impact_slide.png)  
*Summary of technical learnings and project impact on sustainable finance.*

![Thank You - Project Conclusion](images/thank_you_slide.png)  
*Closing slide acknowledging the internship and support.*

## Tech Stack

- **Backend**: Python, Flask, NLTK, spaCy, PyMuPDF, Pandas, VADER Sentiment, Gunicorn
- **Frontend**: React.js, Chart.js, JavaScript (ES6), HTML/CSS
- **Deployment**: Backend on Render, Frontend on Netlify
- **Other**: Git for version control, Tableau for prototype visualization

## Installation

### Prerequisites
- Python 3.8+
- Node.js and npm
- Git

### Backend Setup
```bash
# Clone the repository
git clone https://github.com/Shashankshekhar13/AI-ESG-Risk-Analyzer.git
cd AI-ESG-Risk-Analyzer

# Navigate to the backend directory
cd backend

# Create and activate a virtual environment
# On Windows:
python -m venv venv
venv\Scripts\activate
# On Mac/Linux:
python3 -m venv venv
source venv/bin/activate

# Install the required Python packages
pip install -r requirements.txt

# Download the spaCy language model
python -m spacy download en_core_web_sm

# Add your PDF reports to the 'backend/data' folder

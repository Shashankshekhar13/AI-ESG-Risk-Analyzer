import os
import spacy
import pandas as pd
import PyPDF2
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask import Flask, jsonify, request
from flask_cors import CORS

# --- Initialize Flask App and CORS ---
# This sets up our web server
app = Flask(__name__)
# CORS is a security feature that allows our React frontend to make requests to this backend
CORS(app)

# --- Global Variables and Models (loaded once at startup) ---
PDF_SOURCE_FOLDER = 'data'
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    print("Spacy model not found. Please run 'python -m spacy download en_core_web_sm'")
    nlp = None
analyzer = SentimentIntensityAnalyzer()

esg_lexicon = {
    'Environmental': [
        'emission', 'spill', 'pollution', 'waste', 'climate change', 'deforestation',
        'contamination', 'environmental fine', 'greenhouse gas', 'ghg', 'carbon footprint'
    ],
    'Social': [
        'layoff', 'strike', 'discrimination', 'safety violation', 'labor', 'workforce',
        'community complaint', 'workplace injury', 'human rights', 'diversity', 'inclusion'
    ],
    'Governance': [
        'lawsuit', 'fine', 'fraud', 'bribery', 'corruption', 'investigation',
        'shareholder complaint', 'non-compliance', 'board diversity', 'executive pay'
    ]
}

# --- Core Functions ---

def extract_text_from_pdf(pdf_path):
    """Extracts all text from a single PDF file."""
    text = ""
    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return None
    return text

def analyze_text(text):
    """Analyzes a block of text for ESG risks."""
    if not nlp:
        return []
        
    flagged_risks = []
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    
    for sentence in sentences:
        for category, keywords in esg_lexicon.items():
            for keyword in keywords:
                if keyword in sentence.lower():
                    sentiment_scores = analyzer.polarity_scores(sentence)
                    negativity_score = sentiment_scores['neg']
                    
                    if negativity_score > 0.1: # Adjustable threshold
                        flagged_risks.append({
                            'category': category,
                            'keyword': keyword,
                            'negativity_score': round(negativity_score, 2),
                            'sentence': sentence.strip()
                        })
                        break  # Move to the next sentence
            else:
                continue
            break
            
    return flagged_risks

# --- API Endpoints ---

@app.route('/api/reports', methods=['GET'])
def get_reports():
    """API endpoint to list available PDF reports in the data folder."""
    try:
        files = [f for f in os.listdir(PDF_SOURCE_FOLDER) if f.endswith('.pdf')]
        return jsonify(files)
    except FileNotFoundError:
        return jsonify({"error": "Data directory not found"}), 404

@app.route('/api/analyze', methods=['GET'])
def analyze_report():
    """API endpoint to analyze a specific report."""
    # Get the filename from the request's query parameters (e.g., /api/analyze?report=company_a.pdf)
    report_name = request.args.get('report')
    
    if not report_name:
        return jsonify({"error": "Report name is required"}), 400
        
    pdf_path = os.path.join(PDF_SOURCE_FOLDER, report_name)
    
    if not os.path.exists(pdf_path):
        return jsonify({"error": f"Report '{report_name}' not found"}), 404
        
    print(f"-> Received request to analyze: {report_name}")
    
    # 1. Extract text
    text = extract_text_from_pdf(pdf_path)
    if text is None:
        return jsonify({"error": "Failed to extract text from PDF"}), 500
        
    # 2. Analyze text
    results = analyze_text(text)
    
    print(f"-> Analysis complete. Found {len(results)} potential risks.")
    
    # 3. Return results as JSON
    return jsonify(results)

# --- Main entry point ---
if __name__ == '__main__':
    # Runs the Flask server
    # debug=True means the server will automatically reload if you change the code
    app.run(debug=True, port=5000)
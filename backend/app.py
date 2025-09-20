import os
import spacy
import pandas as pd
import PyPDF2
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask import Flask, jsonify, request
from flask_cors import CORS

# --- Initialize Flask App and CORS ---
app = Flask(__name__)
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

# --- NEW: ADVANCED SCORING FUNCTION ---
def calculate_risk_score(risks, total_sentences):
    """Calculates a risk score out of 10 based on frequency and severity."""
    if not risks or total_sentences == 0:
        return {
            "score": 0,
            "severity": 0,
            "frequency": 0
        }

    # Factor 1: Severity (the average negativity of all flagged sentences)
    total_negativity = sum(item['negativity_score'] for item in risks)
    average_severity = total_negativity / len(risks)

    # Factor 2: Frequency (how often risks appear, normalized per 1000 sentences)
    normalized_frequency = (len(risks) / total_sentences) * 1000

    # Combine them into a final score. We can weigh them, e.g., 60% for severity, 40% for frequency.
    final_score = (average_severity * 6) + (normalized_frequency * 0.4) 
    
    return {
        "score": min(round(final_score, 1), 10.0), # Cap the score at 10 and round it
        "severity": round(average_severity, 2),
        "frequency": round(normalized_frequency, 2)
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

# --- UPGRADED: analyze_text function now returns a full analysis object ---
def analyze_text(text):
    """Analyzes a block of text for ESG risks and calculates scores."""
    if not nlp:
        return {} # Return empty object if NLP model fails
        
    flagged_risks = []
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    
    # The loop to find risks is the same
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
            
    # Calculate scores after finding all risks
    total_sentences_in_doc = len(sentences)
    scores = calculate_risk_score(flagged_risks, total_sentences_in_doc)
    
    # Return a complete analysis object
    return {
        "overall_risk_score": scores["score"],
        "average_severity": scores["severity"],
        "normalized_frequency": scores["frequency"],
        "total_risks_found": len(flagged_risks),
        "report_length_sentences": total_sentences_in_doc,
        "findings": flagged_risks  # The detailed list of sentences
    }

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
        
    # 2. Analyze text (this now returns the full analysis object)
    results = analyze_text(text)
    
    if results:
      print(f"-> Analysis complete. Score: {results.get('overall_risk_score')}. Found {results.get('total_risks_found')} risks.")
    else:
      print("-> Analysis complete. No results generated.")

    # 3. Return the entire results object as JSON
    return jsonify(results)

# --- Main entry point ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)
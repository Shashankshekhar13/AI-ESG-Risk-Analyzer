import os
import nltk
from nltk.tokenize import sent_tokenize
import pandas as pd
import fitz  # PyMuPDF
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask import Flask, jsonify, request
from flask_cors import CORS

# Download the NLTK model for sentence tokenization
nltk.download('punkt')

# Initialize Flask App and CORS
app = Flask(__name__)
CORS(app)

# Global Variables and Models
PDF_SOURCE_FOLDER = 'data'
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

# The scoring function is unchanged
def calculate_risk_score(risks, total_sentences):
    """Calculates a risk score out of 10 based on frequency and severity."""
    if not risks or total_sentences == 0:
        return {"score": 0, "severity": 0, "frequency": 0}
    total_negativity = sum(item['negativity_score'] for item in risks)
    average_severity = total_negativity / len(risks)
    normalized_frequency = (len(risks) / total_sentences) * 1000
    final_score = (average_severity * 6) + (normalized_frequency * 0.4) 
    return {
        "score": min(round(final_score, 1), 10.0),
        "severity": round(average_severity, 2),
        "frequency": round(normalized_frequency, 2)
    }

# --- UPGRADED: High-speed PDF text extraction function ---
def extract_text_from_pdf(pdf_path):
    """Extracts all text from a single PDF file using the fast PyMuPDF library."""
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return None
    return text

# The analysis function is unchanged (it already uses NLTK)
def analyze_text(text):
    """Analyzes a block of text for ESG risks using NLTK (low memory)."""
    flagged_risks = []
    sentences = sent_tokenize(text)
    for sentence in sentences:
        sentence = sentence.replace('\n', ' ').strip()
        if not sentence:
            continue
        for category, keywords in esg_lexicon.items():
            for keyword in keywords:
                if keyword in sentence.lower():
                    sentiment_scores = analyzer.polarity_scores(sentence)
                    negativity_score = sentiment_scores['neg']
                    if negativity_score > 0.1:
                        flagged_risks.append({
                            'category': category,
                            'keyword': keyword,
                            'negativity_score': round(negativity_score, 2),
                            'sentence': sentence
                        })
                        break
            else:
                continue
            break
            
    total_sentences_in_doc = len(sentences)
    scores = calculate_risk_score(flagged_risks, total_sentences_in_doc)
    
    return {
        "overall_risk_score": scores["score"],
        "average_severity": scores["severity"],
        "normalized_frequency": scores["frequency"],
        "total_risks_found": len(flagged_risks),
        "report_length_sentences": total_sentences_in_doc,
        "findings": flagged_risks
    }

# The API endpoints are unchanged
@app.route('/api/reports', methods=['GET'])
def get_reports():
    try:
        files = [f for f in os.listdir(PDF_SOURCE_FOLDER) if f.endswith('.pdf')]
        return jsonify(files)
    except FileNotFoundError:
        return jsonify({"error": "Data directory not found"}), 404

@app.route('/api/analyze', methods=['GET'])
def analyze_report():
    report_name = request.args.get('report')
    if not report_name:
        return jsonify({"error": "Report name is required"}), 400
    pdf_path = os.path.join(PDF_SOURCE_FOLDER, report_name)
    if not os.path.exists(pdf_path):
        return jsonify({"error": f"Report '{report_name}' not found"}), 404
        
    print(f"-> Received request to analyze: {report_name}")
    text = extract_text_from_pdf(pdf_path)
    if text is None:
        return jsonify({"error": "Failed to extract text from PDF"}), 500
        
    results = analyze_text(text)
    
    if results and 'overall_risk_score' in results:
      print(f"-> Analysis complete. Score: {results.get('overall_risk_score')}. Found {results.get('total_risks_found')} risks.")
    else:
      print("-> Analysis complete. No valid results generated.")

    return jsonify(results)

# The main entry point is unchanged
if __name__ == '__main__':
    app.run(debug=True, port=5000)
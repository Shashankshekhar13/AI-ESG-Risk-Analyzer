import os
import spacy
import pandas as pd
import PyPDF2
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# --- Configuration ---
PDF_SOURCE_FOLDER = 'data'  # Folder where all your ESG reports are stored
OUTPUT_CSV_FILE = 'tableau_export_data.csv'
# --- End of Configuration ---

# Load NLP models once to be efficient
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    print("Spacy model not found. Please run 'python -m spacy download en_core_web_sm'")
    nlp = None
analyzer = SentimentIntensityAnalyzer()

# The "brain" of our analysis: a dictionary of ESG keywords
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

def extract_text_from_pdf(pdf_path):
    """Extracts all text from a single PDF file."""
    text = ""
    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"  -> ERROR extracting text from {pdf_path}: {e}")
        return ""
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

                    if negativity_score > 0.1:  # Adjustable threshold
                        flagged_risks.append({
                            'category': category,
                            'keyword': keyword,
                            'negativity_score': round(negativity_score, 2),
                            'sentence': sentence.strip()
                        })
                        break  # Move to next sentence after first match
            else:
                continue
            break

    return flagged_risks

# --- Main Script Logic ---
if __name__ == '__main__':
    all_results = []
    print("Starting batch analysis for Tableau export...")

    for filename in os.listdir(PDF_SOURCE_FOLDER):
        if filename.endswith('.pdf'):
            print(f"  -> Processing {filename}...")
            pdf_path = os.path.join(PDF_SOURCE_FOLDER, filename)

            # --- Smart Company Name Extraction ---
            simple_name = filename.lower()
            if 'microsoft' in simple_name:
                company_name = 'Microsoft'
            elif 'google' in simple_name or 'alphabet' in simple_name:
                company_name = 'Alphabet (Google)'
            elif 'apple' in simple_name:
                company_name = 'Apple'
            elif 'amazon' in simple_name:
                company_name = 'Amazon'
            elif 'nvidia' in simple_name:
                company_name = 'NVIDIA'
            else:
                company_name = os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' ').title()
            # --- End of Name Extraction ---

            text = extract_text_from_pdf(pdf_path)
            results = analyze_text(text)

            for res in results:
                res['company'] = company_name

            all_results.extend(results)

    # --- Save Results for Tableau ---
    if all_results:
        df = pd.DataFrame(all_results)

        # ✅ Summarize for Tableau: One row per company-category
        summary_df = df.groupby(['company', 'category']).agg(
            Risk_Count=('keyword', 'count'),
            Avg_Negativity=('negativity_score', 'mean')
        ).reset_index()

        summary_df.to_csv(OUTPUT_CSV_FILE, index=False, encoding='utf-8')
        print(f"\n✅ Export complete. {len(summary_df)} rows saved for Tableau.")
        print(f"📁 Data saved to '{OUTPUT_CSV_FILE}'. You can now import this into Tableau.")
    else:
        print("⚠️ No risks found in any documents.")

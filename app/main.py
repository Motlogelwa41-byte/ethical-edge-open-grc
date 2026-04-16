import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
import PyPDF2

# Load environment variables (API Keys)
load_dotenv()

app = Flask(__name__)
import os

# 1. Define the path: Start at main.py, go UP one level (..), then into 'uploads'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_PATH = os.path.normpath(os.path.join(BASE_DIR, "..", "uploads"))

# 2. Configure Flask to use this absolute path
app.config['UPLOAD_FOLDER'] = UPLOAD_PATH

# 3. Safety check: Create the folder automatically if it's missing
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
def process_ngo_report(file_path):
    # 1. Load the King V Checklist logic
    try:
        with open('../data/king_v_checklist.json', 'r') as f:
            guidelines = f.read()
    except FileNotFoundError:
        guidelines = "King V Principles: Transparency, Accountability, Ethical Leadership."

    # 2. Extract Text from the uploaded PDF
    reader = PyPDF2.PdfReader(file_path)
    report_text = ""
    for page in reader.pages:
        report_text += page.extract_text()

    # 3. Initialize AI Agent (GPT-4)
    chat = ChatOpenAI(model="gpt-4-turbo", temperature=0)
    
    # 4. Construct the prompt for the Gates Foundation 'Trust Bridge'
    query = f"""
    You are an expert GRC Auditor for the Gates Foundation. 
    Analyze this NGO Financial Report against these King V Governance Principles:
    
    Principles: {guidelines}
    
    Report Content: {report_text[:4000]} 
    
    Response Format (JSON):
    1. Compliance_Score (0-100)
    2. Missing_Disclosures (List)
    3. Recommendations (List)
    """
    
    response = chat.invoke([HumanMessage(content=query)])
    return response.content

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/v1/analyze-report', methods=['POST'])
def analyze_report():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save file to uploads folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Run AI Analysis
    result = process_ngo_report(file_path)
    
    return jsonify({
        "status": "success",
        "analysis": result
    })

if __name__ == '__main__':
    app.run(debug=True)

# Gates Foundation AI Grand Challenge: Ethical Edge Open GRC

## Problem Statement
International giving to LMICs is hindered by compliance friction. Donors lack real-time visibility into the governance health of regional NGOs.

## Our Solution
We are converting our static GRC framework into an AI-powered "Trust Bridge." 
1. **AI Auditor:** An agent that parses financial reports against King V standards.
2. **Compliance API:** A standardized data pipeline for donor discovery tools.

## Alignment with RFP
- **Track:** Reducing Friction & Infrastructure.
- **Geography:** Botswana & SADC Region.
3. Next Technical Step
Open your app/main.py and replace the pass in the process_ngo_report function with this logic to start the AI integration:

Python
def process_ngo_report(file_path):
    import PyPDF2
    # Load the King V Checklist for the AI to use as a reference
    with open('data/king_v_checklist.json', 'r') as f:
        guidelines = f.read()
    
    # Extract text from the uploaded NGO report
    reader = PyPDF2.PdfReader(file_path)
    report_text = ""
    for page in reader.pages:
        report_text += page.extract_text()

    # This string will be sent to the LLM in the next step
    prompt = f"Analyze this NGO report against these King V guidelines: {guidelines}. Report: {report_text}"
    return prompt

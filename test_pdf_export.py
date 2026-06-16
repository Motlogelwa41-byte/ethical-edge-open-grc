import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.api.endpoints.reports import export_compliance_audit_report

async def run_pdf_test():
    print("🎨 Initializing PDF Reporting Engine...")
    try:
        streaming_response = await export_compliance_audit_report(tenant_id="tenant_sme_001")
        output_filename = "SME_Command_Center_Audit_Packet.pdf"
        
        with open(output_filename, "wb") as f:
            async for chunk in streaming_response.body_iterator:
                f.write(chunk)
                
        print(f"✅ Success! Report programmatically compiled and saved.")
        print(f"👉 File generated in root: {os.path.abspath(output_filename)}")
        
    except Exception as e:
        print(f"❌ PDF Engine Failure: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_pdf_test())

# Save this update within your report generation pipeline logic

def get_report_meta_and_cover(client_name):
    from datetime import datetime
    current_date = datetime.now().strftime("%d %B %Y")
    
    cover_letter_data = {
        "company": "Ethical Edge GRC Consulting",
        "date": current_date,
        "client": client_name,
        "signatory": "Boitshwarelo Motlogelwa",
        "title": "Managing Director & Principal Consultant",
        "intro_philosophy": "Organizations that actively build trust into their operational DNA capture a 'Trust Dividend'—resulting in stronger stakeholder relations, protected revenue streams, and long-term resilience."
    }
    return cover_letter_data

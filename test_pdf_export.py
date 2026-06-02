cat << 'EOF' > test_pdf_export.py
import asyncio
from app.api.endpoints.reports import export_compliance_audit_report

async def run_pdf_test():
    print("🎨 Initializing PDF Reporting Engine...")
    try:
        # Call the reporting function directly
        streaming_response = await export_compliance_audit_report(tenant_id="tenant_sme_001")
        
        # Consume the streaming content and write it to a physical file
        output_filename = "SME_Command_Center_Audit_Packet.pdf"
        with open(output_filename, "wb") as f:
            async for chunk in streaming_response.body_iterator:
                f.write(chunk)
                
        print(f"✅ Success! Report programmatically compiled and saved to your directory.")
        print(f"👉 File generated: {output_filename}")
        
    except Exception as e:
        print(f"❌ PDF Engine Failure: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_pdf_test())
EOF

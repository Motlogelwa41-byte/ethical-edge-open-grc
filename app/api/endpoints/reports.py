from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse
from io import BytesIO
from datetime import datetime, timezone

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

router = APIRouter()

class Line(Flowable):
    def __init__(self, x1, y1, x2, y2, thickness=1, color=colors.black):
        super().__init__()
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.thickness, self.color = thickness, color
    def draw(self):
        self.canv.saveState()
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(self.x1, self.y1, self.x2, self.y2)
        self.canv.restoreState()

@router.get("/export-audit-pdf", status_code=status.HTTP_200_OK)
async def export_compliance_audit_report(tenant_id: str = "tenant_sme_001"):
    report_date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    attainment_rate = 50.0  
    system_status = "AT RISK" if attainment_rate < 70 else "COMPLIANT"
    
    control_results = [
        {"id": "A.8.5", "name": "Multi-Factor Authentication Enforcement", "framework": "ISO/IEC 27001:2022", "status": "FAILED", "details": "AWS API Token Invalid (InvalidClientTokenId)"},
        {"id": "PR.DS-01", "name": "Data Repositories Protection & Leak Mitigation", "framework": "NIST CSF 2.0", "status": "PASSED", "details": "0 public repositories exposed on target workspace profile."}
    ]

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=45, leftMargin=45, topMargin=45, bottomMargin=45)
    story = []
    styles = getSampleStyleSheet()
    
    PRIMARY_COLOR = colors.HexColor("#1A365D")
    ACCENT_RED = colors.HexColor("#C53030")
    TEXT_COLOR = colors.HexColor("#2D3748")

    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=PRIMARY_COLOR, spaceAfter=6)
    subtitle_style = ParagraphStyle('DocSubtitle', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor("#718096"), spaceAfter=20)
    section_heading = ParagraphStyle('SecHeading', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=PRIMARY_COLOR, spaceBefore=15, spaceAfter=10)
    body_style = ParagraphStyle('BodyDark', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=TEXT_COLOR)

    story.append(Paragraph("ETHICAL EDGE OPEN GRC — COMMAND CENTER", title_style))
    story.append(Paragraph(f"<b>Executive Compliance & Audit Report</b> | System Instance: {tenant_id} | Generated: {report_date}", subtitle_style))
    story.append(Spacer(1, 10))

    summary_data = [
        [Paragraph("<b>Framework Attainment</b>", body_style), Paragraph("<b>Active Threats Monitor</b>", body_style), Paragraph("<b>Audit Posture Status</b>", body_style)],
        [Paragraph(f"<font size=20 color='{PRIMARY_COLOR.hexval()}'><b>{attainment_rate}%</b></font>", body_style), Paragraph("<font size=20 color='#C53030'><b>1 Issue</b></font>", body_style), Paragraph(f"<font size=16 color='{ACCENT_RED.hexval() if system_status == 'AT RISK' else '#2F855A'}'><b>{system_status}</b></font>", body_style)]
    ]
    
    summary_table = Table(summary_data, colWidths=[2.3*inch, 2.3*inch, 2.3*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EDF2F7")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 20))

    story.append(Paragraph("Continuous Control Monitoring (CCM) Log Registry", section_heading))
    story.append(Spacer(1, 10))

    grid_data = [[
        Paragraph("<font color='white'><b>Control Ref</b></font>", body_style),
        Paragraph("<font color='white'><b>Target Domain Name</b></font>", body_style),
        Paragraph("<font color='white'><b>Standard</b></font>", body_style),
        Paragraph("<font color='white'><b>Status</b></font>", body_style),
        Paragraph("<font color='white'><b>Telemetry Audit Context Proof</b></font>", body_style)
    ]]

    for item in control_results:
        status_color = "#2F855A" if item["status"] == "PASSED" else "#C53030"
        grid_data.append([
            Paragraph(item["id"], body_style),
            Paragraph(item["name"], body_style),
            Paragraph(item["framework"], body_style),
            Paragraph(f"<font color='{status_color}'><b>{item['status']}</b></font>", body_style),
            Paragraph(item["details"], body_style)
        ])

    evidence_table = Table(grid_data, colWidths=[1.0*inch, 1.8*inch, 1.4*inch, 0.9*inch, 2.4*inch])
    evidence_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_COLOR),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
    ]))
    story.append(evidence_table)
    story.append(Spacer(1, 30))

    footer_text = "<b>Regulatory Disclaimer:</b> Compiled programmatically by Ethical Edge GRC continuous verification modules."
    story.append(KeepTogether([
        Line(0, 0, 480, 0, thickness=0.5, color=colors.HexColor("#CBD5E0")),
        Spacer(1, 10),
        Paragraph(footer_text, ParagraphStyle('Foot', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=8, leading=11, textColor=colors.HexColor("#A0AEC0")))
    ]))

    doc.build(story)
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="application/pdf")

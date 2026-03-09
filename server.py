from flask import Flask, request, send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
import uuid

app = Flask(_name_)

@app.route("/")
def home():
    return "Receipt server running"

@app.route("/generate-receipt", methods=["POST"])
def generate_receipt():
    data = request.json
    file_path = f"receipt_{uuid.uuid4().hex}.pdf"

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    story = []

    story.append(Paragraph("PAYMENT RECEIPT", styles['Heading1']))
    story.append(Spacer(1,12))

    details = [
        ["Receipt No:", uuid.uuid4().hex[:8].upper()],
        ["Date:", datetime.now().strftime("%Y-%m-%d %H:%M")],
        ["Customer:", data["customer"]],
        ["Email:", data["email"]],
        ["Payment Method:", data["method"]],
        ["Amount Paid:", f"KES {data['amount']}"],
    ]

    table = Table(details, colWidths=[120, 300])
    table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(0,-1),colors.whitesmoke),
        ('GRID',(0,0),(-1,-1),1,colors.black),
    ]))

    story.append(table)
    story.append(Spacer(1,12))
    story.append(Paragraph("Thank you for your business!", styles['Normal']))

    doc.build(story)
    return send_file(file_path, as_attachment=True)

if _name_ == "_main_":
    app.run()

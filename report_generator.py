import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


def generate_pdf(assessment, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    document = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    elements = []

    elements.append(
        Paragraph("IoT Security Risk Assessment Report", styles["Title"])
    )
    elements.append(Spacer(1, 15))

    elements.append(
        Paragraph(
            f"Device: {assessment.device_name}",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            f"Device Type: {assessment.device_type}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Assessment Date: {assessment.created_at.strftime('%Y-%m-%d %H:%M')}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 15))

    summary = [
        ["Risk Score", "Risk Classification"],
        [
            f"{assessment.risk_score}/100",
            assessment.risk_level
        ]
    ]

    table = Table(summary, colWidths=[200, 200])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#172B4D")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#F0F3F8")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 10),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph("Identified Security Weaknesses", styles["Heading2"])
    )

    if assessment.findings:
        for finding in assessment.findings:
            text = (
                f"<b>{finding['factor']}</b>: "
                f"{finding['value']} "
                f"(Risk contribution: {finding['weighted_score']})"
            )
            elements.append(Paragraph(text, styles["Normal"]))
            elements.append(Spacer(1, 6))
    else:
        elements.append(
            Paragraph("No elevated-risk configuration factors were identified.",
                      styles["Normal"])
        )

    elements.append(Spacer(1, 15))

    elements.append(
        Paragraph("Security Recommendations", styles["Heading2"])
    )

    for item in assessment.recommendations:
        elements.append(
            Paragraph(
                f"<b>{item['area']}:</b> {item['recommendation']}",
                styles["Normal"]
            )
        )
        elements.append(Spacer(1, 8))

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "Assessment limitation: This report evaluates user-provided "
            "configuration information using predefined rules. It does not "
            "perform live network scanning or independently verify device "
            "vulnerabilities.",
            styles["Italic"]
        )
    )

    document.build(elements)

    return output_path
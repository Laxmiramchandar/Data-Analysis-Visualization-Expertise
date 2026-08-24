import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

class ReportGenerator:
    """
    Automated PDF Report Engine built on ReportLab Platypus framework.
    Generates executive-ready PDF reports with embedded charts, KPI summary tables, and business insights.
    """

    def __init__(self, output_dir='reports'):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._init_custom_styles()

    def _init_custom_styles(self):
        """Initializes report color palette and custom typography hierarchy."""
        primary_color = colors.HexColor('#0f172a')
        secondary_color = colors.HexColor('#1e40af')
        accent_color = colors.HexColor('#0284c7')

        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=22,
            leading=26,
            textColor=colors.white,
            alignment=TA_CENTER,
            spaceAfter=10
        ))

        self.styles.add(ParagraphStyle(
            name='ReportSubTitle',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=12,
            leading=16,
            textColor=colors.HexColor('#cbd5e1'),
            alignment=TA_CENTER,
            spaceAfter=15
        ))

        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=15,
            leading=19,
            textColor=secondary_color,
            spaceBefore=14,
            spaceAfter=8,
            keepWithNext=True
        ))

        self.styles.add(ParagraphStyle(
            name='SubSectionHeading',
            parent=self.styles['Heading3'],
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=15,
            textColor=accent_color,
            spaceBefore=10,
            spaceAfter=6,
            keepWithNext=True
        ))

        self.styles.add(ParagraphStyle(
            name='ExecutiveBody',
            parent=self.styles['BodyText'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#334155'),
            alignment=TA_JUSTIFY,
            spaceAfter=8
        ))

        self.styles.add(ParagraphStyle(
            name='InsightBullet',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13.5,
            textColor=colors.HexColor('#1e293b'),
            leftIndent=15,
            firstLineIndent=-10,
            spaceAfter=5
        ))

        self.styles.add(ParagraphStyle(
            name='TableHead',
            fontName='Helvetica-Bold',
            fontSize=9.5,
            leading=12,
            textColor=colors.white,
            alignment=TA_CENTER
        ))

        self.styles.add(ParagraphStyle(
            name='TableCell',
            fontName='Helvetica',
            fontSize=9,
            leading=12,
            textColor=colors.HexColor('#0f172a'),
            alignment=TA_CENTER
        ))

        self.styles.add(ParagraphStyle(
            name='FigureCaption',
            fontName='Helvetica-Oblique',
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor('#64748b'),
            alignment=TA_CENTER,
            spaceBefore=4,
            spaceAfter=12
        ))

    def generate_project_report(self, title, domain_name, filename, executive_summary, kpi_data, insights, recommendations, image_paths, hypothesis_data=None):
        """
        Generates a complete domain analysis PDF report.
        """
        filepath = os.path.join(self.output_dir, filename)
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
        )

        elements = []

        # --- Header Banner ---
        banner_table_data = [
            [Paragraph(title.upper(), self.styles['ReportTitle'])],
            [Paragraph(f"Domain Executive Briefing: {domain_name} | Date: August 2026", self.styles['ReportSubTitle'])]
        ]
        banner_table = Table(banner_table_data, colWidths=[530])
        banner_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0f172a')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 16),
            ('BOTTOMPADDING', (0,0), (-1,-1), 14),
            ('LEFTPADDING', (0,0), (-1,-1), 15),
            ('RIGHTPADDING', (0,0), (-1,-1), 15),
        ]))
        elements.append(banner_table)
        elements.append(Spacer(1, 15))

        # --- Executive Summary ---
        elements.append(Paragraph("1. Executive Summary", self.styles['SectionHeading']))
        elements.append(Paragraph(executive_summary, self.styles['ExecutiveBody']))
        elements.append(Spacer(1, 10))

        # --- Key Performance Indicators (KPIs) ---
        elements.append(Paragraph("2. Key Performance Indicators (KPI Overview)", self.styles['SectionHeading']))
        kpi_table_content = [
            [Paragraph("Metric Description", self.styles['TableHead']), Paragraph("Key Performance Value", self.styles['TableHead']), Paragraph("Strategic Benchmark / Context", self.styles['TableHead'])]
        ]
        for row in kpi_data:
            kpi_table_content.append([
                Paragraph(str(row[0]), self.styles['TableCell']),
                Paragraph(str(row[1]), self.styles['TableCell']),
                Paragraph(str(row[2]), self.styles['TableCell'])
            ])

        kpi_table = Table(kpi_table_content, colWidths=[200, 150, 180])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        elements.append(kpi_table)
        elements.append(Spacer(1, 15))

        # --- Formal Hypothesis Testing (NEW) ---
        if hypothesis_data:
            elements.append(Paragraph("3. Formal Statistical Hypothesis Testing", self.styles['SectionHeading']))
            for key, val in hypothesis_data.items():
                elements.append(Paragraph(f"<b>{key}:</b> {val}", self.styles['InsightBullet']))
            elements.append(Spacer(1, 15))
            
            elements.append(Paragraph("4. Core Analytical & Statistical Insights", self.styles['SectionHeading']))
        else:
            elements.append(Paragraph("3. Core Analytical & Statistical Insights", self.styles['SectionHeading']))
            
        for idx, insight in enumerate(insights, 1):
            bullet_text = f"<b>Insight {idx}:</b> {insight}"
            elements.append(Paragraph(bullet_text, self.styles['InsightBullet']))
        elements.append(Spacer(1, 15))

        # --- Visualizations ---
        if hypothesis_data:
            elements.append(Paragraph("5. Graphical Analytics & Visual Evidence", self.styles['SectionHeading']))
        else:
            elements.append(Paragraph("4. Graphical Analytics & Visual Evidence", self.styles['SectionHeading']))
            
        for idx, img_path in enumerate(image_paths, 1):
            if os.path.exists(img_path):
                img = Image(img_path, width=500, height=250)
                elements.append(img)
                caption = f"Figure {idx}: Visual analytical representation derived from {domain_name} dataset."
                elements.append(Paragraph(caption, self.styles['FigureCaption']))
                elements.append(Spacer(1, 10))

        # --- Recommendations ---
        if hypothesis_data:
            elements.append(Paragraph("6. Strategic Recommendations & Action Plan", self.styles['SectionHeading']))
        else:
            elements.append(Paragraph("5. Strategic Recommendations & Action Plan", self.styles['SectionHeading']))
            
        for idx, rec in enumerate(recommendations, 1):
            bullet_text = f"<b>Action {idx}:</b> {rec}"
            elements.append(Paragraph(bullet_text, self.styles['InsightBullet']))

        # Build document
        doc.build(elements)
        print(f"Report generated successfully: {filepath}")
        return filepath

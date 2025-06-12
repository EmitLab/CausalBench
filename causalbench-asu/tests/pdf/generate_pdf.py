from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Spacer


# Create a PDF document
pdf_filename = "example.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=A4)

# Styles for text
styles = getSampleStyleSheet()

# Define left-aligned styles
title_style = ParagraphStyle(
    name="Title",
    parent=styles["Title"],
    alignment=0
)
subtitle_style = ParagraphStyle(
    name="Subtitle",
    parent=styles["Heading3"],
    alignment=0,
    spaceBefore=0,
    spaceAfter=20
)
body_style = ParagraphStyle(
    name="Body",
    parent=styles["BodyText"],
    alignment=0
)
legend_style = ParagraphStyle(
    name="Body",
    parent=styles["BodyText"],
    alignment=0,

)

# Text above the table
title = Paragraph("CausalBench: Causal Analysis Report", title_style)
subtitle = Paragraph("&lt;YYYY-MM-dd HH:mm:ss&gt;", subtitle_style)
effect = Paragraph("<b>Effect on:</b> &lt;effect variable name&gt;", body_style)
filters = Paragraph("<b>Filters:</b> &lt;specified filters&gt;", body_style)
spacer = Spacer(1, 25)

# Load images
img_up = Image("images/up.png", width=16, height=16)
img_down = Image("images/down.png", width=16, height=16)

# Table data
table_data = [
    ["Variable", "Effect", "Strength"],
    ["CPU Single Core", img_up, -0.8],
    ["CPU Multi Core", img_down, 0.7],
    ["GPU Score", img_down, 0.6]
]

# Create the table
table = Table(table_data, colWidths="*")

# Style the table
table_style = [
    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

    # Column alignment
    ("ALIGN", (0, 0), (0, -1), "LEFT"),
    ("ALIGN", (1, 0), (1, -1), "CENTER"),
    ("ALIGN", (2, 0), (2, -1), "RIGHT"),

    # Vertical alignment
    ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),

    # Outer box
    ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
]

# Line below each row
for i in range(len(table_data) - 1):
    table_style.append(("LINEBELOW", (0, i), (-1, i), 0.5, colors.grey))

table.setStyle(TableStyle(table_style))

# Legend
legend_data = [
    [img_up, "This variable improves <effect variable name>"],
    [img_down, "This variable worsens <effect variable name>"],
]

legend = Table(legend_data, hAlign="LEFT")

legend_style = [
    # Column alignment
    ("ALIGN", (0, 0), (0, -1), "CENTER"),
    ("ALIGN", (1, 0), (1, -1), "LEFT"),

    # Vertical alignment
    ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
]

legend.setStyle(TableStyle(legend_style))

# Build PDF
doc.build([title, subtitle, effect, filters, spacer, table, spacer, legend])

print(f"PDF created: {pdf_filename}")

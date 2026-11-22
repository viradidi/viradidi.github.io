from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable, KeepTogether
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "resume" / "Isaiah-Nyakundi-Data-Engineer-Resume.pdf"

INK = HexColor("#182B3A")
ACCENT = HexColor("#1C657A")
MUTED = HexColor("#586875")
LIGHT = HexColor("#D9E3E8")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="NameCV", fontName="Helvetica-Bold", fontSize=21, leading=23, textColor=INK, spaceAfter=2))
styles.add(ParagraphStyle(name="RoleCV", fontName="Helvetica-Bold", fontSize=9.2, leading=12, textColor=ACCENT, spaceAfter=5))
styles.add(ParagraphStyle(name="ContactCV", fontName="Helvetica", fontSize=7.55, leading=10.4, textColor=MUTED, spaceAfter=2))
styles.add(ParagraphStyle(name="SectionCV", fontName="Helvetica-Bold", fontSize=9.1, leading=11, textColor=ACCENT, spaceBefore=8, spaceAfter=3, keepWithNext=True))
styles.add(ParagraphStyle(name="BodyCV", fontName="Helvetica", fontSize=8.15, leading=10.25, textColor=INK, spaceAfter=2.6))
styles.add(ParagraphStyle(name="BulletCV", fontName="Helvetica", fontSize=8.05, leading=10.1, textColor=INK, leftIndent=11, firstLineIndent=-7, bulletIndent=1, spaceAfter=1.4))
styles.add(ParagraphStyle(name="ProjectTitleCV", fontName="Helvetica-Bold", fontSize=8.85, leading=10.2, textColor=INK, spaceBefore=4.2, spaceAfter=1.2, keepWithNext=True))
styles.add(ParagraphStyle(name="StackCV", fontName="Helvetica-Oblique", fontSize=7.45, leading=9.2, textColor=MUTED, spaceAfter=1.7, keepWithNext=True))
styles.add(ParagraphStyle(name="SmallCV", fontName="Helvetica", fontSize=7.8, leading=9.7, textColor=INK, spaceAfter=1.5))
styles.add(ParagraphStyle(name="PageHeaderCV", fontName="Helvetica-Bold", fontSize=8, leading=9, textColor=ACCENT))

story = []

def para(text, style="BodyCV"):
    story.append(Paragraph(text, styles[style]))

def section(title):
    para(escape(title.upper()), "SectionCV")
    story.append(HRFlowable(width="100%", thickness=0.55, color=LIGHT, spaceBefore=0, spaceAfter=4))

def bullet(text):
    para("&#8226;&nbsp; " + text, "BulletCV")

def project(title, stack, problem, built, result, quality=None):
    parts = [
        Paragraph(escape(title), styles["ProjectTitleCV"]),
        Paragraph("<b>Stack:</b> " + escape(stack), styles["StackCV"]),
        Paragraph("<b>Problem:</b> " + escape(problem), styles["SmallCV"]),
        Paragraph("<b>What I built:</b> " + escape(built), styles["SmallCV"]),
    ]
    if quality:
        parts.append(Paragraph("<b>Quality:</b> " + escape(quality), styles["SmallCV"]))
    parts.append(Paragraph("<b>Result:</b> " + escape(result), styles["SmallCV"]))
    story.append(KeepTogether(parts))

para("Isaiah Nyakundi", "NameCV")
para("Data Engineer | Cloud Data Platforms | Analytics Engineering", "RoleCV")
para("Nairobi, Kenya &nbsp;|&nbsp; +254 719 367 955 &nbsp;|&nbsp; <link href='mailto:isaiahnyakundi87@gmail.com' color='#1C657A'>isaiahnyakundi87@gmail.com</link>", "ContactCV")
para("<link href='https://www.linkedin.com/in/isaiah-nyakundi-2b58812b4' color='#1C657A'>linkedin.com/in/isaiah-nyakundi-2b58812b4</link> &nbsp;|&nbsp; <link href='https://github.com/viradidi' color='#1C657A'>github.com/viradidi</link> &nbsp;|&nbsp; Portfolio: <link href='https://viradidi.github.io/' color='#1C657A'>https://viradidi.github.io/</link>", "ContactCV")
story.append(Spacer(1, 3))

section("Professional Summary")
para("Data engineer with nearly two years of freelance experience building cloud and real-time data pipelines on Azure, Databricks, Snowflake, Kafka, Flink and Apache Iceberg. Builds pipelines that load incrementally, check data quality and can be rerun safely. Each project below was built and run end to end.")

section("Experience")
para("<b>Freelance Data Engineer</b>")
para("<font color='#586875'>Independent | December 2024 – Present</font>", "SmallCV")
bullet("Design and build cloud data pipelines and lakehouses for ingestion, transformation and reporting on Azure and Snowflake.")
bullet("Load data incrementally with watermarks and control tables, so reruns do not create duplicate records.")
bullet("Add data quality checks, audit logs and reconciliation to each pipeline stage.")
bullet("Orchestrate pipelines with Azure Data Factory, Databricks Jobs and Snowflake Tasks, using Python, PySpark and SQL.")

section("Projects")
project(
    "AtlasFlow: Real-Time Logistics Control Tower",
    "PostgreSQL, Debezium, Apache Kafka, Apache Flink SQL, Apache Iceberg, Trino, Apache Superset, Docker Compose",
    "Operations teams need current shipment status, but batch reporting lags behind changes in the source database.",
    "Captured PostgreSQL changes with Debezium and Kafka, then ran three Flink SQL streaming jobs that write Bronze, Silver and Gold Iceberg tables.",
    "Gold holds one current record per shipment, updated by key, with a rule-based risk classification. Runs end to end in Docker Compose on synthetic data."
)
project(
    "HealthGrid Data Platform",
    "Azure Data Factory, Azure Databricks, PySpark, Azure SQL, PostgreSQL, ADLS Gen2",
    "Repeated, missed or overwritten source loads leave inconsistent records.",
    "Azure SQL control tables choose a FULL, APPEND or MERGE load for each source. Watermarks and a file manifest block repeat loads. MERGE rejects null or duplicate keys and updates a row only when the incoming version is newer.",
    "Every stage is audit-logged from landing to Gold. Runs end to end in Azure on synthetic data."
)
project(
    "Uber Eats Data Analytics Platform",
    "Azure Data Factory, ADLS Gen2, Azure Databricks, PySpark, FastAPI, Python",
    "Data from REST APIs, CSV files and SQL sources arrives in different formats and needs one reliable reporting layer.",
    "Three metadata-driven Data Factory pipelines load into ADLS Gen2. Databricks PySpark builds the Bronze and Silver layers, then publishes Gold with reconciliation checks.",
    "Checkpointed incremental loads and recovery runbooks. Deployed and run end to end in Azure on synthetic data."
)

story.append(PageBreak())
para("Isaiah Nyakundi", "PageHeaderCV")
para("Data Engineer | Cloud Data Platforms | Analytics Engineering", "ContactCV")
story.append(HRFlowable(width="100%", thickness=0.55, color=LIGHT, spaceBefore=1, spaceAfter=5))

section("Projects (continued)")
project(
    "NovaCart Incremental Retail Lakehouse",
    "Azure Databricks, Delta Lake, PySpark, Azure SQL, Databricks Jobs",
    "Retail order data changes constantly, and order history has to stay accurate.",
    "Bronze, Silver and Gold layers loaded incrementally, using timestamp and key watermarks in a control table. Delta MERGE and SCD Type 2 keep order history. A Databricks Job runs the layers in sequence.",
    "A repeatable workflow that can be rerun safely. Resources were shut down after the run to control cost."
)
project(
    "FlowBridge Snowflake Project",
    "Snowflake, Snowpipe, Streams and Tasks, ADLS Gen2, Streamlit",
    "Files landing in cloud storage must reach the warehouse automatically and be ready for dashboards.",
    "Event-driven ingestion from Azure into Snowflake with Bronze, Silver and Gold layers, a star schema (SCD Type 1) and a Streamlit dashboard.",
    "Latest version reran successfully in Snowflake on 8 November 2026. Synthetic data."
)
project(
    "CFPB Consumer Complaint Analytics",
    "Microsoft Fabric, PySpark, Fabric Warehouse, Power BI",
    "Shows how complaint volumes change over time, which products, issues and companies generate the most complaints, and how often companies respond on time.",
    "Bronze, Silver and Gold layers in Microsoft Fabric. Kaggle API and a Fabric pipeline load the CFPB CSV into a Bronze Lakehouse. PySpark profiles and cleans it into Silver. A stored procedure loads the Gold fact and dimension tables into a Fabric Warehouse. A semantic model feeds a three-page Power BI report.",
    "Run end to end in Fabric with a DEV-to-PROD deployment. Uses real CFPB complaint data.",
    "Records where the date sent precedes the date received are quarantined. Silver holds 896,931 records and quarantine holds 7,052, reconciling to the 903,983 source records."
)

section("Technical Skills")
for label, value in [
    ("Languages", "Python, SQL, PySpark, Flink SQL"),
    ("Cloud platforms", "Microsoft Azure (ADLS Gen2, Data Factory, Databricks, Key Vault, SQL Database), Microsoft Fabric, Snowflake"),
    ("Data engineering", "Apache Spark, Delta Lake, Apache Iceberg, Apache Kafka, Debezium (PostgreSQL CDC), Apache Flink, Apache Airflow, Trino, ETL/ELT, incremental and batch processing, medallion architecture"),
    ("Data modelling and analytics", "Star schema, SCD Types 1 and 2, dbt, Power BI, Apache Superset, Streamlit"),
    ("Quality, DevOps and testing", "Data quality checks, logging and auditing, Prometheus, Grafana, Docker, Docker Compose, GitHub Actions, Git, pytest"),
]:
    para("<b>" + escape(label) + ":</b> " + escape(value), "SmallCV")

section("Education")
para("<b>Bachelor of Science in Biostatistics</b>")
para("Jomo Kenyatta University of Agriculture and Technology (JKUAT)", "SmallCV")
para("Coursework in statistical reasoning, data handling and analysis of structured data.", "SmallCV")

section("Certifications")
para("Professional Data Engineer in Python, DataCamp (May 2026)")

def footer(canvas, doc):
    canvas.saveState()
    width, _ = A4
    canvas.setStrokeColor(LIGHT)
    canvas.setLineWidth(0.45)
    canvas.line(18 * mm, 13 * mm, width - 18 * mm, 13 * mm)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(18 * mm, 8.5 * mm, "ISAIAH NYAKUNDI | DATA ENGINEER")
    canvas.drawRightString(width - 18 * mm, 8.5 * mm, f"PAGE {doc.page}")
    canvas.restoreState()

OUT.parent.mkdir(parents=True, exist_ok=True)
pdf = SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    rightMargin=18 * mm,
    leftMargin=18 * mm,
    topMargin=14 * mm,
    bottomMargin=19 * mm,
    title="Isaiah Nyakundi - Data Engineer CV",
    author="Isaiah Nyakundi",
    subject="Curriculum Vitae",
)
pdf.build(story, onFirstPage=footer, onLaterPages=footer)

data = OUT.read_bytes()
if not data.startswith(b"%PDF-") or not data.rstrip().endswith(b"%%EOF"):
    raise RuntimeError("Generated CV PDF failed its file-signature check.")
print(f"Built {OUT} ({len(data)} bytes)")

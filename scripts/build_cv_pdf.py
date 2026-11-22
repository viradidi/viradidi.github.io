from pathlib import Path
from xml.sax.saxutils import escape
from bs4 import BeautifulSoup
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable, KeepTogether

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "cv.html"
OUT = ROOT / "resume" / "Isaiah-Nyakundi-Data-Engineer-Resume.pdf"
INK = HexColor("#222222")
MUTED = HexColor("#555555")
RULE = HexColor("#777777")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CVName", fontName="Helvetica-Bold", fontSize=20, leading=22, alignment=1, textColor=INK, spaceAfter=1))
styles.add(ParagraphStyle(name="CVRole", fontName="Helvetica-Bold", fontSize=9.5, leading=11, alignment=1, textColor=INK, spaceAfter=3))
styles.add(ParagraphStyle(name="CVContact", fontName="Helvetica", fontSize=8, leading=9.5, alignment=1, textColor=INK, spaceAfter=1))
styles.add(ParagraphStyle(name="CVSection", fontName="Helvetica-Bold", fontSize=10, leading=11.5, textColor=INK, spaceBefore=5, spaceAfter=3, keepWithNext=True))
styles.add(ParagraphStyle(name="CVBody", fontName="Helvetica", fontSize=8.7, leading=10.3, textColor=INK, spaceAfter=2.2))
styles.add(ParagraphStyle(name="CVSkill", fontName="Helvetica", fontSize=8.45, leading=9.8, textColor=INK, spaceAfter=1.4))
styles.add(ParagraphStyle(name="CVResumeBullet", fontName="Helvetica", fontSize=8.45, leading=9.8, textColor=INK, leftIndent=11, firstLineIndent=-7, spaceAfter=1.4))
styles.add(ParagraphStyle(name="CVProjectTitle", fontName="Helvetica-Bold", fontSize=9.1, leading=10.5, textColor=INK, spaceBefore=3, spaceAfter=0.5, keepWithNext=True))
styles.add(ParagraphStyle(name="CVStack", fontName="Helvetica-Oblique", fontSize=7.9, leading=9.1, textColor=MUTED, spaceAfter=1.1, keepWithNext=True))
styles.add(ParagraphStyle(name="CVMeta", fontName="Helvetica", fontSize=8.3, leading=9.4, textColor=MUTED, spaceAfter=1.5))
styles.add(ParagraphStyle(name="CVPageTwoName", fontName="Helvetica-Bold", fontSize=9.2, leading=10.5, textColor=INK, spaceAfter=1))

def text(node):
    return node.get_text(" ", strip=True) if node else ""

def section(story, label):
    story.append(Paragraph(escape(label.upper()), styles["CVSection"]))
    story.append(HRFlowable(width="100%", thickness=0.55, color=RULE, spaceBefore=0, spaceAfter=3))

def bullet(story, value):
    story.append(Paragraph("&#8226;&nbsp; " + escape(value), styles["CVResumeBullet"]))

def project(story, entry):
    title = text(entry.find("h3"))
    stack = text(entry.find("p", class_="cv-meta"))
    items = [Paragraph(escape(title), styles["CVProjectTitle"]), Paragraph(escape(stack), styles["CVStack"])]
    for li in entry.select("ul li"):
        items.append(Paragraph("&#8226;&nbsp; " + escape(text(li)), styles["CVResumeBullet"]))
    story.append(KeepTogether(items))

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(HexColor("#C8C8C8"))
    canvas.setLineWidth(0.4)
    canvas.line(14 * mm, 11 * mm, A4[0] - 14 * mm, 11 * mm)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(MUTED)
    canvas.drawCentredString(A4[0] / 2, 7 * mm, f"ISAIAH NYAKUNDI | DATA ENGINEER   |   PAGE {doc.page}")
    canvas.restoreState()

def main():
    soup = BeautifulSoup(HTML_PATH.read_text(encoding="utf-8"), "html.parser")
    header = soup.select_one(".cv-header")
    sections = {text(x.find("h2")): x for x in soup.select("main .cv-section")}
    required = ["SUMMARY", "TECHNICAL SKILLS", "PROFESSIONAL EXPERIENCE", "PROJECTS", "EDUCATION", "CERTIFICATIONS"]
    missing = [x for x in required if x not in sections]
    if not header or missing:
        raise ValueError(f"Missing CV structure: {missing or ['header']}")
    name = text(header.find("h1"))
    role = text(header.select_one(".cv-role"))
    contacts = [text(li) for li in header.select(".cv-contact li")]
    skill_items = sections["TECHNICAL SKILLS"].select("ul.cv-skills li")
    experience = sections["PROFESSIONAL EXPERIENCE"].select_one(".cv-entry")
    projects = sections["PROJECTS"].select(".cv-entry")
    if len(projects) != 6:
        raise ValueError(f"Expected six projects, found {len(projects)}")

    story = [Paragraph(escape(name), styles["CVName"]), Paragraph(escape(role), styles["CVRole"])]
    for value in contacts:
        story.append(Paragraph(escape(value), styles["CVContact"]))
    story.append(Spacer(1, 3))

    section(story, "SUMMARY")
    story.append(Paragraph(escape(text(sections["SUMMARY"].find("p"))), styles["CVBody"]))

    section(story, "TECHNICAL SKILLS")
    for li in skill_items:
        label = li.find("strong")
        label_text = text(label)
        value = text(li)[len(label_text):].lstrip(": ").strip()
        story.append(Paragraph("<b>" + escape(label_text) + "</b> " + escape(value), styles["CVSkill"]))

    section(story, "PROFESSIONAL EXPERIENCE")
    head = experience.select_one(".cv-entry-head")
    role_name = text(head.find("h3"))
    date = text(head.select_one(".cv-date"))
    story.append(Paragraph("<b>" + escape(role_name) + "</b> <font name='Helvetica-Bold'>" + escape(date) + "</font>", styles["CVBody"]))
    meta = [text(x) for x in experience.select(".cv-meta span")]
    story.append(Paragraph(escape(" | ".join(meta)), styles["CVMeta"]))
    for li in experience.select("ul li"):
        bullet(story, text(li))

    section(story, "PROJECTS")
    for entry in projects[:3]:
        project(story, entry)

    story.append(PageBreak())
    story.append(Paragraph("ISAIAH NYAKUNDI | DATA ENGINEER", styles["CVPageTwoName"]))
    story.append(Paragraph("Nairobi, Kenya | +254 719 367 955 | isaiahnyakundi87@gmail.com | github.com/viradidi", styles["CVMeta"]))
    section(story, "PROJECTS (CONTINUED)")
    for entry in projects[3:]:
        project(story, entry)

    section(story, "EDUCATION")
    education = sections["EDUCATION"].select_one(".cv-entry")
    story.append(Paragraph("<b>" + escape(text(education.find("h3"))) + "</b>", styles["CVBody"]))
    for p in education.find_all("p", recursive=False):
        story.append(Paragraph(escape(text(p)), styles["CVBody"]))

    section(story, "CERTIFICATIONS")
    certification = sections["CERTIFICATIONS"].select_one(".cv-entry")
    story.append(Paragraph(escape(text(certification)), styles["CVBody"]))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=14*mm, leftMargin=14*mm, topMargin=12*mm, bottomMargin=16*mm, title=f"{name} - Data Engineer Resume", author=name)
    pdf.build(story, onFirstPage=footer, onLaterPages=footer)
    data = OUT.read_bytes()
    if not data.startswith(b"%PDF-") or b"%%EOF" not in data[-32:]:
        raise RuntimeError("Generated PDF failed signature check")
    print(f"Generated {OUT} ({len(data)} bytes)")

if __name__ == "__main__":
    main()

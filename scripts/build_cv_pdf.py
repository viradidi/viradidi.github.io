from pathlib import Path
from xml.sax.saxutils import escape
from bs4 import BeautifulSoup
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable, KeepTogether, Flowable

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "cv.html"
OUT = ROOT / "resume" / "Isaiah-Nyakundi-Data-Engineer-Resume.pdf"
INK = HexColor("#222222")
MUTED = HexColor("#555555")
RULE = HexColor("#777777")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Name", fontName="Helvetica-Bold", fontSize=20, leading=22, alignment=1, textColor=INK, spaceAfter=1))
styles.add(ParagraphStyle(name="Role", fontName="Helvetica-Bold", fontSize=9.5, leading=11, alignment=1, textColor=INK, spaceAfter=3))
styles.add(ParagraphStyle(name="Contact", fontName="Helvetica", fontSize=8, leading=9.5, alignment=1, textColor=INK, spaceAfter=1))
styles.add(ParagraphStyle(name="Section", fontName="Helvetica-Bold", fontSize=10, leading=11.5, textColor=INK, spaceBefore=5, spaceAfter=3, keepWithNext=True))
styles.add(ParagraphStyle(name="Body", fontName="Helvetica", fontSize=8.7, leading=10.3, textColor=INK, spaceAfter=2.2))
styles.add(ParagraphStyle(name="Skill", fontName="Helvetica", fontSize=8.45, leading=9.8, textColor=INK, spaceAfter=1.4))
styles.add(ParagraphStyle(name="ResumeBullet", fontName="Helvetica", fontSize=8.45, leading=9.8, textColor=INK, leftIndent=11, firstLineIndent=-7, spaceAfter=1.4))
styles.add(ParagraphStyle(name="ProjectTitle", fontName="Helvetica-Bold", fontSize=9.1, leading=10.5, textColor=INK, spaceBefore=3, spaceAfter=0.5, keepWithNext=True))
styles.add(ParagraphStyle(name="Stack", fontName="Helvetica-Oblique", fontSize=7.9, leading=9.1, textColor=MUTED, spaceAfter=1.1, keepWithNext=True))
styles.add(ParagraphStyle(name="Meta", fontName="Helvetica", fontSize=8.3, leading=9.4, textColor=MUTED, spaceAfter=1.5))
styles.add(ParagraphStyle(name="PageTwoName", fontName="Helvetica-Bold", fontSize=9.2, leading=10.5, textColor=INK, spaceAfter=1))

class LeftRightLine(Flowable):
    """Selectable single-line content with left and right aligned text."""
    def __init__(self, left, right, font_name="Helvetica-Bold", font_size=8.8, color=INK, height=12):
        super().__init__()
        self.left, self.right = left, right
        self.font_name, self.font_size = font_name, font_size
        self.color, self.height = color, height

    def wrap(self, avail_width, avail_height):
        self.width = avail_width
        return avail_width, self.height

    def draw(self):
        self.canv.setFont(self.font_name, self.font_size)
        self.canv.setFillColor(self.color)
        self.canv.drawString(0, 1, self.left)
        self.canv.drawRightString(self.width, 1, self.right)

def txt(node):
    return node.get_text(" ", strip=True) if node else ""

def add_section(story, label):
    story.append(Paragraph(escape(label.upper()), styles["Section"]))
    story.append(HRFlowable(width="100%", thickness=0.55, color=RULE, spaceBefore=0, spaceAfter=3))

def add_bullet(story, text):
    story.append(Paragraph("&#8226;&nbsp; " + escape(text), styles["ResumeBullet"]))

def add_project(story, entry):
    title = txt(entry.find("h3"))
    stack = txt(entry.find("p", class_="cv-meta"))
    bullet_list = entry.find("ul")
    parts = [Paragraph(escape(title), styles["ProjectTitle"]), Paragraph(escape(stack), styles["Stack"])]
    for li in bullet_list.find_all("li", recursive=False):
        parts.append(Paragraph("&#8226;&nbsp; " + escape(txt(li)), styles["ResumeBullet"]))
    story.append(KeepTogether(parts))

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
    sections = {txt(x.find("h2")): x for x in soup.select("main .cv-section")}
    required = ["SUMMARY", "TECHNICAL SKILLS", "PROFESSIONAL EXPERIENCE", "PROJECTS", "EDUCATION", "CERTIFICATIONS"]
    missing = [x for x in required if x not in sections]
    if not header or missing:
        raise ValueError(f"Missing CV structure: {missing or ['header']}")
    name = txt(header.find("h1"))
    role = txt(header.select_one(".cv-role"))
    contacts = [txt(li) for li in header.select(".cv-contact li")]
    skills = sections["TECHNICAL SKILLS"].select("ul.cv-skills li")
    experience = sections["PROFESSIONAL EXPERIENCE"].select_one(".cv-entry")
    projects = sections["PROJECTS"].select(".cv-entry")
    if len(projects) != 6:
        raise ValueError(f"Expected 6 project entries, found {len(projects)}")
    story = []
    story.append(Paragraph(escape(name), styles["Name"]))
    story.append(Paragraph(escape(role), styles["Role"]))
    for contact in contacts:
        story.append(Paragraph(escape(contact), styles["Contact"]))
    story.append(Spacer(1, 3))

    add_section(story, "SUMMARY")
    story.append(Paragraph(escape(txt(sections["SUMMARY"].find("p"))), styles["Body"]))

    add_section(story, "TECHNICAL SKILLS")
    for li in skills:
        label = li.find("strong")
        label_text = txt(label)
        whole = txt(li)
        value = whole[len(label_text):].lstrip(": ").strip()
        story.append(Paragraph("<b>" + escape(label_text) + "</b> " + escape(value), styles["Skill"]))

    add_section(story, "PROFESSIONAL EXPERIENCE")
    head = experience.select_one(".cv-entry-head")
    role_name = txt(head.find("h3"))
    date = txt(head.select_one(".cv-date"))
    story.append(LeftRightLine(role_name, date, font_name="Helvetica-Bold", font_size=9.1, height=12))
    metas = experience.select_one(".cv-meta")
    meta_spans = [txt(x) for x in metas.find_all("span")]
    story.append(LeftRightLine(meta_spans[0] if meta_spans else "", meta_spans[1] if len(meta_spans) > 1 else "", font_name="Helvetica", font_size=8.3, color=MUTED, height=11))
    for li in experience.select("ul li"):
        add_bullet(story, txt(li))

    add_section(story, "PROJECTS")
    for entry in projects[:3]:
        add_project(story, entry)

    story.append(PageBreak())
    story.append(Paragraph("ISAIAH NYAKUNDI | DATA ENGINEER", styles["PageTwoName"]))
    story.append(Paragraph(escape("Nairobi, Kenya | +254 719 367 955 | isaiahnyakundi87@gmail.com | github.com/viradidi"), styles["Meta"]))
    add_section(story, "PROJECTS (CONTINUED)")
    for entry in projects[3:]:
        add_project(story, entry)

    add_section(story, "EDUCATION")
    education = sections["EDUCATION"].select_one(".cv-entry")
    story.append(Paragraph("<b>" + escape(txt(education.find("h3"))) + "</b>", styles["Body"]))
    for para in education.find_all("p", recursive=False):
        story.append(Paragraph(escape(txt(para)), styles["Body"]))

    add_section(story, "CERTIFICATIONS")
    certification = sections["CERTIFICATIONS"].select_one(".cv-entry")
    story.append(Paragraph(escape(txt(certification)), styles["Body"]))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=14*mm, leftMargin=14*mm, topMargin=12*mm, bottomMargin=16*mm, title=f"{name} - Data Engineer Resume", author=name)
    pdf.build(story, onFirstPage=footer, onLaterPages=footer)
    data = OUT.read_bytes()
    if not data.startswith(b"%PDF-") or b"%%EOF" not in data[-32:]:
        raise RuntimeError("Generated PDF failed signature check")
    print(f"Generated {OUT} ({len(data)} bytes)")

if __name__ == "__main__":
    main()

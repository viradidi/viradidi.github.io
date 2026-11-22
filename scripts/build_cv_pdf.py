from pathlib import Path
from xml.sax.saxutils import escape

from bs4 import BeautifulSoup, NavigableString, Tag
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable, KeepTogether
)

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "cv.html"
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


def inline_markup(node):
    """Preserve plain text and links when turning the CV header into a PDF."""
    parts = []
    for child in node.children:
        if isinstance(child, NavigableString):
            parts.append(escape(str(child)))
        elif isinstance(child, Tag):
            content = inline_markup(child)
            if child.name == "a" and child.get("href"):
                href = escape(child["href"], {'"': "&quot;", "'": "&apos;"})
                parts.append(f'<link href="{href}" color="#1C657A">{content}</link>')
            else:
                parts.append(content)
    return "".join(parts)


def text_of(node):
    return node.get_text(" ", strip=True) if node else ""


def detail_paragraphs(entry):
    details = []
    for paragraph in entry.find_all("p", recursive=False):
        if "cv-meta" in paragraph.get("class", []):
            continue
        label = paragraph.find("strong", recursive=False)
        if not label:
            details.append(("", text_of(paragraph)))
            continue
        label_text = text_of(label)
        label_name = label_text.rstrip(":")
        value = text_of(paragraph)[len(label_text):].lstrip(": ")
        details.append((label_name, value))
    return details


def add_para(story, content, style="BodyCV"):
    story.append(Paragraph(content, styles[style]))


def add_section(story, title):
    add_para(story, escape(title.upper()), "SectionCV")
    story.append(HRFlowable(width="100%", thickness=0.55, color=LIGHT, spaceBefore=0, spaceAfter=4))


def add_bullet(story, content):
    add_para(story, "&#8226;&nbsp; " + escape(content), "BulletCV")


def add_project(story, entry):
    heading = text_of(entry.find("h3"))
    stack = text_of(entry.find("p", class_="cv-meta"))
    detail = detail_paragraphs(entry)
    block = [
        Paragraph(escape(heading), styles["ProjectTitleCV"]),
        Paragraph("<b>Stack:</b> " + escape(stack), styles["StackCV"]),
    ]
    for label, value in detail:
        if label:
            block.append(Paragraph("<b>" + escape(label) + ":</b> " + escape(value), styles["SmallCV"]))
        else:
            block.append(Paragraph(escape(value), styles["SmallCV"]))
    story.append(KeepTogether(block))


def main():
    if not HTML_PATH.is_file():
        raise FileNotFoundError(f"CV HTML source not found: {HTML_PATH}")
    soup = BeautifulSoup(HTML_PATH.read_text(encoding="utf-8"), "html.parser")
    header = soup.select_one(".cv-header")
    sections = {text_of(section.find("h2")): section for section in soup.select("main .cv-section")}
    required = ["Professional Summary", "Experience", "Projects", "Technical Skills", "Education", "Certifications"]
    missing = [name for name in required if name not in sections]
    if not header or missing:
        raise ValueError(f"CV source is missing required structure: {', '.join(missing) if missing else 'header'}")

    name = text_of(header.find("h1"))
    role = text_of(header.select_one(".cv-role"))
    contact_items = [inline_markup(item) for item in header.select(".cv-contact li")]
    if len(contact_items) < 6:
        raise ValueError("CV contact section must include location, phone, email, LinkedIn, GitHub and portfolio")

    story = []
    add_para(story, escape(name), "NameCV")
    add_para(story, escape(role), "RoleCV")
    add_para(story, " &nbsp;|&nbsp; ".join(contact_items[:3]), "ContactCV")
    add_para(story, " &nbsp;|&nbsp; ".join(contact_items[3:]), "ContactCV")
    story.append(Spacer(1, 3))

    add_section(story, "Professional Summary")
    add_para(story, escape(text_of(sections["Professional Summary"].find("p"))))

    add_section(story, "Experience")
    for entry in sections["Experience"].select(".cv-entry"):
        add_para(story, "<b>" + escape(text_of(entry.find("h3"))) + "</b>")
        add_para(story, escape(text_of(entry.find("p", class_="cv-meta"))), "SmallCV")
        for item in entry.select("ul li"):
            add_bullet(story, text_of(item))

    project_entries = sections["Projects"].select(".cv-entry")
    if len(project_entries) != 6:
        raise ValueError(f"Expected six project entries, found {len(project_entries)}")
    add_section(story, "Projects")
    for entry in project_entries[:3]:
        add_project(story, entry)

    story.append(PageBreak())
    add_para(story, escape(name), "PageHeaderCV")
    add_para(story, escape(role), "ContactCV")
    story.append(HRFlowable(width="100%", thickness=0.55, color=LIGHT, spaceBefore=1, spaceAfter=5))
    add_section(story, "Projects (continued)")
    for entry in project_entries[3:]:
        add_project(story, entry)

    add_section(story, "Technical Skills")
    for item in sections["Technical Skills"].select("ul.cv-skills li"):
        strong = item.find("strong", recursive=False)
        label_text = text_of(strong)
        label = label_text.rstrip(":")
        full_text = text_of(item)
        value = full_text[len(label_text):].lstrip(": ") if strong else full_text
        add_para(story, "<b>" + escape(label) + ":</b> " + escape(value), "SmallCV")

    add_section(story, "Education")
    for entry in sections["Education"].select(".cv-entry"):
        add_para(story, "<b>" + escape(text_of(entry.find("h3"))) + "</b>")
        for paragraph in entry.find_all("p", recursive=False):
            add_para(story, escape(text_of(paragraph)), "SmallCV")

    add_section(story, "Certifications")
    for entry in sections["Certifications"].select(".cv-entry"):
        for paragraph in entry.find_all("p", recursive=False):
            add_para(story, escape(text_of(paragraph)))

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
        title=f"{name} - Data Engineer CV",
        author=name,
        subject="Curriculum Vitae",
    )
    pdf.build(story, onFirstPage=footer, onLaterPages=footer)

    data = OUT.read_bytes()
    if not data.startswith(b"%PDF-") or not data.rstrip().endswith(b"%%EOF"):
        raise RuntimeError("Generated CV PDF failed its file-signature check.")
    print(f"Built {OUT} ({len(data)} bytes) from {HTML_PATH}")


if __name__ == "__main__":
    main()

from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "cv.html"
OUT = ROOT / "resume" / "Isaiah_Nyakundi_Data_Engineer_Resume.docx"
INK = RGBColor(35, 35, 35)
MUTED = RGBColor(80, 80, 80)

def text(node):
    return node.get_text(" ", strip=True) if node else ""

def add_run(p, value, bold=False, italic=False, size=8.7, color=INK):
    r = p.add_run(value)
    r.bold = bold
    r.italic = italic
    r.font.name = "Arial"
    r._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), "Arial")
    r.font.size = Pt(size)
    r.font.color.rgb = color
    return r

def keep(p, next_=False):
    pPr = p._p.get_or_add_pPr()
    pPr.append(OxmlElement("w:keepLines"))
    if next_:
        pPr.append(OxmlElement("w:keepNext"))

def border(p):
    pPr = p._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "5")
    bottom.set(qn("w:space"), "3")
    bottom.set(qn("w:color"), "777777")
    borders.append(bottom)
    pPr.append(borders)

def section(doc, label):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    add_run(p, label, bold=True, size=10.2)
    border(p)
    keep(p, True)

def bullet(doc, value):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.left_indent = Inches(0.18)
    p.paragraph_format.first_line_indent = Inches(-0.12)
    p.paragraph_format.space_after = Pt(1.45)
    p.paragraph_format.line_spacing = 1.02
    p.paragraph_format.keep_together = True
    add_run(p, value, size=8.55)
    keep(p)

def project(doc, entry):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(0.5)
    p.paragraph_format.keep_with_next = True
    add_run(p, text(entry.find("h3")), bold=True, size=9.15)
    keep(p, True)
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(1.25)
    p.paragraph_format.keep_with_next = True
    add_run(p, text(entry.find("p", class_="cv-meta")), italic=True, size=8.0, color=MUTED)
    keep(p, True)
    for li in entry.select("ul li"):
        bullet(doc, text(li))

def add_footer(doc):
    for sec in doc.sections:
        p = sec.footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        add_run(p, "ISAIAH NYAKUNDI | DATA ENGINEER   |   PAGE ", size=7.2, color=MUTED)
        field = OxmlElement("w:fldSimple")
        field.set(qn("w:instr"), "PAGE")
        p._p.append(field)

def main():
    soup = BeautifulSoup(HTML_PATH.read_text(encoding="utf-8"), "html.parser")
    header = soup.select_one(".cv-header")
    sections = {text(x.find("h2")): x for x in soup.select("main .cv-section")}
    required = ["SUMMARY", "TECHNICAL SKILLS", "PROFESSIONAL EXPERIENCE", "PROJECTS", "EDUCATION", "CERTIFICATIONS"]
    missing = [x for x in required if x not in sections]
    projects = sections.get("PROJECTS").select(".cv-entry") if "PROJECTS" in sections else []
    if not header or missing or len(projects) != 6:
        raise ValueError(f"Invalid CV content. Missing sections: {missing}; project count: {len(projects)}")

    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.27), Inches(11.69)
    sec.top_margin = Inches(0.48)
    sec.bottom_margin = Inches(0.48)
    sec.left_margin = Inches(0.55)
    sec.right_margin = Inches(0.55)
    sec.header_distance, sec.footer_distance = Inches(0.2), Inches(0.22)
    normal = doc.styles["Normal"]
    normal.font.name = "Arial"
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
    normal.font.size = Pt(8.8)
    normal.font.color.rgb = INK
    normal.paragraph_format.space_after = Pt(2.1)
    normal.paragraph_format.line_spacing = 1.04
    list_style = doc.styles["List Bullet"]
    list_style.font.name = "Arial"
    list_style._element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
    list_style.font.size = Pt(8.55)

    name = text(header.find("h1"))
    role = text(header.select_one(".cv-role"))
    contacts = [text(x) for x in header.select(".cv-contact li")]
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(1)
    add_run(p, name, bold=True, size=20)
    keep(p, True)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(3)
    add_run(p, role, bold=True, size=9.6)
    keep(p, True)
    for contact in contacts:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0.5)
        add_run(p, contact, size=8.0)
        keep(p, True)

    section(doc, "SUMMARY")
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2.6)
    p.paragraph_format.line_spacing = 1.06
    add_run(p, text(sections["SUMMARY"].find("p")), size=8.85)
    keep(p)

    section(doc, "TECHNICAL SKILLS")
    for li in sections["TECHNICAL SKILLS"].select("ul.cv-skills li"):
        strong = li.find("strong")
        label = text(strong)
        value = text(li)[len(label):].lstrip(": ").strip()
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(1.6)
        p.paragraph_format.line_spacing = 1.0
        add_run(p, label + " ", bold=True, size=8.45)
        add_run(p, value, size=8.45)
        keep(p)

    section(doc, "PROFESSIONAL EXPERIENCE")
    exp = sections["PROFESSIONAL EXPERIENCE"].select_one(".cv-entry")
    head = exp.select_one(".cv-entry-head")
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0.5)
    p.paragraph_format.tab_stops.add_tab_stop(Inches(7.15), WD_TAB_ALIGNMENT.RIGHT)
    add_run(p, text(head.find("h3")), bold=True, size=9.45)
    add_run(p, chr(9) + text(head.select_one(".cv-date")), bold=True, size=8.8)
    keep(p, True)
    meta = [text(x) for x in exp.select(".cv-meta span")]
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(1.4)
    p.paragraph_format.tab_stops.add_tab_stop(Inches(7.15), WD_TAB_ALIGNMENT.RIGHT)
    add_run(p, meta[0] if meta else "", size=8.8)
    if len(meta) > 1:
        add_run(p, chr(9) + meta[1], size=8.5, color=MUTED)
    keep(p, True)
    for li in exp.select("ul li"):
        bullet(doc, text(li))

    section(doc, "PROJECTS")
    for entry in projects[:3]:
        project(doc, entry)

    doc.add_page_break()
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0.5)
    add_run(p, "ISAIAH NYAKUNDI | DATA ENGINEER", bold=True, size=9.2)
    keep(p, True)
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(3.2)
    add_run(p, "Nairobi, Kenya | +254 719 367 955 | isaiahnyakundi87@gmail.com | github.com/viradidi", size=8.0)
    keep(p, True)

    section(doc, "PROJECTS (CONTINUED)")
    for entry in projects[3:]:
        project(doc, entry)

    section(doc, "EDUCATION")
    education = sections["EDUCATION"].select_one(".cv-entry")
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0.8)
    add_run(p, text(education.find("h3")), bold=True, size=9.1)
    keep(p, True)
    for para in education.find_all("p", recursive=False):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(1.2)
        add_run(p, text(para), size=8.6)
        keep(p)

    section(doc, "CERTIFICATIONS")
    for entry in sections["CERTIFICATIONS"].select(".cv-entry"):
        p = doc.add_paragraph()
        for para in entry.find_all("p", recursive=False):
            add_run(p, text(para), size=8.7)

    add_footer(doc)
    doc.core_properties.title = f"{name} - Data Engineer Resume"
    doc.core_properties.subject = "Data Engineering | Cloud Data Platforms | Analytics Engineering"
    doc.core_properties.author = "Isaiah Nyakundi"
    doc.core_properties.keywords = "Data Engineer, Azure, Databricks, Snowflake, Microsoft Fabric, PySpark, Kafka"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print(f"Generated {OUT}")

if __name__ == "__main__":
    main()

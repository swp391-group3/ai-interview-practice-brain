from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_ALIGN_VERTICAL, WD_CELL_VERTICAL_ALIGNMENT, WD_ROW_HEIGHT_RULE, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path("/home/dorriss/Documents/SEP490")
REFERENCE = ROOT / "08_Reports/Report-1-3/Report1_Project_Introduction_v0.1.docx"
OUTPUT = ROOT / "08_Reports/Report-1-3/Report1_Project_Introduction_v0.2.docx"

FONT = "Times New Roman"
BLACK = "000000"
RED = "C00000"
HEADER_FILL = "FCE4D6"
BORDER = "A6A6A6"


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=80, start=100, bottom=80, end=100):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for m, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{m}"))
        if node is None:
            node = OxmlElement(f"w:{m}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_table_borders(table, color=BORDER, size="6"):
    tbl_pr = table._tbl.tblPr
    borders = tbl_pr.find(qn("w:tblBorders"))
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        tbl_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = borders.find(qn(f"w:{edge}"))
        if tag is None:
            tag = OxmlElement(f"w:{edge}")
            borders.append(tag)
        tag.set(qn("w:val"), "single")
        tag.set(qn("w:sz"), size)
        tag.set(qn("w:space"), "0")
        tag.set(qn("w:color"), color)


def cant_split(row):
    tr_pr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:cantSplit")
    tr_pr.append(el)


def repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def format_run(run, size=11, bold=False, italic=False, color=BLACK):
    run.font.name = FONT
    run._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor.from_string(color)


def format_paragraph(p, justify=True, before=0, after=4, line=1.12, keep=False):
    if justify:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = line
    pf.keep_together = False
    pf.keep_with_next = keep


def add_body(doc, text="", bold_lead=None, italic=False, after=5, keep=False):
    p = doc.add_paragraph()
    format_paragraph(p, after=after, keep=keep)
    if bold_lead and text.startswith(bold_lead):
        r1 = p.add_run(bold_lead)
        format_run(r1, bold=True)
        r2 = p.add_run(text[len(bold_lead):])
        format_run(r2, italic=italic)
    else:
        r = p.add_run(text)
        format_run(r, italic=italic)
    return p


def add_label(doc, text):
    p = doc.add_paragraph()
    format_paragraph(p, justify=False, before=5, after=2, line=1.0, keep=True)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.left_indent = Inches(0)
    p.paragraph_format.right_indent = Inches(0)
    r = p.add_run(text)
    format_run(r, size=11, bold=True)
    return p


def add_feature_heading(doc, text):
    p = doc.add_paragraph()
    format_paragraph(p, justify=False, before=6, after=2, line=1.0, keep=True)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.left_indent = Inches(0)
    p.paragraph_format.right_indent = Inches(0)
    r = p.add_run(text)
    format_run(r, size=11, bold=True)
    return p


def add_bullet(doc, text, level=0, bold_lead=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = p.paragraph_format
    pf.left_indent = Inches(0.28 + 0.25 * level)
    pf.first_line_indent = Inches(-0.18)
    pf.space_after = Pt(3)
    pf.line_spacing = 1.08
    marker = "• " if level == 0 else "- "
    r = p.add_run(marker)
    format_run(r, size=10.7)
    if bold_lead and text.startswith(bold_lead):
        r = p.add_run(bold_lead)
        format_run(r, size=10.7, bold=True)
        r = p.add_run(text[len(bold_lead):])
        format_run(r, size=10.7)
    else:
        r = p.add_run(text)
        format_run(r, size=10.7)
    return p


def add_heading(doc, text, level, page_break_before=False):
    p = doc.add_paragraph(style=f"Heading {level}")
    if page_break_before:
        p.paragraph_format.page_break_before = True
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(8 if level == 1 else 6)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(text)
    format_run(r, size={1: 16, 2: 13, 3: 12}.get(level, 11), bold=True, color=RED if level == 1 else BLACK)
    return p


def add_hyperlink(paragraph, text, url):
    part = paragraph.part
    rel_id = part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), rel_id)
    new_run = OxmlElement("w:r")
    r_pr = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "0563C1")
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    r_pr.extend([color, underline])
    new_run.append(r_pr)
    text_el = OxmlElement("w:t")
    text_el.text = text
    new_run.append(text_el)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)
    return hyperlink


def add_source_line(doc, label, links):
    p = doc.add_paragraph()
    format_paragraph(p, after=6)
    r = p.add_run(label)
    format_run(r, size=10, bold=True)
    for i, (text, url) in enumerate(links):
        if i:
            r = p.add_run("; ")
            format_run(r, size=10)
        add_hyperlink(p, text, url)
    return p


def add_page_number(section):
    section.different_first_page_header_footer = True
    footer = section.footer
    p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run()
    format_run(run, size=10)
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = "2"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.extend([begin, instr, separate, text, end])


TOC_ENTRIES = [
    (1, "I. Record of Changes", "3"),
    (1, "II. Project Introduction", "4"),
    (2, "1. Overview", "4"),
    (3, "1.1 Project Information", "4"),
    (3, "1.2 Project Team", "4"),
    (2, "2. Product Background", "4"),
    (2, "3. Existing Systems", "5"),
    (3, "3.1 Final Round AI", "5"),
    (3, "3.2 interviewing.io", "6"),
    (2, "4. Business Opportunity", "7"),
    (2, "5. Software Product Vision", "8"),
    (2, "6. Project Scope and Limitations", "8"),
    (3, "6.1 Major Features", "9"),
    (3, "6.2 Limitations and Exclusions", "10"),
]


def add_toc(doc):
    title = doc.add_paragraph(style="TOC Heading")
    title.paragraph_format.space_after = Pt(8)
    r = title.add_run("Table of Contents")
    format_run(r, size=16, bold=True, color="2E74B5")
    for level, text, page in TOC_ENTRIES:
        style_name = f"toc {level}"
        p = doc.add_paragraph(style=style_name if style_name in [s.name for s in doc.styles] else "Normal")
        p.paragraph_format.left_indent = Inches(0.22 * (level - 1))
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.tab_stops.add_tab_stop(Inches(6.15), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        r = p.add_run(text)
        format_run(r, size=11)
        r = p.add_run("\t" + page)
        format_run(r, size=11)
        p._p.set(qn("w:rsidR"), "00A00001")


def add_record_table(doc):
    table = doc.add_table(rows=14, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    widths = [0.80, 0.72, 1.45, 3.25]
    for row in table.rows:
        cant_split(row)
        row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
        for i, cell in enumerate(row.cells):
            cell.width = Inches(widths[i])
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            set_cell_margins(cell)
    headers = ["Date", "A* / M, D", "In charge", "Change Description"]
    for i, text in enumerate(headers):
        cell = table.cell(0, i)
        set_cell_shading(cell, HEADER_FILL)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(text)
        format_run(r, size=9.5, bold=True)
    repeat_table_header(table.rows[0])
    records = [
        ["07/09/2026", "A", "Nguyễn Huỳnh Nhật Anh and project team", "Initial v0.1 draft prepared from the Capstone Project Register and SEP490 report template."],
        ["17/09/2026", "M", "Nguyễn Huỳnh Nhật Anh and project team", "Expanded the project background, researched existing systems, clarified the business opportunity and product vision, detailed the feature scope, and replaced unresolved non-personal placeholders with verified information."],
    ]
    for ridx, record in enumerate(records, 1):
        for cidx, text in enumerate(record):
            p = table.cell(ridx, cidx).paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if cidx < 3 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(text)
            format_run(r, size=9.2)
    for row in table.rows[3:]:
        row.height = Inches(0.27)
    set_table_borders(table)
    return table


def add_team_table(doc):
    table = doc.add_table(rows=7, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    widths = [1.95, 1.30, 2.05, 1.00]
    for row in table.rows:
        cant_split(row)
        for i, cell in enumerate(row.cells):
            cell.width = Inches(widths[i])
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            set_cell_margins(cell, top=70, start=85, bottom=70, end=85)
    headers = ["Full Name", "Role", "Email", "Mobile"]
    for i, text in enumerate(headers):
        cell = table.cell(0, i)
        set_cell_shading(cell, HEADER_FILL)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(text)
        format_run(r, size=9.5, bold=True)
    repeat_table_header(table.rows[0])
    rows = [
        ["Nguyễn Thế Hoàng", "Supervisor", "hoangnt20@fe.edu.vn", "0986 628 525"],
        ["Tô Chí Bảo\nSE190084", "Full Stack", "", ""],
        ["Huỳnh Minh Khang\nSE192197", "Full Stack", "", ""],
        ["Nguyễn Huỳnh Nhật Anh\nSE190291", "Team Leader / Full Stack", "", ""],
        ["Nguyễn Tấn Trọng\nSE190353", "Full Stack", "", ""],
        ["Đặng Phương Nam\nSE192107", "Full Stack", "", ""],
    ]
    for ridx, record in enumerate(rows, 1):
        for cidx, text in enumerate(record):
            cell = table.cell(ridx, cidx)
            cell.text = ""
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if cidx in (1, 3) else WD_ALIGN_PARAGRAPH.LEFT
            pieces = text.split("\n") if text else [""]
            for j, piece in enumerate(pieces):
                if j:
                    p.add_run().add_break()
                r = p.add_run(piece)
                format_run(r, size=9.3, italic=(j == 1))
    set_table_borders(table)
    return table


def add_competitor_finalround(doc):
    add_body(doc, "Final Round AI is an interview-preparation platform that organizes practice around a specific job goal. Its official documentation describes a goal as a target role and company together with the job description, resume, and other supporting materials. Candidates can launch an AI-led practice interview, answer questions aloud, and review an automatically generated debrief after the session.")
    add_body(doc, "System Actors: Job candidates preparing for a target role. The broader product also supports live Interview Copilot sessions, but this report evaluates its practice-interview capability because RoleCue is a preparation product.", bold_lead="System Actors:")
    add_label(doc, "Key Features")
    features = [
        ("Job-specific context: ", "Uses a goal containing the target role, company, job description, resume, and uploaded materials to tailor the practice session."),
        ("Multiple interview scenarios: ", "Provides General, Coding, System Design, Behavioral, Product Case, Data and Machine Learning, Salary Negotiation, and Recruiter Screen scenarios."),
        ("Spoken interview practice: ", "Candidates answer aloud in a live back-and-forth conversation with an AI interviewer."),
        ("Contextual follow-up questions: ", "The chosen scenario guides the opening direction, while follow-up questions can respond to what the candidate says."),
        ("Automatic debrief: ", "Each completed practice produces a debrief that summarizes performance, identifies weak moments, and creates areas for repeated practice."),
        ("Video interviewer window: ", "The practice interface presents an interviewer video, a private candidate self-view, microphone status, captions, and recovery behavior for a temporary connection interruption."),
    ]
    for lead, text in features:
        add_bullet(doc, lead + text, bold_lead=lead)
    add_label(doc, "Pros")
    for lead, text in [
        ("Strong personalization: ", "The session can use the candidate's target role, company, job description, resume, and prior preparation context."),
        ("Broad scenario coverage: ", "Technical and non-technical formats are available within one workflow."),
        ("Voice-based rehearsal: ", "Candidates practise speaking rather than only reading or typing answers."),
        ("Continuous improvement loop: ", "The debrief links one practice session to the next by identifying areas for re-drilling."),
    ]:
        add_bullet(doc, lead + text, bold_lead=lead)
    add_label(doc, "Cons and gaps relative to RoleCue")
    for lead, text in [
        ("Preparation and live-assistance scopes are combined: ", "The wider product includes real-time assistance for live interviews. RoleCue intentionally limits itself to simulated practice and post-session learning."),
        ("No documented candidate-reviewed JD requirement model: ", "The reviewed official pages describe using a job description as goal context, but they do not describe a structured list of extracted technical requirements that the candidate approves before an interview blueprint is generated."),
        ("No documented reusable assessment blueprint: ", "The public workflow explains goals, scenarios, sessions, and debriefs, but does not document RoleCue's planned separation between reviewed JD, assessment blueprint, runtime questions, and reproducible evaluation snapshot."),
        ("Limited platform-governance visibility: ", "The public candidate documentation does not describe an administrator console for technical taxonomy, evaluation policies, avatar and voice catalogues, or aggregate weakness analytics."),
    ]:
        add_bullet(doc, lead + text, bold_lead=lead)
    add_source_line(doc, "Official sources accessed 17 September 2026: ", [
        ("Final Round AI Practice Interview", "https://www.finalroundai.com/ai-mock-interview"),
        ("Starting a practice interview", "https://docs.finalroundai.com/docs/mock-interviews/starting-a-mock"),
        ("Goals, Sessions and the Library", "https://docs.finalroundai.com/docs/core-concepts/goals-sessions-library"),
    ])


def add_competitor_interviewing(doc):
    add_body(doc, "interviewing.io is a technical interview-practice platform for software engineers. Its public product page combines anonymous mock interviews with experienced engineers and an AI Interviewer for coding and system-design practice. The service focuses on interview formats used by major technology companies and provides feedback after practice sessions.")
    add_body(doc, "System Actors: Software-engineering candidates, experienced engineer interviewers, mentors, and the AI Interviewer.", bold_lead="System Actors:")
    add_label(doc, "Key Features")
    for lead, text in [
        ("Anonymous human mock interviews: ", "Candidates can practise with engineers from major technology companies without exposing identifying information during the interview."),
        ("AI technical interviewer: ", "The AI Interviewer conducts coding and system-design interviews in a style modelled on major technology-company interviews."),
        ("Detailed feedback: ", "The platform provides post-session feedback intended to be specific and actionable."),
        ("Technical practice library: ", "Candidates can work through more than 200 coding and technical interview problems made available through the platform."),
        ("Interview-type coverage: ", "The service covers coding, system design, machine learning, and behavioural preparation."),
        ("Mentor programmes: ", "Candidates may purchase a sequence of one-to-one sessions with a mentor for repeated practice."),
    ]:
        add_bullet(doc, lead + text, bold_lead=lead)
    add_label(doc, "Pros")
    for lead, text in [
        ("Technical depth: ", "Coding and system-design formats are central rather than secondary additions to a general interview tool."),
        ("Human and AI practice options: ", "Candidates can choose scalable AI practice or direct feedback from experienced engineers."),
        ("Realistic technical formats: ", "The platform supports the problem-solving and system-design styles commonly used in software-engineering interviews."),
        ("Actionable feedback: ", "Post-session feedback gives candidates a basis for targeted improvement."),
    ]:
        add_bullet(doc, lead + text, bold_lead=lead)
    add_label(doc, "Cons and gaps relative to RoleCue")
    for lead, text in [
        ("Limited JD-specific workflow in public documentation: ", "The public product page emphasizes interview category and company-style technical practice rather than candidate review of technical requirements extracted from an uploaded JD."),
        ("Human-practice availability and cost: ", "Sessions with engineers or mentors depend on scheduling and paid service packages, so they do not provide the same unlimited self-service model as an automated simulator."),
        ("No documented 3D avatar and voice catalogue: ", "The public product description does not identify a configurable 3D virtual interviewer with synchronized lip movement or an administrator-managed avatar and voice catalogue."),
        ("Different governance model: ", "Its public candidate-facing materials do not describe RoleCue's planned administrator controls for interview policy, evaluation criteria, domain taxonomy, subscriptions, or aggregate performance analytics."),
    ]:
        add_bullet(doc, lead + text, bold_lead=lead)
    add_source_line(doc, "Official source accessed 17 September 2026: ", [
        ("interviewing.io product page", "https://interviewing.io/"),
    ])


def build():
    doc = Document(REFERENCE)
    body = doc._element.body

    # Retain the cover through its date line, then remove the previous TOC and body.
    date_p = None
    for p in doc.paragraphs:
        if "Ho Chi Minh City, September 2026" in p.text:
            date_p = p._p
            break
    if date_p is None:
        raise RuntimeError("Could not locate the cover date paragraph")
    passed_date = False
    for child in list(body):
        if child is date_p:
            passed_date = True
            continue
        if passed_date and child.tag != qn("w:sectPr"):
            body.remove(child)

    # Update cover and use an existing blank cover paragraph for the version line.
    for idx, p in enumerate(doc.paragraphs):
        if "Report 1" in p.text and "Project Introduction" in p.text:
            p.text = "Report 1 - Project Introduction"
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                format_run(r, size=22, bold=True, color="C00000")
            for candidate in doc.paragraphs[idx + 1:]:
                if not candidate.text.strip():
                    candidate.text = "Version 0.2"
                    candidate.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    for r in candidate.runs:
                        format_run(r, size=14, bold=True)
                    break
            break

    # Front matter.
    doc.add_page_break()
    add_toc(doc)
    doc.add_page_break()
    add_heading(doc, "I. Record of Changes", 1)
    add_record_table(doc)
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    r = p.add_run("* A - Added   M - Modified   D - Deleted")
    format_run(r, size=9, italic=True)

    # Main report.
    add_heading(doc, "II. Project Introduction", 1, page_break_before=True)
    add_heading(doc, "1. Overview", 2)
    add_heading(doc, "1.1 Project Information", 3)
    info = [
        ("Project name: ", "Design and Development of an AI-Powered Virtual Technical Interview Simulation Platform with a 3D Virtual Interviewer"),
        ("Product name: ", "RoleCue"),
        ("Project code: ", "09_GFA26SE84"),
        ("Group name: ", "Group 09"),
        ("Software type: ", "Web-based full-stack application"),
        ("Source code repository: ", "https://github.com/swp391-group3/ai-interview-practice"),
        ("Production URL: ", "Not yet published at version 0.2"),
    ]
    for lead, value in info:
        add_bullet(doc, lead + value, bold_lead=lead)
    add_heading(doc, "1.2 Project Team", 3)
    add_team_table(doc)
    add_body(doc, "Student email addresses and mobile numbers are intentionally left blank for the project team to complete.", italic=True, after=7)

    add_heading(doc, "2. Product Background", 2)
    background = [
        "Technical interviews are a major entry point into software internships and employment. Candidates must demonstrate knowledge, explain trade-offs, solve unfamiliar problems, and communicate clearly under time pressure. Preparation is therefore different from memorizing isolated answers: candidates need repeated opportunities to practise complete responses and receive feedback that is tied to the role they want.",
        "The Capstone Project Register identifies four practical limitations in common preparation methods. Generic question banks do not reflect a specific Job Description (JD). Access to experienced interviewers is limited, especially when candidates need repeated practice. Static exercises cannot ask contextual follow-up questions based on an earlier answer. Finally, many preparation methods provide no structured evaluation or only a final score, leaving candidates unsure which technical areas and communication habits require improvement.",
        "A JD contains the employer's expected technologies, responsibilities, seniority signals, and domain context. However, a long or ambiguous JD is difficult to translate directly into a balanced interview plan. RoleCue therefore treats JD analysis as a separate stage. A Candidate can paste text or upload a PDF; the system extracts technical requirements; the Candidate reviews and edits the extracted information; and the approved result becomes the evidence base for an interview blueprint. This human review step reduces the risk that an extraction error silently shapes the interview.",
        "The interview blueprint defines what the session should assess: coverage areas, stages, time allocation, question budget, expected depth, and evaluation competencies. It is not a fixed question list. During the session, the AI interviewer can formulate questions and follow-ups in response to the Candidate's answers while staying within the approved blueprint. This separation supports both personalization and traceability because each evaluated skill can be linked to a reviewed JD requirement or a Candidate-selected focus area.",
        "RoleCue presents the interview through a web-based 3D virtual interviewer. Speech-to-Text converts the Candidate's answer to text; the interview engine maintains the conversation context; Text-to-Speech produces the interviewer's voice; and synchronized mouth animation presents the response through the avatar. If 3D rendering is not usable on a device, the product contract requires a lower-resource audio-focused fallback so that the conversation can continue.",
        "After the interview, the system evaluates Technical Accuracy, Depth of Understanding, Problem-Solving, Answer Relevance, and Communication Clarity against the expectations associated with the selected JD. The report combines overall and technical-domain scores with question-level feedback, strengths, weaknesses, and improvement recommendations. A Candidate can review previous sessions and repeat a blueprint, allowing progress to be compared across separate attempts without changing the historical basis of earlier reports.",
        "The platform also includes an Admin role. Administrators manage Candidate accounts, monitor interview sessions, maintain technical domains and interview policies, manage available avatar and voice profiles, review system analytics, and oversee subscription and revenue information. These functions support platform governance but do not allow an Admin to use the Candidate's report as an automated hiring decision.",
    ]
    for para in background:
        add_body(doc, para)

    add_heading(doc, "3. Existing Systems", 2)
    add_body(doc, "Two current systems were reviewed because they represent the closest public alternatives to different parts of RoleCue. Final Round AI demonstrates job-specific AI practice and debriefing, while interviewing.io emphasizes technical interview depth through AI and experienced engineers. The comparison below uses public product information available on 17 September 2026. A missing capability means that it was not documented on the cited public pages; it does not prove that the vendor has no internal or newly released implementation.")
    add_heading(doc, "3.1 Final Round AI", 3)
    add_competitor_finalround(doc)
    add_heading(doc, "3.2 interviewing.io", 3)
    add_competitor_interviewing(doc)

    add_heading(doc, "4. Business Opportunity", 2)
    opportunity = [
        "RoleCue addresses a repeat-practice problem for students, recent graduates, career switchers, and software developers preparing for a specific technical role. These candidates may have access to articles, question banks, or occasional mock interviews, but those resources are difficult to repeat under consistent conditions. An automated simulator can make structured practice available on demand without requiring another person to schedule and conduct every session.",
        "The principal opportunity is job-specific preparation. A Candidate is usually applying to a role defined by a particular technology stack and set of responsibilities. RoleCue converts that JD into reviewed requirements and then into an interview blueprint. The result is more targeted than selecting only a broad category such as Backend, Frontend, or Data. It also gives the Candidate visibility into why a subject appears in the session.",
        "A second opportunity is to combine technical depth with realistic communication practice. Technical knowledge alone does not guarantee a clear interview answer. Candidates must describe assumptions, explain reasoning, respond to follow-up questions, and communicate trade-offs. Voice interaction and a visible interviewer create a stronger rehearsal context than a text-only quiz, while the five evaluation competencies separate correctness from depth, relevance, problem-solving, and communication.",
        "Research supports the value of structured interview preparation, although it also warns against assuming that repetition alone is sufficient. Roulin, Pham, and Bourdage's 2023 study of asynchronous video interviews found that training was associated with more structured responses and improved performance, while a basic practice opportunity by itself had negligible effects in the studied conditions. This supports RoleCue's decision to pair repeated simulation with explicit criteria, question-level feedback, and recommendations rather than treating completion of a mock session as the learning outcome.",
        "Virtual interview training also has potential when it provides concrete behavioural feedback. Langer and colleagues reported improved interview performance and reduced anxiety in a virtual employment-interview training study that analysed non-verbal behaviour and provided real-time feedback. RoleCue does not adopt camera-based behavioural scoring in the current scope, but the study supports the broader value of an interactive virtual training environment. RoleCue focuses its assessment on spoken content and the competencies approved in the project register.",
        "The competitor review shows an integration opportunity. Final Round AI publicly documents job-goal context, spoken AI practice, multiple scenarios, and automatic debriefing. interviewing.io offers strong coding and system-design practice with both AI and experienced engineers. RoleCue's proposed contribution is the combination of a Candidate-reviewed JD model, a reusable and traceable interview blueprint, adaptive runtime questions, a synchronized 3D interviewer, JD-grounded evaluation, and an administrator-controlled technical taxonomy within one academic project.",
        "The system also creates an opportunity for measurable improvement. Because JDs, blueprints, interview turns, and reports are stored separately, a Candidate can repeat practice while preserving the basis of each historical result. Administrators can examine aggregate activity and commonly identified technical weaknesses without changing individual reports. This data can support product improvement, domain coverage decisions, and future evaluation of whether the platform's recommendations help Candidates improve over multiple sessions.",
        "A subscription or interview-credit model can support the operating costs of external AI, speech, and payment services. The registered project scope includes subscription tiers, credit packages, transaction history, and revenue reporting. Exact pricing and free-tier rules are intentionally deferred until provider costs and team policy are confirmed; version 0.2 therefore defines the commercial capability without inventing prices.",
        "RoleCue is a preparation tool, not a recruitment or automated selection system. The business value depends on transparent practice, useful feedback, privacy, and reliable recovery from external-service failures. The product must avoid presenting AI feedback as a hiring verdict and must protect each Candidate's JDs, transcripts, reports, and payment records.",
    ]
    for para in opportunity:
        add_body(doc, para)
    add_source_line(doc, "Research sources: ", [
        ("Roulin, Pham and Bourdage 2023", "https://doi.org/10.1016/j.jvb.2023.103912"),
        ("Langer et al. 2016", "https://doi.org/10.1111/ijsa.12150"),
    ])

    add_heading(doc, "5. Software Product Vision", 2)
    add_body(doc, "For Candidates preparing for technical roles, RoleCue is a web-based interview practice platform that turns a target Job Description into a transparent, repeatable, and realistic mock interview. Unlike generic question banks, RoleCue allows the Candidate to review extracted requirements before the system creates an assessment blueprint. The platform then conducts a voice-based interview through a 3D virtual interviewer, adapts follow-up questions to the conversation, and produces feedback grounded in the selected role.")
    add_body(doc, "For Administrators, RoleCue provides the governance needed to operate the learning platform: account and session management, technical-domain configuration, interview and evaluation settings, avatar and voice catalogue management, subscription and transaction oversight, revenue reporting, and aggregate analytics. The intended product outcome is an accessible practice environment in which Candidates understand what was assessed, why it was assessed, and what to improve before their next interview.")

    add_heading(doc, "6. Project Scope and Limitations", 2)
    add_body(doc, "The project delivers a deployed full-stack web application for two roles: Candidate and Admin. The Candidate journey covers authentication, JD ingestion and review, interview configuration, blueprint generation, voice-based interview execution, history, evaluation reports, subscriptions, credits, billing, and payment. The Admin journey covers governance of accounts, sessions, technical context, interview rules, avatar and voice availability, analytics, subscriptions, transactions, and revenue information.")
    add_body(doc, "The approved implementation direction uses a Next.js web client, a Go back end, PostgreSQL, JWT-based authentication, role-based authorization, Large Language Model APIs, Speech-to-Text and Text-to-Speech services, web-based 3D rendering, and a third-party payment gateway. Provider selection and detailed commercial conditions remain implementation decisions; the product requirements do not depend on one vendor.")

    add_heading(doc, "6.1 Major Features", 3)
    feature_groups = [
        ("FE-01 Authentication and Candidate Profile", [
            "FE-01.1 Register, log in, and log out.",
            "FE-01.2 View and update personal profile information and account credentials.",
            "FE-01.3 Protect Candidate and Admin functions through authentication and role-based authorization.",
        ]),
        ("FE-02 Job Description Management", [
            "FE-02.1 Paste or enter JD text and upload a supported JD document.",
            "FE-02.2 Extract job title, seniority indicators, domain knowledge, programming languages, frameworks, databases, tools, and other technical requirements.",
            "FE-02.3 Allow the Candidate to review, correct, add, or remove extracted requirements.",
            "FE-02.4 Save the reviewed JD and prevent blueprint generation until Candidate review is complete.",
            "FE-02.5 Allow a Candidate to access only their own JDs.",
        ]),
        ("FE-03 Interview Blueprint and Configuration", [
            "FE-03.1 Select a reviewed JD and configure difficulty, duration, question count, and optional focus areas.",
            "FE-03.2 Generate a reusable interview blueprint containing coverage, stages, time allocation, question budget, expected depth, and evaluation competencies.",
            "FE-03.3 Keep configured difficulty separate from seniority inferred from the JD.",
            "FE-03.4 Validate that stage time and question budgets agree with the Candidate's selected configuration.",
            "FE-03.5 Support non-destructive blueprint regeneration so that a failed attempt does not erase a previously valid blueprint.",
        ]),
        ("FE-04 AI Virtual Interview", [
            "FE-04.1 Start a one-to-one interview session from an approved and persisted blueprint.",
            "FE-04.2 Ask questions and contextual follow-up questions at runtime while remaining within the blueprint's assessment boundaries.",
            "FE-04.3 Maintain ordered interview turns containing interviewer questions, Candidate transcripts, and session context.",
            "FE-04.4 Track completed, failed, interrupted, and active session states.",
            "FE-04.5 Pause or recover gracefully when an AI or voice provider temporarily fails without corrupting completed turns.",
        ]),
        ("FE-05 Voice and 3D Interviewer", [
            "FE-05.1 Capture Candidate speech through the browser microphone and convert it to text.",
            "FE-05.2 Synthesize the interviewer's questions as spoken audio.",
            "FE-05.3 Present a web-based 3D interviewer with synchronized speaking and lip movement.",
            "FE-05.4 Provide a lower-resource audio-focused fallback when 3D rendering is unavailable or unusable.",
            "FE-05.5 Display clear microphone, listening, processing, speaking, and connection states.",
        ]),
        ("FE-06 Evaluation and Performance Reporting", [
            "FE-06.1 Evaluate Technical Accuracy, Depth of Understanding, Problem-Solving, Answer Relevance, and Communication Clarity.",
            "FE-06.2 Ground evaluation criteria in reviewed JD expectations and Candidate-selected focus areas.",
            "FE-06.3 Produce an overall score and technical-domain scores.",
            "FE-06.4 Provide question-level feedback, strengths, weaknesses, and personalized improvement recommendations.",
            "FE-06.5 Preserve the blueprint snapshot used by a session so that a historical report remains reproducible after later configuration changes.",
        ]),
        ("FE-07 Interview History", [
            "FE-07.1 List previous interviews by target JD, date, status, and overall score.",
            "FE-07.2 Allow the Candidate to reopen completed reports and review session details.",
            "FE-07.3 Allow repeat practice from a reusable blueprint while keeping each session and report separate.",
        ]),
        ("FE-08 Subscription Billing and Payment", [
            "FE-08.1 Show the Candidate's current subscription plan and remaining interview credits.",
            "FE-08.2 Support plan upgrades or additional credit purchases through a third-party payment gateway.",
            "FE-08.3 Store transaction history and payment status.",
            "FE-08.4 Process payment callbacks idempotently and grant credits only after verified successful payment.",
        ]),
        ("FE-09 Admin Account and Session Management", [
            "FE-09.1 View Candidate accounts and account details.",
            "FE-09.2 Lock or unlock Candidate accounts.",
            "FE-09.3 View and filter interview sessions by Candidate, status, or date.",
            "FE-09.4 Inspect session details and monitor completed, failed, or interrupted sessions.",
        ]),
        ("FE-10 Admin Interview Configuration", [
            "FE-10.1 Manage technical domains and technologies used as interview context.",
            "FE-10.2 Configure allowed difficulty levels, duration constraints, evaluation criteria, and interview behaviour guidelines.",
            "FE-10.3 Configure AI interview and evaluation settings without changing completed historical reports.",
        ]),
        ("FE-11 Admin Avatar and Voice Management", [
            "FE-11.1 Manage available 3D virtual interviewer avatars.",
            "FE-11.2 Manage supported interviewer voice profiles.",
            "FE-11.3 Control which avatar and voice combinations are available to Candidates.",
        ]),
        ("FE-12 Analytics Subscription and Revenue Management", [
            "FE-12.1 View totals for active, completed, failed, and interrupted interview sessions.",
            "FE-12.2 Analyse interview volume, average Candidate performance, and commonly identified technical weaknesses.",
            "FE-12.3 Manage pricing plans, subscription tiers, or credit packages.",
            "FE-12.4 View transaction status and revenue reports by day, month, or year.",
        ]),
    ]
    for title, items in feature_groups:
        add_feature_heading(doc, title)
        for item in items:
            lead = item.split(" ", 1)[0] + " "
            add_bullet(doc, item, level=0, bold_lead=lead)

    add_heading(doc, "6.2 Limitations and Exclusions", 3)
    add_body(doc, "The following limitations define the version 0.2 product boundary. They distinguish confirmed operational constraints from capabilities that are not included in the registered capstone scope.")
    add_label(doc, "Limitations")
    limitations = [
        "LI-01: The platform supports Candidate and Admin roles. Employer, recruiter, mentor, and human interviewer roles are not part of the approved scope.",
        "LI-02: A Candidate can access only their own profile, JDs, interview sessions, transcripts, reports, subscriptions, credits, and transaction records.",
        "LI-03: An interview cannot start until its JD requirements have been reviewed and an interview blueprint has been persisted.",
        "LI-04: Evaluation is limited to requirements traceable to the reviewed JD or Candidate-selected focus areas and to the five registered competencies.",
        "LI-05: Common operations such as login, profile viewing, interview-history retrieval, and report viewing target a response time within three seconds under normal test conditions. AI analysis and evaluation may take longer and must show progress.",
        "LI-06: The capstone test target is at least 20 concurrent users under normal testing; version 0.2 does not claim large-scale production capacity.",
        "LI-07: Interview quality and latency depend on the Candidate's microphone, network connection, browser capability, and external AI and speech services.",
        "LI-08: When 3D rendering is unavailable or performs poorly, the system uses an audio-focused fallback. The fallback preserves the interview but cannot provide the complete avatar experience.",
        "LI-09: Temporary external-service failures must produce a clear error or paused state and preserve completed interview turns, but uninterrupted service cannot be guaranteed by the project team.",
        "LI-10: Supported JD file types, maximum file size, language coverage, AI provider, speech providers, payment gateway, exact pricing, and free-credit allocation remain configurable implementation decisions until formally approved.",
        "LI-11: AI-generated questions and evaluations may contain errors. Candidate review of extracted JD requirements and transparent question-level feedback reduce risk but do not eliminate it.",
        "LI-12: Payment credits are granted only after a verified successful transaction; pending or failed transactions do not increase the Candidate's balance.",
    ]
    for item in limitations:
        lead = item.split(" ", 1)[0] + " "
        add_bullet(doc, item, bold_lead=lead)

    add_label(doc, "Exclusions")
    exclusions = [
        "EX-01: RoleCue does not conduct real recruitment interviews, rank applicants for employers, or make hiring decisions.",
        "EX-02: RoleCue does not provide concealed real-time answers during an actual third-party interview. Its AI interviewer and feedback operate only inside RoleCue practice sessions.",
        "EX-03: A built-in live coding execution sandbox, automated compilation, and hidden test-case grading are not included in the registered scope.",
        "EX-04: Camera-based facial-expression analysis, emotion inference, gaze tracking, identity verification, and personality scoring are excluded.",
        "EX-05: Native Android and iOS applications are excluded; the product is delivered as a responsive web application.",
        "EX-06: A marketplace for booking human interviewers or mentors is excluded.",
        "EX-07: Employer job posting, applicant tracking, résumé screening, and recruitment workflow management are excluded.",
        "EX-08: Custom avatar creation by Candidates and unrestricted voice cloning are excluded. Candidates select from administrator-approved profiles.",
        "EX-09: Offline interview execution is excluded because AI, speech, and synchronization services require network connectivity.",
        "EX-10: The platform does not guarantee employment outcomes, interview scores from external companies, or equivalence with a particular employer's private hiring rubric.",
        "EX-11: Provider-specific service-level agreements and enterprise-scale availability guarantees are outside the capstone deliverable.",
        "EX-12: Biometric conclusions, medical or psychological assessment, and automated judgments about protected personal characteristics are excluded.",
    ]
    for item in exclusions:
        lead = item.split(" ", 1)[0] + " "
        add_bullet(doc, item, bold_lead=lead)

    # Footer page numbering and field refresh on open.
    for section in doc.sections:
        add_page_number(section)
    settings = doc.settings._element
    update = settings.find(qn("w:updateFields"))
    if update is None:
        update = OxmlElement("w:updateFields")
        settings.append(update)
    update.set(qn("w:val"), "true")

    # Prevent accidental blue/italic carry-over from the earlier draft in all new body content.
    doc.core_properties.title = "Report 1 Project Introduction Version 0.2"
    doc.core_properties.subject = "RoleCue Capstone Project Introduction"
    doc.core_properties.author = "Group 09"
    doc.core_properties.comments = "Expanded from version 0.1 using the lecturer sample, Capstone Project Register, current project contracts, and cited official research sources."

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    build()

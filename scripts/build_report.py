"""Build the report from editable Markdown. Optional dependency: reportlab."""
from pathlib import Path
import re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable, PageBreak, Paragraph, Preformatted,
    SimpleDocTemplate, Spacer,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "NLPApp-Mini-Project-Report.pdf"
NAVY = colors.HexColor("#152D44")
TEAL = colors.HexColor("#087F8C")
GREY = colors.HexColor("#526273")


def inline(text):
    text = escape(text)
    text = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return re.sub(r"(https://[^\s]+)", r'<link href="\1" color="#087F8C">\1</link>', text)


def footer(canvas, document):
    width, height = A4
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D8E1E8"))
    canvas.line(46, 42, width - 46, 42)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GREY)
    canvas.drawString(46, 28, "NLPApp  /  College Mini Project")
    canvas.drawRightString(width - 46, 28, str(document.page))
    if document.page > 1:
        canvas.setFillColor(TEAL)
        canvas.rect(46, height - 34, 25, 3, fill=1, stroke=0)
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(width - 46, height - 33, "OFFLINE TEXT STUDIO")
    canvas.restoreState()


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    mono = "Courier-Bold"
    for candidate in [Path("C:/Windows/Fonts/consola.ttf"), Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")]:
        if candidate.exists():
            pdfmetrics.registerFont(TTFont("ReportMono", str(candidate)))
            mono = "ReportMono"
            break
    body = ParagraphStyle("ReportBody", fontName="Helvetica", fontSize=10, leading=14.1,
                          textColor=NAVY, spaceAfter=9, alignment=TA_LEFT)
    title = ParagraphStyle("ReportTitle", parent=body, fontName="Helvetica-Bold", fontSize=23,
                           leading=28, spaceAfter=18)
    heading = ParagraphStyle("ReportHeading", parent=body, fontName="Helvetica-Bold",
                             fontSize=12, leading=16, textColor=TEAL, spaceBefore=8,
                             spaceAfter=7, keepWithNext=True)
    cover_title = ParagraphStyle("CoverTitle", parent=title, fontSize=48, leading=54, spaceAfter=5)
    cover_subtitle = ParagraphStyle("CoverSubtitle", parent=title, fontSize=23, leading=29, spaceAfter=4)
    cover_kicker = ParagraphStyle("CoverKicker", parent=body, fontSize=12, leading=17, textColor=TEAL, spaceAfter=20)
    bullet = ParagraphStyle("ReportBullet", parent=body, leftIndent=12, firstLineIndent=0,
                            bulletIndent=0, spaceAfter=6)
    code = ParagraphStyle("ReportCode", fontName=mono, fontSize=9, leading=11.5,
                          textColor=NAVY, backColor=colors.HexColor("#EFF4F7"),
                          borderPadding=10, spaceBefore=7, spaceAfter=16)
    document = SimpleDocTemplate(str(OUTPUT), pagesize=A4, rightMargin=46, leftMargin=46,
                                topMargin=57, bottomMargin=57,
                                title="NLPApp - Offline Text Studio: Mini Project Report",
                                author="NLPApp Project", subject="Architecture, algorithms, setup, tests and demonstration")
    sections = (ROOT / "docs" / "project-report.md").read_text(encoding="utf-8-sig").strip().split("\n---\n")
    story = []
    for page, section in enumerate(sections):
        if page:
            story.append(PageBreak())
        else:
            story.append(Spacer(1, 22))
        lines = section.strip().splitlines()
        index = 0
        while index < len(lines):
            line = lines[index].strip()
            if not line:
                index += 1
                continue
            if line.startswith("```"):
                block = []
                index += 1
                while index < len(lines) and not lines[index].startswith("```"):
                    block.append(lines[index])
                    index += 1
                story.append(Preformatted("\n".join(block), code))
            elif line.startswith("# "):
                story.append(Paragraph(inline(line[2:]), cover_title if page == 0 else title))
            elif line.startswith("## "):
                use = cover_subtitle if page == 0 and line == "## Offline Text Studio" else heading
                story.append(Paragraph(inline(line[3:]), use))
            elif line.startswith("### "):
                story.append(Paragraph(inline(line[4:]), cover_kicker))
                story.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=18))
            elif line.startswith("- "):
                story.append(Paragraph(inline(line[2:]), bullet, bulletText="-"))
            else:
                paragraph = [line]
                while index + 1 < len(lines) and lines[index + 1].strip() and not lines[index + 1].startswith(("#", "- ", "```")):
                    index += 1
                    paragraph.append(lines[index].strip())
                story.append(Paragraph(inline(" ".join(paragraph)), body))
            index += 1
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)


if __name__ == "__main__":
    main()

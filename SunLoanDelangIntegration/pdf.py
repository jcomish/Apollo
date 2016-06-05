import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


def generate_doc():

    doc = SimpleDocTemplate("form_letter.pdf", pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    story = []
    logo = "assets/logo.png"
    magName = "Pythonista"
    issueNum = 12
    subPrice = "99.00"
    limitedDate = "03/05/2010"
    freeGift = "tin foil hat"

    formatted_time = time.ctime()
    full_name = "Mike Driscoll"
    address_parts = ["411 State St.", "Marshalltown, IA 50158"]

    im = Image(logo, 2 * inch, 2 * inch)
    story.append(im)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    ptext = '<font size=12>%s</font>' % formatted_time

    story.append(Paragraph(ptext, styles["Normal"]))
    story.append(Spacer(1, 12))

    # Create return address
    ptext = '<font size=12>%s</font>' % full_name
    story.append(Paragraph(ptext, styles["Normal"]))
    for part in address_parts:
        ptext = '<font size=12>%s</font>' % part.strip()
        story.append(Paragraph(ptext, styles["Normal"]))

    story.append(Spacer(1, 12))
    ptext = '<font size=12>Dear %s:</font>' % full_name.split()[0].strip()
    story.append(Paragraph(ptext, styles["Normal"]))
    story.append(Spacer(1, 12))

    ptext = '<font size=12>We would like to welcome you to our subscriber base for %s Magazine! \
            You will receive %s issues at the excellent introductory price of $%s. Please respond by\
            %s to start receiving your subscription and get the following free gift: %s.</font>' % (magName,
                                                                                                    issueNum,
                                                                                                    subPrice,
                                                                                                    limitedDate,
                                                                                                    freeGift)
    story.append(Paragraph(ptext, styles["Justify"]))
    story.append(Spacer(1, 12))

    ptext = '<font size=12>Thank you very much and we look forward to serving you.</font>'
    story.append(Paragraph(ptext, styles["Justify"]))
    story.append(Spacer(1, 12))
    ptext = '<font size=12>Sincerely,</font>'
    story.append(Paragraph(ptext, styles["Normal"]))
    story.append(Spacer(1, 48))
    ptext = '<font size=12>Ima Sucker</font>'
    story.append(Paragraph(ptext, styles["Normal"]))
    story.append(Spacer(1, 12))
    doc.build(story)


# http://www.blog.pythonlibrary.org/2010/03/08/a-simple-step-by-step-reportlab-tutorial/
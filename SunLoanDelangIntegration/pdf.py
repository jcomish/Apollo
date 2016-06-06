import time
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from django.contrib.staticfiles.templatetags.staticfiles import static
import datetime


def generate_doc(customer):

    customer = customer
    doc = SimpleDocTemplate(str(customer.id) + "_form_letter" + str(datetime.datetime.now()) + ".pdf", pagesize=letter,
                            rightMargin=50, leftMargin=50,
                            topMargin=18, bottomMargin=18)
    story = []
    logo = "http://localhost:8000" + static('logo.png')
    # todo PROD: update for production use

    formatted_time = time.ctime()
    full_name = customer.first_name + " " + customer.last_name

    im = Image(logo, 1.5 * inch, 1.5 * inch)
    story.append(im)

    title_style = getSampleStyleSheet()
    title_style.add(ParagraphStyle(name='Bold-Cent', fontName='Times-Bold', alignment=TA_CENTER))

    heading_style = getSampleStyleSheet()
    heading_style.add(ParagraphStyle(name='Bold', fontName='Times-Bold', alignment=TA_JUSTIFY))

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    ptext = '<font size=12>%s</font>' % formatted_time

    story.append(Paragraph(ptext, styles["Normal"]))
    story.append(Spacer(1, 12))

    # Create return address

    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    story.append(Spacer(1, 12))
    ptext = '<font size=14>SHORT MESSAGE SERVICE (SMS)/EMAIL NOTICE AND OPT-IN FORM</font>'
    # Dear %s:</font>' % full_name.split()[0].strip()
    story.append(Spacer(1, 12))
    story.append(Paragraph(ptext, title_style["Bold-Cent"]))
    story.append(Spacer(1, 12))

    heading_about = '<font size=12>About</font>'
    story.append(Paragraph(heading_about, heading_style["Bold"]))
    story.append(Spacer(1, 12))

    ptext = '<font size=10>Sun Loan Company offers, as an additional convenience to you, the ability' \
            'to receive Short Message Service (SMS) messages (also known as text.......</font>'
    story.append(Paragraph(ptext, styles["Justify"]))
    story.append(Spacer(1, 12))

    heading_about = '<font size=12>How to Enroll</font>'
    story.append(Paragraph(heading_about, heading_style["Bold"]))
    story.append(Spacer(1, 12))

    ptext = '<font size=12>Thank you very much and we look forward to serving you.</font>'
    story.append(Paragraph(ptext, styles["Justify"]))
    story.append(Spacer(1, 12))
    ptext = '<font size=12>Sincerely,</font>'
    story.append(Paragraph(ptext, styles["Normal"]))
    story.append(Spacer(1, 48))
    ptext = '<font size=12>Sun Loan Inc</font>'
    story.append(Paragraph(ptext, styles["Normal"]))
    story.append(Spacer(1, 12))
    doc.build(story)


# http://www.blog.pythonlibrary.org/2010/03/08/a-simple-step-by-step-reportlab-tutorial/
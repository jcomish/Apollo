import time
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from django.contrib.staticfiles.templatetags.staticfiles import static
import datetime
from .models import CustomerPDF


def generate_doc(customer):
    try:
        customer = customer
        filename = 'static/' + str(customer.id) + "_form_letter" + str(datetime.datetime.now()) + ".pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter,
                                rightMargin=50, leftMargin=50,
                                topMargin=18, bottomMargin=18)
        story = []
        logo = "http://localhost:8000" + static('logo.png')
        # todo PROD: update for production use

        formatted_date = str(time.strftime("%d/%m/%Y"))
        im = Image(logo, 1.5 * inch, 1.5 * inch)
        story.append(im)

        title_style = getSampleStyleSheet()
        title_style.add(ParagraphStyle(name='Bold-Cent', fontName='Times-Bold', alignment=TA_CENTER))

        heading_style = getSampleStyleSheet()
        heading_style.add(ParagraphStyle(name='Bold', fontName='Times-Bold', alignment=TA_JUSTIFY))

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

        story.append(Spacer(1, 12))

        # Create return address

        styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
        story.append(Spacer(1, 12))
        paragraph_text = '<font size=14>SHORT MESSAGE SERVICE (SMS)/EMAIL NOTICE AND OPT-IN FORM</font>'
        # Dear %s:</font>' % full_name.split()[0].strip()
        story.append(Spacer(1, 12))
        story.append(Paragraph(paragraph_text, title_style["Bold-Cent"]))
        story.append(Spacer(1, 12))
        story.append(Spacer(1, 12))

        heading_about = '<font size=12>About</font>'
        story.append(Paragraph(heading_about, heading_style["Bold"]))
        story.append(Spacer(1, 12))

        paragraph_text = '<font size=10>Sun Loan Company offers, as an additional convenience to you, the ability' \
                'to receive Short Message Service (SMS) messages (also known as text messages) and electronic mail ' \
                '(email). Generally, the messages that we would send will provide you with information about your account' \
                ', or will provide you with information and Sun Loan Company offers or promotions</font>'
        story.append(Paragraph(paragraph_text, styles["Justify"]))
        story.append(Spacer(1, 12))

        heading_about = '<font size=12>How to Enroll</font>'
        story.append(Paragraph(heading_about, heading_style["Bold"]))

        paragraph_text = '<font size=10>To sign up to receive SMS messages and/or email from Sun Loan Company please check the ' \
                'box below:</font>'
        story.append(Spacer(1, 12))
        story.append(Paragraph(paragraph_text, styles["Justify"]))
        paragraph_text = '<font size=10>[ ]</font>'

        story.append(Spacer(1, 12))
        story.append(Paragraph(paragraph_text, styles["Justify"]))
        story.append(Spacer(1, 12))

        paragraph_text = '<font size=10>By checking the box above, I understand that I am choosing to receive SMS' \
                ' messages/email from Sun Loan Company. I understand that any such SMS messages/email ' \
                'will be subject to whatever rates and charges associated with are my responsibility and ' \
                'not the responsibility of Sun Loan Company. My signature shall include an electronic,' \
                ' digital or handwritten form of signature, to the extent that such form of signature ' \
                'is recognized as a valid signature under applicable federal law or state contract law.' \
                'I understand that I am not required to sign this agreement (directly or indirectly), or ' \
                'to agree to enter into such an agreement as a condition of any loan or the purchase ' \
                'of any property, goods, or services. Message and Data Rates May Apply.</font>'
        story.append(Paragraph(paragraph_text, styles["Justify"]))
        story.append(Spacer(1, 12))

        paragraph_text = '<font size=10>Cell Number: ' + customer.phone_number + '</font>'
        story.append(Paragraph(paragraph_text, styles["Justify"]))
        story.append(Spacer(1, 12))

        paragraph_text = '<font size=10>Printed Name: ' + customer.first_name + ' ' + customer.last_name + '</font>'
        story.append(Paragraph(paragraph_text, styles["Justify"]))
        story.append(Spacer(1, 12))
        paragraph_text = '<font size=10>Signed(SMS)_______________________________________________________________</font>'
        story.append(Paragraph(paragraph_text, styles["Justify"]))
        story.append(Spacer(1, 12))
        paragraph_text = '<font size=10>Signed(Email)_____________________________________________________________</font>'
        story.append(Paragraph(paragraph_text, styles["Justify"]))
        story.append(Spacer(1, 12))
        paragraph_text = '<font size=12>Date: ' + formatted_date + '</font>'
        story.append(Paragraph(paragraph_text, styles["Justify"]))
        story.append(Spacer(1, 48))
        paragraph_text = '<font size=12>Sun Loan Inc</font>'
        story.append(Paragraph(paragraph_text, styles["Normal"]))
        story.append(Spacer(1, 12))
        doc.build(story)

        customer_pdf = CustomerPDF()
        customer_pdf.customer_id = customer
        customer_pdf.path = filename
        customer_pdf.save()

        return filename
    except:

        return 'failed to generate pdf'

    # http://www.blog.pythonlibrary.org/2010/03/08/a-simple-step-by-step-reportlab-tutorial/

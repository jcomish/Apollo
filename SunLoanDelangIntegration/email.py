import requests
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, tostring


class Email(object):
    def __init__(self):
        self.baseEndPoint = "http://sunloanapi.dlangemobile.com/xml/email/"
        self.contentType = ""
        self.message = "python test"
        self.subject = "Test Subject"
        self.email_address = "test@test.com"
        self.apiKey = "8dba905330fa4d5a9b5193c4cedb540c"
        self.headers = {'Content-Type': 'application/xml'}
        self.messageId = 0
        self.contactID = 0

    def send(self):
        # http://sunloanapi.dlangemobile.com/xml/email/8dba905330fa4d5a9b5193c4cedb540c/
        endpoint = self.baseEndPoint + self.apiKey + "/send"

        if int(self.contactID) > 1:
            root = Element('EmailInfo')
            content = SubElement(root, 'Content')
            content.text = self.message
            subject = SubElement(root, 'Subject')
            subject.text = self.subject
            recipient_contacts = SubElement(root, 'RecipientContacts')
            recipient_contacts_int = SubElement(recipient_contacts, 'int')
            recipient_contacts_int.text = str(self.contactID)

        elif len(self.email_address) > 1:
            root = Element('EmailInfo')
            subject = SubElement(root, 'Subject')
            subject.text = self.subject
            content = SubElement(root, 'Content')
            content.text = self.message
            email_addresses = SubElement(root, 'EmailAddresses')
            email_address_string = SubElement(email_addresses, 'string')
            email_address_string.text = self.email_address
        else:
            self.messageId = -1
            root = ''

        if root != '':
            # Add Try Catch Logic and also input validation for Message and Phone Number
            try:
                data = tostring(root)
                response = requests.post(endpoint, data=data, headers=self.headers)
                status_code = response.status_code

                if status_code == 200:
                    tree = ET.fromstring(response.content)
                    for elem in tree.iter():
                        if elem.tag == "int":
                            self.messageId = elem.text
            except Exception as e:
                return e

                        # Sample Response from Delange
                        # <Message>
                        # 	<Content>Test 2 String content</Content>
                        # 	<PhoneNumbers><string>+12109191320</string></PhoneNumbers>
                        # </Message>

                        # sample usage
                        # mysms = SMS()
                        # mysms.message = "Hello Chris"
                        # mysms.send()








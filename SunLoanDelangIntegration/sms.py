import requests
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, tostring


class SMS(object):
    def __init__(self):
        self.baseEndPoint = "http://sunloanapi.dlangemobile.com/xml/messages/"
        self.contentType = ""
        self.message = "python test"
        self.phoneNumber = "+12109191320"
        self.apiKey = "8dba905330fa4d5a9b5193c4cedb540c"
        self.headers = {'Content-Type': 'application/xml'}
        self.messageId = 0
        self.contactID = 0

    def send(self):
        # http://sunloanapi.dlangemobile.com/xml/messages/8dba905330fa4d5a9b5193c4cedb540c/longcode
        endpoint = self.baseEndPoint + self.apiKey + "/longcode"

        if int(self.contactID) > 1:
            root = Element('Message')
            content = SubElement(root, 'Content')
            content.text = self.message
            recipient_contacts = SubElement(root, 'RecipientContacts')
            recipient_contacts_int = SubElement(recipient_contacts, 'int')
            recipient_contacts_int.text = self.contactID

        elif len(self.phoneNumber) > 1:
            root = Element('Message')
            content = SubElement(root, 'Content')
            content.text = self.message
            phone_number = SubElement(root, 'PhoneNumbers')
            phone_number_string = SubElement(phone_number, 'string')
            phone_number_string.text = self.phoneNumber
        else:
            self.messageId = -1
            root = ''

        if root != '':
            # Add Try Catch Logic and also input validation for Message and Phone Number
            response = requests.post(endpoint, data=tostring(root), headers=self.headers)
            status_code = response.status_code

            if status_code == 200:
                tree = ET.fromstring(response.content)
                for elem in tree.iter():
                    if elem.tag == "int":
                        self.messageId = elem.text

                        # Sample Response from Delange
                        # <Message>
                        # 	<Content>Test 2 String content</Content>
                        # 	<PhoneNumbers><string>+12109191320</string></PhoneNumbers>
                        # </Message>

                        # sample usage
                        # mysms = SMS()
                        # mysms.message = "Hello Chris"
                        # mysms.send()








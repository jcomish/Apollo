import requests
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, tostring
import logging

contactLogging = logging.getLogger('contact_api')


class Contact(object):
    def __init__(self):
        self.baseEndPoint = "http://sunloanapi.dlangemobile.com/xml/contacts/"
        self.contentType = ""
        self.firstName = "python test"
        self.lastName = "python test"
        self.phoneNumber = "+12109191320"
        self.apiKey = "8dba905330fa4d5a9b5193c4cedb540c"
        self.headers = {'Content-Type': 'application/xml'}
        self.contactId = 0

    def create(self):
        # http://sunloanapi.dlangemobile.com/xml/contact/8dba905330fa4d5a9b5193c4cedb540c
        endpoint = self.baseEndPoint + self.apiKey
        root = Element('Contact')
        phone_number = SubElement(root, 'PhoneNumber')
        phone_number.text = self.phoneNumber
        first_name = SubElement(root, 'FirstName')
        first_name.text = self.firstName
        last_name = SubElement(root, 'LastName')
        last_name.text = self.lastName

        # Add Try Catch Logic and also input validation for Message and Phone Number
        response = requests.post(endpoint, data=tostring(root), headers=self.headers)
        status_code = response.status_code

        contactLogging.debug(response)

        if status_code == 200:
            tree = ET.fromstring(response.content)
            for elem in tree.iter():
                if elem.tag == "ID":
                    self.contactId = elem.text

        elif status_code == 400:
            contactLogging.warning(response)
            tree = ET.fromstring(response.content)
            for elem in tree.iter():
                if elem.tag == "ErrorMessage":
                    error_msg = elem.text
                    self.contactId = error_msg.replace('Phone number already exists. ID = ','')
            # todo: retrieve info for previous contactid and record to another table, possibly compare lastname?
        else:
            contactLogging.error(response)

        # Sample Response from Delange
        # <Message>
        # 	<Content>Test 2 String content</Content>
        # 	<PhoneNumbers><string>+12109191320</string></PhoneNumbers>
        # </Message>

        # sample usage
        # mysms = SMS()
        # mysms.message = "Hello Chris"
        # mysms.send()








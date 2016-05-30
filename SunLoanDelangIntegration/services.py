from random import randint
from . import contact
import logging

contactLogging = logging.getLogger('contact_api')


def get_verification_code():
    random_number = randint(1000,9999)
    return random_number


def create_contact(customer):
    myContact = contact.Contact()
    myContact.firstName = customer.first_name
    myContact.lastName = customer.last_name
    myContact.phoneNumber = customer.phone_number
    try:
        myContact.create()
    except Exception as e:
        contactLogging.error(e)
        myContact.contactId = 0

    return myContact.contactId

from random import randint
from . import contact
from . import sms
from .models import SentMessages
import logging

contactLogging = logging.getLogger('contact_api')


def get_verification_code():
    random_number = randint(1000,9999)
    return random_number


def create_contact(customer):
    my_contact = contact.Contact()
    my_contact.firstName = customer.first_name
    my_contact.lastName = customer.last_name
    my_contact.phoneNumber = customer.phone_number
    try:
        my_contact.create()
    except Exception as e:
        contactLogging.error(e)
        my_contact.contactId = 0

    return my_contact.contactId


def send_welcome_message(customer):
    welcome_sms = sms.SMS()
    welcome_sms.contactID = customer.delang_contact_id
    # todo: retrieve store api key and phone number
    # todo: retrieve welcome message from model and find and replace
    welcome_sms.message = "Welcome to Sun Loan Notifications. Please call your Loan Coordinator at XXX-XXXX and give" \
                          " them this verification code: " + str(customer.verification_code)

    # messageid = 1 for welcome message todo: retrieve welcome message id from DB
    log_message(customer, 1, 1, welcome_sms) # todo: make a welcome message class abstracted to be the same as email
    welcome_sms.send()

    return welcome_sms.messageId


def log_message(customer, message_type, message_id, message):
    cust_message = SentMessages()
    cust_message.customer_id = customer.id
    cust_message.raw_message = message.message
    cust_message.delang_message_id = message.messageId
    cust_message.message = message_id


    return True

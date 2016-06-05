from random import randint
from . import contact
from . import sms
from .models import SentMessages
from .models import Message
from .models import Customer
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
    log_message(customer, 1, welcome_sms) # todo: make a welcome message class abstracted to be the same as email
    welcome_sms.send()
    log_message(customer, 1, welcome_sms) # todo: make a welcome message class abstracted to be the same as email

    return welcome_sms.messageId


def send_message(customer_id, message_id):
    customer = Customer.objects.get(pk=customer_id)
    message = Message.objects.get(pk=message_id)
    sms_message = sms.SMS()
    sms_message.contactID = customer.delang_contact_id
    # todo: retrieve store api key and phone number
    # todo: retrieve welcome message from model and find and replace
    sms_message.message = message.verbiage

    # messageid = 1 for welcome message todo: retrieve welcome message id from DB
    log_message(customer, message.id, sms_message) # todo: make a welcome message class abstracted to be the same as email
    sms_message.send()
    log_message(customer, message.id, sms_message) # todo: make a welcome message class abstracted to be the same as email

    return sms_message.messageId


def log_message(customer, message_type, message):

    # todo: change to not null
    if message_type is not None:
        my_message = Message.objects.get(pk=message_type)
        cust_message = SentMessages()
        cust_message.customer_id = customer.id
        cust_message.raw_message = message.message
        cust_message.delang_message_id = message.messageId
        cust_message.message = my_message
        cust_message.save()
        cust_message_id = cust_message.id

        return cust_message_id

    return False

from random import randint
from . import smscontact
from . import emailcontact
from . import sms
from .models import SentMessages
from .models import Message
from .models import Customer
import logging
import datetime

contactLogging = logging.getLogger('contact_api')


def get_verification_code():
    random_number = randint(1000,9999)
    return random_number


def create_sms_contact(customer):
    my_contact = smscontact.SMSContact()
    my_contact.firstName = customer.first_name
    my_contact.lastName = customer.last_name
    my_contact.phoneNumber = customer.phone_number
    try:
        my_contact.create()
    except Exception as e:
        contactLogging.error(e)
        my_contact.contactId = 0

    return my_contact.contactId

def create_email_contact(customer):
    my_contact = emailcontact.EmailContact()
    my_contact.firstName = customer.first_name
    my_contact.lastName = customer.last_name
    my_contact.emailAddress = customer.email_address
    try:
        my_contact.create()
    except Exception as e:
        contactLogging.error(e)
        my_contact.contactId = 0

    return my_contact.contactId


def send_sms_welcome_message(customer):
    welcome_sms = sms.SMS()
    welcome_sms.contactID = customer.delang_contact_id
    # todo: retrieve store api key and phone number
    # todo: retrieve welcome message from model and find and replace
    # todo: add try catch logic
    welcome_sms.message = "Welcome to Sun Loan Notifications. Please call your Loan Coordinator at XXX-XXXX and give" \
                          " them this verification code: " + str(customer.verification_code)

    # messageid = 1 for welcome message todo: retrieve welcome message id from DB
    log_message(customer, 1, welcome_sms) # todo: make a welcome message class abstracted to be the same as email
    welcome_sms.send()
    log_message(customer, 1, welcome_sms) # todo: make a welcome message class abstracted to be the same as email

    return welcome_sms.messageId

def send_email_welcome_message(customer):
    # todo: change to email class
    welcome_sms = sms.SMS()
    welcome_sms.contactID = customer.delang_contact_id
    # todo: retrieve store api key and phone number
    # todo: retrieve welcome message from model and find and replace
    # todo: add try catch logic
    welcome_sms.message = "Welcome to Sun Loan Notifications. Please call your Loan Coordinator at XXX-XXXX and give" \
                          " them this verification code: " + str(customer.verification_code)

    # messageid = 1 for welcome message todo: retrieve welcome message id from DB
    log_message(customer, 1, welcome_sms) # todo: make a welcome message class abstracted to be the same as email
    welcome_sms.send()
    log_message(customer, 1, welcome_sms) # todo: make a welcome message class abstracted to be the same as email

    return welcome_sms.messageId


def send_message(customer_id, message_id):
    customer = Customer.objects.get(pk=customer_id)
    last_message = SentMessages.objects.filter(customer=customer).exclude(delang_message_id=0, message_id = 1).order_by('-date_sent')[:1]
    offset = datetime.datetime.now()-datetime.timedelta(hours=24)
    message = Message.objects.get(pk=message_id)
    sms_message = sms.SMS()
    sms_message.contactID = customer.delang_contact_id
    # todo: retrieve store api key and phone number
    # todo: retrieve welcome message from model and find and replace
    sms_message.message = message.verbiage

    if last_message:
        for messages in last_message:
            if messages.date_sent.replace(tzinfo=None) < offset:
                    # messageid = 1 for welcome message todo: retrieve welcome message id from DB
                    log_message(customer, message.id, sms_message) # todo: make a welcome message class abstracted to be the same as email
                    sms_message.send()
                    if sms_message.messageId > 0:
                        log_message(customer, message.id, sms_message, 'Success') # todo: make a welcome message class abstracted to be the same as email
                    else:
                        log_message(customer, message.id, sms_message, 'Failed') # todo: make a welcome message class abstracted to be the same as email
                    return sms_message.messageId
            else:
                log_message(customer, message.id, sms_message, 'Messaging Limit Reached')  # todo: make a welcome message class abstracted to be the same as email
            break
    else:
        return 0


def log_message(customer, message_type, message, status='Attempting'):

    # todo: change to not null
    if message_type is not None:
        my_message = Message.objects.get(pk=message_type)
        cust_message = SentMessages()
        cust_message.customer_id = customer.id
        cust_message.raw_message = message.message
        cust_message.delang_message_id = message.messageId
        cust_message.message = my_message
        cust_message.status = status
        cust_message.save()
        cust_message_id = cust_message.id

        return cust_message_id

    return False

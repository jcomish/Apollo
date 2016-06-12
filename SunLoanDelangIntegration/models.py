from django.db import models
from django.core.validators import RegexValidator


class Customer(models.Model):
    phone_regex = RegexValidator(regex=r'^\d{9,10}$',
                                 message="Phone number must be entered in the format: '9999999999'. /"
                                         "Up to 10 digits allowed.")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=12,validators=[phone_regex], blank=True)
    # todo: split phonenumber up into area code and number then concatenate with +1 when SMS
    # todo: timezone to CST - maybe base off browser due to stores locations
    email_address = models.EmailField()
    account_id = models.CharField(max_length=20, default='')
    store = models.ForeignKey('Store', default=1)
    status = models.ForeignKey('Status', default=1)
    user_id = models.IntegerField(default=0)
    notification_setting = models.ForeignKey('NotificationSetting', default=1)
    verification_code = models.IntegerField(default=0)
    delang_contact_id = models.IntegerField(default=0)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name, self.last_name, self.email_address


class CustomerPDF(models.Model):
    customer_id = models.ForeignKey('Customer')
    path = models.CharField(max_length=500)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_id, self.path


class Message(models.Model):
    name = models.CharField(max_length=200)
    verbiage = models.CharField(max_length=2000)

    def __self__(self):
        return self.name


class MessageType(models.Model):
    name = models.CharField(max_length=10)

    def __self__(self):
        return self.name


class SentMessages(models.Model):
    customer = models.ForeignKey('Customer', null=False )
    delang_message_id = models.IntegerField(null=False) # will log 0 for failures. todo: need monitoring for 0's
    raw_message = models.CharField(max_length=2000)
    message = models.ForeignKey('Message', null=False)
    date_sent = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='Attempting')

    def __self__(self):
        return self.customer, self.message


class Status(models.Model):
    status_name = models.CharField(max_length=200)

    def __str__(self):
        return self.id, self.status_name


class NotificationSetting(models.Model):
    setting = models.CharField(max_length=200)

    def __str__(self):
        return self.setting


class Store(models.Model):
    store_name = models.CharField(max_length=200)
    store_number = models.CharField(max_length=20, default='TEST')
    street = models.CharField(max_length=200, default='TEST')
    state = models.CharField(max_length=20, default='TX')
    zip_code = models.CharField(max_length=15, default= '55555')
    phone_number = models.CharField(max_length=12, default='')
    api_key = models.CharField(max_length=200, default='8dba905330fa4d5a9b5193c4cedb540c')

    def __str__(self):
        return self.store_name


    # question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # auto_increment_id = models.AutoField(primary_key=True)

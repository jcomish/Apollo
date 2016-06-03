from django import forms
from django.forms import ModelForm
from .models import Customer
from django.utils.translation import ugettext_lazy as _
from . import services
from .models import SentMessages


class CustomerForm(ModelForm):
        class Meta:
            model = Customer
            widgets = {'store': forms.HiddenInput(), 'user_id': forms.HiddenInput(), 'account_id': forms.NumberInput()}
            exclude = ('create_date', 'status', 'verification_code', 'delang_contact_id' )
            labels = {
                "notification_setting": _('Notifications:'),
            }

        def save_and_email(self):
            message_id = 0

            if self.is_valid():
                customer = self.save(commit=False)
                customer.verification_code = services.get_verification_code()
                message_id = self.data.get('notification_setting')

                # if customer opt-in SMS or both
                # todo: may change depending on email api delang exposes
                if int(message_id) == 2 or (message_id) == 4:
                    customer.delang_contact_id = services.create_contact(customer)
                customer.save()

                if int(customer.id) > 0 and int(customer.delang_contact_id) > 0:
                    services.send_welcome_message(customer)

                return customer.id
            else:
                return 0

        def update_and_email(self, customer_id):
            if self.is_valid():
                customer = Customer.objects.get(pk=int(customer_id))
                customer.last_name = self.data.get('last_name')
                customer.first_name = self.data.get('first_name')
                customer.phone_number = self.data.get('phone_number')
                customer.account_id = self.data.get('account_id')
                customer.email_address = self.data.get('email_address')
                # check old notification settings did it change?
                customer.notification_setting_id = self.data.get('notification_setting')
                customer.save()

                if int(customer.id) > 0 and int(customer.delang_contact_id) > 0:

                    # check to see if welcome message has been sent
                    try:
                        SentMessages.objects.get(customer_id=customer.id, message_id=1, delang_message_id__gt=0)
                    except SentMessages.DoesNotExist:
                        services.send_welcome_message(customer)

                return customer.id
            else:
                return 0


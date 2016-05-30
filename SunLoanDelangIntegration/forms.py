from django import forms
from django.forms import ModelForm
from .models import Customer
from django.utils.translation import ugettext_lazy as _
from . import services


class CustomerForm(ModelForm):
        class Meta:
            model = Customer
            widgets = {'store': forms.HiddenInput(), 'user_id': forms.HiddenInput(), 'account_id': forms.NumberInput()}
            exclude = ('create_date', 'status', 'verification_code', 'delang_contact_id' )
            labels = {
                'messagetype': _('Notifications:'),
            }

        # not used todo: remove
        def save_and_email(self):
            if self.is_valid():
                customer = self.save(commit=False)
                customer.verification_code = services.get_verification_code()
                customer.delang_contact_id = services.create_contact(customer)
                customer.save()
                return customer.id
            else:
                return 0


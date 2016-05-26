from django import forms
from django.forms import ModelForm
from .models import Customer
from django.utils.translation import ugettext_lazy as _


class CustomerForm(ModelForm):

        class Meta:
            model = Customer
            widgets = {'store': forms.HiddenInput(), 'user_id': forms.HiddenInput(), 'account_id': forms.NumberInput()}
            exclude = ('create_date', 'status', )
            labels = {
                'messagetype': _('Notifications:'),
            }

        # not used todo: remove
        def save_and_email(self):
            if self.is_valid():
                contact = self.save(commit=False)
                contact.answered = False
                contact.save()
                return contact.id
            else:
                return 0


#class CustomerForm(forms.Form):
    # first_name = forms.CharField(label='First Name', max_length=100, required='true')
    # last_name = forms.CharField(label='Last Name', max_length=100,required='true')
    # account_id = forms.CharField(label='Account ID', max_length=100)
    # email = forms.CharField(label='Email Address', max_length=100)
    # email_opt_in = forms.BooleanField()
    # phone_number = forms.CharField(label='Phone Number', max_length=100)
    # sms_opt_in = forms.BooleanField()
    # message = forms.CharField(label='Message', max_length=500)
    # opt_out_of_all_notifications_ = forms.BooleanField()

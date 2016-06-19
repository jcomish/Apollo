from django import forms


class SMSForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    phone_number = forms.CharField(label='Phone Number', max_length=100)
    message = forms.CharField(label='Message', max_length=500)


class EmailForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    phone_number = forms.CharField(label='Phone Number', max_length=100)
    message = forms.CharField(label='Message', max_length=500)
    subject = forms.CharField(label='Subject', max_length=500)
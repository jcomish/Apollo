from UserProfile.models import Employee
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.http import HttpResponseRedirect
from SunLoanDelangIntegration import sms
from SunLoanDelangIntegration import email
from .forms import SMSForm
from .forms import EmailForm


# todo - lockdown to admins
@login_required
@user_passes_test(lambda u: u.groups.filter(name='employee').count() == 1)
def index(request):
    if Employee.objects.filter(user_id=request.user.id).exists():
        employee = Employee.objects.get(user_id=request.user.id)
    else:
        employee = ''

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        if request.POST['action'] == 'Submit SMS':

        # create a form instance and populate it with data from the request:
            form = SMSForm(request.POST)
        # check whether it's valid:
            if form.is_valid():
                name = form.cleaned_data['your_name']
                mySMS = sms.SMS()
                mySMS.message = form.cleaned_data['message']
                mySMS.phoneNumber = form.cleaned_data['phone_number']
                mySMS.send()

                return HttpResponseRedirect('/test/?id=' + str(mySMS.messageId))
                # do this
        elif request.POST['action'] == 'Submit Email':
            email_form = EmailForm(request.POST)
            # do that
            if email_form.is_valid():
                name = email_form.cleaned_data['your_name']
                myEmail = email.Email()
                myEmail.message = email_form.cleaned_data['message']
                myEmail.email_address = email_form.cleaned_data['email_address']
                myEmail.subject = email_form.cleaned_data['subject']
                myEmail.send()

                return HttpResponseRedirect('/test/?id=' + str(myEmail.messageId))

    else:
        form = SMSForm()
        email_form = EmailForm()

        context = {
            'employee': employee, 'form': form, 'email_form': email_form}

    return render(request, 'test.html', context)
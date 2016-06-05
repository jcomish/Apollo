import sys
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from UserProfile.models import Employee
from django.contrib.auth.models import Group
from SunLoanDelangIntegration.models import Store
from SunLoanDelangIntegration.models import NotificationSetting
from SunLoanDelangIntegration.models import Status
from SunLoanDelangIntegration.models import Message
User = get_user_model()

# notes: CreateSuperUser - Import Stores - Import Users


def import_users(request):
    write = ''
    users = [
        ('test_employee', 'Test@123!', 'user1@example.com', 'employee', '1'),
        ('test_nonemployee', 'Test@123!', 'user2@example.com', 'nonemployee', '2'),
    ]

    # add superuser logged into employee class so that they can access site
    if Group.objects.filter(name='employee').exists():
        g = Group.objects.get(name='employee')
        g.user_set.add(request.user)
    else:
        g = Group.objects.create(name='employee')
        g.user_set.add(request.user)

    if Employee.objects.filter(user_id=request.user.id).exists() == False:
        employee = Employee.objects.create(user_id=request.user.id, store_id=1)
        employee.save()

    for username, password, email, group, store_id in users:
        if User.objects.filter(username=username).exists():
            write = 'end' # todo: will convert to array and store info per user
        else:
            try:
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.save()
                assert authenticate(username=username, password=password)

                employee = Employee.objects.create(user_id=user.id, store_id=store_id)
                employee.save()

                if Group.objects.filter(name=group).exists():
                    g = Group.objects.get(name=group)
                    g.user_set.add(user)
                else:
                    g = Group.objects.create(name=group)
                    g.user_set.add(user)

                write = "success"
            except:
                write = str(format(username, sys.exc_info()[1]))
    return write


def import_stores():
    write = ''
    stores = ['Test Store 1', 'Test Store 2', ]

    for store_name in stores:
        if Store.objects.filter(store_name=store_name).exists():
            write = 'end' # todo: will convert to array and store info per user
        else:
            try:
                store = Store.objects.create(store_name=store_name)
                store.save()

                write = "success"
            except:
                write = "error"
    return write


def import_messages():
    write = ''
    messages = {'Welcome': 'Welcome to Sun Loan Notifications. Please call your Loan Coordinator at XXX-XXXX and give' \
                ' them this verification code: ZZZZ', 'Payment Due': 'Please Contact XXXXX in order to make a payment today',
                'Refinance Reminder': 'Refinance today', 'Former Borrower Message': 'As a valued customer, we are offering XXXX'}

    for name in messages:
        if Message.objects.filter(name=name).exists():
            write = 'end' # todo: will convert to array and store info per user
        else:
            try:
                msg = Message.objects.create()
                msg.name = name
                msg.verbiage = messages[name]
                msg.save()
                write = "success"
            except:
                write = "error"
    return write


def import_statuses():
    write = ''
    statuses = ['New Customer', 'Awating Verification', 'Verified', ]

    for status in statuses:
        if Status.objects.filter(status_name=status).exists():
            write = 'end' # todo: will convert to array and store info per user
        else:
            try:
                status = Status.objects.create(status_name=status)
                status.save()

                write = "success"
            except:
                write = "error"
    return write


def import_notification_settings():
    write = ''
    notification_settings = ['Opt-Out of Notifications', 'Opt-In to SMS', 'Opt-In to Email', 'Opt-In to SMS and Email', ]

    for setting in notification_settings:
        if NotificationSetting.objects.filter(setting=setting).exists():
            write = 'end' # todo: will convert to array and store info per user
        else:
            try:
                msg = NotificationSetting.objects.create(setting=setting)
                msg.save()

                write = "success"
            except:
                write = "error"
    return write

import sys
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from UserProfile.models import Employee
from django.contrib.auth.models import Group
from SunLoanDelangIntegration.models import Store
from SunLoanDelangIntegration.models import MessageType

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


def import_message_types():
    write = ''
    msg_types = ['Opt-Out of Notifications', 'Opt-In to SMS', 'Opt-In to Email', 'Opt-In to SMS and Email', ]

    for type in msg_types:
        if MessageType.objects.filter(type=type).exists():
            write = 'end' # todo: will convert to array and store info per user
        else:
            try:
                msg = MessageType.objects.create(type=type)
                msg.save()

                write = "success"
            except:
                write = "error"
    return write

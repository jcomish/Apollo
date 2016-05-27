import sys
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from UserProfile.models import Employee
from django.contrib.auth.models import Group
from SunLoanDelangIntegration.models import Store
from SunLoanDelangIntegration.models import MessageType


User = get_user_model()
Employee = Employee()
# Store = Store()
MessageType = MessageType()


#  Update the users in this list.
#  Each tuple represents the username, password, and email of a user.
def import_users():
    write = ''
    users = [
        ('test_employee', 'Test@123!', 'user1@example.com', 'employee',),
        ('test_nonemployee', 'Test@123!', 'user2@example.com', 'nonemployee',),
    ]

    for username, password, email, group in users:
        if User.objects.filter(username=username).exists():
            write = 'end' # todo: will convert to array and store info per user
        else:
            try:
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.save()
                assert authenticate(username=username, password=password)

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


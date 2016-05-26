import sys
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from UserProfile.models import Employee
from django.contrib.auth.models import Group

User = get_user_model()


#  Update the users in this list.
#  Each tuple represents the username, password, and email of a user.
def import_users():
    write = ''
    users = [
        ('test_employee111', 'Test@123!', 'user1_911@example.com', 'employee',),
        ('test_nonemployee111', 'Test@123!', '1user_011@example.com', 'nonemployee',),
    ]

    for username, password, email, group in users:
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


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
        ('user_2', 'phgzHpXcnJ', 'user_4@example.com', 'employee',),
        ('user_3', 'ktMmqKcpJw', 'user_5@example.com', 'employee',),
    ]

    g = Group.objects.get(name='employee')


    for username, password, email, group in users:
        try:
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.save()
            assert authenticate(username=username, password=password)

            g.user_set.add(user)

            write = "success"
        except:
            write = str(format(username, sys.exc_info()[1]))
    return write


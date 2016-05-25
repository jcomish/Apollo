from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(User, unique=True)
    store = models.ForeignKey('SunLoanDelangIntegration.Store')

# Create student instance on access - very useful if you plan to always have a Student obj associated with a User object anyway
User.student = property(lambda u: Employee.objects.get_or_create(user=u)[0])

# from django.db import models
# from django.contrib.auth.models import User
#
#
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     store = models.ForeignKey('SunLoanDelangIntegration.Store')
#
# User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
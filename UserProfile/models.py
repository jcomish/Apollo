from django.db import models
from django.contrib.auth.models import User
from SunLoanDelangIntegration import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    store = models.ForeignKey('SunLoanDelangIntegration.Store')

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
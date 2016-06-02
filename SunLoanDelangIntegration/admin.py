from django.contrib import admin
from .models import Customer
from .models import Store
from .models import NotificationSetting

admin.site.register(NotificationSetting)
admin.site.register(Store)
admin.site.register(Customer)

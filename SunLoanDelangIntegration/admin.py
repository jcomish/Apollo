from django.contrib import admin
from .models import Customer
from .models import Store
from .models import MessageType

admin.site.register(MessageType)
admin.site.register(Store)
admin.site.register(Customer)

from django.db import models


class Customers(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    email_address = models.CharField(max_length=200)
    account_id = models.IntegerField(default=0)
    store_id = models.IntegerField(default=0)
    status_id = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    messagetype_id = models.IntegerField(default=0)
    create_date = models.DateTimeField(auto_now_add=True)

class Statuses(models.Model):
        status_name = models.CharField(max_length=200)

class MessageTypes(models.Model):
        type = models.CharField(max_length=200)

class Stores(models.Model):
        store_name = models.CharField(max_length=200)




    #question = models.ForeignKey(Question, on_delete=models.CASCADE)
    #auto_increment_id = models.AutoField(primary_key=True)

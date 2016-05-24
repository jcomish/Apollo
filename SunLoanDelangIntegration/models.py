from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    email_address = models.EmailField()
    account_id = models.IntegerField(default=0)
    store = models.ForeignKey('Store')
    status_id = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    messagetype = models.ForeignKey('MessageType')
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id


class Status(models.Model):
    status_name = models.CharField(max_length=200)

    def __str__(self):
        return self.status_name


class MessageType(models.Model):
    type = models.CharField(max_length=200)

    def __str__(self):
        return self.type


class Store(models.Model):
    store_name = models.CharField(max_length=200)

    def __str__(self):
        return self.store_name




    #question = models.ForeignKey(Question, on_delete=models.CASCADE)
    #auto_increment_id = models.AutoField(primary_key=True)

from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    email_address = models.EmailField()
    account_id = models.IntegerField(default=0)
    store = models.ForeignKey('Store', default=1)
    status = models.ForeignKey('Status', default=1)
    user_id = models.IntegerField(default=0)
    messagetype = models.ForeignKey('MessageType', default=1)
    verification_code = models.IntegerField(default=0)
    delang_contact_id = models.IntegerField(default=0)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name, self.last_name, self.email_address


class Status(models.Model):
    status_name = models.CharField(max_length=200)

    def __str__(self):
        return self.id, self.status_name


class MessageType(models.Model):
    type = models.CharField(max_length=200)

    def __str__(self):
        return self.type


class Store(models.Model):
    store_name = models.CharField(max_length=200)
    api_key = models.CharField(max_length=200, default='8dba905330fa4d5a9b5193c4cedb540c')


    def __str__(self):
        return self.store_name




    #question = models.ForeignKey(Question, on_delete=models.CASCADE)
    #auto_increment_id = models.AutoField(primary_key=True)

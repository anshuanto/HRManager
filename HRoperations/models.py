from django.db import models

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    position = models.CharField(max_length=100)
    salary = models.CharField(max_length=10,default=1000)
    phone_number = models.CharField(max_length=15)
    passport_expiry_date = models.DateField()
    brp_expiry_date = models.DateField()
    passport_document = models.FileField(upload_to='documents/passport/')
    brp_document = models.FileField(upload_to='documents/brp/')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


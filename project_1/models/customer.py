from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    phone_number = models.CharField(max_length=20,blank=True)

    def __str__(self):
        return self.name
    class Meta:
        app_label = 'core'
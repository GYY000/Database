from django.db import models

# Create your models here.
class User(models.Model):
    uid=models.IntegerField()
    user_name=models.CharField(max_length=30)
    password=models.CharField(max_length=30)
    register_date=models.DateField()
    profile_photo=models.BinaryField(null=True,blank=True)


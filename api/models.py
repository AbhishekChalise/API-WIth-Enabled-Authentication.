from django.db import models
from account.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Student(models.Model):
    user = models.ForeignKey(User , on_delete= models.SET_NULL, null = True , blank= True)
    #name = models.CharField(max_length = 100)
    roll = models.IntegerField(unique=True)
    city = models.CharField(max_length = 100)
    is_deleted = models.BooleanField(default = False)
    

    # @receiver(post_save, sender  = User) 
    # def create_student(sender , instance , created , **kwargs):
    #     if created:
    #         Student.objects.create(user = instance , name = instance.name , city = "Default City" , roll = 1)


# Created_by , Updated_by etc.
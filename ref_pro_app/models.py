from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    desc=models.TextField(max_length=500)
    phonenumber=models.IntegerField()

    def __str__(self):
        return self.name
    

class Students(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Demo Done", "Demo Done"),
        ("Registration Done", "Registration Done"),
        ("Admission Confirmed", "Admission Confirmed"),
        ("Cancelled", "Cancelled"),
    ]
    COURSE_CHOICES = [
        ("Data Science", "Data Science"),
        ("Data Analytics", "Data Analytics"),
        ("Web Development", "Web Development"),
        ("Business Analytics", "Business Analytics"),
        ("Machine Learning", "Machine Learning"),
        ("Artificial Intelligence", "Artificial Intelligence"),
        ("Other", "Other"),
    ]

    
    name=models.CharField(max_length=50)
    course=models.CharField(max_length=200, choices=COURSE_CHOICES, default="Data Analytics")
    phonenumber=models.IntegerField(unique=True)
    alternatenumber = models.IntegerField(null=True, blank=True, default=0)
    email=models.EmailField(default="")
    remarks=models.TextField(max_length=300, default="")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")
    referer=models.CharField(max_length=50, default=User)
    #referer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


# Bank Details
class Withdraw(models.Model):
    STATUS_CHOICES = [
        ("Verification Pending", "Verification Pending"),
        ("Verified", "Verified"),
        ("Cancelled", "Cancelled"),
    ]
   
    
    account_holder_name = models.CharField(max_length=50)
    account_number = models.BigIntegerField()
    phonenumber=models.IntegerField()
    bankname=models.CharField(max_length=50)
    branch=models.CharField(max_length=50)
    ifsc_code=models.CharField(max_length=50)
    pannumber=models.CharField(max_length=50)
    cancelled_cheque = models.FileField(upload_to='cancelled_cheques/', null=True, blank=True)
    remarks=models.TextField(max_length=300, default="")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Verification Pending")
    referer=models.CharField(max_length=50, default=User)
    

    def __str__(self):
        return self.account_holder_name
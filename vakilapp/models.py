from django.db import models
from datetime import datetime
from django.contrib.auth.models import User,AbstractUser

# Create your models here.
class customer(models.Model):

    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    Name=models.CharField(max_length=122)
    Email=models.CharField(max_length=122)
    Phone=models.CharField(max_length=20)
    Subject=models.CharField(max_length=100)
    Message=models.CharField(max_length=1000)
    Date=models.DateField(null=True, default=None)

    def __str__(self):
        return self.Name
    
    class Meta:
        ordering = ['-id']
    
class Team_Member(models.Model):

    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    Image=models.ImageField(upload_to='Team_Photo')
    Name=models.CharField(max_length=122 ,null=True)
    Qualification=models.CharField(max_length=122 ,null=True)
    Description=models.CharField(max_length=1000 ,null=True)
    Email=models.CharField(max_length=122 ,null=True) 

    def __str__(self):
        return self.Name
    
class Appointment_schedule(models.Model):

    sc_name=models.CharField(max_length=122 ,null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.sc_name     

class Appointment(models.Model):

    Name=models.CharField(max_length=122 ,null=True)
    Email=models.CharField(max_length=122)
    Phone=models.CharField(max_length=20)
    Date=models.DateField(null=True, default=None)
    Subject=models.CharField(max_length=100)
    schedule=models.ForeignKey(Appointment_schedule,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.Name
    
class Blog(models.Model):

    Image=models.ImageField(upload_to='Blog_Photo')
    Title=models.CharField(max_length=122 ,null=True)
    editor=models.CharField(max_length=122 ,null=True)
    date_blog=models.DateField()
    para=models.TextField()
    views_count=models.IntegerField(default=0)
    comment_count=models.IntegerField(default=0)

    def __str__(self):
        return self.Title
    

class blog_subscribers(models.Model):

    Name=models.CharField(max_length=122 ,null=True)
    Email=models.CharField(max_length=122,default=None)
    Date=models.DateField(null=True, default=None)
    
    
class comment(models.Model):

    reply_blog=models.ForeignKey(Blog,on_delete=models.CASCADE)
    Name=models.CharField(max_length=122 ,null=True)
    Email=models.CharField(max_length=122,default=None)
    comment_text=models.TextField()
    Date=models.DateField(null=True, default=None)


class IPAddress(models.Model):
    ip_address = models.CharField(max_length=100)
    timestamp = models.DateTimeField()   


class IPAddress_blog(models.Model):
    ip_address = models.CharField(max_length=100)
    timestamp = models.DateTimeField()   
    Blog_id = models.ForeignKey(Blog,on_delete=models.CASCADE)


class notification(models.Model):

    Section_name=models.CharField(max_length=122 ,null=True)
    noti_text=models.CharField(max_length=122,default=None)
    noti_url=models.CharField(max_length=122,default=None)
    Date=models.DateField(null=True, default=None)



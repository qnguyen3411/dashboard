import string
import re
import datetime
from django.db import models
# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def info_validation(self, 
                        postData, 
                        check_all=False, 
                        name_only=False,
                        email_only=False,
                        password_only=False,
                        birthday_only=False):
        errors = {}
        try:
            if name_only or check_all:
                if len(postData['first_name']) < 2 :
                    errors['first_name_length'] = "First name must be 2 characters or more"
                elif not postData['first_name'].isalpha():
                    errors['first_name_noalpha'] = "First name must consist of only characters"
                
                if len(postData['last_name']) < 2 :
                    errors['last_name_length'] = "Last name must be 2 characters or more"
                elif not postData['last_name'].isalpha():
                    errors['last_name_noalpha'] = "Last name must consist of only characters"
            
            if email_only or check_all:
                #If empty/invalid format
                if len(postData['email']) < 1 :
                    errors['email_length'] = "Email must not be empty"
                elif not EMAIL_REGEX.match(postData['email']):
                    errors['email_invalid']= "Invalid email address"
                #If already in database
                else:
                    match = self.filter(email=postData['email'])
                    if len(match):
                        errors['email_match'] = "Email is already in database"
            
            if password_only or check_all:
                if len(postData['password']) < 8:
                    errors['password_short'] = "Password must be at least 8 characters"
                elif postData['password'] != postData['confirm']:
                    errors['confirm_wrong'] = "Password must match password confirm"
            
            if birthday_only or check_all:
                try:
                    birthday = datetime.date(
                        month=int(postData['month']),
                        day=int(postData['day']),
                        year=int(postData['year']))
                    if datetime.date.today().year - birthday.year < 13:
                        errors['invalid_age'] = "You must be at least 13 to hang out in this club"
                except ValueError:
                    errors['invalid_birthday'] = "Invalid birthday"
        except KeyError:
            errors['invalid_form'] = "Invalid Form"
        return errors



class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=255)
    birthday = models.DateField()
    user_level = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class Message(models.Model):
    content = models.TextField()
    sender = models.ForeignKey(User, related_name="sent_messages")
    receiver = models.ForeignKey(User, related_name="received_messages")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    content = models.TextField()
    commenter = models.ForeignKey(User, related_name="comments")
    message = models.ForeignKey(Message, related_name= "comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


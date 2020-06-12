from __future__ import unicode_literals
from django.db import models
import bcrypt, re

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['fname'] = "First name MUST BE at least 2 characters!"
        if len(postData['last_name']) < 3:
            errors['lname'] = "Last name MUST BE at least 3 characters!"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):          
            errors['emails'] = "Email is NOT invalid!"
        if len(postData['password']) < 5:
            errors['pword'] = "Password MUST consist of at least 5 characters!"
        if postData['password'] != postData['confirm_password']:
            errors['pword'] = "Password and Confirm Password DO NOT match!"
        return errors
    def login_validator(self,postData):
        errors = {}
        if len(postData['email']) < 3:
            errors['email'] = "Sorry, Incorrect Email was provided!"
        if len(postData['password']) < 8:
            errors['pword'] = "Sorry, Incorrect Password was provided!"
        return errors

class WishManager(models.Manager):
    def wish_validator(self, postData):
        errors = {}
        if len(postData['item']) < 3:
            errors['item'] = "A Wish Must Consist of at Least 3 Characters!"
        if len(postData['description']) < 3:
            errors['desc'] = "A Description Must Be Provided!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Wish(models.Model):
    item = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    granted = models.BooleanField(null=True)
    creator = models.ForeignKey(User,related_name='wishes',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()


    
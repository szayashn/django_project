from __future__ import unicode_literals
from django.db import models
from datetime import date
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if len(postData['f_name']) < 1:
            errors["f_name"] = "First name must be at least 2 characters"
        if len(postData['l_name']) < 1:
            errors["l_name"] = "Last name must be at least 2 characters"
        if not postData['f_name'].isalpha():
            errors["f_name_l"] = "First name must contain only alphabet letters"
        if not postData['l_name'].isalpha():
            errors["l_name_l"] = "Last name must contain only alphabet letters"
        if not(re.search(regex,postData['email'])):
            errors["email"] = "Please enter a valid email address"
        if User.objects.filter(email = postData['email']):
            errors["email"] = "Sorry, email already exists"
        if len(postData['b_day']) == 10:
            if calculate_age(postData['b_day']) < 12:
                errors["b_day"] = "You are too young for this web site, plese comeback when you will be 13"
        if len(postData['password']) < 7:
            errors["password"] = "Passwords must be at least 8 characters"
        elif not postData['password'] == postData['c_password']:
                errors["password"] = "Passwords do not match"
        return errors

    def login_validator(self, postData):
        errors = {}
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if not(re.search(regex,postData['login'])):
            errors["login"] = "Please enter a valid email address"
        if len(postData['password']) < 7:
            errors["password"] = "Incorrect password"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    email = models.CharField(max_length=225)
    password = models.CharField(max_length=100)
    birthday = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()  

class Message(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, related_name="messages")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, related_name="comments")
    message = models.ForeignKey(Message, related_name="messages")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def calculate_age(born):
    today = date.today()
    born = born.split('-')
    return today.year - int(born[0]) - ((today.month, today.day) < (int(born[1]), int(born[2])))
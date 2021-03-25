from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validations(self, postData):
        errors = {}
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Not a valid email address"

        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name should be at least 2 characters"

        if len(postData['password']) < 7:
            errors['password'] = "Password should be at least 8 characters"
        if not len(postData['password']) == len(postData['confirm_password']):
            errors['password'] = "Passwords don't match"
        email_exists= User.objects.filter(email=postData['email']).exists()
        if (email_exists):
            errors['email'] = "Email already exists"
        
        return errors
        
    def login_validations(self, postData):
        errors = {}
        email_exists= User.objects.filter(email=postData['email2']).exists()
        if not (email_exists):
            errors['email2'] = "failed to login"
            
        user = User.objects.get(email=postData['email2'])
        

        if not bcrypt.checkpw(postData['password2'].encode(), user.password.encode()):
            errors['password2'] = "failed to login"
            
        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return f"first_name: {self.first_name} last_name: {self.last_name} email: {self.email} password: {self.password}"
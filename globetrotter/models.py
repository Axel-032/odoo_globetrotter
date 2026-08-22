from django.db import models
from django.contrib.auth.hashers import make_password, check_password
 
 
class User(models.Model):
    """
    Plain model matching the signup/login form fields:
    Full Name, Email Address, Password, and Terms & Conditions agreement.
    (Confirm Password and Remember Me are not stored — handled in the form/view.)
    """
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    agreed_to_terms = models.BooleanField(default=False)
    terms_agreed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
 
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
 
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
 
    def __str__(self):
        return self.email
from django.db import models
from account.models import User
from datetime import timedelta
from django.utils.timezone import now
import uuid


class CustomToken(models.Model):
    user = models.OneToOneField(User , on_delete= models.SET_NULL , related_name="custom_token_foreignkey", null = True) # Import User Model
    token = models.UUIDField(max_length = 255 , default= (uuid.uuid4) , unique = True ) # Generate a token
    created_at = models.DateTimeField(auto_now_add=True) # Token Created Time 
    expires_at = models.DateTimeField(default= now() + timedelta(minutes=15)) # Token Expiry Time

    def is_valid(self):
        # Check wheater the token is valid or not
        return now() < self.expires_at
    








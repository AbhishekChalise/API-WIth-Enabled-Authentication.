from Tokens.models import CustomToken
import uuid
from django.utils.timezone import now,timedelta


def create_custom_token(user):
    try:
        token , created = CustomToken.objects.get_or_create(user = user)
        print("This is the token Custom Genereated token: ",token)
        print(created)
        if not created:
            token.token =  uuid.uuid4()
            token.expires_at = now()+timedelta(minutes=15)
            token.save()
            return token.token
    except CustomToken.DoesNotExist:
        print("TOken Does NOt Exists")

def validate_custom_token(token_str):
    try:
        token = CustomToken.objects.filter(token = token_str).last()
        if token.is_valid():
            return token.user
    except CustomToken.DoesNotExist:
        print("Token DoesNot Exists , It may have been Destroyed because of the timeout!")
        return None
    


    







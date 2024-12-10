# from rest_framework import serializers
# from api.models import Student

# # We are going to implement the validator class.
# # In this start_with_r method we have added a argument where the value hold the value
# # and value[0] means the name so we have implemented the view level validation.

# def start_with_r(value):
#     if value[0].lower()!= 'r':
#         raise serializers.ValidationError("Name should be start with R")

# class StudentSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length = 100)
#     roll = serializers.IntegerField()
#     city = serializers.CharField(max_length = 100)

#     def create(self , validated_data):
#         return Student.objects.create(**validated_data)
    
#     def update(self,instance,validated_data):
#         print(instance.name)
#         instance.name = validated_data.get('name',instance.name)
#         print(instance.roll)
#         instance.roll = validated_data.get('roll',instance.roll)
#         print(instance.city)
#         instance.city = validated_data.get('city',instance.city)
#         instance.save()
#         return instance
    
#     # Field level validation in django:
#     # So here we have implemented field level validation where we check if the value> 200 or not 

#     def validate_roll(self,value):
#         if value >= 200:
#             raise serializers.ValidationError('Seat Full')
#         return value
    
#     # Objet Level Validation.

#     # When we want to validate multiple fields the we implement object level validation by adding a method called validate() to 
#     # Serializer Subclass
#     #  It raises a ValidationError if necessary , or just return the validated issues.

#     # Object Level Validation.
#     def validate(self,data):
#         nm = data.get('name')
#         rl = data.get('roll')
#         ct = data.get('city')

#         if nm.lower() == 'rohit' and  ct.lower() != 'ranchi':
#             raise serializers.ValidationError("City must be Ranchi!!!")
#         return data
    
# # In case of the model serializer its same as the form method in  the django,
# #  


# from rest_framework import serializers
# from api.models import Student
# class StudentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fields = ['id','name','roll','city']
#         read_only_fields = ['name','roll']
#         extra_kwargs = {'name':{'read_only':True}, # The 'name' field is set to be read-only
#                         'city':{'read_only':True}, # The 'city' field is made mandatory
#                         }
        
# fields = '__all__'
# exclude = ['roll']


from charset_normalizer import from_bytes
from django.db import IntegrityError
from rest_framework import serializers
from api.models import Student
from account.models import User
from account.serializers import UserSerializer
from Tokens.utils import create_custom_token,validate_custom_token

class StudentSerializer(serializers.ModelSerializer):
    # This helps us connect StudentSerializer and the UserSerializer in nested Fashion.
    user = UserSerializer() 
    class Meta:
        model = Student
        fields = ['id','roll','city','user']
        # Field level validation in the ModelSerializer class 
        def validate_roll(self,value):
            if value >=200:
                raise serializers.ValidationError('Seat Full')
            return value  
        
        # Object Level Validation (We have implemented object level validation in the  )
        # def validate(self,data):
        #     nm = data.get('name')
        #     ct = data.get('city')
        #     if nm.lower() == 'veeru' and ct.lower() != 'ranchi':
        #         raise serializers.ValidationError('City must be Ranchi')
        #     return data    
        # So create method will be called automatically!!!!.
        # def create(self, validated_data):
        # # Extract user data from the validated data
        #     user_data = validated_data.pop('user', None)
        #     if user_data:
        #         user = User.object.create_user(**user_data)
        #     else:
        #         user = None
        #     # Create the Student object
        #     student = Student.objects.create(user=user, **validated_data)
        #     return student

    # def create(self, validated_data):
    #     user_data = validated_data.pop('user')
    #     try:
    #         user = User.object.create_user(**user_data)
    #         student = Student.objects.create(user=user, **validated_data)
    #         return student
    #     except IntegrityError as e:
    #         raise serializers.ValidationError({"error": "Error creating user or student: " + str(e)})
    
    def create(self, validated_data):
        # Extract user data from the validated data
        user_data = validated_data.pop('user', None)
        if user_data:
            user = User.objects.create_user(**user_data)
        else:
            user = None
        # Create the Student object
        student = Student.objects.create(user=user, **validated_data)
        return student 


# from django.contrib.auth import authenticate
# from django.contrib.auth.hashers import make_password, check_password
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255) # Actually you need to specify this field becaues 
    # Since email is unique and 
    class Meta:
        model = User
        fields = ['email','password'] # Now what happens here is that fields take it directly from 
        # The data base so in data base we have unique  =True , instead we define 
        # email = email = serializers.EmailField()
            
class UserChangePasswordSerializer(serializers.Serializer):
    oldpassword = serializers.CharField(max_length = 255 , style = {'input_type':'password'},write_only = True)
    new_password = serializers.CharField(max_length = 255 , style = {'input_type':'password'},write_only = True)
    confirm_password = serializers.CharField(max_length = 255, style = {'input_type':'password'},write_only = True)
    class Meta:
        model = User
        fields = ['oldpassword','new_password','confirm_password'] # We just Simply first ask the initial password

    def validate(self, attrs):
        user = self.context.get('user')
        oldpassword = attrs.get('oldpassword')
        #hashed_pwd = make_password(oldpassword)
        #print(hashed_pwd)
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if not user.check_password(oldpassword):
            raise serializers.ValidationError("Your old Password is incorrect")
        if oldpassword == password:
            raise serializers.ValidationError("New Password and Old password cannot be same!!!")
        elif password!=password2:
            raise serializers.ValidationError("Password and Confirm Password doesnot match!!!")
        user.set_password(password)
        return attrs

from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,smart_str,DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util
from Tokens.utils import create_custom_token , validate_custom_token
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        #model = User
        fields = ['email']
    
    def validate(self , attrs):
        email = attrs.get('email')
        if User.objects.filter(email = email).exists():
            user = User.objects.get(email = email)
            print("This is the Force bytes code:",force_bytes(user.id))
            print("This is the base 64 encoded code:",urlsafe_base64_encode(force_bytes(user.id)))
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print("Encoded UID",uid)
            token = create_custom_token(user)
            print("Password Reset Token:",token)
            link = 'http://127.0.0.1:8000/studentapi/user-password-reset-view/'+ uid + '/' + str(token)
            print("password Reset Link",link)
            # send Email
            body = 'Click the following link to Reset the Password:' + link
            data = {
                'subject':'Reset Your Password!!!',
                'body':body,
                'to_email': user.email
            }
            Util.send_email(data)

            return attrs
        else:
            raise serializers.ValidationError("Cannot Send you the Email because you are not the registered Email User")
     

class UserResetPasswordSerializer(serializers.Serializer):
    oldpassword = serializers.CharField(max_length = 255 , style = {'input_type':'password'},write_only = True)
    new_password = serializers.CharField(max_length = 255 , style = {'input_type':'password'},write_only = True)
    confirm_password = serializers.CharField(max_length = 255, style = {'input_type':'password'},write_only = True)
    class Meta:
        model = User
        fields = ['oldpassword','new_password','confirm_password'] # We just Simply first ask the initial password

    def validate(self, attrs):
      print("Validation......")
      try:
            # user = self.context.get('user')
        oldpassword = attrs.get('oldpassword')
        #hashed_pwd = make_password(oldpassword)
        #print(hashed_pwd)
        password = attrs.get('new_password')
        password2 = attrs.get('confirm_password')
        uid = self.context.get('uid')
        token = self.context.get('token')
        id = smart_str(urlsafe_base64_decode(uid))
        print(id)
        user = User.objects.get(pk = id)
       # print(user,"This is the user data!!!")
        if not user.check_password(oldpassword):
            raise serializers.ValidationError("Your old Password is incorrect")
        if oldpassword == password:
            raise serializers.ValidationError("New Password and Old password cannot be same!!!")
        elif password!=password2:
            raise serializers.ValidationError("Password and Confirm Password doesnot match!!!")
        if not PasswordResetTokenGenerator().check_token(user,token):
            raise serializers.ValidationError("Cannot Validate the user , There seems to be something wrong with the token!!!!")
        user.set_password(password)
        user.save()
        return attrs
      except DjangoUnicodeDecodeError as identifier:
          PasswordResetTokenGenerator().check_token(user,token) 
          raise serializers.ValidationError('Token is not Valid or Expired!!!')
      
      
# class UserSendRegistrationEmail(serializers.Serializer):
#     email = serializers.EmailField(max_length = 255)
#     class Meta:





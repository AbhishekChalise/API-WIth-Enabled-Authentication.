from rest_framework import serializers
from account.models import User
#from api.models import Student
#from api.serializer import StudentSerializer

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style = {'input_type':'password'}, write_only = True)
    #password = serializers.CharField(style = {'input_type':'password'}, write_only = True)
    class Meta:
        model = User
        fields = ['email','name','password','password2','tc']
        extra_kwargs = {
            'password':{'write_only':True}
         }
    
    # This validation ansd

    def validate(self,data):
        nm = data.get('password')
        ct = data.get('password2')
        if nm != ct:
            raise serializers.ValidationError('Idiot Both Password and Password2 must be same!!!!!')
        return data
        
    def create(self,validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)
    
    

    # def validate(self , attrs):
    #     email = attrs.get('email')
    #     password = attrs.get('password')
    #     user = authenticate(request = self.context.get('request'),email = email,password = password)
    #     if not user:
    #         raise serializers.ValidationError("Invalid login Credential")
    #     return attrs
    





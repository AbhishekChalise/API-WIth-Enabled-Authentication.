from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView,Response
from .serializers import UserSerializer
from .serializers import UserSerializer
from api.serializer import UserLoginSerializer
from django.contrib.auth import authenticate, aauthenticate,login,logout
# Create your views here.

class UserRegistrationView(APIView):
    def post(self , request , format = None):
        print(request.data)
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid(raise_exception= True):
            user = serializer.save()
            return Response({'msg':'Registration SuccessFull'} , status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors , status= status.HTTP_400_BAD_REQUEST)
    

# class UserLoginView(APIView):
#     def post(self,request,format = None):
#         serializer = UserLoginSerializer(data = request.data)
#         if serializer.is_valid(raise_exception = True):
#             email = serializer.data.get('email')
#             password = serializer.data.get('password')
#             print(f'This is the Email:{email} and Password: {password}')
#             user = authenticate(request , username = email , password = password)
#             print(f'This is the user:{user}')
#             if user is not None:
#                 return Response({'msg':'Login Success!!!'},status = status.HTTP_200_OK)
#                 #login(user)
#             else:
#                 return Response({'msg':'Login UnsuccessFull!!!'},status = status.HTTP_401_UNAUTHORIZED)
            
#         #return Response({'msg':'Login Successfull!!!'}, status = status.HTTP_200_OK)

# # Success fully log out the user!!!!.

# class UserLogoutView(APIView):
#     def get(self,request,format = None):
#         logout(request)


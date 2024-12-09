from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse,JsonResponse
from api.models import Student
from .serializer import StudentSerializer
import io
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
#from .cutompermission import MyPermission
from api.serializer import UserLoginSerializer
from django.contrib.auth import authenticate,login,logout
from rest_framework.views import Response
from rest_framework import status
from account.models import User
from api.renderers import UserJsonRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from api.serializer import UserChangePasswordSerializer

# ACCESS_TOKEN_LIFETIME This token for the Access Lifetime ,
# REFRESH_TOKEN_LIFETIME This token is for the process for refreshing the tokens.
# Generate Token Manually.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@method_decorator(csrf_exempt, name='dispatch')  # Disable CSRF for all methods
class StudentView(APIView):
    renderer_classes = [UserJsonRenderer]
    #permission_classes = [IsAuthenticated]
    # This is for the Authentication process where MyPermission is the custom authentication.
    def get(self, request):
        # Handle GET request

        id = request.GET.get('id', None)
        if id is not None:
            try:
                student = Student.objects.get(id=id)
                serializer = StudentSerializer(student)
                json_data = JSONRenderer().render(serializer.data)
                return HttpResponse(json_data, content_type='application/json')
            except Student.DoesNotExist:
                return HttpResponse('{"error": "Student not found"}', content_type='application/json', status=404)

        # Return all students if no ID is provided
        students = Student.objects.filter(is_deleted = False)
        serializer = StudentSerializer(students, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')

    def post(self, request):
        # Handle POST request
        #json_data = request.body
        #stream = io.BytesIO(json_data)
        #python_data = JSONParser().parse(stream)
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)            
            err_data={
            'msg': 'Data Created',
            'token':token
            }
            json_data = JSONRenderer().render(err_data)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json', status=400)

    def put(self, request):
        # Handle PUT request
        print(request.body)
        if not request.body:
            return JsonResponse({'error':'Empty request body'},status = 400)
        try:
            python_data = JSONParser().parse(io.BytesIO(request.body))

        except Exception as e:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        id = python_data.get('id', None)
        print(id)

        if not id:
            print("I am Here !!!!!! inside this not id")
            return HttpResponse('{"error": "ID is required"}', content_type='application/json', status=400)

        try:
            student = Student.objects.get(id=id)
        except Student.DoesNotExist:
            return HttpResponse('{"error": "Student not found"}', content_type='application/json', status=404)

        serializer = StudentSerializer(student, data=python_data , partial = True)
        if serializer.is_valid():
            serializer.save()
            res = {'msg': 'Data Updated!'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json', status=400)


    def delete(self, request):
    # Parse the JSON data from the request body
        if not request.body:
            return JsonResponse({'error': 'Empty request body'}, status=400)

        try:
            python_data = JSONParser().parse(io.BytesIO(request.body))
            student_id = python_data.get('id', None)
            if not student_id:
                return JsonResponse({'error': 'ID is required'}, status=400)

            # Try to find the student and mark them as deleted
            student = Student.objects.filter(pk=student_id).last()
            student.is_deleted = True
            student.save()  # Save the changes to the database
            
            return JsonResponse({'msg': 'Data Deleted!'}, status=200)

        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': 'Invalid JSON or request'}, status=400)

from rest_framework.permissions import AllowAny
from api.cutompermission import IsStudent
class UserLoginView(APIView): 
    permission_classes = [AllowAny]
    #renderer_classes = [UserJsonRenderer] # Its like inheriting the JsonRenderer , we are providing UserJsonRenderer class to the renderer_classes 
    # Which is the proprety of the classes.
    #permission_classes = [IsAuthenticated]
    def post(self,request,format = None):
        serializer = UserLoginSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            print(f'This is the Email:{email} and Password: {password}')
            user = authenticate(request , email = email , password = password)
            # We have created this token but now what we have to do remaining is to validate the token from the server.
            if not IsStudent().has_permission(request,self):
                return Response({"error:" "Only Student can login: "} , status = 403 )
            token = get_tokens_for_user(user)
            str = {
                'msg':'Login Success!!!',
                'token':token
            }
            print(f'This is the user:{user}')
            if user is not None:
                login(request , user)
                return Response(str,status = status.HTTP_200_OK)
            else:
                return Response({'msg':'Login UnsuccessFull!!!'},status = status.HTTP_401_UNAUTHORIZED)
          
        #return Response({'msg':'Login Successfull!!!'}, status = status.HTTP_200_OK)

class LogOutView(APIView):
    def get(self , request , format = None ):
        # Log out the user by creatin the session
        logout(request)
        return Response({'msg':'Logged Out Successfully!!'}, status = status.HTTP_200_OK)
        
class UserChangePasswordView(APIView):
    renderer_classes = [UserJsonRenderer]
    # permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        try:
            # Parse JSON data from request
            json_data = request.body
            stream = io.BytesIO(json_data)
            python_data = JSONParser().parse(stream)
        except Exception as e:
            return JsonResponse({"msg": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)

        # Get user object by ID
        id = python_data.get('id')
        try:
            User_Object = User.objects.get(pk=id)
        except User.DoesNotExist:
            return JsonResponse({"msg": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Initialize serializer with request data
        serializer = UserChangePasswordSerializer(
            data=python_data, context={'user': User_Object}
        )

        if serializer.is_valid():
            # Set new password and save user
            User_Object.set_password(serializer.validated_data['password'])
            User_Object.save()
            return JsonResponse({"msg": "Password changed successfully"}, status=status.HTTP_200_OK)

        # Return validation errors
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from .serializer import SendPasswordResetEmailSerializer

class UserSendPasswordResetView(APIView):
    renderer_classes = [UserJsonRenderer]

    def post(self,request,format = None):
        serializer = SendPasswordResetEmailSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"The Email for password change is successfully send to the user" },status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors , status= status.HTTP_400_BAD_REQUEST)

from .serializer import UserResetPasswordSerializer
class ResetPasswordView(APIView):

    renderer_classes = [UserJsonRenderer]

    def post(self,request,uid,token,format = None):
        serializer = UserResetPasswordSerializer(data = request.data ,   context = {
            "uid":uid,
            "token":token
        })
        if serializer.is_valid():
            return Response({"msg":"Password Successfully Changed"},status = status.HTTP_200_OK)
        else:
            return Response({"msg":"Password Cannot be Changed"} , status  = status.HTTP_404_NOT_FOUND)
        







    
    


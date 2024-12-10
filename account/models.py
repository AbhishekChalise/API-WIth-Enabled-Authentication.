from django.db import models

# Create your models here.

from django.contrib.auth.models import BaseUserManager , AbstractBaseUser


# Custom User Manager.
class UserManager(BaseUserManager):
    def create_user(self, email, name, tc , password = None,password2 = None):
        '''
        Creates and saves a User with the given email,date of birth and password.

        '''
        if not email:
            raise ValueError("User must have an Email Address!!!!")
        
        user = self.model(
            email = self.normalize_email(email),
            name = name,
            tc = tc,
        )

        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self , email , name , tc, password = None):

        user = self.create_user(
            email,
            password=password,
            name = name,
            tc = tc 
        )
        user.is_admin = True
        user.save(using = self._db)
        return user

# Custom User Model
# Here the AbstractBaseUser is the prebuild model and What our UserModel does is it finds this exact model.
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name= 'email address', # This is the email field we describe.
        max_length=255,
        unique = True 
    )
    name = models.CharField(max_length = 200) 
    tc = models.BooleanField()
    is_active = models.BooleanField(default = True)
    is_admin = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ROLE_CHOICES = [
        ('student','Student'),
        ('teacher','teacher'),
        ('admin','Admin'),
    ]
    role = models.CharField(max_length=10,choices = ROLE_CHOICES , default='student', null = True)

    # When we call User.objects then the instance can call UserManager.
    objects = UserManager() # using objects we can call create_user and create_superuser methods.

    USERNAME_FIELD = 'email' # This is the USERNAME_FIELD in this perticular field the email is used instead of the username for verification.
    REQUIRED_FIELDS = ['name' , 'tc',] # This is the required Field where the name and tc are required and obviously the password will also be required

    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj = None):
        "Does the user have a specific permission?"
        # Simplets possible answer: Yes, always
        return self.is_admin  
    
    def has_module_perms(self,app_label):
        "Does the user have permission to view the app 'app_label'"
        # Simplest possible answer: Yes, always
        return True
    
    @property # This property makes the is_staff access like a property not a method.
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    class Meta:
        db_table = 'user'
# We actually didnt specify the that use implemented abstractbaseuser in django , so we must specify it in the settings.py file in django.


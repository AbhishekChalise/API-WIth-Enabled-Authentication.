from django.contrib import admin
from account.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm , UserCreationForm

# Register your models here.
# from account.models import User
#admin.site.register(User)

class UserModelAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the BaseUserAdmin.
    # that reference specific field on auth.User.
    # This list_display,list_filter,fieldsets,add_fieldsets,search_fields,ordering,filter_horizontal are all properties predefined in the BaseUserAdmin 
    # We are just changing the properties values.
    list_display = ('id','email','name','is_admin','tc')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials',{'fields':('email','password')}),
        ('Personal Info',{'fields':('name','tc')}),
        ('Permissions',{'fields':('is_admin',)}),
    )

    add_fieldsets = (
        (None , {
            'classes': ('wide',),
            'fields':('email','name','tc','password1','password2'),
        }),
    )

    search_fields = ('email',)
    ordering = ('email','id')
    filter_horizontal = ()

admin.site.register(User , UserModelAdmin)
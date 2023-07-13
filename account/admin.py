from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from account.models import User

# Register your models here.

class UserModelAdmin(BaseUserAdmin):
    """
    The fields to be used in displaying the User Model.
    These Override the definition on the base UserModelAdmin
    that referance specific fields on auth.User
    
    """
    list_display=["id","email","name","is_admin"]
    list_filter=["is_admin"]
    fieldsets=[
        ("User Credentials",{"fields":["email","password"]}),
        ("Personal info",{"fields":["name"]}),
        ("Permissions",{"fields":["is_admin"]}),

    ]
    

    add_fieldsets=[
        (
            None,
            {
                "classes": ["wide"],
                "fields":["email","name","password1","password2"],
            },
        ),
    ]
    search_fields=["email"]
    ordering=["email","id"]
    filter_horizontal=[]


admin.site.register(User,UserModelAdmin)


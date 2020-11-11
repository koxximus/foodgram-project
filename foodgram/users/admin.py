from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class MyUserAdmin(admin.ModelAdmin):
    list_display = ["first_name", "username", "email"]
    list_filter = ["first_name", "email"]


#admin.site.unregister(User)
#admin.site.register(User, MyUserAdmin)

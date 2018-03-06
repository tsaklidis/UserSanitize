from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from Sanitizer.users.models import SimpleUser


@admin.register(SimpleUser)
class SimpleUserAdmin(admin.ModelAdmin):
    model = SimpleUser
    list_display = ('user', 'email', 'subscribed', 'created_on', 'key_expired')
    search_fields = ('user__email',)


# Add extra fields to default Django User model
class CustomUserAdmin(UserAdmin):

    def __init__(self, *args, **kwargs):
        super(CustomUserAdmin, self).__init__(*args, **kwargs)
        UserAdmin.list_display = list(UserAdmin.list_display) + ['date_joined']
        UserAdmin.list_display = list(UserAdmin.list_display) + ['last_login']


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

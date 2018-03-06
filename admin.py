from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from ..users.models import SimpleUser


@admin.register(SimpleUser)
class SimpleUserAdmin(admin.ModelAdmin):
    model = SimpleUser
    list_display = ('user', 'email', 'subscribed', 'created_on', 'key_info')
    list_filter = ('subscribed',)
    search_fields = ('user__email',)

    def key_info(self, obj):
        if obj.key_expired:
            return 'Yes'
        return 'No'
    key_info.short_description = 'Key expired:'


# Add extra fields to default Django User model
class CustomUserAdmin(UserAdmin):

    def __init__(self, *args, **kwargs):
        super(CustomUserAdmin, self).__init__(*args, **kwargs)
        UserAdmin.list_display = list(UserAdmin.list_display) + ['date_joined']
        UserAdmin.list_display = list(UserAdmin.list_display) + ['last_login']


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

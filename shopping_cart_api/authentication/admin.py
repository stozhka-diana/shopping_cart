from django.contrib import admin

from authentication.models import CustomUser


@admin.register(CustomUser)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name']

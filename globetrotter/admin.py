from django.contrib import admin

from .models import User
 
 
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "agreed_to_terms", "created_at")
    search_fields = ("full_name", "email")
    list_filter = ("agreed_to_terms",)
    readonly_fields = ("password", "created_at")

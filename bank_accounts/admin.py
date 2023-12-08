from django.contrib import admin
from .models import BankAccount


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):

    ordering = ["id"]
    list_display = ('id', 'user_username', 'balance')

    def user_username(self, obj):
        return obj.user.username

    user_username.short_description = 'Username'




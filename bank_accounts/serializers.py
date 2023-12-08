from rest_framework import serializers
from .models import BankAccount
from django.contrib.auth import get_user_model

User = get_user_model()


class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class BankAccountSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = BankAccount
        fields = ['id', 'username', 'email', 'balance']

    def create(self, validated_data):
        user_data = validated_data.pop('user', {})
        username = user_data.get('username')
        email = user_data.get('email')
        user_instance, _ = User.objects.get_or_create(username=username, email=email)
        bank_account_instance = BankAccount.objects.create(user=user_instance, **validated_data)
        return bank_account_instance


class SelfDepositWithdrawSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankAccount
        fields = ['id', 'balance']


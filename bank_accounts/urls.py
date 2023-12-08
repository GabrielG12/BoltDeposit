from django.urls import path
from .views import BankAccountCreateAPIView, SelfDepositWithdrawView


urlpatterns = [
    path('create/', BankAccountCreateAPIView.as_view(), name="bank-account-create"),
    path('operate/<int:pk>/', SelfDepositWithdrawView.as_view(), name="bank-account-self-deposit-withdraw"),
    #path('deposit/<int:id>', BankAccountDepositView.as_view(), name="user-deposit"),
]
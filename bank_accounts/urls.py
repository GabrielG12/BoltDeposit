from django.urls import path
from .views import BankAccountCreateAPIView, WithdrawView, DepositView, AdminBalanceUpdate

urlpatterns = [
    path('create/', BankAccountCreateAPIView.as_view(), name="bank-account-create"),
    path('withdraw/<int:pk>/', WithdrawView.as_view(), name="bank-account-self-deposit-withdraw"),
    path('deposit/<int:id>/', DepositView.as_view(), name="user-deposit"),
    path('admin_balance_update/<int:pk>/', AdminBalanceUpdate.as_view(), name="admin-balance-update"),
]

from .models import BankAccount
from .serializers import BankAccountSerializer
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAccountOwner
from decimal import Decimal


class BankAccountCreateAPIView(generics.CreateAPIView):

    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classe = [IsAuthenticated]


class SelfDepositWithdrawView(generics.UpdateAPIView):

    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [IsAccountOwner]

    def update(self, request, *args, **kwargs):
        amount = Decimal(request.data.get('amount', 0))
        amount_type = request.data.get('amount_type')
        account = self.get_object()

        if amount >= 0 and amount_type in ['deposit', 'withdraw']:
            if amount_type == 'deposit':
                account.balance += amount
                action_message = f"The amount of {amount} was deposited to the account number {account.id}"
            elif amount_type == 'withdraw':
                account.balance -= amount
                action_message = f"The amount of {amount} was withdrawn from the account number {account.id}"

            account.save()
            serializer = self.get_serializer(account)

            response = {
                "Message": action_message,
                "Account information": serializer.data
            }
            return Response(response, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error': 'Invalid amount or operation'}, status=status.HTTP_400_BAD_REQUEST)

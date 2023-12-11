from .models import BankAccount
from .serializers import BankAccountSerializer
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsAccountOwner
from decimal import Decimal
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import NotFound


class BankAccountCreateAPIView(generics.CreateAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Customize the response as needed
        response_data = {
            'Message': 'Bank account created successfully.',
            'Data': serializer.data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class WithdrawView(generics.UpdateAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated, IsAccountOwner]

    def update(self, request, *args, **kwargs):

        # Ensure that the request is properly authenticated
        if not request.auth or not isinstance(request.auth, AccessToken):
            return Response({'error': 'Authentication credentials not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        amount = Decimal(request.data.get('amount', 0))
        account = self.get_object()

        if amount <= account.balance != 0:
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
            return Response({'Error': 'Invalid amount or negative balance status!'}, status=status.HTTP_400_BAD_REQUEST)


class DepositView(generics.UpdateAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated, IsAccountOwner]

    def update(self, request, *args, **kwargs):

        if not request.auth or not isinstance(request.auth, AccessToken):
            return Response({'error': 'Authentication credentials not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        amount = Decimal(request.data.get('amount', 0))

        # Fetch the source account using the source_account_id from the request data
        source_account_id = request.data.get('source_account_id')

        try:
            source_account = BankAccount.objects.get(id=source_account_id)
        except BankAccount.DoesNotExist:
            return Response({'error': 'Source account not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Fetch the target account using the target_account_id from the URL
        target_account_id = request.data.get('target_account_id')

        try:
            target_account = BankAccount.objects.get(id=target_account_id)
        except BankAccount.DoesNotExist:
            return Response({'error': 'Target account not found.'}, status=status.HTTP_404_NOT_FOUND)

        if source_account.balance >= amount > 0:
            source_account.balance -= amount
            target_account.balance += amount
            action_message = f"The amount of {amount} was deposited to the account number {target_account_id}"

            source_account.save()
            target_account.save()

            source_serializer = self.get_serializer(source_account)

            response = {
                "Message": action_message,
                "Your account": source_serializer.data,
            }
            return Response(response, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error': 'Invalid amount or operation'}, status=status.HTTP_400_BAD_REQUEST)


class AdminBalanceUpdate(generics.UpdateAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):

        try:
            target_account = self.get_object()
        except NotFound:
            return Response({'error': 'Target account not found.'}, status=status.HTTP_404_NOT_FOUND)

        if not isinstance(request.auth, AccessToken):
            return Response({'Error': 'Invalid authentication credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_staff:
            return Response({'Error': 'Only admins can proceed with this operation!.'},
                            status=status.HTTP_403_FORBIDDEN)

        amount = Decimal(request.data.get('amount', 0))
        target_account.balance = amount
        target_account.save()
        target_serializer = self.get_serializer(target_account)

        response = {
            "Message": f"The balance of {target_account.user.username} was updated to {amount}",
            "Account Information": target_serializer.data
        }
        return Response(response, status=status.HTTP_202_ACCEPTED)

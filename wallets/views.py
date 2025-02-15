from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from wallets.models import Wallet
from wallets.serializers import WalletOperationSerializer, WalletSerializer


class WalletCreateAPIView(CreateAPIView):
    serializer_class = WalletSerializer


class WalletOperationAPIView(APIView):

    def post(self, request, wallet_uuid, *args, **kwargs):
        try:
            wallet = Wallet.objects.get(id=wallet_uuid)
        except Wallet.DoesNotExist:
            return Response({"error": "По заданным параметрам не удалось найти кошелёк"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = WalletOperationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        operation_type = serializer.validated_data["operationType"]
        amount = serializer.validated_data["amount"]

        if operation_type == "DEPOSIT":
            wallet.balance += amount
        elif operation_type == "WITHDRAW":
            if wallet.balance < amount:
                return Response({"error": "Недостаточно средств"}, status=status.HTTP_400_BAD_REQUEST)
            wallet.balance -= amount

        wallet.save()

        return Response({"message": "Операция прошла успешно", "new_balance": wallet.balance},
                        status=status.HTTP_200_OK)


class WalletBalanceAPIView(APIView):

    def get(self, request, wallet_uuid, *args, **kwargs):
        try:
            wallet = Wallet.objects.get(id=wallet_uuid)
        except Wallet.DoesNotExist:
            return Response({"error": "По заданным параметрам не удалось найти кошелёк"},
                            status=status.HTTP_404_NOT_FOUND)

        return Response({"balance": wallet.balance}, status=status.HTTP_200_OK)

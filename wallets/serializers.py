import decimal

from rest_framework import serializers

from wallets.models import Wallet


class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = "__all__"


class WalletOperationSerializer(serializers.Serializer):
    operationType = serializers.ChoiceField(choices=['DEPOSIT', 'WITHDRAW'])
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=decimal.Decimal('0.01'))


class WalletBalanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = ("balance",)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from wallets.models import Wallet


class WalletTestCase(APITestCase):

    def setUp(self) -> None:
        self.wallet = Wallet.objects.create(balance=1000)

    def test_wallet_create(self):
        url = reverse("wallets:wallet-create")
        data = {"balance": 100}
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(data.get("balance"), "100.00")
        self.assertEqual(len(data.get("id")), 36)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wallet.objects.all().count(), 2)

    def test_wallet_balance(self):
        url = reverse("wallets:wallet-balance", args=(self.wallet.id,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(data.get("balance"), self.wallet.balance)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wallet_balance_deposit(self):
        url = reverse("wallets:wallet-operation", args=(self.wallet.id,))
        data = {"operationType": "DEPOSIT", "amount": 100}
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(data.get("message"), "Операция прошла успешно")
        self.assertEqual(data.get("new_balance"), self.wallet.balance + 100)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wallet_balance_withdraw_success(self):
        url = reverse("wallets:wallet-operation", args=(self.wallet.id,))
        data = {"operationType": "WITHDRAW", "amount": 100}
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(data.get("message"), "Операция прошла успешно")
        self.assertEqual(data.get("new_balance"), self.wallet.balance - 100)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wallet_balance_withdraw_insufficient_funds(self):
        url = reverse("wallets:wallet-operation", args=(self.wallet.id,))
        data = {"operationType": "WITHDRAW", "amount": 1001}
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(data.get("error"), "Недостаточно средств")
        self.assertEqual(self.wallet.balance, 1000)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

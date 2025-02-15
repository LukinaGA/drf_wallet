from django.urls import path

from wallets.views import WalletOperationAPIView, WalletBalanceAPIView, WalletCreateAPIView

urlpatterns = [
    path("api/v1/wallets/<uuid:wallet_uuid>/operation/", WalletOperationAPIView.as_view(), name="wallet-operation"),
    path("api/v1/wallets/<uuid:wallet_uuid>/", WalletBalanceAPIView.as_view(), name="wallet-balance"),
    path("api/v1/wallets/create/", WalletCreateAPIView.as_view(), name="wallet-create"),
]
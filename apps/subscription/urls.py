from django.urls import path
from .views import SubscribeView, UserSubscriptionsView, CancelSubscriptionView, ExchangeRateAPIView

urlpatterns = [
    path('subscribe/', SubscribeView.as_view()),
    path('subscriptions/', UserSubscriptionsView.as_view()),
    path('cancel/', CancelSubscriptionView.as_view()),
    path('exchange-rate/', ExchangeRateAPIView.as_view()),

]

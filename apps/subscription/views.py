from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db import transaction
from .models import Plan, Subscription, ExchangeRateLog
from .serializers import SubscriptionSerializer
import requests
from django.shortcuts import render
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import status

key = settings.EXCHANGE_API_KEY


class BaseAPIView(APIView):
    def success_response(self, message="Your request Accepted", data=None, status_code=status.HTTP_200_OK):
        return Response(
            {"success": True, "message": message, "status": status_code, "data": data or {}},
            status=status_code
        )

    def error_response(self, message="Your request rejected", data=None, status_code=status.HTTP_400_BAD_REQUEST):
        return Response(
            {"success": False, "message": message, "status": status_code, "data": data or {}},
            status=status_code
        )


class SubscribeView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        plan_id = request.data.get("plan_id")
        try:
            plan = Plan.objects.get(id=plan_id)
        except Plan.DoesNotExist:
            return self.error_response("Invalid plan")

        start_date = timezone.now().date()
        end_date = start_date + timezone.timedelta(days=plan.duration_days)

        with transaction.atomic():
            subscription = Subscription.objects.create(
                user=request.user,
                plan=plan,
                start_date=start_date,
                end_date=end_date,
                status="active"
            )
        return self.success_response("Subscription created", SubscriptionSerializer(subscription).data)


class UserSubscriptionsView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subs = Subscription.objects.filter(user=request.user)
        return self.success_response("Subscriptions fetched", SubscriptionSerializer(subs, many=True).data)


class CancelSubscriptionView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sub_id = request.data.get("subscription_id")
        try:
            sub = Subscription.objects.get(id=sub_id, user=request.user)
            sub.status = "cancelled"
            sub.save()
            return self.success_response("Subscription cancelled")
        except Subscription.DoesNotExist:
            return self.error_response("Invalid subscription ID", status_code=404)


class ExchangeRateAPIView(BaseAPIView):
    def get(self, request):
        base = request.GET.get("base", "USD")
        target = request.GET.get("target", "BDT")

        url = f"https://v6.exchangerate-api.com/v6/{key}/latest/{base}"
        r = requests.get(url)
        
        try:
            data = r.json()
        except Exception:
            return self.error_response("Invalid response from exchange rate API")

        rate = data.get("conversion_rates", {}).get(target)
        if rate:
            ExchangeRateLog.objects.create(
                base_currency=base,
                target_currency=target,
                rate=rate
            )
            return self.success_response("Rate fetched", {"rate": rate})
        
        return self.error_response("Rate not found")




def subscription_list(request):
    users = User.objects.all().prefetch_related("subscription_set")
    return render(request, "subscriptions.html", {"users": users})

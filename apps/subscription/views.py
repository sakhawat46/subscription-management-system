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


class SubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        plan_id = request.data.get("plan_id")
        try:
            plan = Plan.objects.get(id=plan_id)
        except Plan.DoesNotExist:
            return Response({"error": "Invalid plan"}, status=400)

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
        return Response(SubscriptionSerializer(subscription).data)

class UserSubscriptionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subs = Subscription.objects.filter(user=request.user)
        return Response(SubscriptionSerializer(subs, many=True).data)

class CancelSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sub_id = request.data.get("subscription_id")
        try:
            sub = Subscription.objects.get(id=sub_id, user=request.user)
            sub.status = "cancelled"
            sub.save()
            return Response({"message": "Cancelled"})
        except Subscription.DoesNotExist:
            return Response({"error": "Invalid ID"}, status=404)

class ExchangeRateAPIView(APIView):
    def get(self, request):
        base = request.GET.get("base", "USD")
        target = request.GET.get("target", "BDT")

        url = f"https://v6.exchangerate-api.com/v6/71d1c36a50bfaa7d66102767/latest/{base}"
        r = requests.get(url)
        data = r.json()

        rate = data["conversion_rates"].get(target)
        if rate:
            ExchangeRateLog.objects.create(
                base_currency=base,
                target_currency=target,
                rate=rate
            )
            return Response({"rate": rate})
        return Response({"error": "Rate not found"}, status=400)



def subscription_list(request):
    users = User.objects.all().prefetch_related("subscription_set")
    return render(request, "subscriptions.html", {"users": users})

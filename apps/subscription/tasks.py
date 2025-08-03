from celery import shared_task
import requests
from .models import ExchangeRateLog
from django.conf import settings


@shared_task
def fetch_usd_to_bdt_rate():
    try:
        key = settings.EXCHANGE_API_KEY
        url = f"https://v6.exchangerate-api.com/v6/{key}/latest/USD"
        response = requests.get(url)
        data = response.json()

        conversion_rates = data.get("conversion_rates", {})
        rate = conversion_rates.get("BDT")

        if rate:
            ExchangeRateLog.objects.create(
                base_currency="USD",
                target_currency="BDT",
                rate=rate
            )
            print("Rate saved:", rate)
        else:
            print("BDT rate not found. Full data:", data)

    except Exception as e:
        print("Error fetching exchange rate:", str(e))

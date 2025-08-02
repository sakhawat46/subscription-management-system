# from celery import shared_task
# import requests
# from .models import ExchangeRateLog

# @shared_task
# def fetch_usd_to_bdt_rate():
#     url = "https://v6.exchangerate-api.com/v6/71d1c36a50bfaa7d66102767/latest/USD"
#     response = requests.get(url)
#     data = response.json()
#     rate = data["conversion_rates"].get("BDT")
#     if rate:
#         ExchangeRateLog.objects.create(
#             base_currency="USD",
#             target_currency="BDT",
#             rate=rate
#         )

from celery import shared_task
import requests
from .models import ExchangeRateLog

@shared_task
def fetch_usd_to_bdt_rate():
    try:
        url = "https://v6.exchangerate-api.com/v6/YOUR_API_KEY/latest/USD"
        response = requests.get(url)
        data = response.json()

        rate = data["conversion_rates"].get("BDT")

        if rate:
            ExchangeRateLog.objects.create(
                base_currency="USD",
                target_currency="BDT",
                rate=rate
            )
    except Exception as e:
        print("Error fetching exchange rate:", str(e))

from django.shortcuts import render

# Create your views here.

# api/views.py
from django.http import JsonResponse
from rest_framework.decorators import api_view
import requests

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

@api_view(['GET'])
def get_candles(request):
    symbol = request.GET.get('symbol', 'BTCUSDT')
    interval = request.GET.get('interval', '1h')
    limit = request.GET.get('limit', 100)

    url = f'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': symbol.upper(),
        'interval': interval,
        'limit': limit
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Преобразуем в структуру для графика: [time, open, high, low, close]
    candles = []
    for entry in data:
        candles.append({
            'time': entry[0] // 1000,  # timestamp в секундах
            'open': float(entry[1]),
            'high': float(entry[2]),
            'low': float(entry[3]),
            'close': float(entry[4]),
        })

    return JsonResponse({'candles': candles}, safe=False)
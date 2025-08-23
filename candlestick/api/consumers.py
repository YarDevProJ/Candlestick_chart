import json
import asyncio
import websockets
from channels.generic.websocket import AsyncWebsocketConsumer


class CandleConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.symbol = self.scope['url_route']['kwargs']['symbol'].upper()
        self.interval = self.scope['url_route']['kwargs']['interval']
        self.pair = f"{self.symbol.lower()}@kline_{self.interval}"

        await self.channel_layer.group_add(
            self.pair,
            self.channel_name
        )
        await self.accept()

        asyncio.create_task(self.start_stream())

    async def disconnect(self, close_code):
        await self.channel_layer.group_discart(
            self.pair,
            self.channel_name
        )

    async def start_stream(self):
        uri = f"wss://stream.binance.com:9443/ws/{self.pair}"
        try:
            async with websockets.connect(uri) as ws:
                while True:
                    try:
                        response = await ws.recv()
                        data = json.loads(response)
                        if data['e'] == 'kline':
                            kline = data['k']
                            is_close = kline['x']
                            candle = {
                                'time': int(kline['t']),
                                'open': float(kline['o']),
                                'high': float(kline['h']),
                                'low': float(kline['l']),
                                'close': float(kline['c']),
                                'closed': is_close
                            }
                            await self.channel_layer.group_send(
                                self.pair,
                                {
                                    'type': 'candle_update',
                                    'candle': candle
                                }
                            )
                    except Exception as e:
                        print("error parsing massage:", e)
        except Exception as e:
            print("websoket connection error:", e)

    async def candle_update(self, event):
        candle = event['candle']
        await self.send(text_data=json.dumps({
            'candle': candle
        }))
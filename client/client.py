import asyncio
import os
import signal
import time
import uuid

from gmqtt import Client as MQTTClient

# gmqtt also compatibility with uvloop  
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


STOP = asyncio.Event()


def on_connect(client, flags, rc, properties):
    print('Connected')
    client.subscribe('TEST/#', qos=0)


def on_message(client, topic, payload, qos, properties):
    print('TOPIC:', topic)
    print('RECV MSG:', payload)


def on_disconnect(client, packet, exc=None):
    print('Disconnected')

def on_subscribe(client, mid, qos, properties):
    print('SUBSCRIBED')

def ask_exit(*args):
    STOP.set()

async def main(broker_host, token):
    client_id = "68d4c956d73e4d89b9090476198765bb"
    client = MQTTClient("client-id")

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe

    # client.set_auth_credentials(token, None)
    await client.connect(broker_host)

    client.publish('screen/register', client_id, qos=1, content_type='json')

    await STOP.wait()
    await client.disconnect()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    host = 'mqtt'
    token = os.environ.get('FLESPI_TOKEN')

    loop.add_signal_handler(signal.SIGINT, ask_exit)
    loop.add_signal_handler(signal.SIGTERM, ask_exit)

    loop.run_until_complete(main(host, token))
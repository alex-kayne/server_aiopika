from aio_pika import connect, Message, DeliveryMode
import yaml
import asyncio
import sys

with open(u'.\\connections\config') as f:
    data_map = yaml.safe_load(f)
    rabbitmq_conn_parametrs = data_map['rabbitmq']


async def main(loop):
    # Perform connection
    connection = await connect(
        rabbitmq_conn_parametrs['rabbitmq_url'], loop=loop
    )
    channel = await connection.channel()
    logs_exchange = await channel.get_exchange("DEV")
    message_body = b" ".join(arg.encode() for arg in sys.argv[1:]) or b'Hello world!'
    message = Message(message_body, delivery_mode=DeliveryMode.PERSISTENT)
    await logs_exchange.publish(
        message,
        routing_key='kan_task'
    )

    print(" [x] Sent 'Hello world!'")
    await connection.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop=loop))

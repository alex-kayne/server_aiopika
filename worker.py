from aio_pika import connect, Message, IncomingMessage
import yaml
import asyncio

with open(u'.\\connections\config') as f:
    data_map = yaml.safe_load(f)
    rabbitmq_conn_parametrs = data_map['rabbitmq']


async def on_message(message: IncomingMessage):
    async with message.process():
        print(" [x] Received message %r" % message)
        await asyncio.sleep(5)
        print(" [X] Done")

async def main(loop):
    # Perform connection
    connection = await connect(
        rabbitmq_conn_parametrs['rabbitmq_url'], loop=loop
    )
    channel = await connection.channel()
    logs_exchange = await channel.get_exchange("DEV")
    await channel.set_qos(prefetch_count=1)
    queue = await channel.declare_queue(exclusive=True)
    print(queue)
    await queue.bind(logs_exchange, routing_key='kek.kan_task')
    await queue.bind(logs_exchange, routing_key='kek.kan_kek')
    await queue.consume(on_message)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main(loop))
    loop.run_forever()
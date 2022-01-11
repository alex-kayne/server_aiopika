import asyncio
import yaml
from user_db import postgres_db
from aio_pika import connect, Message, IncomingMessage, DeliveryMode
from template import rabbitmq_request
import uuid
from datetime import datetime
import json


async def on_message(message: IncomingMessage):
    async with message.process():
        message_body = json.loads(message.body.decode('utf-8'))
        await on_message.postgres_connection.delete('catalogs_data', {'catalog_name': on_message.catalogue_name})
        for record in message_body['params']['data']:
            await on_message.postgres_connection.insert(
                'catalogs_data',
                {'data': json.dumps(record), 'catalog_name': on_message.catalogue_name})
        on_message.message_processed = True


async def main(loop):
    with open(r'..\connections\config') as file:
        data_map = yaml.safe_load(file)
        postgres_conn_parametrs = data_map['postgres']
        rabbitmq_conn_parametrs = data_map['rabbitmq']
    on_message.catalogue_name = catalogue_name = input('Введите название каталога: ').strip()
    on_message.postgres_connection = postgres_connection = postgres_db.Connection(**postgres_conn_parametrs)
    await postgres_connection.connect()
    print(' [X] Подключил постгрю')
    rabbitmq_connection = await connect(rabbitmq_conn_parametrs['rabbitmq_url'], loop=loop)
    print(' [X] Подключил ребит')
    channel = await rabbitmq_connection.channel()
    dev_exchange = await channel.get_exchange('DEV')
    queue = await channel.declare_queue(exclusive=True)
    print(f'Название очереди в ребите - {queue}')
    await queue.bind(dev_exchange, routing_key=f'{catalogue_name}.all_reply')
    request = rabbitmq_request.request
    request['reference_id'] = request['message_id'] = str(uuid.uuid4())
    request['datetime_created'] = str(datetime.now())
    request['object'] = catalogue_name
    message_body = json.dumps(request).encode('utf-8')
    message = Message(message_body, delivery_mode=DeliveryMode.PERSISTENT)
    await dev_exchange.publish(message, routing_key=f'{catalogue_name}.all')
    on_message.message_processed = False
    await queue.consume(on_message)
    while not on_message.message_processed:
        await asyncio.sleep(1)
    await rabbitmq_connection.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))

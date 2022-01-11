import asyncpg
import asyncio
import datetime
import json


# создаю объект класса


class Connection():
    def __init__(self, database, user, password, host, port):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(database=self.database, user=self.user,
                                              password=self.password, host=self.host, port=self.port)

    async def insert(self, table_name, data):
        operand = '%s, '
        data['dt_created'] = data['dt_updated'] = datetime.datetime.now()
        placeholders = ', '.join([f'${i}' for i in range(1, len(data) + 1)])
        columns = ', '.join(data.keys())
        sql = f'''INSERT INTO %s (%s) VALUES (%s);''' % (table_name, columns, placeholders)
        pool = self.pool
        async with self.pool.acquire() as conn:
            #print(f'выполняю инсерт: {sql}')
            await conn.execute(sql, *[json.dumps(data) if isinstance(data, list) else data for data in data.values()])

    async def select(self, table_name, data: dict = None):
        if not data:
            data = {}
        columns = ', '.join(data.keys())
        conditions_string = ''
        for key in data.keys():
            if isinstance(data[key], int):
                conditions_string += f'{key} = {data[key]}' \
                    if list(data.keys()).index(key) == len(data.keys()) - 1 else f'{key} = {data[key]} and '
            elif isinstance(data[key], list):
                values = ', '.join(map(str, data[key]))
                conditions_string += f'{key} in ({values})' if list(data.keys()).index(key) == len(
                    data.keys()) - 1 else f'{key} in {values} and '
            else:
                conditions_string += f'{key} = \'{data[key]}\'' \
                    if list(data.keys()).index(key) == len(data.keys()) - 1 else f'{key} = \'{data[key]}\' and '
        sql = f'''SELECT * FROM %s WHERE %s;''' % (table_name, conditions_string) if len(data.keys()) != 0 \
            else f'''SELECT * FROM %s;''' % (table_name)

        async with self.pool.acquire() as conn:
            #print(f'выполняю селект: {sql}')
            result = await conn.fetch(sql)
        return result

    async def update(self, table_name, data):
        pass

    async def delete(self, table_name, data):
        if not data:
            data = {}
        columns = ', '.join(data.keys())
        conditions_string = ''
        for key in data.keys():
            if isinstance(data[key], int):
                conditions_string += f'{key} = {data[key]}' \
                    if list(data.keys()).index(key) == len(data.keys()) - 1 else f'{key} = {data[key]} and '
            elif isinstance(data[key], list):
                values = ', '.join(map(str, data[key]))
                conditions_string += f'{key} in ({values})' if list(data.keys()).index(key) == len(
                    data.keys()) - 1 else f'{key} in {values} and '
            else:
                conditions_string += f'{key} = \'{data[key]}\'' \
                    if list(data.keys()).index(key) == len(data.keys()) - 1 else f'{key} = \'{data[key]}\' and '
        sql = f'''DELETE FROM %s WHERE %s;''' % (table_name, conditions_string) if len(data.keys()) != 0 \
            else f'''DELETE FROM %s;''' % (table_name)

        async with self.pool.acquire() as conn:
            #print(f'выполняю делит: {sql}')
            result = await conn.fetch(sql)
        return result

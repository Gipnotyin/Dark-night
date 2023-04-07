import asyncio
import pymysql
import aiomysql

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config.config import Config, load_config
from keyboard.keyboard import create_inline_kb


config: Config = load_config('.env')

loop = asyncio.get_event_loop()


async def add_user(id_user, *adata: dict):
    print(adata, 'Add_user')
    try:
        conn = await aiomysql.connect(user=config.database.user,
                                      password=config.database.password, db=config.database.database,
                                      loop=loop)
        cur = await conn.cursor()
        async with conn.cursor() as cur:
            name = adata[0]['name']
            surname = adata[0]['surname']
            group = adata[0]['group']
            photo_id = adata[0]['id_photo']
            course = int(adata[0]['cours'])
            info = adata[0]['info']
            gender = adata[0]['gender']
            find_gender = adata[0]['find_gender']
            age = int(adata[0]['age'])
            print(name, surname, group, photo_id, course, info, gender, find_gender, age)

            add_user_str = f'INSERT INTO users '\
                           f"VALUES({id_user}, %s, %s, %s, %s,"\
                           f"%s, %s, %s, %s, %s, 1, 1);"

            await cur.execute(add_user_str, (name, surname, group, photo_id, course, info, gender,
                                             find_gender, age))
            await conn.commit()

        conn.close()

    except Exception as ex:
        print(ex, "addUser")


def is_user_db(id: int) -> bool:
    try:
        conn = pymysql.connect(host=config.database.host, user=config.database.user, password=config.database.password,
                               database=config.database.database)
        result: str
        with conn.cursor() as cursor:
            user_str = f"SELECT id_user FROM users WHERE id_user={id};"
            cursor.execute(user_str)
            result = cursor.fetchone()

        if result:
            print("f False", result)
            conn.close()
            return True
        else:
            print("f True", result)
            conn.close()
            return False

    except Exception as ex:
        print(ex)


async def delete_user(callback: CallbackQuery):
    try:
        conn = await aiomysql.connect(user=config.database.user, password=config.database.password,
                                      db=config.database.database, loop=loop)
        async with conn.cursor() as cursor:
            user_delete = f"DELETE FROM users WHERE id_user={callback.from_user.id}"
            await cursor.execute(user_delete)
            await conn.commit()
        conn.close()
    except Exception as ex:
        print(ex)


async def output_user(callback: CallbackQuery):
    try:
        conn = await aiomysql.connect(user=config.database.user, password=config.database.password,
                                      db=config.database.database, loop=loop)
        result: str = ""
        async with conn.cursor() as cursor:
            user = f"SELECT * FROM users WHERE id_user={callback.from_user.id};"
            await cursor.execute(user)
            result = await cursor.fetchone()
        return result
    except Exception as ex:
        print(ex)


async def update_user(id_user: int, request: str, *data: dict):
    try:
        conn: aiomysql.connect = await aiomysql.connect(user=config.database.user, password=config.database.password,
                                                        db=config.database.database, loop=loop)
        async with conn.cursor() as cursor:
            match request:
                case 'name':
                    upd_user = 'UPDATE users SET name=%s WHERE id_user=%s'
                case 'photo':
                    upd_user = 'UPDATE users SET photo_id=%s WHERE id_user=%s'
                case 'surname':
                    upd_user = 'UPDATE users SET surname=%s WHERE id_user=%s'
                case 'group':
                    upd_user = 'UPDATE users SET grp=%s WHERE id_user=%s'
                case 'course':
                    upd_user = 'UPDATE users SET cours=%s WHERE id_user=%s'
                case 'info':
                    upd_user = 'UPDATE users SET info=%s WHERE id_user=%s'
                case 'gender':
                    upd_user = 'UPDATE users SET gender=%s WHERE id_user=%s'
                case 'find_gender':
                    upd_user = 'UPDATE users SET findgender=%s WHERE id_user=%s'
                case 'age':
                    upd_user = 'UPDATE users SET age=%s WHERE id_user=%s'
                case 'activ':
                    upd_user = "UPDATE users SET activ=%s WHERE (id_user=%s);"
                    data[0][request] = '0' if data[0][request] == 'off' else '1'

            await cursor.execute(upd_user, (data[0][request], id_user))
            await conn.commit()

        conn.close()
    except Exception as ex:
        print(ex)


async def is_activ(callback: CallbackQuery) -> str:
    try:
        conn = await aiomysql.connect(user=config.database.user, password=config.database.password,
                                      db=config.database.database, loop=loop)
        string: str = ''
        async with conn.cursor() as cursor:
            user = f'SELECT activ FROM users WHERE id_user={callback.from_user.id}'
            await cursor.execute(user)
            string = await cursor.fetchone()
        if string:
            return string[0]
        else:
            return ''
    except Exception as ex:
        print(ex)

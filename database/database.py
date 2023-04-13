import asyncio
import aiomysql

from aiogram.types import CallbackQuery

from config.config import Config, load_config


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
                           f"%s, %s, %s, %s, %s, 1, 1, %s);"

            await cur.execute(add_user_str, (name, surname, group, photo_id, course, info, gender,
                                             find_gender, age, None))
            await conn.commit()

        conn.close()

    except Exception as ex:
        print(ex, "addUser")


async def is_user_db(id: int) -> bool:
    try:
        conn = await aiomysql.connect(user=config.database.user, password=config.database.password,
                                      db=config.database.database, loop=loop)
        result: str
        async with conn.cursor() as cursor:
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


async def output_user(id_user: int) -> str:
    try:
        conn = await aiomysql.connect(user=config.database.user, password=config.database.password,
                                      db=config.database.database, loop=loop)
        result: str = ""
        async with conn.cursor() as cursor:
            user = f"SELECT * FROM users WHERE id_user={id_user};"
            await cursor.execute(user)
            result = await cursor.fetchone()
        return result
    except Exception as ex:
        print(ex)


async def return_id_from(id_user: int) -> int | None:
    try:
        conn = await aiomysql.connect(user=config.database.user, password=config.database.password,
                                      db=config.database.database, loop=loop)
        result: str = ""
        async with conn.cursor() as cursor:
            user = f'SELECT from_user_id FROM users WHERE id_user=%s'
            await cursor.execute(user, (id_user,))
            result = await cursor.fetchone()
        return int(result[0]) if result else None
    except Exception as ex:
        print(ex)
        return None


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


async def update_from_user_id(id_user: int, from_user_id: int | None) -> None:
    try:
        conn = await aiomysql.connect(user=config.database.user, password=config.database.password,
                                      db=config.database.database, loop=loop)
        async with conn.cursor() as cursor:
            request = 'UPDATE users SET from_user_id=%s WHERE id_user=%s'
            await cursor.execute(request, (from_user_id, id_user))
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


async def search_user(id_user: int, find_gender: str, gender: str) -> int | None:
    try:
        conn = await aiomysql.connect(user=config.database.user, password=config.database.password,
                                      db=config.database.database, loop=loop)
        result: str = ''
        async with conn.cursor() as cursor:
            match find_gender:
                case 'idk':
                    request = f'''
                        SELECT id_user 
                        FROM users 
                        WHERE activ = 1 
                        AND id_user NOT IN (
                            SELECT id_to 
                            FROM likes 
                            WHERE id_from = {id_user}
                        )
                        AND id_user != {id_user}
                        AND (
                            gender = 'female' AND (findgender = 'male' OR findgender = 'idk') OR
                            gender = 'male' AND (findgender = 'female' OR findgender = 'idk')
                        )
                        ORDER BY RAND()
                        LIMIT 1;
                    '''
                case _:
                    request = f'''
                        SELECT id_user FROM users WHERE findgender = '{gender}' AND gender = '{find_gender}' 
                        AND activ = 1 AND id_user NOT
                         IN (SELECT id_to FROM likes WHERE id_from = {id_user})
                         AND id_user != {id_user}
                         ORDER BY RAND()
                         LIMIT 1;
                    '''
            await cursor.execute(request)
            result = await cursor.fetchone()
        return result[0] if result else None
    except Exception as ex:
        print(ex)
        return None


async def process_add_is_like(id_user: int, from_user_id: int, is_like: bool) -> None:
    try:
        conn = await aiomysql.connect(user=config.database.user, password=config.database.password,
                                      db=config.database.database, loop=loop)
        async with conn.cursor() as cursor:
            request = f'INSERT INTO likes VALUES(%s, %s, %s);'
            await cursor.execute(request, (int(id_user), int(from_user_id), is_like))
            await conn.commit()
        conn.close()
    except Exception as ex:
        print(ex)


async def is_match(id_from: int, id_to: int) -> bool | None:
    try:
        conn = await aiomysql.connect(user=config.database.user, password=config.database.password,
                                      db=config.database.database, loop=loop)
        async with conn.cursor() as cursor:
            query = "SELECT is_like FROM likes WHERE id_from=%s AND id_to=%s"
            params = (id_to, id_from)
            await cursor.execute(query, params)
            result = await cursor.fetchone()
            return result[0]
    except Exception as ex:
        print(ex)
        return None


async def match(id_from: int, id_to: int, is_match: bool = True):
    try:
        conn = await aiomysql.connect(user=config.database.user, password=config.database.password,
                                      db=config.database.database, loop=loop)
        async with conn.cursor() as cursor:
            query = f'''
                INSERT INTO matches (id_user, id_matched_user, is_match) VALUES ({id_from}, {id_to}, {is_match})
            '''
            await cursor.execute(query)
            await conn.commit()
        conn.close()
    except Exception as ex:
        print(ex)


async def get_new_likes(id_user: int):
    try:
        conn = await aiomysql.connect(user=config.database.user, password=config.database.password,
                                      db=config.database.database, loop=loop)
        async with conn.cursor() as cursor:
            query = """
                SELECT users.*, likes.is_like AS is_like
                FROM users
                INNER JOIN likes ON likes.id_from = users.id_user
                LEFT JOIN matches ON matches.id_user = %s AND matches.id_matched_user = users.id_user
                WHERE likes.id_to = %s AND matches.id IS NULL AND users.id_user != %s
                ORDER BY RAND() LIMIT 1
            """
            params = (id_user, id_user, id_user)
            await cursor.execute(query, params)
            result = await cursor.fetchone()
        conn.close()
        print(result)
        return result
    except Exception as ex:
        print(ex)
        return []


async def is_like_in_likes(id_from: int, id_to: int) -> bool:
    try:
        conn = await aiomysql.connect(user=config.database.user, password=config.database.password,
                                      db=config.database.database, loop=loop)
        async with conn.cursor() as cursor:
            query = 'SELECT is_like FROM likes WHERE id_from =%s AND id_to = %s;'
            await cursor.execute(query, (id_from, id_to))
            result = await cursor.fetchone()
            return True if result else False
    except Exception as ex:
        print(ex)
        return False


async def update_is_like(id_from: int, id_to: int, is_like: bool = True) -> None:
    try:
        conn = await aiomysql.connect(user=config.database.user, password=config.database.password,
                                      db=config.database.database, loop=loop)
        async with conn.cursor() as cursor:
            query = 'UPDATE likes SET is_like = %s WHERE id_from = %s AND id_to = %s;'
            await cursor.execute(query, (id_from, id_to, is_like))
            await conn.commit()
        conn.close()
    except Exception as ex:
        print(ex)
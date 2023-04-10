import asyncio

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text, Command

from database.database import output_user, return_id_from, search_user
from lexicon.watching_lex import LEXICON
from keyboard.keyboard import create_inline_kb

router: Router = Router()


@router.callback_query(Text(text=['search']))
async def start_search(callback: CallbackQuery):
    user = await output_user(callback.from_user.id)
    id_user = await search_user(int(user[0]), user[8], user[7])
    if id_user is not None:
        await callback.message.delete()
        await watch_blank(callback, id_user)
    else:
        await empty_search(callback)


async def watch_blank(callback: CallbackQuery, user_id: int | None) -> None:
    user = await output_user(user_id)
    print(user)
    if user is None:
        await empty_search(callback)
        return
    result = '{} {}, {}, {} группа, {} курс - \n{}'.format(user[1], user[2], user[9], user[3], user[5], user[6])
    await callback.message.answer_photo(photo=f'{user[4]}', caption=result,
                                        reply_markup=create_inline_kb(4, **{"dislike": "👎🏿",
                                                                            "match": "👬",
                                                                            "menu": "💤",
                                                                            "like": "❤️‍🔥"}))


async def empty_search(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(text=LEXICON['error_search'],
                                  reply_markup=create_inline_kb(1, **{"search": "Повторить поиск"}))




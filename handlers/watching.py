from aiogram import Router, Bot
from aiogram.types import CallbackQuery
from aiogram.filters import Text

from database.database import (output_user, search_user, update_from_user_id, process_add_is_like,
                               is_match, match, get_new_likes, update_is_like, is_like_in_likes)
from lexicon.watching_lex import LEXICON_M
from keyboard.keyboard import create_inline_kb, create_url_marcup

router: Router = Router()


@router.callback_query(Text(text=['search']))
async def start_search(callback: CallbackQuery):
    user = await output_user(callback.from_user.id)

    id_user = await search_user(int(user[0]), user[8], user[7])
    print(id_user)
    if id_user is not None:
        await update_from_user_id(callback.from_user.id, id_user)
        await callback.message.delete()
        await watch_blank(callback, id_user)
    else:
        await update_from_user_id(callback.from_user.id, None)
        await empty_search(callback)


async def watch_blank(callback: CallbackQuery, user_id: int | None) -> None:
    user = await output_user(user_id)
    print(user)
    if user is None:
        await empty_search(callback)
        return
    await callback.message.answer_photo(photo=f'{user[4]}', caption=await user_profile_message(user),
                                        reply_markup=await create_inline_kb(4, **{"dislike": "👎🏿",
                                                                                  "match": "👬",
                                                                                  "menu": "💤",
                                                                                  "like": "❤️‍🔥"}))


@router.callback_query(Text(text=['dislike']))
async def sent_dislike(callback: CallbackQuery):
    from_user_id = await output_user(callback.from_user.id)
    await process_add_is_like(callback.from_user.id, int(from_user_id[12]), False)
    await start_search(callback)


@router.callback_query(Text(text=['like']))
async def sent_like(callback: CallbackQuery, bot: Bot):
    from_user_id = await output_user(callback.from_user.id)
    is_like = await is_match(callback.from_user.id, int(from_user_id[12]))
    try:
        await process_add_is_like(callback.from_user.id, int(from_user_id[12]), True)
        if is_like:
            await send_match_message(bot, callback.from_user.id, int(from_user_id[12]))
        else:
            await send_like_message(bot, int(from_user_id[12]))
        await start_search(callback)
    except Exception as ex:
        print(ex)
        await start_search(callback)


@router.callback_query(Text(text=['match']))
async def sent_match(callback: CallbackQuery):
    user = await get_new_likes(callback.from_user.id)
    await callback.message.delete()
    if user:
        await update_from_user_id(callback.from_user.id, int(user[0]))
        await callback.message.answer_photo(
            photo=f'{user[4]}',
            caption=await user_profile_message(user),
            reply_markup=await create_inline_kb(3, **{"dislike_match": "👎🏿", "menu": "💤", "like_match": "❤️‍🔥"})
        )
    else:
        await callback.message.answer(text=LEXICON_M['error_match'],
                                      reply_markup=await create_inline_kb(4, **{"menu": "💤",
                                                                                "search": "👁",
                                                                                "my_blank": "🏠",
                                                                                "edit": "🎭"}))


@router.callback_query(Text(text=['dislike_match']))
async def process_sent_dislike(callback: CallbackQuery):
    from_user_id = await output_user(callback.from_user.id)
    await process_add_is_like(callback.from_user.id, int(from_user_id[12]), False)
    await match(callback.from_user.id, int(from_user_id[12]), is_match=False)
    await start_search(callback)


@router.callback_query(Text(text=['like_match']))
async def process_sent_like(callback: CallbackQuery, bot: Bot):
    from_user_id = await output_user(callback.from_user.id)
    try:
        if await is_like_in_likes(callback.from_user.id, int(from_user_id[12])):
            await update_is_like(callback.from_user.id, int(from_user_id[12]))
            await send_match_message(bot, callback.from_user.id, int(from_user_id[12]))
        else:
            await process_add_is_like(callback.from_user.id, int(from_user_id[12]), True)
            await send_match_message(bot, callback.from_user.id, int(from_user_id[12]))
    except Exception as ex:
        print(ex)
        await start_search(callback)


async def send_match_message(bot: Bot, id_from: int, id_to: int):
    await send_messages(bot, id_from, id_to, await output_user(id_to))
    await send_messages(bot, id_to, id_from, await output_user(id_from))
    await match(id_from, id_to)


async def send_messages(bot: Bot, id_from: int, id_to: int, user: str):
    await bot.send_photo(id_from, photo=f'{user[4]}',
                         caption=await user_profile_message(user),
                         reply_markup=await create_url_marcup(id_to))
    await bot.send_message(id_from, text=LEXICON_M['match'],
                           reply_markup=await create_inline_kb(2, **{"search": "Продолжить", "menu": "Меню"}))


async def user_profile_message(user: str) -> str:
    return '{} {}, {}, {} группа, {} курс - \n{}'.format(
        user[1], user[2], user[9], user[3], user[5], user[6])


async def send_like_message(bot: Bot, id_to: int):
    await bot.send_message(id_to,
                           text='Заканчивайте просмотр, вы кому-то понравились!',
                           reply_markup=await create_inline_kb(2, **{"search": "Продолжить", "match": "Посмотреть"}))


async def empty_search(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(text=LEXICON_M['error_search'],
                                  reply_markup=await create_inline_kb(4, **{"match": "👬",
                                                                            "menu": "💤",
                                                                            "my_blank": "🏠",
                                                                            "edit": "🎭",
                                                                            "search": "Повторить поиск"}))

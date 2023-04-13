from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command, Text

from lexicon.lexicon import LEXICON
from keyboard.keyboard import create_inline_kb
from lexicon.watching_lex import LEXICON_M


router: Router = Router()


@router.message(Command(commands=['start']))
async def start_message(message: Message):
    await message.delete()
    await message.answer(text=LEXICON['/start'], reply_markup=await create_inline_kb(1, **{"register": "Регистрация"}))


@router.message(Command(commands=['help']))
async def help_message(message: Message):
    await message.delete()
    await message.answer(text=LEXICON['/help'], reply_markup=await create_inline_kb(1, **{"register": "Регистрация"}))


@router.callback_query(Text(text=['info']))
async def help_message(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['/help'],
                                     reply_markup=await create_inline_kb(1, **{"register": "Регистрация"}))


@router.message(Command(commands=['menu']))
@router.callback_query(Text(text=['menu']))
async def sent_menu(callback: CallbackQuery | Message):
    if isinstance(callback, CallbackQuery):
        await callback.message.delete()
        await callback.message.answer(text=LEXICON_M['menu'],
                                      reply_markup=await create_inline_kb(3, **{'my_blank': "🏠",
                                                                                "edit": "🎭",
                                                                                "search": "👁",
                                                                                'register': 'Регистрация'}))
    else:
        await callback.answer(text=LEXICON_M['menu'],
                              reply_markup=await create_inline_kb(3, **{'my_blank': "🏠",
                                                                        "edit": "🎭",
                                                                        "search": "👁",
                                                                        'register': 'Регистрация'}))

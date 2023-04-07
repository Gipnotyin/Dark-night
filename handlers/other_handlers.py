from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text, StateFilter
from aiogram.fsm.state import default_state

from keyboard.keyboard import create_inline_kb
from lexicon.lexicon_menu import LEXICON

router: Router = Router()


@router.message()
async def other_message(message: Message):
    await message.answer(text=LEXICON['other'],
                         reply_markup=create_inline_kb(1, **{'Регистрация': 'Регистрация',
                                                             "Редактировать": "Редактировать анкету",
                                                             "search": "Начать просмотр анкет",
                                                             "info": "Важная информация"}))


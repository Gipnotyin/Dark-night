from aiogram import Router
from aiogram.types import Message

from keyboard.keyboard import create_inline_kb
from lexicon.lexicon_menu import LEXICON

router: Router = Router()


@router.message()
async def other_message(message: Message):
    await message.answer(text=LEXICON['other'],
                         reply_markup=await create_inline_kb(3, **{'my_blank': "🏠",
                                                                   "edit": "🎭",
                                                                   "search": "👁",
                                                                   'register': 'Регистрация'}))

from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command, Text

from lexicon.lexicon import LEXICON
from keyboard.keyboard import create_inline_kb


router: Router = Router()


@router.message(Command(commands=['start']))
async def start_message(message: Message):
    await message.delete()
    await message.answer(text=LEXICON['/start'], reply_markup=create_inline_kb(1, 'Регистрация'))


@router.message(Command(commands=['help']))
async def help_message(message: Message):
    await message.delete()
    await message.answer(text=LEXICON['/help'], reply_markup=create_inline_kb(1, 'Регистрация'))


@router.callback_query(Text(text=['info']))
async def help_message(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['/help'], reply_markup=create_inline_kb(1, 'Регистрация'))

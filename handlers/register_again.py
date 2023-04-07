import asyncio

from aiogram import Router
from aiogram.filters import Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.types import (CallbackQuery, Message, ReplyKeyboardRemove)
from aiogram.fsm.state import default_state

from lexicon.lexicon import LEXICON
from keyboard.keyboard import create_inline_kb, create_tipical_keyboard
from handlers.register_user import FSMRegForm
from database.database import delete_user, is_user_db, output_user


router: Router = Router()


class FSMUpdateForm(StatesGroup):
    fill_update = State()


@router.callback_query(Text(text=['Да', 'Нет']), StateFilter(FSMUpdateForm.fill_update))
async def process_update_form(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'Да':
        await delete_user(callback)
        await callback.message.edit_text(text=LEXICON['/register'])
        await state.clear()
        await state.set_state(FSMRegForm.fill_name)
    else:
        await callback.message.edit_text(text=LEXICON['choice'],
                                         reply_markup=create_inline_kb(2, **{"search": 'Начать просмотр анкет',
                                                                             "my_blank": 'Моя анкета'}))
        await state.clear()


@router.message(StateFilter(FSMUpdateForm.fill_update))
async def warning_update_form(message: Message):
    await message.answer(text=LEXICON['error_choice'], reply_markup=create_inline_kb(2, 'Да', 'Нет'))


@router.callback_query(Text(text=['my_blank']))
async def process_see_my_form(callback: CallbackQuery):

    result = await output_user(callback)

    if result:
        user_str = '{} {}, {}, {} группа, {} курс - \n{}'.format(result[1], result[2], result[9], result[3], result[5],
                                                                 result[6])
        await callback.message.answer_photo(photo=f'{result[4]}', caption=user_str,
                                            reply_markup=create_inline_kb(2, **{'Редактировать': 'Редактировать',
                                                                          'search': 'Начать просмотр анкет'}))
    else:
        await callback.message.edit_text(text='Похоже, что у вас нет анкеты, хотите создать?',
                                         reply_markup=create_inline_kb(1, **{'Регистрация': 'Регистрация'}))


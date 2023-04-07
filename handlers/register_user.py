import asyncio

from aiogram import Router, F
from aiogram.filters import Command, Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters.state import State, StatesGroup
from aiogram.types import (CallbackQuery, Message)

from lexicon.lexicon import LEXICON
from keyboard.keyboard import create_inline_kb, create_tipical_keyboard
from servises.servises import isCorrectGroup
from database.database import add_user, is_user_db


router: Router = Router()


class FSMUpdateForm(StatesGroup):
    fill_update = State()


class FSMRegForm(StatesGroup):
    fill_name = State()
    fill_surname = State()
    fill_age = State()
    fill_course = State()
    fill_group = State()
    fill_info = State()
    fill_photo = State()
    fill_gender = State()
    fill_find_gender = State()


@router.callback_query(Text(text='Регистрация'), StateFilter(default_state))
async def process_register_user(callback: CallbackQuery, state: FSMContext):
    if is_user_db(callback.from_user.id):
        await callback.message.edit_text(text=LEXICON['already_reg'], reply_markup=create_inline_kb(2, 'Да', 'Нет'))
        await state.set_state(FSMUpdateForm.fill_update)
    else:
        await callback.message.edit_text(text=LEXICON['/register'])

        await state.set_state(FSMRegForm.fill_name)


@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['/cancel'], reply_markup=create_inline_kb(1, **{"Регистрация": "Регистрация"}))
    await state.clear()


@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text='Отменять нечего. Вы вне машины состояний\n\n'
                              'Чтобы перейти к заполнению анкеты - '
                              'нажмите на кнопку ниже', reply_markup=create_inline_kb(1, 'Регистрация'))


@router.message(StateFilter(FSMRegForm.fill_name), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    
    await message.answer(text=LEXICON['sent_surname'])

    await state.set_state(FSMRegForm.fill_surname)


@router.message(StateFilter(FSMRegForm.fill_name))
async def warning_sent_name(message: Message):
    await message.answer(text=LEXICON['error_name'])


@router.message(StateFilter(FSMRegForm.fill_surname), lambda x: x.text.isalpha())
async def process_sent_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    
    await message.answer(text=LEXICON['sent_age'])

    await state.set_state(FSMRegForm.fill_age)


@router.message(StateFilter(FSMRegForm.fill_surname))
async def warning_sent_surname(message: Message):
    await message.answer(text=LEXICON['error_surname'])


@router.message(StateFilter(FSMRegForm.fill_age), lambda x: x.text.isdigit() and 15 < int(x.text) < 99)
async def process_sent_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)

    await message.answer(text=LEXICON['sent_course'])

    await state.set_state(FSMRegForm.fill_course)


@router.message(StateFilter(FSMRegForm.fill_age))
async def warning_sent_age(message: Message):
    await message.answer(text=LEXICON['error_age'])


@router.message(StateFilter(FSMRegForm.fill_course), lambda x: x.text.isdigit() and 1 <= int(x.text) <= 5)
async def process_sent_course(message: Message, state: FSMContext):
    await state.update_data(cours=message.text)

    await message.answer(text=LEXICON['sent_group'])

    await state.set_state(FSMRegForm.fill_group)


@router.message(StateFilter(FSMRegForm.fill_course))
async def warning_sent_course(message: Message):
    await message.answer(text=LEXICON['error_course'])


@router.message(StateFilter(FSMRegForm.fill_group), lambda x: isCorrectGroup(x.text))
async def process_sent_group(message: Message, state: FSMContext):
    await state.update_data(group=message.text)
    
    await message.answer(text=LEXICON['sent_gender'], reply_markup=create_inline_kb(2, **{'male': "Парень",
                                                                                          'female': 'Девушка'}))

    await state.set_state(FSMRegForm.fill_gender)


@router.message(StateFilter(FSMRegForm.fill_group))
async def warning_sent_group(message: Message):
    await message.answer(text=LEXICON['error_group'])


@router.callback_query(StateFilter(FSMRegForm.fill_gender), Text(text=['male', 'female']))
async def process_sent_gender(callback: CallbackQuery, state: FSMContext):
    await state.update_data(gender=callback.data)
    
    await callback.answer()
    await callback.message.edit_text(text=LEXICON['sent_findgender'],
                                     reply_markup=create_inline_kb(2, **{'female': 'Девушек',
                                                                         'male': 'Парней', 'idk': 'Всё равно'}))

    await state.set_state(FSMRegForm.fill_find_gender)


@router.message(StateFilter(FSMRegForm.fill_gender))
async def warning_sent_gender(message: Message):
    await message.answer(text=LEXICON['error_gender'], reply_markup=create_inline_kb(2, **{'male': 'Парень',
                                                                                           'female': 'Девушка'}))


@router.callback_query(StateFilter(FSMRegForm.fill_find_gender), Text(text=['female', 'male', 'idk']))
async def process_sent_find_gender(callback: CallbackQuery, state: FSMContext):
    await state.update_data(find_gender=callback.data)

    await callback.message.delete()
    await callback.message.answer(text=LEXICON['sent_photo'])

    await state.set_state(FSMRegForm.fill_photo)


@router.message(StateFilter(FSMRegForm.fill_find_gender))
async def warning_sent_find_gender(message: Message):
    await message.answer(text=LEXICON['error_findgender'],
                         reply_markup=create_inline_kb(2, **{'female': 'Девушек',
                                                             'male': 'Парней', 'idk': 'Всё равно'}))


@router.message(StateFilter(FSMRegForm.fill_photo), F.photo[-1].as_('largest_photo'))
async def process_sent_photo(message: Message, state: FSMContext):
    await state.update_data(id_photo=message.photo[0].file_id, photo_unique_id=message.photo[0].file_unique_id)
    
    await message.answer(text=LEXICON['sent_info'], reply_markup=create_inline_kb(1, **{'text': 'Оставить без текста'}))

    await state.set_state(FSMRegForm.fill_info)


@router.message(StateFilter(FSMRegForm.fill_photo))
async def warning_sent_photo(message: Message):
    await message.answer(text=LEXICON['error_photo'])


@router.message(StateFilter(FSMRegForm.fill_info), lambda x: x.text.isalpha() or not x.text.isalpha())
async def process_sent_info(message: Message, state: FSMContext):
    await state.update_data(info=message.text)

    task = asyncio.create_task(add_user(message.from_user.id, await state.get_data()))

    await task

    await state.clear()

    await message.answer(text=LEXICON['end_register'],
                         reply_markup=create_inline_kb(2, **{"search": 'Начать просмотр анкет',
                                                             "my_blank": 'Моя анкета'}))


@router.callback_query(StateFilter(FSMRegForm.fill_info), Text(text=['text']))
async def process_sent_info(callback: CallbackQuery, state: FSMContext):
    await state.update_data(info='')

    task = asyncio.create_task(add_user(callback.from_user.id, await state.get_data()))

    await task

    await state.clear()

    await callback.message.edit_text(text=LEXICON['end_register'],
                                     reply_markup=create_inline_kb(2, **{"search": 'Начать просмотр анкет',
                                                                         "my_blank": 'Моя анкета'}))


@router.message(StateFilter(FSMRegForm.fill_info))
async def warning_sent_info(message: Message):
    await message.answer(text=LEXICON['error_info'],
                         reply_markup=create_inline_kb(1, **{'text': 'Оставить без текста'}))

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters.state import State, StatesGroup
from aiogram.filters import Text

from lexicon.lexicon_for_form import LEXICON
from keyboard.keyboard import create_inline_kb
from database.database import update_user, is_activ
from servises.servises import isCorrectGroup

router: Router = Router()


class FSMUpdate(StatesGroup):
    start_update = State()
    photo = State()
    name = State()
    surname = State()
    group = State()
    info = State()
    age = State()
    gender = State()
    course = State()
    activ = State()
    find_gender = State()


@router.callback_query(Text(text='edit'), StateFilter(default_state))
async def update_form(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text=LEXICON['update_form'],
                                  reply_markup=create_inline_kb(3, 'Фото', 'Имя', 'Фамилия',
                                                                   'Группа', 'О себе', 'Возраст',
                                                                   'Курс', 'Пол', 'Кого ищем?',
                                                                   'Отк/Вкл', 'Меню'))
    await callback.answer()
    await state.set_state(FSMUpdate.start_update)


@router.callback_query(StateFilter(FSMUpdate.start_update), Text(text=['Фото', 'Имя', 'Фамилия',
                                                                       'Группа', 'О себе', 'Возраст',
                                                                       'Курс', 'Пол', 'Кого ищем?',
                                                                       'Отк/Вкл', 'Меню']))
async def process_choice(callback: CallbackQuery, state: FSMContext):
    match callback.data:
        case 'Фото':
            await callback.message.edit_text(text=LEXICON['sent_photo'])
            await state.set_state(FSMUpdate.photo)
        case 'Имя':
            await callback.message.edit_text(text=LEXICON['sent_name'])
            await state.set_state(FSMUpdate.name)
        case 'Фамилия':
            await callback.message.edit_text(text=LEXICON['sent_surname'])
            await state.set_state(FSMUpdate.surname)
        case 'Группа':
            await callback.message.edit_text(text=LEXICON['sent_group'])
            await state.set_state(FSMUpdate.group)
        case 'О себе':
            await callback.message.edit_text(text=LEXICON['sent_info'])
            await state.set_state(FSMUpdate.info)
        case 'Возраст':
            await callback.message.edit_text(text=LEXICON['sent_age'])
            await state.set_state(FSMUpdate.age)
        case 'Курс':
            await callback.message.edit_text(text=LEXICON['sent_course'])
            await state.set_state(FSMUpdate.course)
        case 'Пол':
            await callback.message.edit_text(text=LEXICON['sent_gender'],
                                             reply_markup=create_inline_kb(2, **{"male": 'Парень', "female": 'Девушка'}))
            await state.set_state(FSMUpdate.gender)
        case 'Кого ищем?':
            await callback.message.edit_text(text=LEXICON['sent_find_gender'],
                                             reply_markup=create_inline_kb(2, **{'male': "Парней", 'female': "Девушек",
                                                                                 'idk': "Всё равно"}))
            await state.set_state(FSMUpdate.find_gender)
        case 'Отк/Вкл':
            await callback.message.edit_text(text=LEXICON['off/on'],
                                             reply_markup=create_inline_kb(2, **{'off': "Отключить", 'on': "Включить"}))
            await state.set_state(FSMUpdate.activ)
        case 'Меню':
            await callback.message.edit_text(text=LEXICON['menu'],
                                             reply_markup=create_inline_kb(1,
                                                                           **{'register': 'Регистрация',
                                                                              "edit": "Редактировать",
                                                                              "search": "Начать просмотр анкет"}))
            await state.clear()


@router.message(StateFilter(FSMUpdate.start_update))
async def error_process_choice(message: Message):
    await message.answer(text=LEXICON['error_message'],
                         reply_markup=create_inline_kb(3, 'Фото', 'Имя', 'Фамилия',
                                                          'Группа', 'О себе', 'Возраст',
                                                          'Курс', 'Пол', 'Кого ищем?',
                                                          'Отк/Вкл', 'Меню'))


@router.message(StateFilter(FSMUpdate.photo), F.photo[-1].as_('largest_photo'))
async def sent_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[0].file_id, photo_unique_id=message.photo[0].file_unique_id)
    await update_user(message.from_user.id, 'photo', await state.get_data())
    await message.answer(text=LEXICON['update'], reply_markup=create_inline_kb(2, **{"search": 'Начать просмотр анкет',
                                                                               "my_blank": 'Моя анкета'}))
    await state.clear()


@router.message(StateFilter(FSMUpdate.photo))
async def send_echo(message: Message):
    await message.reply(text='Извините, но это не похоже на фотографию')


@router.message(StateFilter(FSMUpdate.name), F.text.isalpha())
async def send_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await update_user(message.from_user.id, 'name', await state.get_data())
    await message.answer(text=LEXICON['update'],
                         reply_markup=create_inline_kb(2, **{"search": 'Начать просмотр анкет',
                                                             "my_blank": 'Моя анкета'}))
    await state.clear()


@router.message(StateFilter(FSMUpdate.name))
async def error_send_name(message: Message):
    await message.reply(text=LEXICON['error_name'])


@router.message(StateFilter(FSMUpdate.surname), F.text.isalpha())
async def send_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await update_user(message.from_user.id, 'surname', await state.get_data())
    await message.answer(text=LEXICON['update'],
                         reply_markup=create_inline_kb(2, **{"search": 'Начать просмотр анкет',
                                                             "my_blank": 'Моя анкета'}))
    await state.clear()


@router.message(StateFilter(FSMUpdate.surname))
async def error_send_surname(message: Message):
    await message.reply(text=LEXICON['error_surname'])


@router.message(StateFilter(FSMUpdate.group), lambda x: isCorrectGroup(x.text))
async def sent_group(message: Message, state: FSMContext):
    await state.update_data(group=message.text)
    await update_user(message.from_user.id, 'group', await state.get_data())
    await message.answer(text=LEXICON['update'],
                         reply_markup=create_inline_kb(2, **{"search": 'Начать просмотр анкет',
                                                             "my_blank": 'Моя анкета'}))
    await state.clear()


@router.message(StateFilter(FSMUpdate.group))
async def error_sent_group(message: Message):
    await message.reply(text=LEXICON['error_group'])


@router.message(StateFilter(FSMUpdate.info), lambda x: x.text.isalpha() or not x.text.isalpha())
async def sent_info(message: Message, state: FSMContext):
    await state.update_data(info=message.text)
    await update_user(message.from_user.id, 'info', await state.get_data())
    await message.answer(text=LEXICON['update'],
                         reply_markup=create_inline_kb(2, **{"search": 'Начать просмотр анкет',
                                                             "my_blank": 'Моя анкета'}))
    await state.clear()


@router.message(StateFilter(FSMUpdate.info))
async def error_sent_info(message: Message):
    await message.reply(text=LEXICON['error_info'])


@router.message(StateFilter(FSMUpdate.age), lambda x: x.text.isdigit() and 15 < int(x.text) < 99)
async def sent_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await update_user(message.from_user.id, 'age', await state.get_data())
    await message.answer(text=LEXICON['update'],
                         reply_markup=create_inline_kb(2, **{"search": 'Начать просмотр анкет',
                                                             "my_blank": 'Моя анкета'}))
    await state.clear()


@router.message(StateFilter(FSMUpdate.age))
async def error_sent_age(message: Message):
    await message.reply(text=LEXICON['error_age'])


@router.message(StateFilter(FSMUpdate.course), lambda x: x.text.isdigit() and 1 <= int(x.text) <= 5)
async def sent_course(message: Message, state: FSMContext):
    await state.update_data(course=message.text)
    await update_user(message.from_user.id, 'course', await state.get_data())
    await message.answer(text=LEXICON['update'],
                         reply_markup=create_inline_kb(2, **{"search": 'Начать просмотр анкет',
                                                             "my_blank": 'Моя анкета'}))
    await state.clear()


@router.message(StateFilter(FSMUpdate.course))
async def error_sent_course(message: Message):
    await message.reply(text=LEXICON['error_course'])


@router.callback_query(StateFilter(FSMUpdate.gender), Text(text=['male', 'female']))
async def sent_gender(callback: CallbackQuery, state: FSMContext):
    await state.update_data(gender=callback.data)
    await update_user(callback.from_user.id, 'gender', await state.get_data())
    await callback.message.edit_text(text=LEXICON['update'],
                                     reply_markup=create_inline_kb(2, **{"search": 'Начать просмотр анкет',
                                                                         "my_blank": 'Моя анкета'}))
    await state.clear()


@router.message(StateFilter(FSMUpdate.gender))
async def error_sent_gender(message: Message):
    await message.reply(text=LEXICON['error_gender'],
                        reply_markup=create_inline_kb(2, **{"male": 'Парень', "female": 'Девушка'}))


@router.callback_query(StateFilter(FSMUpdate.find_gender), Text(text=['male', 'female', 'idk']))
async def sent_find_gender(callback: CallbackQuery, state: FSMContext):
    await state.update_data(find_gender=callback.data)
    await update_user(callback.from_user.id, 'find_gender', await state.get_data())
    await callback.message.edit_text(text=LEXICON['update'],
                                     reply_markup=create_inline_kb(2, **{"search": 'Начать просмотр анкет',
                                                                         "my_blank": 'Моя анкета'}))
    await state.clear()


@router.message(StateFilter(FSMUpdate.find_gender))
async def error_sent_find_gender(message: Message):
    await message.reply(text=LEXICON['error_find_gender'],
                        reply_markup=create_inline_kb(2, **{'male': "Парней", 'female': "Девушек", 'idk': "Всё равно"}))


@router.callback_query(StateFilter(FSMUpdate.activ), Text(text=['off', 'on']))
async def sent_activ(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'off' and await is_activ(callback) == '0':
        await callback.message.edit_text(text=LEXICON['off'],
                                         reply_markup=create_inline_kb(2, **{"search": 'Начать просмотр анкет',
                                                                             "my_blank": 'Моя анкета'}))
        await state.clear()
        return
    if callback.data == 'on' and await is_activ(callback) == '1':
        await callback.message.edit_text(text=LEXICON['on'],
                                         reply_markup=create_inline_kb(2, **{"search": 'Начать просмотр анкет',
                                                                             "my_blank": 'Моя анкета'}))
        await state.clear()
        return

    await state.update_data(activ=callback.data)
    await update_user(callback.from_user.id, 'activ', await state.get_data())
    await callback.message.edit_text(text=LEXICON['update'],
                                     reply_markup=create_inline_kb(2, **{"search": 'Начать просмотр анкет',
                                                                         "my_blank": 'Моя анкета'}))
    await state.clear()


@router.message(StateFilter(FSMUpdate.find_gender))
async def error_activ(message: Message):
    await message.reply(text=LEXICON['error_find_gender'],
                        reply_markup=create_inline_kb(2, **{'off': "Отключить", 'on': "Включить"}))

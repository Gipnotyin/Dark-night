from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import LEXICON


async def create_tipical_keyboard(*buttons: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[(LEXICON[button] if button in LEXICON else button) for button in buttons],
                               resize_keyboard=True,
                               one_time_keyboard=True)


async def create_inline_kb(width: int,
                     *args: str,
                     **kwargs: str) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON[button] if button in LEXICON else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


async def create_url_marcup(id_user: int) -> InlineKeyboardMarkup:
    profile_button_user_to = InlineKeyboardButton(text="Перейти к профилю", url=f"tg://user?id={id_user}")
    return InlineKeyboardMarkup(
        inline_keyboard=[[profile_button_user_to]])


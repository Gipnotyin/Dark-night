from aiogram import Bot, types


async def set_main_menu(bot: Bot) -> None:
    main_menu_commands = [
        types.BotCommand(command="/start", description="Начало работы с ботом"),
        types.BotCommand(command="/help", description="Руководство"),
        types.BotCommand(command="/cancel", description="Отменить регистрацию"),
        types.BotCommand(command="/menu", description="Меню")
    ]
    await bot.set_my_commands(main_menu_commands)

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis

from config.config import Config, load_config
from handlers import handler, register_user, register_again, update_information_anketa, other_handlers


logger = logging.getLogger(__name__)


def register_all_handlers(dp: Dispatcher) -> None:
    dp.include_router(handler.router)
    dp.include_router(register_user.router)
    dp.include_router(register_again.router)
    dp.include_router(update_information_anketa.router)
    dp.include_router(other_handlers.router)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s')
    
    logger.info("Starting Bot")

    config: Config = load_config('.env')

    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    redis: Redis = Redis(host='localhost')
    storage: RedisStorage = RedisStorage(redis=redis)
    dp: Dispatcher = Dispatcher(storage=storage)


    #await set_main_menu(dp)

    register_all_handlers(dp)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
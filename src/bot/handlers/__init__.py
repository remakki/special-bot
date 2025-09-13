from aiogram import Dispatcher

from .admin import router as admin_router
from .commands import router as command_router
from .team_process import router as team_process_router


def register_handlers(dp: Dispatcher):
    dp.include_router(command_router)
    dp.include_router(admin_router)
    dp.include_router(team_process_router)

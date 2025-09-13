from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from src.bot.handlers.team_process import TeamProcess

router = Router()


@router.message(CommandStart())
async def start_command(mes: Message, state: FSMContext):
    await state.set_state(TeamProcess.team)
    await mes.answer(
        "Привет, <b>Спецагенты</b>!\n"
        "Я агент-бот под прикрытием, мой позывной <b>R7</b>!\n"
        "Сообщите название вашего отряда:"
    )


@router.message(Command("admin"))
async def admin_command(mes: Message, is_admin: bool):
    if is_admin:
        await mes.answer(
            "Ура! Вы администратор!",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="Посмотреть ответы команд"),
                        KeyboardButton(text="Добавить админа"),
                    ]
                ],
                resize_keyboard=True,
            ),
        )
    else:
        await mes.answer("У вас нет прав администратора!")

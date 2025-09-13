import json

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from redis.asyncio import Redis

from src.bot.handlers.team_process import handle_all_messages

router = Router()


@router.message(F.text == "Посмотреть ответы команд")
async def get_teams_answers(mes: Message, is_admin: bool, redis: Redis):
    if not is_admin:
        await handle_all_messages(mes)
        return

    teams_data = [
        json.loads(team_data) for team_data in await redis.lrange("teams_data", 0, -1)
    ]
    if teams_data:
        await mes.answer(
            "\n".join(
                f"{team_data['team']}: {team_data['answer']}"
                for team_data in teams_data
            )
        )
    else:
        await mes.answer("К сожалению, ответов на данный момент нет.")


class CreateAdmin(StatesGroup):
    admin = State()


@router.message(F.text == "Добавить админа")
async def add_admin(mes: Message, is_admin: bool, state: FSMContext):
    if not is_admin:
        await handle_all_messages(mes)
        return

    await state.set_state(CreateAdmin.admin)
    await mes.answer(
        "Введите имя пользователя (например, <code><b>@username</b></code>):"
    )


@router.message(StateFilter(CreateAdmin.admin))
async def process_admin(mes: Message, is_admin: bool, state: FSMContext, redis: Redis):
    if not is_admin:
        await handle_all_messages(mes)
        return

    admin = mes.text.strip()

    if admin[0] == "@":
        await redis.rpush("admins", admin[1:])
        await mes.answer(f"<code>{admin}</code> успешно добавлен в администраторы!")
        await state.clear()
    else:
        await mes.answer("Неверный формат! Попробуйте снова")

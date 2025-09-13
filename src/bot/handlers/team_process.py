import json

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from redis.asyncio import Redis

router = Router()


class TeamProcess(StatesGroup):
    team = State()
    answer = State()


@router.message(StateFilter(TeamProcess.team))
async def process_team(mes: Message, state: FSMContext):
    team = mes.text.strip()
    await state.update_data(team=team, attempt=1)
    await state.set_state(TeamProcess.answer)
    await mes.answer(
        "Для вас у меня есть <b>секретная загадка</b>!\n"
        "На ответ у вас будет 3 попытки, поэтому будьте внимательны!\n"
        "Ответ напишите мне в чат, а я проверю.\n"
        "Итак, к загадке:"
    )
    await mes.answer("<b>Для НЕГО нет такого отверстия, чтобы ОН не пролез!</b>")


@router.message(StateFilter(TeamProcess.answer))
async def check_answer(mes: Message, state: FSMContext, redis: Redis):
    answer = mes.text.strip().lower()
    attempt = int(await state.get_value("attempt"))
    data = await state.get_data()

    if answer == "свет":
        team_data = json.dumps({"team": data["team"], "answer": "+"})
        await redis.rpush("teams_data", team_data)
        await mes.answer(
            "Абсолютно точно! Ваша миссия выполнена!"
        )
        await mes.answer(
            "Желаю успехов в вашем приключении, до скорых встреч!"
        )
        await state.clear()
    elif attempt < 3:
        await state.update_data(attempt=attempt + 1)
        match attempt:
            case 1:
                await mes.answer(
                    "Ответ неверный. У вас осталось 2 попытки! Верю в вас!"
                )
            case 2:
                await mes.answer(
                    "Ответ неверный. У вас осталась 1 попытка! У вас все получится!"
                )
            case _:
                await mes.answer(
                    "Ошибка! Сообщите организатору!"
                )
    else:
        team_data = json.dumps(
            {
                "team": data["team"],
                "answer": "-"
        }
        )
        await redis.rpush("teams_data", team_data)
        await mes.answer(
            "К сожалению, вы израсходывали все попытки...\n"
            "На самом деле, правильный ответ - свет. Именно он может просочиться сквозь любое отверстие."
        )
        await mes.answer(
            "Желаю успехов в вашем приключении, до скорых встреч!"
        )
        await state.clear()

@router.message()
async def handle_all_messages(mes: Message):
    await mes.answer(
        "Вы выполнили секретное задание, поэтому больше вам ничего не скажу!"
    )

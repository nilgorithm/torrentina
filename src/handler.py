from utils import verification

from aiogram import Router
from aiogram import F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.command import Command 
from aiogram.enums import ParseMode
from glob import glob

import asyncio
import libtorrent as lt
import re


router = Router()


ses = lt.session()
ses.listen_on(6881, 6891)
downloads = []
params = {"save_path": "/code/films/"}

state_str = [
    "queued",
    "checking",
    "downloading metadata",
    "downloading",
    "finished",
    "seeding",
    "allocating",
    "checking fastresume",
]

@router.message(Command(commands=["start", "help"]))
@verification
async def greet_user(message: Message, state: FSMContext) -> None:
    await message.answer('Здарова заебал, используй ссылку magnet для скачивания на minidlna server\n\nВзять ее можно например отсюда:\n[penis](https://t.me/torrents_index_bot)',
            parse_mode="MarkdownV2",
            reply_markup=ReplyKeyboardRemove())


@router.message(Command(commands=["list"]))
@verification
async def list_films(message: Message, state: FSMContext) -> None:
    films = "\n".join([obj.replace("/code/films/", "") for obj in glob(r"/code/films/*")])
    if films != str():
        await message.answer(films)
    else:
        await message.answer("Пока нет новых фильмов")


class States(StatesGroup):
    active = State()
    numb = State()


@router.message(Command(commands=["delete_d"]))
@verification
async def drop_torrent(message: Message, state: FSMContext) -> None:
    films_d = dict(enumerate([obj for obj in glob(r"/code/films/*")]))
    # потом тут можно сделать нормальные реплай клавы
    if len(films_d) > 0:
        await message.answer("Потом доделвю:)0")
    else:
        await message.answer("Пока нет фильмов, чтобы уалить")


@router.message(Command(commands=["delete_t"]))
@verification
async def drop_torrent(message: Message, state: FSMContext) -> None:
    active_torrents = dict(enumerate([t for t in downloads if not t.is_seed()]))
    if len(active_torrents) > 0:
        msg = "\n".join([f"{k}: {v.name()}" for k, v in active_torrents.items()])
        await state.update_data(active=active_torrents)
        await state.set_state(States.numb)
        await message.answer(f"Какой торрент вы хотите удалить?\n{msg}")
    else:
        await message.answer(f"Нет активных торрентов!")
    

@router.message(States.numb)
async def remove_torrent_by_numb(message: Message, state: FSMContext) -> None:
    numb = re.search(pattern="\d+", string=message.text)
    if numb:
        numb = int(next(iter(numb.groups()), "0"))
        data = await state.get_data()
        dactive = data.get("active").get(numb)
        if dactive:
            try:
                ses.remove_torrent(dactive)
                downloads.remove(dactive)
                await message.answer(f"Торрент {dactive.name()} успешно удален")
            except Exception as exp:      
                await message.answer(str(exp))
            await state.clear()
        else:
            await message.answer("Не найдено активного торрента с таким индексом, попробуйте снова /delete")
            await state.clear()
    else:
        await message.answer("Неверный формат, введите число, например: 1\nИли нажмите /cancel")


@router.message(Command(commands=["status"]))
@verification
async def greet_user(message: Message, state: FSMContext) -> None:
    if len(downloads) <= 0:
        await message.answer('Активных загрузок нет',
                         reply_markup=ReplyKeyboardRemove())
        pass
    for index, download in enumerate(downloads[:]):
        if not download.is_seed():
            s = download.status()
            pg = "\n".join([
                    download.name(),
                    str(s.download_rate / 1000),
                    "kB/s",
                    state_str[s.state],
                    str(s.progress * 100)
                    ])
            await message.answer(f'Этот еще качается {pg}',
                         reply_markup=ReplyKeyboardRemove())
        else:
            ses.remove_torrent(download)
            downloads.remove(download)
            await message.answer(f'Этот скачался {download.name()}',
                         reply_markup=ReplyKeyboardRemove())

async def add_new_link(link: str) -> None:
    downloads.append(
        lt.add_magnet_uri(ses, link, params)
    )


@router.message(Command(commands=["cancel"]))
async def cancel_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Действия отменены",
        reply_markup=ReplyKeyboardRemove(),
    )
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()

@router.message(F.text)
@verification
async def bad_message(message: Message, state: FSMContext) -> None:
    reres = re.search(pattern=r"magnet:\?([\W\w][^\n]+)", string=message.text)
    if reres:
        await message.answer('Ну, ща попробуем скачать', reply_markup=ReplyKeyboardRemove())
        try:
            await add_new_link(link=reres.group())
        except Exception as exp:
            await message.answer(str(exp))
    else:
        await message.answer(
                f'Дебилина, сообщение должно соедржать ссылку следующего формата\n```\nmagnet:?xt=urn:btih:{"bestoloch"*10}\n```\nВзять ее можно например отсюда:\n[penis](https://t.me/torrents_index_bot)', 
                parse_mode="MarkdownV2",
                reply_markup=ReplyKeyboardRemove())


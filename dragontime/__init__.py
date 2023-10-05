import json
import random
import os
from pathlib import Path
from graia.saya import Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image, Source
from graia.ariadne.message.parser.twilight import Twilight
from graia.ariadne.event.message import Group, GroupMessage
from graia.saya.builtins.broadcast.schema import ListenerSchema

from shared.utils.module_related import get_command
from shared.utils.control import (
    FrequencyLimit,
    Function,
    BlackListControl,
    UserCalledCountControl,
    Distribute
)

channel = Channel.current()
channel.name("dragontime")
channel.author("SAGIRI-kawaii")
channel.description("龙time")


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[Twilight([get_command(__file__, channel.module)])],
        decorators=[
            Distribute.distribute(),
            FrequencyLimit.require("dragontime", 1),
            Function.require(channel.module, notice=True),
            BlackListControl.enable(),
            UserCalledCountControl.add(UserCalledCountControl.FUNCTIONS),
        ],
    )
)
async def dragontime(app: Ariadne, group: Group, source: Source):
    await app.send_group_message(group, get_dragontime(), quote=source)


def get_dragontime() -> MessageChain:
    path = Path().cwd() / "resources" / "dragontime"
    for root, dirs, files in os.walk(path):
        img_path = Path.cwd() / "resources" / "dragontime" / random.choice(files)
    elements = []
    elements.append(Image(path=img_path))
    #elements.append(content)
    return MessageChain(elements)

'''
    card, filename = get_random_dragontime()
    card_dir = random.choice(["normal", "reverse"])
    card_type = "正位" if card_dir == "normal" else "逆位"
    content = f"{card['name']} ({card['name-en']}) {card_type}\n牌意：{card['meaning'][card_dir]}"
    elements = []
    img_path = Path.cwd() / "resources" / "dragontime" / card_dir / f"{filename}.jpg"
    if filename and img_path.exists():
        elements.append(Image(path=img_path))
    elements.append(content)
    return MessageChain(elements)


def get_random_dragontime():
    path = Path().cwd() / "resources" / "dragontime" / "dragontime.json"
    with open(path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    kinds = ["major", "pentacles", "wands", "cups", "swords"]
    cards = []
    for kind in kinds:
        cards.extend(data[kind])
    card = random.choice(cards)
    filename = next(("{}{:02d}".format(kind, card["num"]) for kind in kinds if card in data[kind]), "")
    return card, filename
'''

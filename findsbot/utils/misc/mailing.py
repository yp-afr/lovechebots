from asyncio import sleep

from findsbot.loader import bot
from findsbot.utils.dp_api.commands import get_users


async def mailing(caption, item_type, item_category, photo, author_):
    type_ = item_type
    if type_ == "Найдено":
        type_ = "Потеряно"
    elif type_ == "Потеряно":
        type_ = "Найдено"
    results = await get_users(type_, item_category)
    for result in results:
        text = f"<b>Новый пост относящийся к твоей категории!\n\n" \
               f"</b><b>{item_type}</b> -- {item_category}\n\n"
        try:
            if photo:
                text += caption
                text += f"\n\nКонтакты: {author_}"
                await bot.send_photo(photo=photo, chat_id=result.author_id, caption=text)
                await sleep(0.3)
            else:
                text += caption
                text += f"\n\nКонтакты: {author_}"
                await bot.send_message(chat_id=result.author_id, text=text)
                await sleep(0.3)
        except Exception:
            pass

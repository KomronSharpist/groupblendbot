import asyncio
import logging
from aiogram import Dispatcher, Bot, types, F
from aiogram.enums import ContentType
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)
bot = Bot(token="6798446304:AAF05g0h5QDgl3GaGcvVmvjjBr0YnOzcEqI")
dp = Dispatcher()
user_invite_count = {}
invited_users = {}
limit = 10

async def handle_new_chat_members(message: types.Message):
    if message.chat.type != 'private':
        inviter_id = message.from_user.id
        for member in message.new_chat_members:
            user_id = member.id
            if user_id != inviter_id:
                if inviter_id not in invited_users:
                    invited_users[inviter_id] = []
                invited_users[inviter_id].append(user_id)
                user_invite_count[inviter_id] = user_invite_count.get(inviter_id, 0) + 1

@dp.message(Command("change"))
async def change_invite_count(message: types.Message):
    user_id = message.from_user.id
    if user_id == 334840538 or user_id == 5377969967 or user_id == 1052097431:
        text = message.text.split(' ', 1)

        if len(text) == 2:
            new_limit = text[1]
            try:
                new_limit = int(new_limit)
                global limit
                limit = new_limit
                await message.reply(f"Limit changed to {limit}.")
            except ValueError:
                await message.reply("Please provide a valid number after /change command.")
        else:
            await message.reply("Please provide a number after /change command.")



@dp.message()
async def handle_message(message: types.Message):
    if message.new_chat_members:
        await handle_new_chat_members(message)
    elif message.content_type == ContentType.LEFT_CHAT_MEMBER:
        user_id = message.left_chat_member.id
        for inviter_id, invited_list in invited_users.items():
            if user_id in invited_list:
                invited_list.remove(user_id)
                user_invite_count[inviter_id] -= 1 if user_invite_count[inviter_id] > 0 else 0
    elif message.chat.type != 'private':
        user_id = message.from_user.id

        if user_id not in user_invite_count:
            user_invite_count[user_id] = 0

        chat_id = message.chat.id
        username = message.from_user.username if message.from_user.username else message.from_user.first_name

        if user_invite_count[user_id] < 10:
            sent_message = await bot.send_message(chat_id, f"Hurmatli @{username}\n\nGuruhga yozolishingiz uchun yana {limit - user_invite_count[user_id]}ta odam qoshishingiz kerak.")
            await message.delete()
            await asyncio.sleep(5)
            await bot.delete_message(chat_id=chat_id, message_id=sent_message.message_id)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        tasks = asyncio.all_tasks(loop=loop)
        for task in tasks:
            task.cancel()

        loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
        loop.close()

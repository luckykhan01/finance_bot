import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from app.core.config import settings
from app.core.database import db
from app.core.ai_client import parse_transaction_text
from app.services.finance import process_transaction, get_user_stats, get_user_balances, create_account


bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "Hi! I'm your Smart AI Finance Tracker 💸\n\n"
        "You don't need to write strict commands. Just write like you are writing a human:\n"
        "• <i>kaspi -5000 food</i>\n"
        "• <i>freedom +150000 salary</i>\n"
        "• <i>spent 2000 on taxi using cash</i>",
        parse_mode="HTML"
    )

@dp.message(Command("new_account"))
async def cmd_new_account(message: types.Message):
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        await message.answer(
            "Please write the name of the account.\n"
            "Example: <code>/new_account Kaspi</code>",
            parse_mode="HTML"
        )
        return

    account_name = args[1].strip()
    user_id = message.from_user.id
    username = message.from_user.username or 'unknown'

    result_msg = await create_account(user_id, username, account_name)
    await message.answer(result_msg, parse_mode="HTML")

@dp.message(Command("balance"))
async def cmd_balance(message: types.Message):
    user_id = message.from_user.id
    balances = await get_user_balances(user_id)

    if not balances:
        await message.answer("You do not have any accounts yet. Make a transaction to add an account.")
        return

    reply = "<b>Your accounts:</b>\n\n"
    total_sum = 0

    for b in balances:
        reply += f"• {b['name']}: <b>{b['balance']} {b['currency']}</b>\n"
        total_sum += float(b['balance'])

    reply += f"\n──────────────\nTotal: <b>{total_sum} KZT</b>"

    await message.answer(reply, parse_mode='HTML')

@dp.message(Command("stats"))
async def cmd_stats(message: types.Message):
    user_id = message.from_user.id
    stats = await get_user_stats(user_id, t_type="expense")

    if not stats:
        await message.answer("You do not have any expenses yet.")
        return

    reply = "<b>Expenses for this month:</b>\n\n"
    total_expense = 0

    for s in stats:
        reply += f"• {s['category']}: <b>{s['total']} KZT</b>\n"
        total_expense += float(s['total'])

    reply += f"\n──────────────\nTotal spent: <b>{total_expense} KZT</b>"

    await message.answer(reply, parse_mode='HTML')

@dp.message()
async def process_user_text(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    user_id = message.from_user.id
    username = message.from_user.username or "unknown"
    text = message.text

    ai_result = await parse_transaction_text(text)

    if not ai_result:
        await message.answer("Couldn't recognize the text. Try to make it a little clearer.")
        return

    try:
        new_balance = await process_transaction(
            user_id=user_id,
            username=username,
            account_name=ai_result["account_name"],
            amount=ai_result["amount"],
            t_type=ai_result["t_type"],
            category=ai_result["category"],
            description=ai_result.get("description", text)
        )

        emoji = "📉Expense" if ai_result["t_type"] == "expense" else "📈Income"

        reply_text = (
            f"{emoji} Recorded!\n"
            f"Account: <b>{ai_result['account_name']}</b>\n"
            f"Amount: <b>{ai_result['amount']}</b>\n"
            f"Category: <b>{ai_result['category']}</b>\n"
            f"──────────────\n"
            f"Remaining: <b>{new_balance}</b>"
        )
        await message.answer(reply_text, parse_mode="HTML")

    except Exception as e:
        await message.answer(f"Error when recording to DB: {e}")

async def main():
    await db.connect()
    print("Bot is running...")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
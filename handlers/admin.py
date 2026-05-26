import asyncio
import logging
from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.future import select
from sqlalchemy import func, update
from database import AsyncSessionLocal, User, ScanHistory
from states import AdminStates
from config import settings

logger = logging.getLogger(__name__)
router = Router()

def is_admin(user_id: int) -> bool:
    return user_id in settings.get_admin_ids()

@router.message(Command("admin"))
async def admin_cmd(message: Message):
    if not is_admin(message.from_user.id):
        return await message.answer("🔒 Access denied.")
    await message.answer(
        "⚡ *Admin Panel*\n\n"
        "/stats — System statistics\n"
        "/broadcast — Send message to all users\n"
        "/premium `user_id` — Grant premium to user\n"
        "/revoke `user_id` — Revoke premium from user",
        parse_mode="Markdown"
    )

@router.message(Command("stats"))
async def stats_cmd(message: Message):
    if not is_admin(message.from_user.id):
        return
    async with AsyncSessionLocal() as session:
        total_users = (await session.execute(select(func.count(User.telegram_id)))).scalar()
        premium_users = (await session.execute(
            select(func.count(User.telegram_id)).where(User.is_premium == True)
        )).scalar()
        total_scans = (await session.execute(select(func.count(ScanHistory.id)))).scalar()

    await message.answer(
        f"📊 *System Statistics*\n\n"
        f"👥 Total Users: `{total_users}`\n"
        f"💎 Premium Users: `{premium_users}`\n"
        f"🔍 Total Scans: `{total_scans}`",
        parse_mode="Markdown"
    )

@router.message(Command("premium"))
async def grant_premium_cmd(message: Message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) < 2:
        return await message.answer("Usage: /premium `user_id`", parse_mode="Markdown")
    try:
        target_id = int(parts[1])
        async with AsyncSessionLocal() as session:
            await session.execute(
                update(User).where(User.telegram_id == target_id).values(is_premium=True)
            )
            await session.commit()
        await message.answer(f"✅ Premium granted to user `{target_id}`.", parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"❌ Error: {e}")

@router.message(Command("revoke"))
async def revoke_premium_cmd(message: Message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) < 2:
        return await message.answer("Usage: /revoke `user_id`", parse_mode="Markdown")
    try:
        target_id = int(parts[1])
        async with AsyncSessionLocal() as session:
            await session.execute(
                update(User).where(User.telegram_id == target_id).values(is_premium=False)
            )
            await session.commit()
        await message.answer(f"✅ Premium revoked from user `{target_id}`.", parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"❌ Error: {e}")

@router.message(Command("broadcast"))
async def broadcast_cmd(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.set_state(AdminStates.waiting_for_broadcast)
    await message.answer("📢 Send the message you want to broadcast to all users.")

@router.message(AdminStates.waiting_for_broadcast)
async def broadcast_execute(message: Message, state: FSMContext, bot: Bot):
    if not is_admin(message.from_user.id):
        return
    await state.clear()
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User.telegram_id))
        user_ids = result.scalars().all()

    delivered, failed = 0, 0
    await message.answer(f"🚀 Broadcasting to {len(user_ids)} users...")
    for uid in user_ids:
        try:
            await bot.send_message(uid, f"📢 *Announcement:*\n\n{message.text}", parse_mode="Markdown")
            delivered += 1
            await asyncio.sleep(0.05)
        except Exception:
            failed += 1

    await message.answer(f"✅ Done. Delivered: `{delivered}` | Failed: `{failed}`", parse_mode="Markdown")

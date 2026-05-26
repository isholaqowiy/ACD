import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy.future import select
from database import AsyncSessionLocal, User
from keyboards import main_keyboard

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("subscription"))
async def subscription_cmd(message: Message):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        is_premium = user.is_premium if user else False

    status = "💎 PREMIUM" if is_premium else "🆓 FREE"
    await message.answer(
        f"💳 *Subscription Status*\n\n"
        f"Current plan: `{status}`\n\n"
        f"✨ *Premium Benefits:*\n"
        f"• Unlimited daily scans\n"
        f"• PDF & DOCX file analysis\n"
        f"• Priority processing\n\n"
        f"To upgrade, contact the admin.",
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )

@router.callback_query(F.data == "premium")
async def premium_callback(callback: CallbackQuery):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        is_premium = user.is_premium if user else False

    status = "💎 PREMIUM ACTIVE" if is_premium else "🆓 FREE TIER"
    try:
        await callback.message.edit_text(
            f"💳 *Subscription Portal*\n\n"
            f"Your plan: `{status}`\n\n"
            f"✨ *Premium includes:*\n"
            f"• Unlimited scans per day\n"
            f"• PDF & DOCX file upload\n"
            f"• Priority AI processing\n\n"
            f"Use /subscription for more details.",
            parse_mode="Markdown",
            reply_markup=main_keyboard()
        )
    except Exception:
        pass
    await callback.answer()

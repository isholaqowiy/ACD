import logging
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.future import select
from database import AsyncSessionLocal, User
from keyboards import main_keyboard

logger = logging.getLogger(__name__)
router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        if not user:
            session.add(User(
                telegram_id=message.from_user.id,
                username=message.from_user.username
            ))
            await session.commit()

    name = message.from_user.first_name or "there"
    await message.answer(
        f"👋 *Welcome, {name}!*\n\n"
        f"I'm your *AI Content Detector* — helping academic instructors "
        f"identify AI-generated student assignments.\n\n"
        f"📌 *What I can do:*\n"
        f"• 🔍 Detect AI content in pasted text\n"
        f"• 📂 Analyze PDF/DOCX files _(Premium)_\n"
        f"• 📜 View your scan history\n"
        f"• 💎 Unlimited scans with Premium\n\n"
        f"Choose an option below 👇",
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )

@router.callback_query(F.data == "help")
async def help_handler(callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            "📖 *Help & Documentation*\n\n"
            "• *Text Scan:* Paste text (min 100 chars)\n"
            "• *File Scan:* Upload PDF/DOCX _(Premium only)_\n"
            "• *Daily Limit:* Free users get 10 scans/day\n"
            "• *Premium:* Unlimited scans + file uploads\n\n"
            "Use /start to return to the main menu.",
            parse_mode="Markdown",
            reply_markup=main_keyboard()
        )
    except Exception:
        pass
    await callback.answer()

@router.callback_query(F.data == "cancel")
async def cancel_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    name = callback.from_user.first_name or "there"
    try:
        await callback.message.edit_text(
            f"✅ Cancelled, {name}. Back to main menu.",
            reply_markup=main_keyboard()
        )
    except Exception:
        pass
    await callback.answer()

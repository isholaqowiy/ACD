from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔍 Detect AI Content", callback_data="detect")],
        [InlineKeyboardButton(text="📂 Upload File (PDF/DOCX)", callback_data="upload")],
        [InlineKeyboardButton(text="📜 Scan History", callback_data="history")],
        [InlineKeyboardButton(text="💎 Premium Plans", callback_data="premium")],
        [InlineKeyboardButton(text="❓ Help", callback_data="help")],
    ])

def cancel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")]
    ])

def export_keyboard(scan_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📄 Export PDF", callback_data=f"export_pdf_{scan_id}"),
            InlineKeyboardButton(text="📝 Export TXT", callback_data=f"export_txt_{scan_id}")
        ],
        [InlineKeyboardButton(text="🏠 Main Menu", callback_data="cancel")]
    ])

def back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Main Menu", callback_data="cancel")]
    ])

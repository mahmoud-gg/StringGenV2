from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import SUPPORT_CHAT


keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(text="بدا الاستخراج", callback_data="gensession")],
        [
            InlineKeyboardButton(text="الدعم", url=SUPPORT_CHAT),
            InlineKeyboardButton(
                text="السورس", url="https://t.me/YY5Y8"
            ),
        ],
    ]
)

gen_key = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="بايروجورام v1", callback_data="pyrogram1"),
            InlineKeyboardButton(text="بايروجورام v2", callback_data="pyrogram"),
        ],
        [InlineKeyboardButton(text="تيرمكس", callback_data="telethon")],
    ]
)

retry_key = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text="حاول مجددا", callback_data="gensession")]]
)

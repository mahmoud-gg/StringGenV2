import asyncio

from pyrogram import Client, filters
from oldpyro import Client as Client1
from oldpyro.errors import ApiIdInvalid as ApiIdInvalid1
from oldpyro.errors import PasswordHashInvalid as PasswordHashInvalid1
from oldpyro.errors import PhoneCodeExpired as PhoneCodeExpired1
from oldpyro.errors import PhoneCodeInvalid as PhoneCodeInvalid1
from oldpyro.errors import PhoneNumberInvalid as PhoneNumberInvalid1
from oldpyro.errors import SessionPasswordNeeded as SessionPasswordNeeded1
from pyrogram.errors import (
    ApiIdInvalid,
    FloodWait,
    PasswordHashInvalid,
    PhoneCodeExpired,
    PhoneCodeInvalid,
    PhoneNumberInvalid,
    SessionPasswordNeeded,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from telethon import TelegramClient
from telethon.errors import (
    ApiIdInvalidError,
    PasswordHashInvalidError,
    PhoneCodeExpiredError,
    PhoneCodeInvalidError,
    PhoneNumberInvalidError,
    SessionPasswordNeededError,
)
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest
from pyromod.listen.listen import ListenerTimeout

from config import SUPPORT_CHAT
from StringGen import Anony
from StringGen.utils import retry_key


async def gen_session(
    message, user_id: int, telethon: bool = False, old_pyro: bool = False
):
    if telethon:
        ty = f"تـيـرمـكـس"
    elif old_pyro:
        ty = f"بـايـوجـرام v1"
    else:
        ty = f"بـايـوجـرام v2"

    await message.reply_text(f"» يحاول ان يبدا {ty} مستخرج جلسات...")

    try:
        api_id = await Anony.ask(
            identifier=(message.chat.id, user_id, None),
            text="» ارسل الايبي ايدي للإكمال",
            filters=filters.text,
            timeout=300,
        )
    except ListenerTimeout:
        return await Anony.send_message(
            user_id,
            "» انتهت مدة الاستخراج 5 دقائق\n\nمن فضلك ابدا الاستخراج استخرج مرا اخرى.",
            reply_markup=retry_key,
        )

    if await cancelled(api_id):
        return

    try:
        api_id = int(api_id.text)
    except ValueError:
        return await Anony.send_message(
            user_id,
            "» الايبي ايدي الذي ارسلتة خاطئ.\n\nمن فضلك اعد الاستخراج ..",
            reply_markup=retry_key,
        )

    try:
        api_hash = await Anony.ask(
            identifier=(message.chat.id, user_id, None),
            text="» من فضلك ارسل الايبي هاش للإكمال",
            filters=filters.text,
            timeout=300,
        )
    except ListenerTimeout:
        return await Anony.send_message(
            user_id,
            "» انتهت مدة الاستخراج 5 دقائق\n\nمن فضلك ابدا الاستخراج استخرج مرا اخرى.",
            reply_markup=retry_key,
        )

    if await cancelled(api_hash):
        return

    api_hash = api_hash.text

    if len(api_hash) < 30:
        return await Anony.send_message(
            user_id,
            "» الايبي هاش الذي ارسلتة خاطئ.\n\nمن فضلك اعد الاستخراج ..",
            reply_markup=retry_key,
        )

    try:
        phone_number = await Anony.ask(
            identifier=(message.chat.id, user_id, None),
            text="»  من فضلك ارسل رقمك للإكمال مثال: +20××××××××××",
            filters=filters.text,
            timeout=300,
        )
    except ListenerTimeout:
        return await Anony.send_message(
            user_id,
            "» انتهت مدة الاستخراج 5 دقائق\n\nمن فضلك ابدا الاستخراج استخرج مرا اخرى.",
            reply_markup=retry_key,
        )

    if await cancelled(phone_number):
        return
    phone_number = phone_number.text

    await Anony.send_message(user_id, "» يتم أرسال الكود لحسابك...")
    if telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif old_pyro:
        client = Client1(":memory:", api_id=api_id, api_hash=api_hash)
    else:
        client = Client(name="Anony", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()

    try:
        if telethon:
            code = await client.send_code_request(phone_number)
        else:
            code = await client.send_code(phone_number)
        await asyncio.sleep(1)

    except FloodWait as f:
        return await Anony.send_message(
            user_id,
            f"» فشل في ارسال الكود لحسابك.\n\nمن فضلك انتظر {f.value or f.x} ثواني و اعد المحاوله.",
            reply_markup=retry_key,
        )
    except (ApiIdInvalid, ApiIdInvalidError, ApiIdInvalid1):
        return await Anony.send_message(
            user_id,
            "» الايبي ايدي او الايبي هاش خاطئ.\n\nمن فضلك ابدا باستخراج جلستك مرا اخري.",
            reply_markup=retry_key,
        )
    except (PhoneNumberInvalid, PhoneNumberInvalidError, PhoneNumberInvalid1):
        return await Anony.send_message(
            user_id,
            "» رقم الهاتف خاطئ.\n\nمن فضلك ابدا باستخراج جلستك مرا اخري.",
            reply_markup=retry_key,
        )

    try:
        otp = await Anony.ask(
            identifier=(message.chat.id, user_id, None),
            text=f" من فضلك ارسل الكود الذي وصل لحسابك {phone_number}.\n\الكود هو <code>12345</code>, من فضلك ارسل بهذه الطريقة<code>1 2 3 4 5.</code>",
            filters=filters.text,
            timeout=600,
        )
        if await cancelled(otp):
            return
    except ListenerTimeout:
        return await Anony.send_message(
            user_id,
            "» انتهت مدة الاستخراج 10 دقائق\n\nمن فضلك ابدا الاستخراج استخرج مرا اخرى.",
            reply_markup=retry_key,
        )

    otp = otp.text.replace(" ", "")
    try:
        if telethon:
            await client.sign_in(phone_number, otp, password=None)
        else:
            await client.sign_in(phone_number, code.phone_code_hash, otp)
    except (PhoneCodeInvalid, PhoneCodeInvalidError, PhoneCodeInvalid1):
        return await Anony.send_message(
            user_id,
            "» الكود الذي ارسلتة <b>خاطئ.</b>\n\nمن فضلك ابدا باستخراج جلستك مرا اخرى.",
            reply_markup=retry_key,
        )
    except (PhoneCodeExpired, PhoneCodeExpiredError, PhoneCodeExpired1):
        return await Anony.send_message(
            user_id,
            "» الكود الذي ارسلتة <b>منتهي.</b>\n\nمن فضلك ابدا باستخراج جلستك مرا اخرى.",
            reply_markup=retry_key,
        )
    except (SessionPasswordNeeded, SessionPasswordNeededError, SessionPasswordNeeded1):
        try:
            pwd = await Anony.ask(
                identifier=(message.chat.id, user_id, None),
                text="» من فضلك ارسل كلمة سر تحقق الخطوتين للإكمال",
                filters=filters.text,
                timeout=300,
            )
        except ListenerTimeout:
            return Anony.send_message(
                user_id,
                "» انتهت مدة الاستخراج 5 دقائق\n\nمن فضلك ابدا الاستخراج استخرج مرا اخرى.",
                reply_markup=retry_key,
            )

        if await cancelled(pwd):
            return
        pwd = pwd.text

        try:
            if telethon:
                await client.sign_in(password=pwd)
            else:
                await client.check_password(password=pwd)
        except (PasswordHashInvalid, PasswordHashInvalidError, PasswordHashInvalid1):
            return await Anony.send_message(
                user_id,
                "» كلمة السر الذي قمت بإرسالها خاطئه.\n\nمن فضلك اعد الاستخراج ..",
                reply_markup=retry_key,
            )

    except Exception as ex:
        return await Anony.send_message(user_id, f"خطأ : <code>{str(ex)}</code>")

    try:
        txt = "تم استخراج الجلسة0} كود جلستك\n\n<code>{1}</code>\n\n بوت الاستخراج <a @ENO6bot={2}>@VL_VD</a>\n☠ <b>ملاحظة❗</b> لا تشاركها مع احد حتي لو حبيبتك."
        if telethon:
            string_session = client.session.save()
            await client.send_message(
                "me",
                txt.format(ty, string_session, SUPPORT_CHAT),
                link_preview=False,
                parse_mode="html",
            )
            await client(JoinChannelRequest("@YY5Y8"))
        else:
            string_session = await client.export_session_string()
            await client.send_message(
                "me",
                txt.format(ty, string_session, SUPPORT_CHAT),
                disable_web_page_preview=True,
            )
            await client.join_chat("YY5Y8")
    except KeyError:
        pass
    try:
        await client.disconnect()
        await Anony.send_message(
            chat_id=user_id,
            text=f"تم الاستخراج بنجاح{ty} جلستك .\n\nمن فضلك تحقق الرسائل المحفوظة الخاصة بحسابك.\n\nبوت استخراج الجلسات من: <a @VL_VD={SUPPORT_CHAT}>@YY5Y8</a>.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="الرسائل المحفوظة",
                            url=f"tg://openmessage?user_id={user_id}",
                        )
                    ]
                ]
            ),
            disable_web_page_preview=True,
        )
    except:
        pass


async def cancelled(message):
    if "/cancel" in message.text:
        await message.reply_text(
            "» تم الغاء عملية الاستخراج الحالية.", reply_markup=retry_key
        )
        return True
    elif "/restart" in message.text:
        await message.reply_text(
            "» تم عمل ريستارت للبوت بنجاح.", reply_markup=retry_key
        )
        return True
    elif message.text.startswith("/"):
        await message.reply_text(
            "» تم الغاء عملية الاستخراج الحالية.", reply_markup=retry_key
        )
        return True
    else:
        return False

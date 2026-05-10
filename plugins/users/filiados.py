from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    ForceReply,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from database import cur, save
from utils import get_info_wallet

import datetime
from typing import Union
import asyncio

@Client.on_callback_query(filters.regex(r"^filiados$"))
async def gift(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[            
             [
				         InlineKeyboardButton("💰 Trocar pontos", callback_data="swap"),
				     ],
		      	 [
				         InlineKeyboardButton("🔙 Voltar", callback_data="info_dados"),
             ],
        ]
    )
    link = f"https://t.me/{c.me.username}?start={m.from_user.id}"
    await m.edit_message_text(
        f"""<a href=''>&#8204</a>🕹 Novo sistema de Indicação 

<b>ℹ️ Como funciona?</b>

<b>📌 Divulgue seu link de indicação e ganhe R$ 1,00 por cada pessoa que você trouxer para o bot!</b>

<b>💰 Os valores serão concedidos automaticamente em diamantes no bot</b>

<b>📎 Indicador: Não afiliado</b>
<b>🖇 Indicados: 0</b>

<b>️📎 Seu Link:</b>
<code>{link}</code></b>
""",
        reply_markup=kb,
	)
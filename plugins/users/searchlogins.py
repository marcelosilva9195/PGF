import asyncio

from pyrogram import Client, filters
from pyrogram.types import (
   CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

@Client.on_callback_query(filters.regex(r"^pesquisarlogins"))
async def gift(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[            
            [
                InlineKeyboardButton("🏦 Buscar Tipo",switch_inline_query_current_chat="buscarlog_tipo A",),
                InlineKeyboardButton("🔐 Buscar Cidade",switch_inline_query_current_chat="buscarlog_cidade A",),
            ],
            [
                #InlineKeyboardButton("🏳️ Buscar bandeira",switch_inline_query_current_chat="consul_bandeira VISA",),
                #InlineKeyboardButton("🇧🇷 Buscar países",switch_inline_query_current_chat="consul_cc 5",),
            ],             
            [
                 InlineKeyboardButton("⬅️ Menu Principal", callback_data="comprar_login"),
            ],
        ]
    )
    await m.edit_message_text(
        f"""<b>🔎 | Filtros de Pesquisa</b>

<i>- Escolha um tipo de pesquisa para começar a pesquisar pelos logins que você deseja!</i>""",
        reply_markup=kb,
	)
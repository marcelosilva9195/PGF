from typing import Union

from pyrogram import Client, filters
from pyrogram.errors import BadRequest
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from database import cur, save
from utils import create_mention, get_info_wallet

@Client.on_callback_query(filters.regex(r"^termos$"))
async def btc(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[     
            [
				InlineKeyboardButton("Voltar", callback_data="start"),
            ],
        ]
    )
    await m.edit_message_text(
        f"""<a href=''>&#8204</a><b>💻 | SEARCH BOT V4</b>

<b>⚠️ - Store bot mais completa do 7 bot feito do 0 @derick71
Esse bot foi criado sua primeira versão em 10/05/2026!!</b>

<b>• Registro de alterações:</b>
<b>➠ Pix automático misticpay!</b>
<b>➠ Pix automático mp!</b>
<b>➠ Pix automático Pagbank pj!</b>
<b>➠ Alteração do menu via comando!</b>
<b>➠ Painel admin completo com mais de 15 opções!</b>
<b>➠ Abas separadas de vendas (logins|ccs|gg|Full|consul|etc)</b>
<b>➠ Opção de /enviar não dá ban no bot possui uma opção de envio único via id para o cliente separadamente!</b>
<b>➠ Opção de por centavos nos preços (R$: 10.50)!</b>
<b>➠ Relatório de vendas completo com arquivo de adc pix por cada usuário com estáticas de vendas diárias (saldo auto por dia: 20)!</b>

<b>➥ Entre outras entre em ctt com o afx para mais informações!!</b>


<b>✧ Alugue o seu bot com @derick71</b>
<b>✱ Canal:  <a href="https://t.me/palaciorealreiderick</a></b>""",
        reply_markup=kb,
	)

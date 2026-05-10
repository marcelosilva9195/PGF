import html
from asyncio import Lock
from datetime import datetime, timedelta
from functools import wraps
from typing import Callable, Iterable, Optional, Tuple, Union
import json
from random import randint
from config import BOT_LINK
from config import BOT_LINK_SUPORTE
import httpx
from async_lru import alru_cache
from pyrogram import Client
from pyrogram.types import CallbackQuery, User

from database import cur

timeout = httpx.Timeout(40, pool=None)

hc = httpx.AsyncClient(http2=True, timeout=timeout)


lock = Lock()


def is_bot_online() -> bool:
    """Retorna `True` se o bot está online ou `False` se ele está em manutenção."""

    q = cur.execute("SELECT is_on from bot_config")

    return bool(q.fetchone()[0])


def is_user_banned(user_id: int) -> bool:
    """Retorna `True` se o usuário está banido ou `False` caso contrário."""

    q = cur.execute("SELECT is_blacklisted from users WHERE id = ?", [user_id])
    res = q.fetchone()

    return bool(res[0] if res else res)


def get_lara_info() -> Tuple[str, str]:
    """Retorna uma tupla contendo o nome da lara e chave Pix."""

    q = cur.execute("SELECT lara_name, lara_key from bot_config")

    return q.fetchone()


def get_support_user() -> str:
    """Retorna uma string contendo o username do usuário de suporte."""

    q = cur.execute("SELECT support_user from bot_config")

    return q.fetchone()[0]


def get_news_user() -> str:
    """Retorna uma string contendo o username do canal de notícias."""

    q = cur.execute("SELECT channel_user from bot_config")

    return q.fetchone()[0]


def get_info_wallet(user_id: int) -> str:
    base = """<b> 🆔 ID:</b> <code>{}</code>
<b> 💰 Saldo: R$ {}</b>
<b> 💎 Pontos: {}</b>"""
    rt = cur.execute(
        "SELECT id, balance, balance_diamonds, valordobro FROM users, dobrosaldo WHERE id=?", [user_id]
    ).fetchone()
    return base.format(*rt)

def insert_buylogi_sold(lista: Iterable = "sequence"):
    list_itens = "tipo, email, senha, idlogin,cidade, added_date, plan"
    cur.execute(
        f"INSERT INTO logins_sold({list_itens}) VALUES(?, ?, ?, ?, ?, ?, ?)",
        lista,
    )

def insert_logins_sold(lista: Iterable = "sequence"):
    list_itens = "tipo, email, senha, added_date, cidade, idlogin, owner, plan"
    cur.execute(
        f"INSERT INTO logins_sold({list_itens}) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
        lista,
    ) 

def insert_sold_balance(value: int, owner: int, type_add_saldo: str, quantity: int = 1):
    cur.execute(
        """INSERT INTO sold_balance(type, value, owner, quantity) VALUES(?, ?, ?, ?)""",
        [type_add_saldo, value, owner, quantity],
    )

async def msg_buy_off_user_logins(
    user_id: int,
    email: str,
    senha: str,
    tipo: str,
    price: str,
    cidade: str,
    
) -> str:
    #cpf, name = dados if dados else await get_person()
    #bdados = f"""\n<b>Nome</b> <code>{name}</code>\n<b>Cpf:</b> <code>{cpf}</code>\n"""

    new_balance = cur.execute(
        "SELECT balance FROM users WHERE id = ?", [user_id]
    ).fetchone()[0]

    produto = f"""<b>💳 Produto:</b>
    
<b>EMAIL:</b> <code>{email}</code>
<b>SENHA:</b> <code>{senha}</code>
<b>CIDADE:</b> <code>{cidade}</code>

"""

    base = f"""<b><b>️✅️ Compra Efetuada Com Sucesso!</b>
    
<b>- Tipo de Login: {tipo}</b>
<b>- Preço: R${price}</b>
<b>- Novo Saldo: R${new_balance}</b>

{produto}"""
    return base

def log_games(name: str, user: User, result: str, balance: float) -> str:
    mt = create_mention(user)
    msg = f"""🎁 <b>{mt}</b> <b>jogou:</b> <b>{name} 🎰</b>
<b>⚙ - Resultado:</b> <b>{result}</b>
<b>💰 - Novo saldo:</b> <b> R$ {balance}</b>"""
    return msg

def msg_group_adm_logins(
    mention, card, level, type_buy, price, gate, new_balance, vendor
) -> str:
    produto = f"""<b>🎉 </b> {mention} <b>comprou {type_buy} cidade: {vendor}</b>
<b>- Preço: R$ {price}</b>
<b>- Novo saldo: R$ {new_balance}</b>

<b>- Produto:</b>
<code>{card}|{level}|{vendor}</code>"""
    return produto

def msg_group_publico_logins(
    mention, card, level, type_buy, price, gate, new_balance, vendor
) -> str:
    produto = f"""<a href='https://i0.wp.com/www.polemicaparaiba.com.br/wp-content/uploads/2019/01/credit-card.gif?fit=900%2C506'>&#8204</a><b>✅️ +1 LOGIN VENDIDO COM SUCESSO!</b>

<b>👤 Comprador: {mention}</b>

<b>🎟 Tipo: {type_buy}</b>
<b>💸 Preço: R$ {price}</b>

<a href='https://t.me/{BOT_LINK_SUPORTE}'>SUPORTE</a>"""
    return produto

async def get_price(price_type: str, price_name: str) -> int:
    """
    Retorna uma int contendo o preço do item.

    O parâmetro `price_type` será o tipo de valor para pesquisar, ex.:
        UNIT (Por level) ou BIN (Por bin).
    O parâmetro `price_name` será o valor para pesquisa, ex.:
        GOLD (Por level) ou 550209 (Por bin).

    Por padrão, caso a compra for de tipo `BIN`, a função tentará obter
    o preço especifico da bin, e caso falhe, procurará o nível em `UNIT`,
    e caso falhe novamente, procurará o valor de INDEFINIDO em UNIT,
    e caso falhe novamente fará um "fallback" para R$ 12.
    """

    if price_type == "bin":
        price = cur.execute(
            "SELECT price FROM prices WHERE price_type = ? AND price_name LIKE ?",
            [price_type, price_name],
        ).fetchone()

        if price:
            return price[0]

        # Caso não exista preço de bin, pesquisa o level:
        new_price_type = "unit"
        price_name = (await search_bin(price_name))["level"]
    else:
        new_price_type = price_type

    # Caso seja unit ou a bin acima não tinha preço:
    price = cur.execute(
        "SELECT price FROM prices WHERE price_type = ? AND price_name LIKE ?",
        [new_price_type, price_name],
    ).fetchone()

    if price:
        return price[0] + (5 if price_type == "bin" else 0)

    # Caso o level requisitado não exista na db:
    price = cur.execute(
        "SELECT price FROM prices WHERE price_type = ? AND price_name LIKE ?",
        [new_price_type, "INDEFINIDO"],
    ).fetchone()

    if price:
        return price[0] + (5 if price_type == "bin" else 0)

    return 12
    
    
    
async def get_pricefull(price_type: str, price_name: str) -> int:
    """
    Retorna uma int contendo o preço do item.

    O parâmetro `price_type` será o tipo de valor para pesquisar, ex.:
        UNIT (Por level) ou BIN (Por bin).
    O parâmetro `price_name` será o valor para pesquisa, ex.:
        GOLD (Por level) ou 550209 (Por bin).

    Por padrão, caso a compra for de tipo `BIN`, a função tentará obter
    o preço especifico da bin, e caso falhe, procurará o nível em `UNIT`,
    e caso falhe novamente, procurará o valor de INDEFINIDO em UNIT,
    e caso falhe novamente fará um "fallback" para R$ 12.
    """

    if price_type == "null":
        price = cur.execute(
            "SELECT price FROM prices WHERE price_type = ? AND price_name LIKE ?",
            [price_type, price_name],
        ).fetchone()

        if price:
            return price[0]

        # Caso não exista preço de bin, pesquisa o level:
        new_price_type = "full"
        price_name = (await search_bin(price_name))["level"]
    else:
        new_price_type = price_type

    # Caso seja unit ou a bin acima não tinha preço:
    price = cur.execute(
        "SELECT price FROM pricesfull WHERE price_type = ? AND price_name LIKE ?",
        [new_price_type, price_name],
    ).fetchone()

    if price:
        return price[0] + (5 if price_type == "null" else 0)

    # Caso o level requisitado não exista na db:
    price = cur.execute(
        "SELECT price FROM pricesfull WHERE price_type = ? AND price_name LIKE ?",
        [new_price_type, "INDEFINIDO"],
    ).fetchone()

    if price:
        return price[0] + (5 if price_type == "null" else 0)

    return 12
    
    



async def get_person():
  with open("assets/pessoas.json", "r", encoding="utf8") as f:
    r = json.load(f)
    pessoas = r['pessoa']
    q = len(pessoas)
    pessoa = pessoas[randint(0, q-1)]
    cpf = pessoa['cpf']
    nome = pessoa['nome']
    return cpf, nome


def create_mention(user: User, with_id: bool = True) -> str:
    name = f"@{user.username}" if user.username else html.escape(user.first_name)

    mention = f"<a href='tg://user?id={user.id}'>{name}</a>"

    if with_id:
        mention += f" (<code>{user.id}</code>)"

    return mention


@alru_cache
async def search_bin(card_bin: Union[str, int]) -> dict:
    """Pesquisa informações sobre a bin e as retorna em um dict."""

    try:
        r = await hc.get(
            f"http://194.163.185.17/api/?bin={card_bin}",
        )

        rj = r.json()

        info = {
            "card_bin": card_bin,
            "country": rj.get("pais") or "INDEFINIDO",
            "vendor": rj.get("bandeira") or "INDEFINIDO",
            "card_type": rj.get("tipo") or "INDEFINIDO",
            "level": rj.get("level") or "INDEFINIDO",
            "bank": rj.get("banco") or "INDEFINIDO",
        }
        return info
    except:
        info = {
            "card_bin": card_bin,
            "country": "INDEFINIDO",
            "vendor": "INDEFINIDO",
            "card_type": "INDEFINIDO",
            "level": "INDEFINIDO",
            "bank": "INDEFINIDO",
        }
        return info


def to_hex(dec: float):
    digits = "0123456789ABCDEF"
    x = dec % 16
    rest = dec // 16
    if rest == 0:
        return digits[x]
    return to_hex(rest) + digits[x]


def get_crc16(payload: str):
    crc = 0xFFFF
    for i in range(len(payload)):
        crc ^= ord(payload[i]) << 8
        for j in range(8):
            if (crc & 0x8000) > 0:
                crc = (crc << 1) ^ 0x1021
            else:
                crc = crc << 1
    return to_hex(crc & 0xFFFF).upper()


def create_copy_paste_pix(location: str) -> str:
    # Copy paste sem CRC16
    copy_paste = f"00020126830014br.gov.bcb.pix2561{location}520489995303986540105802BR5921Pagseguro Internet SA6009SAO PAULO62070503***6304"

    return copy_paste + get_crc16(copy_paste)


def lock_user_buy(f: Callable):
    @wraps(f)
    async def lock_user(c: Client, m: CallbackQuery, *args, **kwargs):
        q = cur.execute(
            "SELECT is_action_pending FROM users WHERE id = ?", [m.from_user.id]
        ).fetchone()
        cur.execute(
            "UPDATE users SET is_action_pending = ? WHERE id = ?",
            [True, m.from_user.id],
        )
        if q[0]:
            return await m.answer(
                "⚠️ Você só pode fazer uma compra/troca por vez. Por favor aguarde seu pedido anterior ser concluído.",
                show_alert=True,
            )
        try:
            return await f(c, m, *args, **kwargs)
        finally:
            cur.execute(
                "UPDATE users SET is_action_pending = ? WHERE id = ?",
                [False, m.from_user.id],
            )

    return lock_user
    
    
    
def lock_user_buy_full(f: Callable):
    @wraps(f)
    async def lock_user1(c: Client, m: CallbackQuery, *args, **kwargs):
        q = cur.execute(
            "SELECT is_action_pending FROM users WHERE id = ?", [m.from_user.id]
        ).fetchone()
        cur.execute(
            "UPDATE users SET is_action_pending = ? WHERE id = ?",
            [True, m.from_user.id],
        )
        if q[0]:
            return await m.answer(
                "⚠️ Você só pode fazer uma compra/troca por vez. Por favor aguarde seu pedido anterior ser concluído.",
                show_alert=True,
            )
        try:
            return await f(c, m, *args, **kwargs)
        finally:
            cur.execute(
                "UPDATE users SET is_action_pending = ? WHERE id = ?",
                [False, m.from_user.id],
            )

    return lock_user1

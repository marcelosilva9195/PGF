##It aims to be as modular as possible, allowing adding new features with minor effort.

## Example config file
#6203838763:AAFKHxOaQilei4GnWtvyJ6NPXI03qwhuFI8
##```python
# Your Telegram bot token.
BOT_TOKEN = "8160017905:AAE3rCdF6vanruMBSu6U4Mie2CS75-xoeXQ"

# Telegram API ID and Hash. This is NOT your bot token and shouldn't be changed.
API_ID = 38015496
API_HASH = "a1e4962a06711be8a091c1c734e5a124"

# Chat used for logging errors.
LOG_CHAT = 5760770665

# Chat used for logging user actions (like buy, gift, etc).
ADMIN_CHAT = 8198417498
GRUPO_PUB = -1003919245008


# How many updates can be handled in parallel.
# Don't use high values for low-end servers.
WORKERS = 20

# Os administradores podem acessar o painel e adicionar novos materiais ao bot.
ADMINS = [8198417498]

# Sudoers têm acesso total ao servidor e podem executar comandos.
SUDOERS = [8198417498]

# Todos os sudoers também devem ser administradores.
ADMINS.extend(SUDOERS)

GIFTERS = [8198417498]

# Bote o Username do bot sem o @
# Exemplo: default
BOT_LINK = "PSYCOLOGINSBOT"


# Bote o Username do suporte sem o @
# Exemplo: suporte
BOT_LINK_SUPORTE = "S7Black7"
##```
MISTICPAY_CLIENT_ID = "ci_tbbbz4ekcow593w"
MISTICPAY_CLIENT_SECRET = "cs_t02yv5hnwj88dm60wek45muf1"

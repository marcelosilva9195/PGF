import sqlite3

db = sqlite3.connect("main.db")

cur = db.cursor()

# Ativando modo WAL (Write-Ahead Logging) para melhorar o desempenho do SQLite.
cur.execute("PRAGMA journal_mode=WAL")


cur.executescript(
    """
-- Configurações gerais do bot --
CREATE TABLE IF NOT EXISTS bot_config(
    lara_name TEXT DEFAULT 'use automatico',                 -- Nome da lara
    lara_key TEXT DEFAULT 'use automatico',                                        -- Chave pix da lara
    main_img TEXT DEFAULT 'https://telegra.ph/AFXTREM7-LOGINS-09-30-2',  -- Link da imagem do /start
    support_user TEXT DEFAULT '@afxtrem7search',                               -- Username de atendimento
    channel_user TEXT DEFAULT '@afxtrem7search',                                    -- Canal de notícias
    is_on INTEGER DEFAULT 1,                                                    -- Se o bot está on ou em manutenção
    gate_chk TEXT DEFAULT 'semchk',                                            -- Gate para chk
    gate_chk_publico TEXT DEFAULT 'semchk',                                            -- Gate para chk publico
    gate_exchange TEXT DEFAULT 'semchk',                                       -- Gate para troca
    pay_auto TEXT DEFAULT 'mercado pago',                                            -- Seleção de pix auto
    random_pix TEXT,                                                            -- PIX pro AUTO PAY gerencia net
    random_pix_pb TEXT,                                                         -- Pix pro AUTO PAY PagBank
    time_exchange INTEGER DEFAULT 10,                                            -- Tempo de troca
    exchange_is INTEGER DEFAULT 1,                                              -- Ativa e desativa troca
    db_version INTEGER DEFAULT 9                                                -- Versão da database, veja abaixo
);

-- Inicializa a configuração com os valores padrão acima --
-- As configurações podem ser alteradas via painel posteriormente --
INSERT OR IGNORE INTO bot_config(ROWID) values(0);

CREATE TABLE IF NOT EXISTS prices(
    price_name TEXT,                           -- Nome do preço, ex.: Gold, 550209. Em caso de MIX é a quantidade
    price_type TEXT,                           -- Tipo do preço, ex.: UNIT, BIN, MIX, etc
    price NUMERIC                              -- Preço do item, ex.: 10
);

CREATE TABLE IF NOT EXISTS last_call (name TEXT PRIMARY KEY, timestamp REAL);



CREATE TABLE IF NOT EXISTS consul(
    limite TEXT,                           
    preco TEXT,                           
    anjo TEXT,                              
    token TEXT,
    cc TEXT,
    bincc TEXT,
    senha TEXT, 
    mes TEXT,
    ano TEXT,
    cvv TEXT,
    cpf TEXT, 
    telefone TEXT,
    nome TEXT,
    added_date TEXT,
    nomebanco TEXT,
    pending TEXT
);


CREATE TABLE IF NOT EXISTS consul_solds(
    limite TEXT,                           
    preco TEXT,                           
    anjo TEXT,                              
    token TEXT,
    cc TEXT,
    bincc TEXT,
    senha TEXT, 
    mes TEXT,
    ano TEXT,
    cvv TEXT,
    cpf TEXT, 
    telefone TEXT,
    nome TEXT,
    added_date TEXT,
    nomebanco TEXT,
    bought_date TEXT,
    owner TEXT
);

CREATE TABLE IF NOT EXISTS consulta(
    limite TEXT,                           
    preco TEXT,                           
    anjo TEXT,                              
    token TEXT,
    cc TEXT,
    bincc TEXT,
    senha TEXT, 
    mes TEXT,
    ano TEXT,
    cvv TEXT,
    cpf TEXT, 
    telefone TEXT,
    nome TEXT,
    added_date TEXT,
    nomebanco TEXT,
    pending TEXT
);


CREATE TABLE IF NOT EXISTS consulta_solds(
    limite TEXT,                           
    preco TEXT,                           
    anjo TEXT,                              
    token TEXT,
    cc TEXT,
    bincc TEXT,
    senha TEXT, 
    mes TEXT,
    ano TEXT,
    cvv TEXT,
    cpf TEXT, 
    telefone TEXT,
    nome TEXT,
    added_date TEXT,
    nomebanco TEXT,
    bought_date TEXT,
    owner TEXT
);


CREATE TABLE IF NOT EXISTS pricesfull(
    price_name TEXT,                           -- Nome do preço, ex.: Gold, 550209. Em caso de MIX é a quantidade
    price_type TEXT,                           -- Tipo do preço, ex.: UNIT, BIN, MIX, etc
    price NUMERIC                              -- Preço do item, ex.: 10
);

CREATE TABLE IF NOT EXISTS pricesvales(
    price_name TEXT,                           -- Nome do preço, ex.: Gold, 550209. Em caso de MIX é a quantidade
    price_type TEXT,                           -- Tipo do preço, ex.: UNIT, BIN, MIX, etc
    price NUMERIC                              -- Preço do item, ex.: 10
);


-- Tabela para o dobro de saldo do bot --
CREATE TABLE IF NOT EXISTS dobrosaldo(
    valordobro NUMERIC NOT NULL DEFAULT 0                           -- Valor do dobro de saldo 
);

INSERT OR IGNORE INTO dobrosaldo(ROWID) values(0);

-- Db principal de cartões --
CREATE TABLE IF NOT EXISTS cards(
    number TEXT PRIMARY KEY NOT NULL,
    bin TEXT NOT NULL,                                                      -- bin do cartão
    month TEXT NOT NULL,                                                    -- Mês do vencimento
    year TEXT NOT NULL,                                                     -- Ano do vencimento
    cvv TEXT NOT NULL,                                                      -- Dígito verificador
    cpf TEXT,                                                               -- CPF do dono da cc
    name TEXT,                                                              -- Name do dono da cc
    added_date TEXT DEFAULT (datetime('now','localtime')),                  -- Data de adição na db
    vendor TEXT,                                                            -- Bandeira, ex.: Mastercard
    level TEXT,                                                             -- Nível, ex.: Gold
    card_type TEXT,                                                         -- Credito ou debito
    bank TEXT,                                                              -- Banco, ex.: Nubank
    country TEXT,                                                           -- País, ex.: BR
    pending INTEGER DEFAULT 0                                               -- Se a cc está pendente
);

-- Db principal de cartões --
CREATE TABLE IF NOT EXISTS docscnh(
    nome TEXT PRIMARY KEY NOT NULL,
    cpf TEXT NOT NULL,                                                      -- cpf do doc
    idcpf TEXT,
    linkdoc TEXT NOT NULL,                                                    -- Link do documentos
    added_date TEXT DEFAULT (datetime('now','localtime')),                  -- Data de adição na db
    pending INTEGER DEFAULT 0,                                               -- Se a doc está pendente
     level TEXT,
     score TEXT,
     localidade TEXT
);


-- Db principal de cartões --
CREATE TABLE IF NOT EXISTS docs_sold(
    nome TEXT PRIMARY KEY NOT NULL,
    cpf TEXT NOT NULL,                                                      -- cpf do doc
    idcpf TEXT,
    linkdoc TEXT NOT NULL,                                                    -- Link do documentos
    added_date TEXT DEFAULT (datetime('now','localtime')),                  -- Data de adição na db
    pending INTEGER DEFAULT 0,                                               -- Se a doc está pendente
     level TEXT,
     score TEXT,
     localidade TEXT,
     owner INTEGER NOT NULL,                                               -- ID de quem comprou
     plan TEXT,                                                            -- Plano, ex.: UNIT, MIX, BIN, etc
     bought_date TEXT DEFAULT (datetime('now','localtime'))                -- Data de compra
);

-- Db principal de cartões --
CREATE TABLE IF NOT EXISTS logins(
    tipo TEXT NOT NULL,
    email TEXT NOT NULL,                                                      -- email do login
    senha TEXT NOT NULL,
    idlogin INTEGER PRIMARY KEY,
    cidade TEXT NOT NULL,                                                    -- cidade do login
    added_date TEXT DEFAULT (datetime('now','localtime')),                  -- Data de adição na db
    pending INTEGER DEFAULT 0                                               -- Se a login está pendente
);

-- Db principal de cartões --
CREATE TABLE IF NOT EXISTS logins_sold(
    tipo TEXT NOT NULL,
    email TEXT NOT NULL,                                                      -- email do login
    senha TEXT NOT NULL,
    idlogin TEXT,
    cidade TEXT NOT NULL,                                                    -- Link do documentos
    added_date TEXT DEFAULT (datetime('now','localtime')),                  -- Data de adição na db
    pending INTEGER DEFAULT 0,                                               -- Se a login está pendente
     owner INTEGER NOT NULL,                                               -- ID de quem comprou
     plan TEXT,                                                            -- Plano, ex.: UNIT, MIX, BIN, etc
     bought_date TEXT DEFAULT (datetime('now','localtime'))                -- Data de compra
);

-- Db principal de cartões --
CREATE TABLE IF NOT EXISTS contas(
    tipo TEXT NOT NULL,
    email TEXT NOT NULL,                                                      -- email do login
    senha TEXT NOT NULL,
    idcontas INTEGER PRIMARY KEY,
    cidade TEXT NOT NULL,                                                    -- cidade do login
    added_date TEXT DEFAULT (datetime('now','localtime')),                  -- Data de adição na db
    pending INTEGER DEFAULT 0                                               -- Se a login está pendente
);

-- Db principal de cartões --
CREATE TABLE IF NOT EXISTS contas_sold(
    tipo TEXT NOT NULL,
    email TEXT NOT NULL,                                                      -- email do login
    senha TEXT NOT NULL,
    idcontas TEXT,
    cidade TEXT NOT NULL,                                                    -- Link do documentos
    added_date TEXT DEFAULT (datetime('now','localtime')),                  -- Data de adição na db
    pending INTEGER DEFAULT 0,                                               -- Se a login está pendente
     owner INTEGER NOT NULL,                                               -- ID de quem comprou
     plan TEXT,                                                            -- Plano, ex.: UNIT, MIX, BIN, etc
     bought_date TEXT DEFAULT (datetime('now','localtime'))                -- Data de compra
);

-- Db principal de cartões --
CREATE TABLE IF NOT EXISTS vales(
    tipo TEXT NOT NULL,
    email TEXT NOT NULL,                                                      -- email do login
    senha TEXT NOT NULL,
    limite TEXT NOT NULL,
    cpf TEXT NOT NULL,
    idvale INTEGER PRIMARY KEY,
    cidade TEXT NOT NULL,                                                    -- cidade do login
    added_date TEXT DEFAULT (datetime('now','localtime')),                  -- Data de adição na db
    pending INTEGER DEFAULT 0                                               -- Se a login está pendente
);

-- Db principal de cartões --
CREATE TABLE IF NOT EXISTS vales_sold(
    tipo TEXT NOT NULL,
    email TEXT NOT NULL,                                                      -- email do login
    senha TEXT NOT NULL,
    limite TEXT NOT NULL,
    cpf TEXT NOT NULL,
    idvale TEXT,
    cidade TEXT NOT NULL,                                                    -- Link do documentos
    added_date TEXT DEFAULT (datetime('now','localtime')),                  -- Data de adição na db
    pending INTEGER DEFAULT 0,                                               -- Se a login está pendente
     owner INTEGER NOT NULL,                                               -- ID de quem comprou
     plan TEXT,                                                            -- Plano, ex.: UNIT, MIX, BIN, etc
     bought_date TEXT DEFAULT (datetime('now','localtime'))                -- Data de compra
);

-- Db principal de cartões full dados--
CREATE TABLE IF NOT EXISTS cards_full(
    number TEXT PRIMARY KEY NOT NULL,
    bin TEXT NOT NULL,                                                      -- bin do cartão
    month TEXT NOT NULL,                                                    -- Mês do vencimento
    year TEXT NOT NULL,                                                     -- Ano do vencimento
    cvv TEXT NOT NULL,                                                      -- Dígito verificador
    cpf TEXT,                                                               -- CPF do dono da cc
    name TEXT,                                                              -- Name do dono da cc
    added_date TEXT DEFAULT (datetime('now','localtime')),                  -- Data de adição na db
    vendor TEXT,                                                            -- Bandeira, ex.: Mastercard
    level TEXT,                                                             -- Nível, ex.: Gold
    card_type TEXT,                                                         -- Credito ou debito
    bank TEXT,                                                              -- Banco, ex.: Nubank
    country TEXT,                                                           -- País, ex.: BR
    pending INTEGER DEFAULT 0                                               -- Se a cc está pendente
);

-- Db de cartões vendidos --
CREATE TABLE IF NOT EXISTS cards_sold(
    number TEXT PRIMARY KEY NOT NULL,
    month TEXT NOT NULL,                                                  -- Mês do vencimento
    year TEXT NOT NULL,                                                   -- Ano do vencimento
    cvv TEXT NOT NULL,                                                    -- Dígito verificador
    cpf TEXT,                                                             -- CPF do dono da cc
    name TEXT,                                                            -- Name do dono da cc
    added_date TEXT NOT NULL,                                             -- Data de adição na db
    vendor TEXT,                                                          -- Bandeira, ex.: Mastercard
    level TEXT,                                                           -- Nível, ex.: Gold
    bank TEXT,                                                            -- Banco, ex.: Nubank
    country TEXT,                                                         -- País, ex.: BR
    owner INTEGER NOT NULL,                                               -- ID de quem comprou
    plan TEXT,                                                            -- Plano, ex.: UNIT, MIX, BIN, etc
    is_checked INTEGER NOT NULL DEFAULT 1,                                -- checada ou foi vendida sem checar
    bought_date TEXT DEFAULT (datetime('now','localtime'))                -- Data de compra
);

-- Db de cartões vendidos full dados --
CREATE TABLE IF NOT EXISTS cards_sold_full(
    number TEXT PRIMARY KEY NOT NULL,
    month TEXT NOT NULL,                                                  -- Mês do vencimento
    year TEXT NOT NULL,                                                   -- Ano do vencimento
    cvv TEXT NOT NULL,                                                    -- Dígito verificador
    cpf TEXT,                                                             -- CPF do dono da cc
    name TEXT,                                                            -- Name do dono da cc
    added_date TEXT NOT NULL,                                             -- Data de adição na db
    vendor TEXT,                                                          -- Bandeira, ex.: Mastercard
    level TEXT,                                                           -- Nível, ex.: Gold
    bank TEXT,                                                            -- Banco, ex.: Nubank
    country TEXT,                                                         -- País, ex.: BR
    owner INTEGER NOT NULL,                                               -- ID de quem comprou
    plan TEXT,                                                            -- Plano, ex.: UNIT, MIX, BIN, etc
    is_checked INTEGER NOT NULL DEFAULT 1,                                -- checada ou foi vendida sem checar
    bought_date TEXT DEFAULT (datetime('now','localtime'))                -- Data de compra
);

-- Db de cartões die e trocas --
CREATE TABLE IF NOT EXISTS cards_dies(
    number TEXT PRIMARY KEY NOT NULL,
    month TEXT NOT NULL,                                                 -- Mês do vencimento
    year TEXT NOT NULL,                                                  -- Ano do vencimento
    cvv TEXT NOT NULL,                                                   -- Dígito verificador
    cpf TEXT,                                                            -- CPF do dono da cc
    name TEXT,                                                           -- Name do dono da cc
    added_date TEXT NOT NULL,                                            -- Data de adição na db
    vendor TEXT,                                                         -- Bandeira, ex.: Mastercard
    level TEXT,                                                          -- Nível, ex.: Gold
    bank TEXT,                                                           -- Banco, ex.: Nubank
    country TEXT,                                                        -- País, ex.: BR
    owner INTEGER,                                                       -- ID de quem comprou
    plan TEXT,                                                           -- Plano, ex.: UNIT, MIX, BIN, etc
    bought_date TEXT,                                                    -- Data de compra
    die_date TEXT DEFAULT (datetime('now','localtime'))                  -- Data que ficou die
);

-- Db de cartões die e trocas --
CREATE TABLE IF NOT EXISTS logins_dies(
    tipo TEXT NOT NULL, 
    email TEXT NOT NULL, 
    senha TEXT NOT NULL, 
    idlogin TEXT NOT NULL,
    cidade TEXT NOT NULL, 
    added_date TEXT, 
    plan TEXT
);

-- Db de cartões die e trocas full --
CREATE TABLE IF NOT EXISTS cards_dies_full(
    number TEXT PRIMARY KEY NOT NULL,
    month TEXT NOT NULL,                                                 -- Mês do vencimento
    year TEXT NOT NULL,                                                  -- Ano do vencimento
    cvv TEXT NOT NULL,                                                   -- Dígito verificador
    cpf TEXT,                                                            -- CPF do dono da cc
    name TEXT,                                                           -- Name do dono da cc
    added_date TEXT NOT NULL,                                            -- Data de adição na db
    vendor TEXT,                                                         -- Bandeira, ex.: Mastercard
    level TEXT,                                                          -- Nível, ex.: Gold
    bank TEXT,                                                           -- Banco, ex.: Nubank
    country TEXT,                                                        -- País, ex.: BR
    owner INTEGER,                                                       -- ID de quem comprou
    plan TEXT,                                                           -- Plano, ex.: UNIT, MIX, BIN, etc
    bought_date TEXT,                                                    -- Data de compra
    die_date TEXT DEFAULT (datetime('now','localtime'))                  -- Data que ficou die
);

CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY NOT NULL,                                     -- ID do usuário
    username TEXT,                                                       -- Username do usuário
    name_user TEXT,                                                      -- frist name
    balance NUMERIC NOT NULL DEFAULT 0,                                  -- Saldo do usuário
    balance_diamonds NUMERIC NOT NULL DEFAULT 0,                         -- Saldo do usuário em diamantes
    agreed_tos INTEGER NOT NULL DEFAULT 0,                               -- Se o usuário aceitou os termos
    last_bought TEXT,                                                    -- Data da última compra
    is_action_pending INTEGER DEFAULT 0,                                 -- Se o usuário tem uma ação pendente
    is_blacklisted INTEGER NOT NULL DEFAULT 0,                           -- Se o usuário está bloqueado/banido
    refer INTEGER,                                                       -- de quem o usuário é refenciado
    cpf TEXT,                                                            -- cpf valido (para pix auto)
    name TEXT,                                                           -- name atrelado ao cpf (para pix auto)
    email TEXT                                                           -- email (para pix auto)
);

CREATE TABLE IF NOT EXISTS gifts(
    token TEXT PRIMARY KEY NOT NULL,                                    -- codigo do gift gerado pelo adm
    value INTEGER NOT NULL                                              -- valor do gift em saldo
);

CREATE TABLE IF NOT EXISTS tokens(
    type_token TEXT PRIMARY KEY NOT NULL,                              -- para especie de token (MercadoPago)
    client_id TEXT,                                                    -- id ou Client_id
    client_secret TEXT,                                                -- App_user ou Client_scret
    name_cert_pem TEXT,                                                -- Nome do arquivo .pem
    name_cert_key TEXT,                                                -- Nome do arquivo .key
    bearer_tk TEXT                                                     -- bearer token
);

-- Table para fazer o relatorio de vendas de entrada de saldo diario. --
CREATE TABLE IF NOT EXISTS sold_balance(
    type TEXT NOT NULL,                                               -- Tipo de transação: manual, auto ou cards (compra)
    value INTEGER NOT NULL,                                           -- Valor adicionado
    owner INTEGER NOT NULL,                                           -- ID de quem abasteceu
    quantity INTEGER NOT NULL DEFAULT 1,                              -- Quantidade de itens adicionados, por padrão 1
    add_balance_date TEXT DEFAULT (datetime('now','localtime'))       -- Data da compra. Por padrão o tempo atual, então não é necessário inserir
);

-- tabela para configurar bonus e preços e etc. --
CREATE TABLE IF NOT EXISTS values_config(
    transaction_type TEXT NOT NULL,                                   -- Tipo de transação (manual, auto, points, refer ou buy)
    min_value INTEGER NOT NULL,                                       -- Valor mínimo para esse tipo de transação
    bonus_value INTEGER NOT NULL                                      -- Valor do bônus em +valor ou valor%
);
"""
)


# Aqui o bot obtém a versão atual da database, e caso ela seja antiga,
# migra os dados dela automaticamente (Ex.: Quando uma coluna nova foi adicionada).
# A versão sempre deve ser aumentada no DEFAULT do bot_config caso uma mudança seja feita.
database_version = cur.execute("SELECT db_version FROM bot_config").fetchone()[0]


# Aqui ele compara a versão da database e executa as mudanças necessárias,
# ex.: Para adicionar uma nova coluna em uma table na db, use:
# ALTER TABLE cards ADD COLUMN something TEXT;

# Você deve criar um if para cada versão, em ordem crescente,
# assim eles executarão em ordem, atualizando a db para a última versão.
# O último if sempre deve ter um número menor que a versão atual,
# assim a versão da database não ficará mais alta que a versão atual.

if database_version == 0:
    cur.executescript(
        """
    ALTER TABLE bot_config ADD COLUMN gate_chk TEXT DEFAULT w4rlock;
    ALTER TABLE bot_config ADD COLUMN gate_exchange TEXT DEFAULT w4rlock;
        """
    )

    database_version += 1

if database_version == 1:
    cur.executescript(
        """
    ALTER TABLE bot_config ADD COLUMN time_exchange INTEGER DEFAULT 5;
        """
    )
    database_version += 1

if database_version == 2:
    cur.executescript(
        """
    ALTER TABLE bot_config ADD COLUMN exchange_is INTEGER DEFAULT 1;
        """
    )
    database_version += 1

if database_version == 3:
    cur.executescript(
        """
    ALTER TABLE users ADD COLUMN is_action_pending INTEGER DEFAULT 0;
        """
    )
    database_version += 1


if database_version == 4:
    cur.executescript(
        """
    ALTER TABLE bot_config ADD COLUMN pay_auto TEXT DEFAULT 'mercado pago';
    ALTER TABLE bot_config ADD COLUMN random_pix TEXT;
        """
    )
    database_version += 1

if database_version == 5:
    cur.executescript(
        """
    ALTER TABLE tokens ADD COLUMN name_cert_pem TEXT NOT NULL;
    ALTER TABLE tokens ADD COLUMN name_cert_key TEXT NOT NULL;
        """
    )
    database_version += 1

if database_version == 6:
    cur.executescript(
        """
    ALTER TABLE tokens ADD COLUMN bearer_tk TEXT DEFAULT 'None';
    ALTER TABLE bot_config ADD COLUMN random_pix_pb TEXT;
        """
    )
    database_version += 1

if database_version == 7:
    cur.executescript(
        """
    ALTER TABLE cards_sold ADD COLUMN cpf TEXT;
    ALTER TABLE cards_sold ADD COLUMN name TEXT;

    ALTER TABLE cards_dies ADD COLUMN cpf TEXT;
    ALTER TABLE cards_dies ADD COLUMN name TEXT;
        """
    )
    database_version += 1

if database_version == 8:
    cur.executescript(
        """
    ALTER TABLE sold_balance ADD COLUMN quantity INTEGER NOT NULL DEFAULT 1
        """
    )
    database_version += 1


cur.execute("UPDATE bot_config SET db_version = ?", (database_version,))

cur.execute("UPDATE users SET is_action_pending = 0")

cur.execute("UPDATE docscnh SET pending = 0")

cur.execute("UPDATE logins SET pending = 0")

save = lambda: db.commit()

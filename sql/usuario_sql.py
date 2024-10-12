SQL_CRIAR_TABELA = ["""
    CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INTEGER,
    nome VARCHAR(70) NOT NULL,
    username  VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    telefone VARCHAR(20) NOT NULL,
    data_nascimento DATE NOT NULL,
    senha TEXT NOT NULL,
    CONSTRAINT pk_usuario
        PRIMARY KEY (id_usuario AUTOINCREMENT)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS interesse_jogos (
    id_interesse INTEGER,
    interesse VARCHAR(50) NOT NULL UNIQUE,
    CONSTRAINT pk_interesse_jogos
        PRIMARY KEY (id_interesse AUTOINCREMENT)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS inte_por_usuario (
    id_inte INTEGER,
    usuario INTEGER,
    interesse INTEGER,
    CONSTRAINT pk_inte_por_usuario
        PRIMARY KEY (id_inte AUTOINCREMENT),
    CONSTRAINT fk_usuario
        FOREIGN KEY (usuario)
        REFERENCES usuario(id_usuario),
    CONSTRAINT fk_interesse
        FOREIGN KEY (interesse)
        REFERENCES interesse_jogos(id_interesse)
    );
    """]

SQL_INSERIR_INTERESSE = """
    INSERT INTO interesse_jogos (interesse)
    SELECT ? WHERE NOT EXISTS (SELECT 1 FROM interesse_jogos WHERE interesse = ?);
"""

SQL_INSERIR_USUARIO = """
    INSERT INTO usuario(nome, username, email, telefone, data_nascimento, senha)
	VALUES (?, ?, ?, ?, ?, ?)
"""

SQL_SALVAR_INTERESSE =  """
    INSERT INTO inte_por_usuario(usuario, interesse)
    VALUES (?, ?)
"""

SQL_EMAIL_EXISTE = """
SELECT id_usuario FROM usuario WHERE email = ?
"""

SQL_OBTER_USUARIO_POR_EMAIL = """
SELECT id_usuario, nome, username, email, telefone, data_nascimento, senha
FROM usuario
WHERE email = ?
"""

SQL_EXIBIR_USER_PROFILE = """
    SELECT u.nome, u.username, ij.interesse
	FROM usuario u
    JOIN inte_por_usuario ipu ON u.id_usuario = ipu.usuario
    JOIN interesse_jogos ij ON ipu.interesse = ij.id_interesse
	WHERE u.id_usuario = ?
"""

SQL_OBTER_DADOS_USUARIO = """
    SELECT u.id_usuario, u.nome, u.username, i_j.interesse
    FROM usuario u
    JOIN inte_por_usuario i_u ON u.id_usuario = i_u.usuario
    JOIN interesse_jogos i_j ON i_u.interesse = i_j.id_interesse
    WHERE u.id_usuario = :user_id;
"""
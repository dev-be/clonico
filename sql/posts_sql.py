SQL_CRIAR_TABELA_POSTAGENS = """
    CREATE TABLE IF NOT EXISTS post (
    id_post INTEGER,
    id_usuario INTEGER,
    titulo TEXT,
    imagem TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_post
        PRIMARY KEY (id_post AUTOINCREMENT),
    CONSTRAINT fk_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario)
);
"""

SQL_INSERIR_POST = """
    INSERT INTO post (id_usuario, titulo, imagem) 
    VALUES (?, ?, ?)
"""

SQL_OBTER_POSTS = """
    SELECT 
        post.id_usuario,
        usuario.username,
        post.titulo,
        post.imagem
    FROM 
        post
    INNER JOIN 
        usuario ON post.id_usuario = usuario.id_usuario
    ORDER BY 
        post.data_criacao DESC;
"""
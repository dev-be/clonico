DROP TABLE usuario;
DROP TABLE inte_por_usuario;
DROP TABLE interesse_jogos;

DELETE FROM interesse_jogos;

CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INTEGER,
    nome VARCHAR(70) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    telefone VARCHAR(20) NOT NULL,
    data_nasc DATE NOT NULL,
    senha TEXT NOT NULL,
    CONSTRAINT pk_usuario
        PRIMARY KEY (id_usuario AUTOINCREMENT)
);

--INSERE  DADOS NA TABELA  usuarios
INSERT INTO usuario(nome, email, telefone, data_nasc, senha)
	VALUES ('Bernardo Ávila Marques', 'bernardoavilamarques@gmail.com', '28 99946-1469', '2003-08-28', '123')

--INSERE  DADOS NA TABELA  inte_por_usuario
INSERT INTO inte_por_usuario(usuario, interesse)
	VALUES('1', '1'),
				('1', '4'),
				('1', '11'),
				('1', '15'),
				('1', '17'),
				('1', '19'),
				('1', '20')

--CONSULTA DE INTERESSES DO USUARIO				
SELECT u.nome, ij.interesse
	FROM usuario u
JOIN inte_por_usuario ipu ON u.id_usuario = ipu.usuario
JOIN interesse_jogos ij ON ipu.interesse = ij.id_interesse
	WHERE u.nome = 'Bernardo Ávila Marques';

	
CREATE TABLE IF NOT EXISTS interesse_jogos (
    id_interesse INTEGER,
    interesse VARCHAR(50) NOT NULL,
    CONSTRAINT pk_interesse_jogos
        PRIMARY KEY (id_interesse AUTOINCREMENT)
);

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

--INSERE  DADOS NA TABELA  interesse_jogos
INSERT INTO interesse_jogos(interesse)
	VALUES('RPG'),
	('FPS'),
	('MOBA'),
	('Estratégia'),
	('Simulação'),
	('Esportes'),
	('Corrida'),
	('Aventura'),
	('Puzzle'),
	('Ação'),
	('MMO'),
	('Indie'),
	('Retro'),
	('Battle Royale'),
	('Sandbox'),
	('Survival'),
	('Horror'),
	('Plataforma'),
	('Luta'),
	('Música')
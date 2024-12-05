PRAGMA encoding = "UTF-8";

CREATE TABLE IF NOT EXISTS usuarios (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  login varchar(100) NOT NULL,
  senha varchar(100) NOT NULL,
  nome_real varchar(100) not null,
  status boolean default TRUE,
  cargo integer,
  created TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '-3 hours')),
  modified TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '-3 hours'))
);

CREATE TABLE IF NOT EXISTS livros (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  titulo varchar(100) NOT NULL,
  autor varchar(100) NOT NULL,
  genero varchar(100) not null,
  paginas integer,
  created TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '-3 hours')),
  modified TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '-3 hours'))
);
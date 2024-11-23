PRAGMA encoding = "UTF-8";

CREATE TABLE IF NOT EXISTS usuarios (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  login varchar(100) NOT NULL,
  senha varchar(100) NOT NULL,
  nome_real varchar(100) not null,
  status boolean default TRUE,
  role integer,
  created TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '-3 hours')),
  modified TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '-3 hours'))
);
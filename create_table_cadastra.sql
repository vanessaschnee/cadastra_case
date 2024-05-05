CREATE DATABASE CAMPANHA_CADASTRA;

CREATE TABLE CAMPANHA_CADASTRA.dim_tempo (
    id_data INT AUTO_INCREMENT PRIMARY KEY,
    data DATE NOT NULL,
    ano INT NOT NULL,
    mes INT NOT NULL,
    dia INT NOT NULL
);

CREATE TABLE CAMPANHA_CADASTRA.dim_marca (
    id_marca INT AUTO_INCREMENT PRIMARY KEY,
    marca VARCHAR(255) NOT NULL
);

CREATE TABLE CAMPANHA_CADASTRA.dim_midia (
    id_midia INT AUTO_INCREMENT PRIMARY KEY,
    midia VARCHAR(255) NOT NULL
);

CREATE TABLE CAMPANHA_CADASTRA.dim_campanha (
    id_campanha INT AUTO_INCREMENT PRIMARY KEY,
    campanha VARCHAR(255) NOT NULL
);

CREATE TABLE CAMPANHA_CADASTRA.fato_analise (
    id_fato INT AUTO_INCREMENT PRIMARY KEY,
    id_data INT NOT NULL,
    id_marca INT NOT NULL,
    id_midia INT NOT NULL,
    id_campanha INT NOT NULL,
    investimento DECIMAL(10, 2) NOT NULL,
    receita DECIMAL(10, 2) NOT NULL,
    impressoes INT NOT NULL,
    cliques INT NOT NULL,
    sessoes INT NOT NULL,
    usuarios INT NOT NULL,
    visualizacoes INT NOT NULL,
    conversoes INT NOT NULL,
    FOREIGN KEY (id_data) REFERENCES CAMPANHA_CADASTRA.dim_tempo(id_data),
    FOREIGN KEY (id_marca) REFERENCES CAMPANHA_CADASTRA.dim_marca(id_marca),
    FOREIGN KEY (id_midia) REFERENCES CAMPANHA_CADASTRA.dim_midia(id_midia),
    FOREIGN KEY (id_campanha) REFERENCES CAMPANHA_CADASTRA.dim_campanha(id_campanha)
);

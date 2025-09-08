### Model baseada em banco de dados

import sqlite3

# Criação das tabelas

sql_create_table_livros = '''
CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY NOT NULL,
    codigo TEXT, 
    titulo TEXT,
    emprestado INTEGER
);
'''

conexao = sqlite3.connect('biblioteca.db')

conexao.execute(sql_create_table_livros)

# Popular a tabela livros

dados_livros = [
    ('br01', 'Tieta', 0),
    ('br02', 'Capitães da areia', 0),
    ('eua01','Jogos vorazes',  0),
    ('eua02','Em chamas',  0),
    ('eua03','A esperança',  0),
    ('br03', 'Tupinilândia', 0),
    ('br04', 'Homens elegantes', 0),
    ('br05', 'Homens cordiais', 0),
    ('esp01','A boa sorte',  0),
    ('esp02','A ridícula ideia de nunca mais te ver',  0)
]

sql_inserir_dados_livros = '''
INSERT INTO livros (codigo, titulo, emprestado)
VALUES (?, ?, ?);
'''

conexao.executemany(sql_inserir_dados_livros, dados_livros)
conexao.commit()
conexao.close()



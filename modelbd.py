# Model baseada em banco de dados

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

sql_create_table_leitor = '''
CREATE TABLE IF NOT EXISTS leitor (
    cpf TEXT PRIMARY KEY NOT NULL,
    nome TEXT
);
'''

sql_create_table_emprestimos = '''
CREATE TABLE IF NOT EXISTS emprestimo (
    id INTEGER PRIMARY KEY NOT NULL,
    id_leitor TEXT NOT NULL,
    id_livro INTEGER NOT NULL,
    data_devolucao TEXT NOT NULL,

    FOREIGN KEY (id_leitor)
        REFERENCES leitor (cpf)
    FOREIGN KEY (id_livro)
        REFERENCES livro (id)
);
'''

sql_create_table_lista_de_emprestimo = '''
CREATE TABLE IF NOT EXISTS leitor_emprestimo (
    id_leitor TEXT NOT NULL,
    id_emprestimo INTEGER NOT NULL,

    FOREIGN KEY (id_leitor)
        REFERENCES leitor (cpf)
    FOREIGN KEY (id_emprestimo)
        REFERENCES emprestimo (id)
);
'''

sql_inserir_dados_livros = '''
    INSERT INTO livros (codigo, titulo, emprestado)
    VALUES (?, ?, ?);
'''

sql_cadastrar_emprestimo = '''
    INSERT INTO emprestimo (id_leitor, id_livro, data_devolucao)
    VALUES (?, ?, ?)
'''

sql_set_livro_emprestado = '''
    UPDATE livros
    SET emprestado = 1
    WHERE codigo = ?
'''


sql_inserir_dados_leitores = '''
    INSERT INTO leitor (cpf, nome)
    VALUES (?, ?)
'''

dados_leitores = [
    ('123.456.789-01', 'Leo da Silva'),
    ('789.789.789-09', 'Lucas de Souza'),
    ('456.456.456-08', 'Gustavo dos Santos'),
    ('159.357.159-07', 'Will Martins'),
]

dados_livros = [
    ('br01', 'Tieta', 0),
    ('br02', 'Capitães da areia', 0),
    ('eua01', 'Jogos vorazes',  0),
    ('eua02', 'Em chamas',  0),
    ('eua03', 'A esperança',  0),
    ('br03', 'Tupinilândia', 0),
    ('br04', 'Homens elegantes', 0),
    ('br05', 'Homens cordiais', 0),
    ('esp01', 'A boa sorte',  0),
    ('esp02', 'A ridícula ideia de nunca mais te ver',  0)
]


with sqlite3.connect('biblioteca.db') as conexao:
    # Criamos as tabelas
    conexao.execute(sql_create_table_livros)
    conexao.execute(sql_create_table_leitor)
    conexao.execute(sql_create_table_emprestimos)
    conexao.execute(sql_create_table_lista_de_emprestimo)

    # Populamos as tabelas
    conexao.executemany(sql_inserir_dados_livros, dados_livros)
    conexao.executemany(sql_inserir_dados_leitores, dados_leitores)
    conexao.commit()


class Biblioteca():
    def cadastrar_leitor(self, leitor):
        with sqlite3.connect('biblioteca.db') as conexao:
            conexao.execute(sql_inserir_dados_leitores,
                            (leitor.cpf, leitor.nome))
            conexao.commit()

    def cadastrar_livro(self, cod, titulo):
        with sqlite3.connect('biblioteca.db') as conexao:
            conexao.execute(sql_inserir_dados_livros, (cod, titulo, 0))
            conexao.commit()

    def consultar_livro(self, cod):
        pass

    def excluir_livro(self, cod):
        pass

    def atualizar_livro(self, cod):
        pass

    def emprestar(self, livro, leitor):
        data_de_devolucao = self.calcular_data_devolucao()

        with sqlite3.connect('biblioteca.db') as conexao:
            conexao.execute(sql_cadastrar_emprestimo, (leitor.cpf, 
                                                       livro.cod,
                                                       data_de_devolucao.isoformat()))

            conexao.execute(sql_set_livro_emprestado, (livro.cod,))
            conexao.commit()

        livro.set_emprestado()
        novo_emprestimo = Emprestimo(livro, leitor, data_de_devolucao)
        return novo_emprestimo

    def calcular_data_devolucao(self):
        import datetime
        hoje = datetime.date.today()
        tempo_de_emprestimo = datetime.timedelta(weeks=1)
        data_de_devolucao = hoje + tempo_de_emprestimo

        return data_de_devolucao


class Leitor():
    def __init__(self):
        self.nome = str()
        self.cpf = str()
        self.emprestimos = list()


class Emprestimo():
    def __init__(self, livro, leitor, data_devolucao):
        self.livro = livro
        self.leitor = leitor
        self.data_devolucao = data_devolucao


class Livro():
    def __init__(self):
        self.emprestado = False

    def set_titulo(self, titulo):
        self.titulo = titulo

    def set_cod(self, cod):
        self.cod = cod

    def set_emprestado(self):
        self.emprestado = True

    def set_devolvido(self):
        self.emprestado = False


biblioteca = Biblioteca()

if __name__ == '__main__':
    # TESTES

    # Teste cadastro de livro
    biblioteca.cadastrar_livro('ABC-0000', 'Livro de teste')

    # Teste cadastro de leitor
    um_leitor = Leitor()
    um_leitor.cpf = '000.000.000-00'
    um_leitor.nome = 'Leitor de teste'

    biblioteca.cadastrar_leitor(um_leitor)

    # Teste de empréstimo

    um_livro = Livro()
    um_livro.set_cod('ABC-0000')
    um_livro.set_titulo('Livro Teste')

    biblioteca.emprestar(um_livro, um_leitor)

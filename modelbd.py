#
# Model baseada em banco de dados
#
import sqlite3

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

sql_create_table_emprestimo = '''
CREATE TABLE IF NOT EXISTS emprestimo (
    id INTEGER PRIMARY KEY NOT NULL,
    id_leitor TEXT NOT NULL,
    id_livro INTEGER  NOT NULL,
    data_devolucao TEXT NOT NULL,

    FOREIGN KEY (id_leitor)
       REFERENCES leitor (cpf),
    FOREIGN KEY (id_livro)
       REFERENCES livro (id)
);
'''

sql_create_table_lista_de_emprestimos = '''
CREATE TABLE IF NOT EXISTS leitor_emprestimo (
    id_leitor TEXT NOT NULL,
    id_emprestimo INTEGER NOT NULL,

    FOREIGN KEY (id_leitor)
        REFERENCES leitor (cpf),
    FOREIGN KEY (id_emprestimo)
        REFERENCES emprestimo (id)
);
'''

sql_inserir_dados_livros = '''
    INSERT INTO livros (codigo, titulo, emprestado)
    VALUES (?, ?, ?);
    '''

sql_inserir_dados_leitores = '''
    INSERT INTO leitor (cpf, nome)
    VALUES (?, ?);
    '''

sql_cadastrar_emprestimo = '''
    INSERT INTO emprestimo (id_leitor, id_livro, data_devolucao)
    VALUES (?, ?, ?);
    '''

sql_set_livro_emprestado = '''
    UPDATE livros
    SET emprestado = 1
    WHERE codigo = ?
    '''

sql_consultar_livro_cod = '''
    SELECT codigo, titulo, emprestado
    FROM livros
    WHERE codigo = ?;
    '''

dados_livros = [
    ("abc-001", "Dom Casmurro", 0),
    ("abc-002", "O Primo Basílio", 0),
    ("abc-003", "Memórias Póstumas de Brás Cubas", 0),
    ("abc-004", "Senhora", 0),
    ("abc-005", "Iracema", 0),
    ("abc-006", "O Guarani", 0),
    ("abc-007", "A Moreninha", 0),
    ("abc-008", "Vidas Secas", 0),
    ("abc-009", "Capitães da Areia", 0),
    ("abc-010", "Grande Sertão: Veredas", 0)
]

dados_leitores = [
    ('387.345.234-23', 'Augusto Zunino'),
    ('432.662.123-45', 'Bianca Ximenes'),
    ('983.163.729-94', 'Cristiano Velazques'),
]

with sqlite3.connect("biblioteca.db") as conexao:
    # Criamos as tabelas
    conexao.execute(sql_create_table_livros)
    conexao.execute(sql_create_table_leitor)
    conexao.execute(sql_create_table_emprestimo)
    conexao.execute(sql_create_table_lista_de_emprestimos)

    # Populamos as tabelas
    conexao.executemany(sql_inserir_dados_livros, dados_livros)
    conexao.executemany(sql_inserir_dados_leitores, dados_leitores)

    conexao.commit()


class Biblioteca:
    def cadastrar_leitor(self, leitor):
        with sqlite3.connect('biblioteca.db') as conexao:
            conexao.execute(sql_inserir_dados_leitores,
                            (leitor.cpf, leitor.nome))
            conexao.commit()

    def cadastrar_livro(self, cod, titulo):
        with sqlite3.connect('biblioteca.db') as conexao:
            conexao.execute(sql_inserir_dados_livros, (cod, titulo, 0))

    def consultar_livro(self, cod):
        um_livro = None

        with sqlite3.connect('biblioteca.db') as conexao:
            cursor = conexao.execute(sql_consultar_livro_cod, (cod,))
            dados_livro = cursor.fetchone()
            
            codigo, titulo, emprestado = dados_livro
            
            um_livro = Livro()
            um_livro.set_cod(codigo)
            um_livro.set_titulo(titulo)

            if int(emprestado):
                um_livro.set_emprestado()
        
        if um_livro:
            return um_livro
        else:
            return False

    def excluir_livro(self, cod):
        pass

    def atualizar_livro(self, cod, titulo):
        pass

    def emprestar(self, livro, leitor):
        data_de_devolucao = self.calcular_data_devolucao()

        with sqlite3.connect('biblioteca.db') as conexao:
            conexao.execute(sql_cadastrar_emprestimo, (leitor.cpf,
                                                       livro.cod,
                                                       data_de_devolucao.isoformat())
                            )
            # UPDATE livro emprestado=True (1)
            conexao.execute(sql_set_livro_emprestado, (livro.cod,))
            conexao.commit()

        livro.set_emprestado()
        novo_emprestimo = Emprestimo(livro, leitor, data_de_devolucao)
        return novo_emprestimo

    def calcular_data_devolucao(self):
        import datetime
        hoje = datetime.date.today()

        tempo_de_emprestimo = datetime.timedelta(weeks=1)
        # somamos 1 semana à data de emprestimo

        return hoje + tempo_de_emprestimo


class Leitor:
    def __init__(self):
        self.nome = str()
        self.cpf = str()
        self.emprestimos = list()


class Emprestimo:

    def __init__(self, livro, leitor, data_devolucao):
        self.livro = livro
        self.leitor = leitor
        self.data_devolucao = data_devolucao


class Livro:
    def __init__(self):
        self.emprestado = False

    def set_titulo(self, titulo):
        self.titulo = titulo

    def set_cod(self, cod):
        self.cod = cod

    def set_emprestado(self):
        self.emprestado = True


# Inicialização


biblioteca = Biblioteca()

if __name__ == '__main__':
    #
    # TESTES
    #
    # teste cadastro de livro
    biblioteca.cadastrar_livro('ABC-9999', 'Livro Teste')

    # teste cadastro de leitor
    um_leitor = Leitor()
    um_leitor.cpf = '999.999.999.99'
    um_leitor.nome = 'Leitor de Teste'
    biblioteca.cadastrar_leitor(um_leitor)

    # teste de emprestimo

    um_livro = Livro()
    um_livro.set_cod('ABC-9999')
    um_livro.set_titulo('Livro Teste')
    biblioteca.emprestar(um_livro, um_leitor)

    livro = biblioteca.consultar_livro('ABC-9999')
    print(f'Código: {livro.cod} | Título: {livro.titulo} | Emprestado: {livro.emprestado}')

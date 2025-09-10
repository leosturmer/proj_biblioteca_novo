# Consultar dados do banco

import sqlite3

with sqlite3.connect('biblioteca.db') as conexao:
    cursor = conexao.execute('''
SELECT id, codigo, titulo, emprestado 
    FROM livros;                    
''')
    
    livros = cursor.fetchall()

    for id, codigo, titulo, emprestado in livros:
        print(id, codigo, titulo, emprestado, sep=' | ')

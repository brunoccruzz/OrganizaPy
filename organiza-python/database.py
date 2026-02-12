import sqlite3

def conectar():
    return sqlite3.connect("organizapy.db")

def criartabela(): #Cria tabela dentro do banco de dados
    conexao = conectar()
    cursor= conexao.cursor()

#Criação da tabela usuarios
    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL 
    )
    ''')
#Crição da tabela tarefas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tarefas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descricao TEXT,
    concluida INTEGER DEFAULT 0,
    usuario_id INTEGER,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')
    conexao.commit()
    conexao.close()


if __name__ == "__main__":
    criartabela()
    print("Banco criado com sucesso!")
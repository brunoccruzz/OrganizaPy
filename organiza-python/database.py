import sqlite3

def conectar():
    return sqlite3.connect("organizapy.db")

def criartabela():
    conexao = conectar()
    cursor= conexao.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL 
    )
    ''')

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
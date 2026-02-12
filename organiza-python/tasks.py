from database import conectar

def criar_tarefa(titulo, usuario_id,descricao:str=None):

    if not titulo or not usuario_id:
        print("❌ Erro: Todos os campos devem ser preenchidos!")
        return
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("INSERT INTO tarefas (titulo,usuario_id,descricao) VALUES (?, ?, ?)",
                       (titulo, usuario_id,descricao))
        conexao.commit()
        print(f"Tarefa {titulo} registrada com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao criar tarefa: {e}")

    finally:
        if 'conexao' in locals():
            conexao.close()


def listar_tarefas(usuario_id):
    print("Tarefas: \n")
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT * FROM tarefas WHERE usuario_id = ?", (usuario_id,))
        tarefas = cursor.fetchall()
        return tarefas

    except Exception as e:
        print(f"❌ Erro ao buscar tarefas: {e}")
        return []

def concluir_tarefa(id_tarefa, usuario_id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            "UPDATE tarefas SET concluida = 1 WHERE id = ? AND usuario_id = ?",
            (id_tarefa, usuario_id)
        )
        conexao.commit()
        return cursor.rowcount > 0

    except Exception as e:
        print(f"Erro ao concluir tarefa: {e}")
        return False

    finally:
        if 'conexao' in locals():
            conexao.close()


def excluir_tarefa(id_tarefa, usuario_id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            "DELETE FROM tarefas WHERE id = ? AND usuario_id = ?",
            (id_tarefa, usuario_id)
        )
        conexao.commit()
        return cursor.rowcount > 0

    except Exception as e:
        print(f"Erro ao excluir tarefa: {e}")
        return False

    finally:
        if 'conexao' in locals():
            conexao.close()


def desmarcar_tarefa(id_tarefa, usuario_id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            "UPDATE tarefas SET concluida = 0 WHERE id = ? AND usuario_id = ?",
            (id_tarefa, usuario_id)
        )
        conexao.commit()
        return cursor.rowcount > 0

    except Exception as e:
        print(f"Erro ao desmarcar tarefa: {e}")
        return False

    finally:
        if 'conexao' in locals():
            conexao.close()




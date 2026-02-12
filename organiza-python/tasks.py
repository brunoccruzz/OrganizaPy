from database import conectar

#Função de criar tarefa pra cada usuario
def criar_tarefa(titulo, usuario_id,descricao:str=None):
    if not titulo or not usuario_id:
        print("❌ Erro: Todos os campos devem ser preenchidos!")
        return
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("INSERT INTO tarefas (titulo,usuario_id,descricao) VALUES (?, ?, ?)", #Insere para o id do usuario, as caract da tarefa
                       (titulo, usuario_id,descricao))
        conexao.commit()
        print(f"Tarefa {titulo} registrada com sucesso!")

    except Exception as e: #se der erro
        print(f"❌ Erro ao criar tarefa: {e}")

    finally:
        if 'conexao' in locals():
            conexao.close()

#Faz aparecer todas as tarefas que o usuario inseriu e n deletou
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

#Aqui ele conclui a tarefa setando a variavel concluida para 1 dizendo que ele ja foi realizada
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

#função de exluir tarefa, pegando o ID dela
def excluir_tarefa(id_tarefa, usuario_id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            "DELETE FROM tarefas WHERE id = ? AND usuario_id = ?",
            (id_tarefa, usuario_id)
        )
        conexao.commit()
        return cursor.rowcount > 0 #checa quantas linhas foram afetadas

    except Exception as e:
        print(f"Erro ao excluir tarefa: {e}")
        return False

    finally:
        if 'conexao' in locals():
            conexao.close()

#Descmarca a tarefa setando a concluida para 0
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




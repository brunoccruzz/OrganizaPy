from auth import registrar, login
from tasks import criar_tarefa,excluir_tarefa,listar_tarefas,concluir_tarefa

def menu_principal():
    while True:
        print("\n--------- OrganizaPy ---------")
        print("1 - Registrar-se")
        print("2 - Login")
        print("3 - Sair")

        resposta = input("O que deseja: ").strip()

        if resposta == "1":
            registrar()
        elif resposta == "2":
            id_logado = login()
            if id_logado:
                menuapp(id_logado)
                print(f"Sessão ativa para o ID: {id_logado}")
        elif resposta == "3":
            print("Encerrando OrganizaPy... Até mais!")
            break
        else:
            print("❌ Opção inválida! Digite 1, 2 ou 3.")


def menuapp(id_logado):
    while True:
        print("\n--------- Bem Vindo ao OrganizaPy ---------")
        print("1 - Adicionar tarefa")
        print("2 - Ver tarefas")
        print("3 - Excluir tarefa")
        print("4 - Sair")

        resposta = input("O que deseja: ").strip()

        if resposta == "1":
            titulo = input("Qual titulo da tarefa: ").strip()
            descricao = input("Deseja colocar alguma descricao? ").strip()
            criar_tarefa(titulo, id_logado, descricao)

        elif resposta == "2":
            tarefas = listar_tarefas(id_logado)
            if not tarefas:
                print("📭 Nenhuma tarefa cadastrada.")
            else:
                for t in tarefas:
                    status = "✅" if t[3] == 1 else "❌"
                    descricao = t[2] if t[2] else "Sem descrição"
                    print(f"{t[0]} - {t[1]} | {descricao} {status}")

        elif resposta == "3":
            try:
                id_tarefa = int(input("Digite o ID da tarefa para excluir: ").strip())
                ok = excluir_tarefa(id_tarefa, id_logado)
                if ok:
                    print("🗑 Tarefa excluída com sucesso!")
                else:
                    print("❌ Não foi possível excluir (ID inválido ou não pertence ao usuário).")
            except ValueError:
                print("❌ ID inválido! Digite um número.")

        elif resposta == "4":
            print("Saindo do menu de tarefas...")
            break

        else:
            print("❌ Opção inválida! Digite 1, 2, 3 ou 4.")

menu_principal()
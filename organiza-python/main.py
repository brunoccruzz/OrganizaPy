from auth import registrar, login
from tasks import criar_tarefa, excluir_tarefa, listar_tarefas, concluir_tarefa, desmarcar_tarefa
from rich.console import Console
from rich.table import Table

console = Console()


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
        print("3 - Concluir tarefa")
        print("4 - Desmarcar tarefa")
        print("5 - Excluir tarefa")
        print("6 - Sair")

        resposta = input("O que deseja: ").strip()

        if resposta == "1":
            titulo = input("Qual titulo da tarefa: ").strip()
            descricao = input("Deseja colocar alguma descricao? ").strip()
            criar_tarefa(titulo, id_logado, descricao)

        elif resposta == "2":
            tarefas = listar_tarefas(id_logado)

            if not tarefas:
                console.print("[yellow]📭 Nenhuma tarefa cadastrada.[/yellow]")
            else:
                table = Table(title="📋 Suas Tarefas")
                table.add_column("ID", justify="right")
                table.add_column("Título")
                table.add_column("Descrição")
                table.add_column("Status")

            for t in tarefas:
                descricao = t[2] if t[2] else "Sem descrição"
                status = "[green]✅ Concluída[/green]" if t[3] == 1 else "[red]❌ Pendente[/red]"
                table.add_row(str(t[0]), t[1], descricao, status)

            console.print(table)


        elif resposta == "3":
            try:
                id_tarefa = int(input("Digite o ID da tarefa para CONCLUIR: ").strip())
                ok = concluir_tarefa(id_tarefa, id_logado)
                if ok:
                    print("✅ Tarefa marcada como concluída!")
                else:
                    print("❌ Não foi possível concluir (ID inválido ou não pertence ao usuário).")
            except ValueError:
                print("❌ ID inválido! Digite um número.")

        elif resposta == "4":
            try:
                id_tarefa = int(input("Digite o ID da tarefa para DESMARCAR: ").strip())
                ok = desmarcar_tarefa(id_tarefa, id_logado)
                if ok:
                    print("↩️ Tarefa desmarcada (não concluída)!")
                else:
                    print("❌ Não foi possível desmarcar (ID inválido ou não pertence ao usuário).")
            except ValueError:
                print("❌ ID inválido! Digite um número.")

        elif resposta == "5":
            try:
                id_tarefa = int(input("Digite o ID da tarefa para EXCLUIR: ").strip())
                ok = excluir_tarefa(id_tarefa, id_logado)
                if ok:
                    print("🗑️ Tarefa excluída com sucesso!")
                else:
                    print("❌ Não foi possível excluir (ID inválido ou não pertence ao usuário).")
            except ValueError:
                print("❌ ID inválido! Digite um número.")

        elif resposta == "6":
            print("Saindo do menu de tarefas...")
            break

        else:
            print("❌ Opção inválida! Digite 1 a 6.")


menu_principal()
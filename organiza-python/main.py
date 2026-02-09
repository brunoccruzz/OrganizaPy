from auth import registrar, login

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
                # menu de tarefas
                print(f"Sessão ativa para o ID: {id_logado}")
        elif resposta == "3":
            print("Encerrando OrganizaPy... Até mais!")
            break
        else:
            print("❌ Opção inválida! Digite 1, 2 ou 3.")

menu_principal()
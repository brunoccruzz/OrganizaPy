import hashlib


from database import conectar

def registrar():
    print("--------- Bem vindo ao OrganizaPy ---------")
    nome = str(input("Digite o seu nome de usuário: ")).strip()
    email=str(input("Digite o email:")).strip()
    senha=str(input("Digite a senha: ")).strip()
    if not nome or not email or not senha:
        print("❌ Erro: Todos os campos devem ser preenchidos!")
        return
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
                       (nome, email, senha_hash))

        conexao.commit()
        print(f"Usuário {nome} cadastrado com sucesso!")

    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            print("❌ Erro: Este email já está cadastrado!")
        else:
            print(f"❌ Erro ao salvar: {e}")

    finally:

        if 'conexao' in locals():
            conexao.close()


def login():
    print("--------- Bem vindo de volta ao OrganizaPy ---------")
    emaillogin=str(input("Digite o email cadastrado: ")).strip()
    senhalogin=str(input(f"Digite a senha da conta {emaillogin}: ")).strip()

    if not emaillogin or not senhalogin:
        print("❌ Erro: Todos os campos devem ser preenchidos!")
        return

    senha_hash_login= hashlib.sha256(senhalogin.encode()).hexdigest()
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT id, nome, senha FROM usuarios WHERE email = ?", (emaillogin,))

        resultado = cursor.fetchone()

        if resultado is None:
            print("❌ Erro: E-mail não cadastrado!")
        else:
            id_usuario = resultado[0]
            nome_usuario = resultado[1]
            senha_do_banco = resultado[2]

            if senha_hash_login == senha_do_banco:
                print(f"✅ Bem-vindo(a) de volta, {nome_usuario}!")
                return id_usuario
            else:
                print("❌ Erro: Senha incorreta!")

    except Exception as e:
        print(f"⚠️ Erro no sistema: {e}")
    if 'conexao' in locals():
        conexao.close()




#Modelo da classe usuario
class Usuario:
    def __init__(
        self,
        id:int,
        nome: str,
        senha:str
    ):
        self.id=id
        self.nome=nome
        self.senha=senha



#Modelo da classe tarefa
class Tarefa:
    def __init__(
            self,
            id: int,
            titulo: str,
            concluida: bool,
            descricao:str,
            usuario_id: int
    ):
        self.id = id
        self.titulo = titulo
        self.concluida = concluida
        self.usuario_id = usuario_id
        self.descricao=descricao

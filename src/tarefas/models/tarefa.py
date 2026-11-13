from datetime import datetime

from tarefas.models.database import Database


class Tarefa:
    """Provê métodos para armazenar, recuperar e processar os dados das
    tarefas criadas a partir do formulário principal.
    """

    def __init__(self, titulo, id = None, data_conclusao = None):
        self.id = id
        self.titulo = titulo
        self.data_conclusao = data_conclusao


    def salvarTarefa(self):
        """Salva a tarefa no banco de dados."""

        sql = 'INSERT INTO tarefa (titulo_tarefa, data_conclusao) VALUES (%s, %s);'
        params = (self.titulo, self.data_conclusao) # protege contra SQL Injection

        with Database() as db:
            db.executar(sql, params)


    @staticmethod
    def listarTarefas() -> list:
        """Retorna uma lista com todas as tarefas cadastradas."""

        sql = '''SELECT id_tarefa, titulo_tarefa, data_conclusao 
        FROM tarefa LIMIT 100; '''

        with Database() as db:
            tarefas_banco = db.executar(sql)

        return tarefas_banco if tarefas_banco else []

    
    @staticmethod
    def apagarTarefa(id_tarefa):

        sql = """DELETE FROM tarefa WHERE id_tarefa = %s;"""
        params = (id_tarefa,)
        with Database() as db:
            db.executar(sql, params)


    @staticmethod
    def buscarPorId(id_tarefa):
        """Carrega uma tarefa do banco na memória (heap), instanciando um objeto Tarefa."""

        sql = '''SELECT id_tarefa, titulo_tarefa, data_conclusao 
        FROM tarefa WHERE id_tarefa = %s;'''
        params = (id_tarefa,)

        with Database() as db:
            resultado = db.executar(sql, params)

        if resultado:
            dados = resultado[0]

            if isinstance(dados, dict):
                return Tarefa(
                    id=dados['id_tarefa'],
                    titulo=dados['titulo_tarefa'],
                    data_conclusao=dados['data_conclusao']
                )
            elif hasattr(dados, 'id_tarefa'):
                return Tarefa(
                    id=dados.id_tarefa,
                    titulo=dados.titulo_tarefa,
                    data_conclusao=dados.data_conclusao
                )
            else:
                return Tarefa(
                    id=dados[0],
                    titulo=dados[1],
                    data_conclusao=dados[2]
                )

        return None


    def atualizarTarefa(self):
        sql = '''UPDATE tarefa 
        SET titulo_tarefa = %s, data_conclusao = %s 
        WHERE id_tarefa = %s;'''
        params = (self.titulo, self.data_conclusao, self.id)

        with Database() as db:
            db.executar(sql, params)

# Área 51 (testes)
#tarefa = Tarefa('Minha nova tarefa')
#tarefa.salvarTarefa()
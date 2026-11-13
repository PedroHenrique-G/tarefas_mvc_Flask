from flask import Flask, redirect, render_template, request, url_for

from tarefas.models.database import init_db
from tarefas.models.tarefa import Tarefa


app = Flask(__name__)

with app.app_context():
    init_db()
    
@app.route('/test')
def test():
    return 'Servidor online!'

@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        titulo_form = request.form['tituloTarefa'] 
        data_conclusao_form = request.form['dataConclusao'] 

        data_corrigida = data_conclusao_form or None

        tarefa = Tarefa(titulo=titulo_form, data_conclusao=data_corrigida)
        
        tarefa.salvarTarefa()

        return redirect(url_for('home'))

    tarefas = Tarefa.listarTarefas()

    return render_template(
        'base.html',
        titulo_da_pagina='Minha lista de tarefas',
        tarefas_da_pagina=tarefas,
        tarefa_editar=None
    )

@app.route('/delete/<int:id>')
def apagar_id_especificado(id):
    Tarefa.apagarTarefa(id)
    return redirect(url_for('home'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def editar_id_especificado(id):
    tarefa = Tarefa.buscarPorId(id)

    if not tarefa:
        return redirect(url_for('home'))

    if request.method == 'POST':
        titulo_form = request.form['tituloTarefa']
        data_conclusao_form = request.form['dataConclusao']

        tarefa.titulo = titulo_form
        tarefa.data_conclusao = data_conclusao_form or None

        tarefa.atualizarTarefa()
        return redirect(url_for('home'))

    tarefas = Tarefa.listarTarefas()

    return render_template(
        'base.html',
        titulo_da_pagina='Editar tarefa',
        tarefas_da_pagina=tarefas,
        tarefa_editar=tarefa
    )

if __name__ == '__main__':
    app.run()
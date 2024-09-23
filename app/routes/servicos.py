from flask import Blueprint, render_template, request, redirect, url_for,jsonify 
from ..models import db, Servico, Categoria

servicos_bp = Blueprint('servicos', __name__, url_prefix='/servicos')

@servicos_bp.route('/')
def listar_servicos():
    servicos = Servico.query.all()
    return render_template('listar_servicos.html', servicos=servicos)

@servicos_bp.route('/novo', methods=['GET', 'POST'])
def novo_servico():
    categorias = Categoria.query.all()
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        categoria_id = request.form['categoria']
        novo_servico = Servico(nome=nome, descricao=descricao, categoria_id=categoria_id)
        db.session.add(novo_servico)
        db.session.commit()
        return redirect(url_for('servicos.listar_servicos'))
    return render_template('novo_servico.html', categorias=categorias)


# Rota para buscar serviços por categoria
@servicos_bp.route('/categoria/<int:categoria_id>', methods=['GET'])
def servicos_por_categoria(categoria_id):
    servicos = Servico.query.filter_by(categoria_id=categoria_id).all()
    servicos_data = [{"id": servico.id, "nome": servico.nome} for servico in servicos]
    return jsonify({"servicos": servicos_data})